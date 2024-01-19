#!/usr/bin/env python3

import argparse
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor
import sys
import subprocess
import signal

def def_handler(sig, frame):
    print(colored("[!] Exiting...", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def parse_args():
    parser = argparse.ArgumentParser(description='ICMP Scanner')
    parser.add_argument('-t', '--target', required=True, dest='targets', help='Target IP Addresses')
    args = parser.parse_args()
    return args.targets

def parser_targets(targets_str):
    octets = targets_str.split('.')
    if len(octets) != 4:
        print(colored("[!] Invalid IP Address", 'red'))
        sys.exit(1)

    first_three_octets = '.'.join(octets[:3])
    last_octect = octets[-1]

    if "-" not in last_octect:
        ip = first_three_octets + "." + last_octect
        return [ip]
    
    start, end = last_octect.split('-')
    ips = [f"{first_three_octets}.{i}" for i in range(int(start), int(end) + 1)]
    return ips

def host_discovery(target):
    command = ['ping', '-c', '1', target]
    try:
        result = subprocess.run(command, timeout=1, stdout=subprocess.DEVNULL)
        if result.returncode == 0:
            print(colored(f"[+] Host {target} is up", 'green'))
    except subprocess.TimeoutExpired:
        pass

def main():
    targets_str = parse_args()
    targets = parser_targets(targets_str)

    max_workers = 10
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(host_discovery, targets)

if __name__ == '__main__':
    main()
