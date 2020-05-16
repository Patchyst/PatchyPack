# Author: Patrick Story
# https://github.com/Patchyst
# https://github.com/Patchyst/PatchyPack
#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import crypt
import re
import argparse
import hashlib
from termcolor import cprint
import pyfiglet
cprint(pyfiglet.figlet_format("Patchy's Hash Cracker"),'red', attrs=['bold'])
cprint(pyfiglet.figlet_format("1.0 "),'red', attrs=['blink'])
cprint("Compatible Hash Formats for 1.0: md5, sha512, sha256, sha224, sha1, sha384, DES", "magenta", attrs=['bold'])
Aparser = argparse.ArgumentParser()
Aparser.add_argument("hash_path", help="Path to password hash file", type=str)
Aparser.add_argument("dict_path", help="Path to password dictionary file", type=str)
Aparser.add_argument("-ht", "--hash_type", help="specify hash type")
Aparser.add_argument("-s", "--salt", help="There is a salt 0:2")
Aparser.add_argument("-va", "--viewall", action="store_true", help=" View all passwords and hashes being compared. usage example: --viewall Y")
Aparser.add_argument('-v', '--version', action='version', version='Patchy\'s Hash Cracker: 1.0')
args = Aparser.parse_args()

def DESdictionaryattack(hashpass):
    if args.viewall:
        view = True
    else:
        view = False
    if args.salt:
        salt = hashpass[0:2]
    dictionary_file = open(args.dict_path)
    for i in dictionary_file:
        word = i.strip("/n")
        word = word.strip("\n")
        word = word.replace(" ", "")
        if args.salt:
            ucryptword = crypt.crypt(word, salt)
        else:
            ucryptword = crypt.crypt(word)
        if view:
            print("[*] Attempting Hash: ", ucryptword, "for word: ", word)
        if ucryptword == hashpass:
            print("[+] Password found: ", word, "\n")
            return word
    print("[-] No password found :c", " Try another word list?")
    return

def dictionaryattack():
    if args.viewall:
        view = True
    else:
        view = False
    counter = 1
    passwordfile = open(args.hash_path)
    dictionary_file = open(args.dict_path, "r", encoding="latin-1")
    for line in passwordfile.readlines():
        line = line.replace(" ", "")
        for i in dictionary_file:
            word = i.strip("/n")
            word = word.strip("\n")
            word = word.replace(" ", "")
            word = str(word)
            if args.hash_type == "sha512":
                ucryptword = hashlib.sha512(word.encode()).hexdigest()
            elif args.hash_type == "sha256":
                ucryptword = hashlib.sha256(word.encode()).hexdigest()
            elif args.hash_type == "sha224":
                ucryptword = hashlib.sha224(word.encode()).hexdigest()
            elif args.hash_type == "md5":
                ucryptword = hashlib.md5(word.encode()).hexdigest()
            elif args.hash_type == "sha1":
                ucryptword = hashlib.sha1(word.encode()).hexdigest()
            elif args.hash_type == "sha384":
                ucryptword = hashlib.sha384(word.encode()).hexdigest()
            elif args.hash_type == "DES":
                passwordfile = open(args.hash_path)
                print("[*] DES hash type selected... \n")
                re_user = re.compile(r'^(.*):')
                re_hash = re.compile(r':(.*)')
                print("[*] Reading lines...")
                for line in passwordfile.readlines():
                    if ":" in line:
                        user = re_user.search(line).group(0)
                        user_hash = re_hash.search(line).group(0)
                        user_hash = user_hash[1:]
                        print("[*] Cracking ", user, "", user_hash)
                        # making sure it's a string with no new lines
                        user_hash = str(user_hash).replace(" ", "")
                        DESdictionaryattack(user_hash)
                        return
                    else:
                        DESdictionaryattack(line)
                        return
            else:
                if counter == 1:
                    print("[*] No hash type specified going with default: md5 \n")
                    print("[*] Use: --hash_type [hash type] to specify hash type\n")
                    counter+=1
                else:
                    pass
                ucryptword = hashlib.md5(word.encode()).hexdigest()
            if view:
                print("[*] Attempting Hash: ", ucryptword, " for word: ", word)
            if ucryptword == line:
                cprint("[+] Password found: " + word + "\n", "red", attrs=["bold"])
                return word
    print("[-] No password found :c", " Try another word list?")
    return


def main():
    try:
        dictionaryattack()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()

