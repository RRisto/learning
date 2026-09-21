# FaceFusion 3.8.3 CUDA setup on RunPod

This guide reproduces the FaceFusion prerecorded-video face-swap environment created on this RunPod RTX 4090 machine. It keeps project data under `/workspace`, runs only the face swapper for the initial comparison, and verifies real CUDA inference before starting the UI.

## 1. Verify the GPU

```bash
nvidia-smi
```

The tested machine reported:

- GPU: NVIDIA GeForce RTX 4090
- Driver: 570.195.03
- Driver-supported CUDA version: 12.8

Do not continue with a CPU fallback if `nvidia-smi` cannot see the GPU.

## 2. Create the experiment directories

```bash
mkdir -p \
  /workspace/deepfake-test/source \
  /workspace/deepfake-test/target \
  /workspace/deepfake-test/output \
  /workspace/deepfake-test/temp \
  /workspace/deepfake-test/jobs
```

Use these file locations:

```text
/workspace/deepfake-test/source/source.jpg
/workspace/deepfake-test/target/mixkit-therapist-in-his-office-talking-to-the-camera-4834-hd-ready.mp4
/workspace/deepfake-test/output/swapped-rerun.mp4
```

## 3. Clone the official Docker repository

```bash
git clone https://github.com/facefusion/facefusion-docker.git \
  /workspace/facefusion-docker

git -C /workspace/facefusion-docker rev-parse HEAD
```

At the time of this setup, the repository commit was:

```text
502497c21b2d1d1e7b5dd8e1f71bdab03fb8d0be
```

The repository's `Dockerfile.cuda` pins FaceFusion 3.8.3. Its normal CUDA startup command is:

```bash
cd /workspace/facefusion-docker
docker compose -f docker-compose.cuda.yml up
```

The compose file publishes host port 7870 and starts FaceFusion with:

```text
python facefusion.py run --execution-providers cuda
```

## 4. Verify Docker and NVIDIA container access

Install the required packages if the RunPod template does not already provide them:

```bash
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  docker.io \
  docker-compose-v2 \
  nvidia-container-toolkit

nvidia-ctk runtime configure --runtime=docker
```

On a normal Docker-capable host, start or restart Docker using the host's service manager, then test GPU access:

```bash
docker --version
docker compose version
docker info --format 'Runtimes={{json .Runtimes}}'
docker run --rm --gpus all \
  nvidia/cuda:12.8.1-base-ubuntu24.04 nvidia-smi
```

The last command must display the RTX 4090 from inside the container.

### RunPod nested-container limitation encountered here

This particular RunPod shell is itself an unprivileged container. PID 1 is RunPod's NVIDIA entrypoint, and the outer container does not grant `CAP_SYS_ADMIN` or namespace creation. Docker could start with an isolated daemon, but container extraction or creation failed with:

```text
operation not permitted
unshare: operation not permitted
```

Changing Docker's storage driver from `overlayfs` to `vfs` did not solve namespace creation. This condition cannot be repaired inside the pod. A RunPod template with privileged Docker support or a mounted host Docker socket is required for the official compose setup.

The remaining steps describe the direct official FaceFusion CUDA installation used on this machine. It uses the same FaceFusion version and CUDA ONNX Runtime selected by the official Dockerfile.

## 5. Install the required system runtime

FaceFusion 3.8.3 requires Python 3.12 for its pinned SciPy version. FFmpeg is required for prerecorded video processing, and ONNX Runtime CUDA requires cuDNN 9. FaceFusion uses FFmpeg's `-fps_mode` option, so Ubuntu 22.04's FFmpeg 4.4 package is too old and fails frame extraction with `Unrecognized option 'fps_mode'`.

```bash
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  python3.12 \
  python3.12-venv \
  libcudnn9-cuda-12=9.10.2.21-1
```

Install a recent static FFmpeg build with NVENC support. This machine was retested with FFmpeg 8.1:

```bash
mkdir -p /opt/ffmpeg-8.1

curl -fL \
  https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n8.1-latest-linux64-gpl-8.1.tar.xz \
  -o /tmp/ffmpeg-n8.1-linux64-gpl.tar.xz

tar -xJf /tmp/ffmpeg-n8.1-linux64-gpl.tar.xz \
  --strip-components=1 \
  -C /opt/ffmpeg-8.1

ln -sf /opt/ffmpeg-8.1/bin/ffmpeg /usr/local/bin/ffmpeg
ln -sf /opt/ffmpeg-8.1/bin/ffprobe /usr/local/bin/ffprobe
```

Verify the active version and required options:

```bash
ffmpeg -version | head -1
ffmpeg -hide_banner -h full 2>&1 | grep fps_mode
ffmpeg -hide_banner -encoders 2>/dev/null | grep hevc_nvenc
```

Confirm that cuDNN is visible:

