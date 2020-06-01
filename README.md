# PatchyPack [Alpha]
Patchy Pack [Alpa]. A set of command line tools for anything from port scanning to web shell generation.
Patchy Pack is far from finished with many more updates, features, and bug fixes on the way.
## Reccomended OS: Linux
# Installation
After downloading the PatchyTools folder run the setup script for setting up aliases/shortcuts:
```
chmod +rwx setup
./setup
```
While you're in the PatchyTools directory give permissions to the genshell bash script. This script is responsible for generating php webshells.
```
chmod +rwx genshell
```
Note that you'll have to close and reopen the current shell session or run:
```
source .bash_profile
```
This will let the changes take effect. Bash profiles may vary. 
Next, run the make.py script for installing necessary dependencies and packages:
```
python3 make.py
```
# Intro
Check out the options for Patchy Pack by typing: 
```
patchy
```
Further Usage and examples can be found on: https://patchyst.github.io/patchy/ (I haven't finished documentation on the tools yet :/)

# Cracking Hashes with Patchy Pack
So far Patchyhash can crack a variety of hashing algorithims such as md5, sha512, sha256, sha224, sha1, sha384, and DES.
 ## Usage and examples:
```
$ patchyhash -h

usage: patchyhash [-h] [-ht HASH_TYPE] [-s SALT] [-va] [-v]
                          hash_path dict_path

positional arguments:
  hash_path             Path to password hash file
  dict_path             Path to password dictionary file

optional arguments:
  -h, --help            show this help message and exit
  -ht HASH_TYPE, --hash_type HASH_TYPE
                        specify hash type
  -va, --viewall        View all passwords and hashes being compared. usage
                        example: --viewall Y
  -v, --version         show program's version number and exit
```
The positional arguments are required. The first is the path to the file containing the target hash. The second positional argument is the wordlist for pathcyhash to check against. If no hashing algorithim is specified patchyhash defaults to md5
Example:
```
patchyhash ~/md5password.txt ~/worlists/rockyou.txt
```
Optional arguments include salt, hash type, and an option to view all hashes being checked against target hash.
```
patchyhash ~/shapassword.txt ~/worlists/rockyou.txt --hast_type sha256 --viewall
```
* --viewall: view all hashes compared with target hash
* --hash_type: specify hashing algorithim (in this case sha256)
```
patchyhash ~/shapassword.txt ~/worlists/rockyou.txt -ht sha256 -va
```
* -va: Same as view all
* -ht: same as hashtype
# Generating and Accessing Web Shell with Patchy Pack
Before accessing a web shell we have to generate it. As of now. patchygen only generates php based webshells.
```
$ patchygen -h
Desc: Used to generate a webshell
Required Usage: patchy genshell webshell_file webshell_name
Optional Usage: [-p]: set a password for php shell
	example: patchy genshell shell.php shell -p passw0rd!
		 patchy genshell /root/webshells/myshell.php nameofmyshell
```
To generate a simple php webshell with no password just give a the webshell file path and the desired shell name:
```
patchygen ~/webshells/shell.php shellname
```
Upload the webshell to a vulnerable site and access it manually using a get request or patchyshell for easier access.
```
patchyshell http://somesite.com/shell.php shellname
```
patchyshell help page:
```
usage: accessshell.py [-h] [--password PASSWORD] target_url shell_name
accessshell.py: error: the following arguments are required: target_url, shell_name
Patricks-MacBook-Air:~ patrick$ patchyshell -h
usage: accessshell.py [-h] [--password PASSWORD] target_url shell_name

positional arguments:
  target_url           The target URL
  shell_name           Name of shell

optional arguments:
  -h, --help           show this help message and exit
  --password PASSWORD  password for shell
  ```
