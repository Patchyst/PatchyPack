# Author: Patrick Story
# https://github.com/Patchyst
# https://github.com/Patchyst/PatchyPack
import zipfile
import argparse
from termcolor import cprint
argsparser = argparse.ArgumentParser()
argsparser.add_argument("zipfile_path", help="Path to zip file", type=str)
argsparser.add_argument("dict_path", help="Path to password dictionary file", type=str)
argsparser.add_argument("--viewall", action="store_true",
                        help="View all attempted passwords. usage example: --viewall Y")
args = argsparser.parse_args()

zfile = zipfile.ZipFile(args.zipfile_path)
dictionaryfile = open(args.dict_path, encoding="latin-1")


def zip_brute_force(zipf, word_list):
    for word in word_list.readlines():
        word = word.strip("\n")
        if args.viewall:
            print("[*] Trying word: " + str(word) + " for ", zfile)
        word = bytes(word, "utf-8")
        try:
            zipf.extractall(pwd=word)
            msg = "[+] password found: " + str(word)
            cprint(msg, "red", attrs=["bold"])
            return True
        except Exception:
            pass


if __name__ == "__main__":
    zip_brute_force(zfile, dictionaryfile)
