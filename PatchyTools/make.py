
import subprocess
print("Starting make script... ")
pip_version = str(input("What is your pip version for Python3 [pip/pip3] "))
if pip_version != "pip3" and pip_version != "pip":
    error_msg = "[-] pip3 or pip not selected this may cause issues, continue with pip version? [Y/N] " + pip_version
    pip_error = input(str(error_msg))
    if pip_error == "Y" or pip_error == "y":
        pass
    else:
        exit(1)
else:
    package_list = ["nclib", "scapy", "ipaddress", "termcolor", "pyfiglet", "requests", "hashlib"]
    for package in package_list:
        try:
            subprocess.call([pip_version, "install", package])
        except Exception as e:
            print(e)