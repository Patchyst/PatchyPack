# Author: Patrick Story
# https://github.com/Patchyst
# https://github.com/Patchyst/PatchyPack
from scapy.all import *
import nclib
import socket
import argparse
from ipaddress import IPv4Address, IPv6Address
import re
import telnetlib
from termcolor import cprint
argsparser = argparse.ArgumentParser()
argsparser.add_argument("target_host", help="The target host. Can be a domain, IPV4 or IPv6")
argsparser.add_argument("--port_range", "-pr", type=int, nargs="*", help="Target a range of ports")
argsparser.add_argument("--port", "-p", type=int, nargs="*",
                        help="target specific ports")
argsparser.add_argument("--interactive", "-i", type=int,
                        help="Establish an interactive session with a port's service")
argsparser.add_argument("--verbose", "-vv", action="store_true", help="Show Exceptions such as error messages")
argsparser.add_argument("--timeout", "-t", type=float,
                        help="Set a custom timeout for connections. This is reccomended if you are doing a specific port scan. Example: patchyscan nmap.scanme.org -t 5.0 -p 443 80 21 23")
args = argsparser.parse_args()
open_ports = []


def YN_error(exception):
    if args.verbose:
        cprint("\nScan encountered an exception: ", "red", attrs=['bold'])
        print(exception)
    else:
        pass


def identify(ipaddr):
    try:
        addr = socket.gethostbyname(ipaddr)
    except:
        addr = args.target_host
    try:
        IPv4Address(addr)
        return socket.AF_INET
    except:
        pass
    try:
        IPv6Address(addr)
        return socket.AF_INET6
    except:
        pass


def host_format(host):
    if host[-1] == "/":
        host = host[0:-1]
        return host
    else:
        return host


def resolve_host(target_host):
    cprint("==== RESOLVING HOST ====", "red", attrs=["bold"])
    IP_addr = str(socket.gethostbyname(host_format(target_host)))
    ans_pkt = sr1(IP(dst=IP_addr) / ICMP(), timeout=5)
    if ans_pkt is None:
        cprint("==== CANNOT RESOLVE HOST ====", "red", attrs=["bold"])
        print("    This may cause issues sending and receiving packets.")
        print("[*] Note that a VPN may cause issues when routing packets")
        if args.verbose:
            print("[-] Error msg: \n")
        exit(1)
    elif ans_pkt is not None:
        cprint("==== HOST IS UP ====", "green", attrs=["bold"])


def TCP_scan(targethost, targetport):
    targethost = host_format(targethost)
    TCPconn = socket.socket(identify(targethost), socket.SOCK_STREAM)
    if args.timeout is not None:
        TCPconn.settimeout(args.timeout)
    else:
        TCPconn.settimeout(0.5)
    if identify(targethost) == socket.AF_INET:
        TCPconn.connect((targethost, int(targetport)))
    elif identify(targethost) == socket.AF_INET6:
        TCPconn.connect((targethost, int(targetport), 0, 0))
    if targetport == 80 or targetport == 443:
        webserverscan(targethost, targetport)
    elif targetport != 80 or targetport != 443 or targetport != 23:
        try:
            dresponse = TCPconn.recv(1024).decode()
            print("\n[+] Open Port " + str(targetport))
            if len(dresponse) < 1:
                print("Response is empty bytes string: ")
                print("Response: ", dresponse)
            else:
                print("Response: ", dresponse)
        except Exception as e:
            YN_error(e)
            if args.verbose:
                print(" for port ", targetport)
            try:
                eresponse = TCPconn.recv(1024)
                print("\n[+] Open Port " + str(targetport))
                if len(eresponse) < 1:
                    print("Response is empty bytes string: ")
                    print("Response: ", eresponse)
                elif len(eresponse) > 0:
                    print("Response: ", eresponse)
            except Exception as e:
                YN_error(e)
                if args.verbose:
                    print(" for port ", targetport)


def webserverscan(targeth, targetp):
    targeth = host_format(targeth)
    targetp = int(targetp)
    conn = socket.socket(identify(targeth), socket.SOCK_STREAM)
    if args.timeout is not None:
        conn.settimeout(args.timeout)
    else:
        conn.settimeout(0.5)
    if identify(targeth) == socket.AF_INET:
        conn.connect((targeth, int(targetp)))
    elif identify(targeth) == socket.AF_INET6:
        conn.connect((targeth, int(targetp), 0, 0))
    if targetp == 80:
        print("[+] Open port 80")
        try:
            conn.send(b"GET / HTTP/1.1\r\n\n\r")
            banner = conn.recv(1024)
            cutbanner = re.search(r'Server.*', banner.decode())
            print(cutbanner.group(0) + "\n")
        except Exception as e:
            YN_error(e)
            if args.verbose:
                print(" for port ", targetp)
    elif targetp == 443:
        print("[+] Open port 443")
        try:
            conn.send(b"GET / HTTPS/1.1\r\n\r\n")
            banner = conn.recv(1024)
            try:
                cutbanner = re.search(r'Server.*', banner.decode())
                print(cutbanner.group(0) + "\n")
            except:
                print(banner.decode())
        except:
            print("Port may be TCP wrapped")


def netcat_interact(targethost, targetport):
    ncat_conn = nclib.netcat.Netcat((targethost, int(targetport)), verbose=True)
    ncat_conn.interact()


def reg_scan(targethost, targetport):
    TCPconn = socket.socket(identify(targethost), socket.SOCK_STREAM)
    if args.timeout is not None:
        TCPconn.settimeout(args.timeout)
    else:
        TCPconn.settimeout(0.5)
    if identify(targethost) == socket.AF_INET:
        TCPconn.connect((targethost, int(targetport)))
    elif identify(targethost) == socket.AF_INET6:
        TCPconn.connect((targethost, int(targetport), 0, 0))
    if targetport == 23:
        with telnetlib.Telnet(targethost, targetport):
            print("[+] Open Port: 23")
            print("Telnet open \n")
    elif targetport == 80 or targetport == 443:
        webserverscan(targethost, targetport)
    elif targetport != 23 and targetport != 80 and targetport != 443:
        TCP_scan(targethost, targetport)


if __name__ == "__main__":
    IP_addr = str(socket.gethostbyname(host_format(args.target_host)))
    resolve_host(socket.gethostbyname(host_format(args.target_host)))
    start_msg = "\n Starting program on " + args.target_host + " [ " + socket.gethostbyname(host_format(args.target_host)) + " ] " + " This may take a few moments. \n"
    cprint(start_msg, 'green')
    if args.port_range is not None and args.port is not None:
        print("--port and --port_range cannot be used simultaneously")
    if args.port_range is not None:
        if len(args.port_range) != 2 | args.port_range[0] > args.port_range[1]:
            print("[ERROR] -pr --port_range requires 2 values (min, max)")
            print("     Usage example: patchyscan www.site.com -pr 22 445")
            exit(1)
        for port in range(args.port_range[0], args.port_range[1] + 1):
            try:
                reg_scan(IP_addr, port)
            except Exception as e:
                YN_error(e)
                if args.verbose:
                    print(" for port ", port)
    elif args.port:
        for port in args.port:
            try:
                reg_scan(IP_addr, port)
            except Exception as e:
                YN_error(e)
                if args.verbose:
                    print("on port ", port, "\n")
    elif args.interactive:
        try:
            netcat_interact(IP_addr, args.interactive)
        except Exception as e:
            YN_error(e)
    else:
        raise Exception("Invalid argument")
cprint("\n================================\n", 'red', attrs=['bold'])
