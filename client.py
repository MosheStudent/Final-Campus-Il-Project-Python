import socket
import chatlib
import sys  

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
	msg = chatlib.build_message(code, data)
	"""
	Builds a new message using chatlib, wanted code and message. 
	Prints debug info, then sends it to the given socket.
	Paramaters: conn (socket object), code (str), data (str)
	Returns: Nothing
	"""
	# Implement Code
	

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
    username = input("Please enter username: \n")
    # Implement code
	
	build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"],"")
	
	# Implement code
	
    pass

def logout(conn):
    # Implement code
    pass

def main():
    # Implement code
    pass

if __name__ == '__main__':
    main()