```bash
ldconfig -p | grep libcudnn.so.9
```

## 6. Clone the exact FaceFusion release

```bash
git clone --branch 3.8.3 --single-branch \
  https://github.com/facefusion/facefusion.git \
  /workspace/facefusion

git -C /workspace/facefusion rev-parse HEAD
git -C /workspace/facefusion describe --tags --exact-match
```

The tested release resolves to:

```text
Version: 3.8.3
Commit: 435521dca8f98dee15fe67abadea6fc4a579f095
```

## 7. Install the Python and CUDA dependencies

On this machine, RunPod's `/workspace` is a network FUSE mount. Installing a large virtual environment there repeatedly stopped while writing package files. The application, models, inputs, outputs, logs, and configuration remain under `/workspace`; only the Python runtime is placed under `/opt`.

```bash
python3.12 -m venv /opt/facefusion-venv

/opt/facefusion-venv/bin/python -m pip install \
  --no-cache-dir \
  -r /workspace/facefusion/requirements.txt

/opt/facefusion-venv/bin/python -m pip uninstall -y onnxruntime

/opt/facefusion-venv/bin/python -m pip install \
  --no-cache-dir \
  onnxruntime-gpu==1.24.4

/opt/facefusion-venv/bin/python -m pip check
```

`onnxruntime-gpu==1.24.4` is the package selected by FaceFusion 3.8.3's official `install.py cuda@12` installer.

## 8. Reject silent CPU fallback

Checking `onnxruntime.get_available_providers()` alone is insufficient. A missing CUDA dependency can leave CUDA in the advertised provider list while session creation silently falls back to CPU.

Run an actual CUDA operation and assert that CUDA remains the first session provider:

```bash
cd /workspace/facefusion

/opt/facefusion-venv/bin/python - <<'PY'
import numpy as np
import onnxruntime as ort
from onnx import TensorProto, helper

a_info = helper.make_tensor_value_info('A', TensorProto.FLOAT, [2048, 2048])
b_info = helper.make_tensor_value_info('B', TensorProto.FLOAT, [2048, 2048])
c_info = helper.make_tensor_value_info('C', TensorProto.FLOAT, [2048, 2048])
graph = helper.make_graph(
    [helper.make_node('MatMul', ['A', 'B'], ['C'])],
    'cuda_check',
    [a_info, b_info],
    [c_info]
)
model = helper.make_model(graph, opset_imports=[helper.make_opsetid('', 13)])
model.ir_version = 10

session = ort.InferenceSession(
    model.SerializeToString(),
    providers=['CUDAExecutionProvider']
)
session.disable_fallback()

assert session.get_providers()[0] == 'CUDAExecutionProvider', session.get_providers()

a = np.ones((2048, 2048), dtype=np.float32)
result = session.run(None, {'A': a, 'B': a})[0]
assert result[0, 0] == 2048.0

print('ONNX Runtime:', ort.__version__)
print('Session providers:', session.get_providers())
print('Device:', ort.get_device())
print('CUDA result:', result.shape, float(result[0, 0]))
PY
```

Expected essential output:

```text
Session providers: ['CUDAExecutionProvider', 'CPUExecutionProvider']
Device: GPU
CUDA result: (2048, 2048) 2048.0
```

The CPU provider appearing second is ONNX Runtime's built-in fallback registration. The assertion ensures CUDA is active and first. FaceFusion itself is launched with only `--execution-providers cuda`.

## 9. Create the experiment configuration

Save the following as `/workspace/deepfake-test/facefusion.ini`:

```ini
[paths]
temp_path = /workspace/deepfake-test/temp
jobs_path = /workspace/deepfake-test/jobs
source_paths = /workspace/deepfake-test/source/source.jpg
target_path = /workspace/deepfake-test/target/mixkit-therapist-in-his-office-talking-to-the-camera-4834-hd-ready.mp4
output_path = /workspace/deepfake-test/output/swapped-rerun.mp4

[face_selector]
face_selector_mode = one

[face_masker]
face_mask_types = box occlusion
face_mask_blur = 0.3

[output_creation]
output_audio_encoder = aac
output_video_encoder = hevc_nvenc
output_video_preset = slow
output_video_quality = 90
output_video_scale = 1.0

[workflow]
workflow_mode = auto
workflow_strategy = disk

[processors]
processors = face_swapper
face_swapper_model = hyperswap_1a_256
face_swapper_pixel_boost = 512x512
face_swapper_weight = 1.0

[uis]
open_browser = false
ui_layouts = default
ui_workflow = instant_runner

[execution]
execution_device_ids = 0
execution_providers = cuda
execution_thread_count = 8

[memory]
video_memory_strategy = tolerant

[misc]
log_level = debug
halt_on_error = true
```

