import socket, random, select

# Constants and Globals
CMD_FIELD_LENGTH = 16
LENGTH_FIELD_LENGTH = 4
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH
DELIMITER = "|"
DATA_DELIMITER = "#"
PROTOCOL_CLIENT = {
    'login_msg': "LOGIN",
    'logout_msg': "LOGOUT",
    'getscore_msg': "MY_SCORE",
    'getlogged_msg': "LOGGED",
    'gethighscore_msg': "HIGHSCORE",
    'getquestion_msg': "GET_QUESTION",
    'sendanswer_msg': "SEND_ANSWER"
}
PROTOCOL_SERVER = {
    'login_ok_msg': "LOGIN_OK",
    'login_failed_msg': "ERROR",
    'yourscore_msg': "YOUR_SCORE",
    'highscore_msg': "ALL_SCORE",
    'logged_msg': "LOGGED_ANSWER",
    'correct_msg': "CORRECT_ANSWER",
    'wrong_msg': "WRONG_ANSWER",
    'question_msg': "YOUR_QUESTION",
    'error_msg': "ERROR",
    'noquestions_msg': "NO_QUESTIONS"
}
ERROR_RETURN = None

users = {}
questions = {}
logged_users = {}
messages_to_send = []
ERROR_MSG = "Error! "
SERVER_PORT = 5678
CORRECT_ANSWER_POINTS = 5
WRONG_ANSWER_POINTS = 0


# Helper Functions
def build_message(cmd, data):
    data_length = len(data)
    cmd_length = len(cmd)
    if data_length > MAX_DATA_LENGTH or cmd_length > CMD_FIELD_LENGTH:
        return ERROR_RETURN
    padded_cmd = cmd.ljust(CMD_FIELD_LENGTH)
    padded_length = str(data_length).zfill(LENGTH_FIELD_LENGTH)
    return f"{padded_cmd}{DELIMITER}{padded_length}{DELIMITER}{data}"


def parse_message(full_msg):
    if len(full_msg) < MSG_HEADER_LENGTH:
        return ERROR_RETURN, ERROR_RETURN
    cmd = full_msg[:CMD_FIELD_LENGTH].strip()
    if full_msg[CMD_FIELD_LENGTH] != DELIMITER:
        return ERROR_RETURN, ERROR_RETURN
    length_str = full_msg[CMD_FIELD_LENGTH + 1:CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH]
    if not length_str.isdigit():
        return ERROR_RETURN, ERROR_RETURN
    length = int(length_str)
    if len(full_msg) < MSG_HEADER_LENGTH + length:
        return ERROR_RETURN, ERROR_RETURN
    data = full_msg[MSG_HEADER_LENGTH:MSG_HEADER_LENGTH + length]
    return cmd, data


def split_data(msg, expected_fields):
    fields = msg.split(DATA_DELIMITER)
    return fields if len(fields) == expected_fields else None


def join_data(msg_fields):
    return DATA_DELIMITER.join(msg_fields)


# Server Functions
def setup_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", SERVER_PORT))
    sock.listen()
    print(f"Server is running on port {SERVER_PORT}")
    return sock


def handle_client_message(conn, cmd, data):
    try:
        if cmd == PROTOCOL_CLIENT['login_msg']:
            handle_login_message(conn, data)
        elif cmd == PROTOCOL_CLIENT['logout_msg']:
            handle_logout_message(conn)
        elif cmd == PROTOCOL_CLIENT['getscore_msg']:
            handle_getscore_message(conn, logged_users[conn])
        elif cmd == PROTOCOL_CLIENT['gethighscore_msg']:
            handle_highscore_message(conn)
        elif cmd == PROTOCOL_CLIENT['getlogged_msg']:
            handle_logged_message(conn)
        elif cmd == PROTOCOL_CLIENT['getquestion_msg']:
            handle_question_message(conn)
        elif cmd == PROTOCOL_CLIENT['sendanswer_msg']:
            handle_answer_message(conn, logged_users[conn], data)
        else:
            send_error(conn, "Unknown command")
    except Exception as e:
        send_error(conn, str(e))


def handle_login_message(conn, data):
    parts = split_data(data, 2)
    if not parts:
        send_error(conn, "Invalid login format")
        return
    username, password = parts
    if username not in users or users[username]["password"] != password:
        send_error(conn, "Invalid username or password")
        return
    logged_users[conn] = username
    build_and_send_message(conn, PROTOCOL_SERVER['login_ok_msg'], "")


def handle_logout_message(conn):
    if conn in logged_users:
        del logged_users[conn]
    conn.close()


def build_and_send_message(conn, cmd, data):
    message = build_message(cmd, data)
    if message:
        messages_to_send.append((conn, message))


def main():
    global users, questions
    users = load_user_database()
    questions = load_questions()

    server_socket = setup_socket()
    client_sockets = []

    while True:
        rlist, wlist, _ = select.select([server_socket] + client_sockets, client_sockets, [])
        for sock in rlist:
            if sock is server_socket:
                client_socket, _ = server_socket.accept()
                client_sockets.append(client_socket)
            else:
                try:
                    msg = sock.recv(MAX_MSG_LENGTH).decode()
                    if not msg:
                        client_sockets.remove(sock)
                        handle_logout_message(sock)
                        continue
                    cmd, data = parse_message(msg)
                    if cmd is None:
                        send_error(sock, "Invalid message format")
                    else:
                        handle_client_message(sock, cmd, data)
                except Exception:
                    client_sockets.remove(sock)
                    handle_logout_message(sock)

        for conn, message in messages_to_send:
            if conn in wlist:
                conn.sendall(message.encode())
        messages_to_send.clear()


if __name__ == "__main__":
    main()
