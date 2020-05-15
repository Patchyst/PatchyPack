import hashlib
import argparse
A = argparse.ArgumentParser()
A.add_argument("word", help="word to be hashed")
args = A.parse_args()
print(hashlib.sha256(args.word.encode()).hexdigest())
