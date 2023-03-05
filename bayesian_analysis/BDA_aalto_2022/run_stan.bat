set APP_PATH=%cd%

docker stop stan_run
docker rm stan_run
docker run -it --rm ^
    -p 8888:8888 ^
    -v %APP_PATH%:/home/jovyan/work ^
    --name stan_run ^
    stan