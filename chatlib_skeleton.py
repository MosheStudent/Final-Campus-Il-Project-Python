# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR"
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
	if cmd not in PROTOCOL_CLIENT.values():
		return ERROR_RETURN        
	
	msg = f"{cmd}\t{DELIMITER} {"0" * (LENGTH_FIELD_LENGTH - int(len(str(len(data)))))}{len(data)}{DELIMITER}{data}"
	
	return msg

def parse_message(data):
	cmd = ""
	msg = ""
	cmdFlag = False

	for char in data:
		if (char == " "):
			cmdFlag = True	

		if not cmdFlag:
			cmd += char

		else:
			msg += char

	return cmd, msg

	
def split_data(msg, expected_fields):
	dataList = []
	data = ""
	iteration = 0
	

	for char in msg:
		iteration += 1

		if char != DATA_DELIMITER:
			data += char

		if char == DATA_DELIMITER or iteration == len(msg):
			dataList.append(data)
			data = ""

	if (len(dataList) == expected_fields):
		return dataList
	
	return ERROR_RETURN






def join_data(msg_fields):

	fullmsg = ""

	for item in msg_fields:
		if item == msg_fields[len(msg_fields) - 1]:
			fullmsg += str(item)
		else:
			fullmsg += str(item) + DATA_DELIMITER

	return fullmsg