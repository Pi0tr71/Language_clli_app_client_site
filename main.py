import json
import socket
import hashlib
from datetime import datetime, timedelta


class Data:
    def __init__(self):
        self.token = None
        self.username = None
        self.password = None
        self.category = None
        self.question_id = None

    def get_token(self):
        return self.token


def client_program(action_type):
    host = socket.gethostname()  # as both code is running on same pc if not change to server's ip address
    port = 5000  # socket server port number
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server
    if action_type == "login" or action_type == "register":
        data = {"action_type": action_type, "username": user_data.username, "password": user_data.password}
    elif action_type == "category":
        data = {"action_type": action_type}
    elif action_type == "questions":
        data = {"action_type": action_type, "token": user_data.token, "category": user_data.category}
    elif action_type == "user_answers":
        after_week = str(datetime.today() + timedelta(days=7))
        data = {"action_type": action_type, "token": user_data.token, "question_id": user_data.question_id, "date": after_week}
    client_socket.send(json.dumps(data).encode())  # send message
    answer = json.loads(client_socket.recv(1024).decode())  # receive response
    client_socket.close()  # close the connection
    if "token" in answer:
        user_data.token = answer["token"]
    return answer


def login_or_register():
    choice = input("Do you want to log in or register? (l/r)")
    if choice == "l":
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        hashed = hashlib.sha256(password.encode()).hexdigest()
        user_data.username = username
        user_data.password = hashed
        answer = client_program("login")
        if answer["answer"]:
            learning()
        else:
            print("Incorrect username or password")
            login_or_register()
    elif choice == "r":
        username = input("Enter a new username: ")
        password = input("Enter a new password: ")
        password_confirm = input("Confirm your password: ")
        if not password_confirm == password:
            print("Passwords are not the same")
            login_or_register()
        hashed = hashlib.sha256(password.encode()).hexdigest()
        user_data.username = username
        user_data.password = hashed
        answer = client_program("register")
        if answer["answer"]:
            learning()
        else:
            print("This username is already taken")
    else:
        print("Invalid choice. Please enter 'l' to log in or 'r' to register.")
        login_or_register()


def learning():
    while True:
        print("Choose which one category you want to learn. Enter number")
        answer = client_program("category")
        if len(answer) == 0:
            print("No more words to learn. Check back in a few days")
        for i, item in enumerate(answer):
            print(i + 1, ".", item)
        user_data.category = input("Number : ")
        questions = client_program("questions")
        for question_id, question_text, question_answer in questions:
            text = "Translate " + str(question_text) + " : "
            user_answer = input(text)
            if user_answer == question_answer:
                print("Good job")
                user_data.question_id = question_id
                client_program("user_answers")
            else:
                print("Bad answer. Correct answer : ", question_answer)
        print("Lesson is over. Good Job !")


user_data = Data()
login_or_register()
