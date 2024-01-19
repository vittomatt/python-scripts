#!/usr/bin/env python3

import argparse
import re
import sys
import signal
import subprocess
from termcolor import colored

def def_handler(sig, frame):
	print(colored("Saliendo!", "red"))
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def get_arguments():
	parser = argparse.ArgumentParser(description="Mac changer")
	parser.add_argument("-i", "--interface", required=True, dest="interface", help="Interface")
	parser.add_argument("-m", "--mac", required=True, dest="mac", help="Mac address")
	args = parser.parse_args()
	return (args.interface, args.mac)

def validate_inputs(interface, mac):
	is_valid_interface = re.match("^[e][n]\d{1,2}$", interface)
	is_valid_mac = re.match("^([A-Fa-f0-9]{2}[:]){5}[A-Fa-f0-9]{2}$", mac)
	if (not is_valid_interface or not is_valid_mac):
		print(colored('Invalid input', "red"))
		sys.exit(1)

def change_mac(interface, mac):
	subprocess.run(["ifconfig", interface, "down"])
	subprocess.run(["ifconfig", interface, "hw", "ether", mac])
	subprocess.run(["ifconfig", interface, "up"])
	print(colored("Mac changed successfully!", "green"))
	sys.exit(0)

def main():
	interface, mac = get_arguments()
	validate_inputs(interface, mac)
	change_mac(interface, mac)

if __name__ == "__main__":
	main()