Only `face_swapper` is enabled. Face enhancement remains off for the first comparison. The disk workflow is more reliable on this machine and completed the full 452-frame test.

Verify that FFmpeg exposes the selected NVIDIA encoder:

```bash
ffmpeg -hide_banner -encoders 2>/dev/null | grep hevc_nvenc
```

## 10. Start FaceFusion

```bash
cd /workspace/facefusion

setsid env \
  GRADIO_SERVER_NAME=0.0.0.0 \
  GRADIO_SERVER_PORT=7870 \
  /opt/facefusion-venv/bin/python facefusion.py run \
  --config-path /workspace/deepfake-test/facefusion.ini \
  --execution-providers cuda \
  --processors face_swapper \
  --log-level debug \
  >/workspace/deepfake-test/facefusion.log 2>&1 </dev/null &

echo $! >/workspace/deepfake-test/facefusion.pid
```

The first startup downloads and validates the required official models. Wait until the UI returns HTTP 200:

```bash
curl -fsS -o /dev/null -w 'HTTP %{http_code}\n' \
  http://127.0.0.1:7870/

ss -ltnp | grep ':7870'
```

Expected listener:

```text
0.0.0.0:7870
```

Inspect startup activity and errors with:

```bash
tail -f /workspace/deepfake-test/facefusion.log
```

## 11. Verify FaceFusion's downloaded swapper model on CUDA

After the first startup has downloaded `hyperswap_1a_256.onnx`, run the model through FaceFusion's own provider construction:

```bash
cd /workspace/facefusion

/opt/facefusion-venv/bin/python - <<'PY'
import numpy as np
from facefusion.execution import create_inference_providers
from facefusion.inference_manager import create_inference_session

providers = create_inference_providers(0, ['cuda'])
session = create_inference_session(
    '.assets/models/hyperswap_1a_256.onnx',
    providers
)
session.disable_fallback()

assert providers[0][0] == 'CUDAExecutionProvider'
assert session.get_providers()[0] == 'CUDAExecutionProvider'

feeds = {}
for model_input in session.get_inputs():
    shape = [dimension if isinstance(dimension, int) and dimension > 0 else 1
             for dimension in model_input.shape]
    feeds[model_input.name] = np.zeros(shape, dtype=np.float32)

outputs = session.run(None, feeds)

print('Requested providers:', providers)
print('Session providers:', session.get_providers())
print('Outputs:', [(output.shape, str(output.dtype)) for output in outputs])
PY
```

The tested model returned two CUDA-generated tensors with shapes `(1, 3, 256, 256)` and `(1, 1, 256, 256)`.

## 12. Stop and restart

Stop FaceFusion cleanly using its recorded PID:

```bash
kill "$(cat /workspace/deepfake-test/facefusion.pid)"
```

Check that it stopped:

```bash
if kill -0 "$(cat /workspace/deepfake-test/facefusion.pid)" 2>/dev/null; then
  echo 'FaceFusion is still running'
else
  echo 'FaceFusion is stopped'
fi
```

Restart it with the command from step 10.

## 13. Available FaceFusion 3.8.3 face swappers

List them directly from the installed version instead of relying on documentation that may describe another release:

```bash
cd /workspace/facefusion

/opt/facefusion-venv/bin/python - <<'PY'
from facefusion.processors.modules.face_swapper.choices import (
    face_swapper_models,
    face_swapper_set,
)

for model in face_swapper_models:
    print(f'{model}: {", ".join(face_swapper_set[model])}')
PY
```

FaceFusion 3.8.3 provides:

```text
blendswap_256
ghost_1_256
ghost_2_256
ghost_3_256
hififace_unofficial_256
hyperswap_1a_256
hyperswap_1b_256
hyperswap_1c_256
inswapper_128
inswapper_128_fp16
simswap_256
simswap_unofficial_512
uniface_256
```

For an initial high-quality single-face comparison on the RTX 4090, compare these with every other setting held constant:

1. `hyperswap_1a_256`, pixel boost `512x512`
2. `hyperswap_1b_256`, pixel boost `512x512`
3. `simswap_unofficial_512`, pixel boost `512x512`

Keep these common settings:

```text
face selector: one
mask types: box occlusion
mask blur: 0.3
swapper weight: 1.0
video encoder: hevc_nvenc
video quality: 90
face enhancer: off
```

Compare short clips containing frontal, profile, fast-motion, partially occluded, and poorly lit frames before processing the entire target video.

## 14. Run and verify the included test data

The included target has no audio stream. FaceFusion therefore logs `restoring audio skipped`; this is expected and does not mean video processing failed.

Run the complete 452-frame test to a new file:

