from pathlib import Path
from sentpiece_mine.sentencepiece import *

txt = Path('data/botchan.txt').read_text()

txt = txt.replace('\n', ' ')
txt = re.sub(' +', ' ', txt)

bpe_enc = BytePairEncoder()
bpe_enc.fit(txt, 2000)

sp_trainer = SentencePieceTrainer()

tokens = bpe_enc.tokens
tokens['_'] = tokens[' ']
tokens.pop(' ')

characters = bpe_enc.characters
characters.discard(' ')
characters.add('_')

sp_trainer.fit(txt, tokens, characters, vocab_size=1000)
