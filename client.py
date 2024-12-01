import socket
import chatlib
import sys  

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
	msg = chatlib.build_message(code, data)

	conn.send(msg.encode())
	

def recv_message_and_parse(conn):
	fullMsg = conn.recv(1024)

	cmd, data = chatlib.parse_message(fullMsg)

	return cmd, data

def connect():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((SERVER_IP, SERVER_PORT))

		print("Connected")

	except:
		print("Could not Establish Connection")

	return s


def error_and_exit(error_msg):
	print (error_msg)
	sys.exit()


def login(conn):
    username = input("username: \n")
	password = input("password: \n")
	
	build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], username)
	build_and_send_message(connn, chatlib.PROTOCOL_CLIENT["login_msg"], password)

	state = recv_message_and_parse(conn)

	print(stat)

def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
	print("logout")

def main():
    # Implement code
    pass

if __name__ == '__main__':
    main()