```bash
cd /workspace/facefusion

/opt/facefusion-venv/bin/python facefusion.py headless-run \
  --config-path /workspace/deepfake-test/facefusion.ini \
  --jobs-path /workspace/deepfake-test/jobs \
  --temp-path /workspace/deepfake-test/temp \
  --workflow-strategy disk \
  --processors face_swapper \
  --execution-providers cuda \
  --execution-thread-count 8 \
  --face-swapper-model hyperswap_1a_256 \
  --face-swapper-pixel-boost 512x512 \
  --output-video-encoder hevc_nvenc \
  --output-video-preset slow \
  --output-video-quality 90 \
  --log-level info \
  -s /workspace/deepfake-test/source/source.jpg \
  -t /workspace/deepfake-test/target/mixkit-therapist-in-his-office-talking-to-the-camera-4834-hd-ready.mp4 \
  -o /workspace/deepfake-test/output/swapped-rerun.mp4
```

Verify the result and fully decode it to catch truncated or corrupt output:

```bash
ffprobe -v error \
  -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,nb_frames \
  -of default=noprint_wrappers=1 \
  /workspace/deepfake-test/output/swapped-rerun.mp4

ffmpeg -v error \
  -i /workspace/deepfake-test/output/swapped-rerun.mp4 \
  -f null -
```

The verified run produced HEVC video at 1280x720, 29.97 fps, 452 frames, and 15.08 seconds.

## 15. Recover after a pod image reset

`/workspace` persisted across the reset observed on this machine, but system packages and `/opt/facefusion-venv` did not. A workspace virtual environment also became unusable because its `/usr/bin/python3.12` target disappeared. After a reset:

1. Repeat sections 5 and 7 to restore FFmpeg, Python, cuDNN, and `/opt/facefusion-venv`.
2. Run the CUDA check in section 8 before processing video.
3. Confirm that the source checkout is intact:

```bash
git -C /workspace/facefusion status --short
test -f /workspace/facefusion/facefusion/core.py
```

If the checkout reports only wholesale deletions under `facefusion/` and `tests/`, restore those tracked files from the pinned local commit:

```bash
git -C /workspace/facefusion restore \
  --source=HEAD \
  --worktree \
  -- facefusion tests
```

## 16. Use a video as the source face

The face swapper expects a source image rather than a source video. Inspect several frames and extract a clear, frontal frame with open eyes and limited motion blur. For example:

```bash
ffmpeg -y -v error \
  -ss 2 \
  -i /workspace/deepfake-test/source/WIN_20260920_18_20_55_Pro.mp4 \
  -frames:v 1 \
  /workspace/deepfake-test/source/WIN_20260920_18_20_55_Pro-frame-2s.png
```

Pass the extracted PNG to `--source-paths`. When the target contains audio, use `output_audio_encoder = aac` or `--output-audio-encoder aac` for broad MP4 playback support. The default FLAC audio is valid but is less widely supported in MP4 players and browsers.

## 17. Higher-quality portrait workflow

A sharp, front-facing portrait usually preserves identity better than a compressed frame extracted from video. Multiple source images may be passed to `--source-paths`; FaceFusion averages their face identities, so only combine images of the same person. Combining portraits of different people creates a blended identity.

This machine tested the following higher-quality settings successfully:

```text
pixel boost: 1024x1024
face enhancer: gpen_bfr_1024
face enhancer blend: 30
face enhancer weight: 0.5
mask: box
mask blur: 0.4
video encoder: hevc_nvenc
video preset: slow
video quality: 95
audio encoder: aac
```

Keep the enhancer blend restrained. A stronger blend can remove natural skin texture and alter facial details. Test representative still frames before rendering a complete video because the best swapper model depends on the particular source and target faces. In this test, `hyperswap_1b_256` was clean for Mihkel-to-Rain, while `hyperswap_1a_256` handled the glasses in Rain-to-Mihkel more consistently.

Example high-quality command:

```bash
cd /workspace/facefusion

/opt/facefusion-venv/bin/python facefusion.py headless-run \
  --config-path /workspace/deepfake-test/facefusion.ini \
  --workflow-strategy disk \
  --processors face_swapper face_enhancer \
  --face-swapper-model hyperswap_1b_256 \
  --face-swapper-pixel-boost 1024x1024 \
  --face-mask-types box \
  --face-mask-blur 0.4 \
  --face-enhancer-model gpen_bfr_1024 \
  --face-enhancer-blend 30 \
  --face-enhancer-weight 0.5 \
  --output-audio-encoder aac \
  --output-audio-quality 90 \
  --output-video-encoder hevc_nvenc \
  --output-video-preset slow \
  --output-video-quality 95 \
  --execution-providers cuda \
  --execution-thread-count 8 \
  -s /path/to/source-portrait.png \
  -t /path/to/target-video.mp4 \
  -o /path/to/output-hq.mp4
```

Verify every final file by decoding the entire video, not only by checking its metadata:

```bash
ffmpeg -v error -i /path/to/output-hq.mp4 -f null -
```
