import socket
import threading
import sqlite3

host = socket.gethostbyname(socket.gethostname())
port = 9090
enc = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Database connection
db = sqlite3.connect("YallaChat.db", check_same_thread=False)
cur = db.cursor()

# Ensure the users table exists
cur.execute("""CREATE TABLE IF NOT EXISTS users (
    username TEXT UNIQUE,
    name TEXT,
    email TEXT,
    password TEXT
)""")
db.commit()

def handle_client(conn, addr):
    try:
        while True:
            execmsg = conn.recv(1024).decode(enc).split(',')
            command = execmsg[0]
            if command == "login":
                user_login(conn, execmsg[1:])
            elif command == "signup":
                user_signup(conn, execmsg[1:])
            elif command == "!DISCONNECT":
                break
    finally:
        conn.close()

def user_signup(conn, data):
    username, name, email, password = data
    try:
        cur.execute("INSERT INTO users (username, name, email, password) VALUES (?, ?, ?, ?)", 
                    (username, name, email, password))
        db.commit()
        conn.send("Signup Successful!".encode(enc))
    except sqlite3.IntegrityError:
        conn.send("Signup failed: Username already exists.".encode(enc))
    except Exception as e:
        conn.send(f"Signup failed with error: {e}".encode(enc))

def user_login(conn, data):
    username, password = data
    try:
        cur.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cur.fetchone()
        if result and result[0] == password:
            conn.send("Login Success!".encode(enc))
        else:
            conn.send("Login failed: Incorrect username or password.".encode(enc))
    except Exception as e:
        conn.send(f"Login failed with error: {e}".encode(enc))

def main():
    print("Server is listening...")
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"Active connections: {threading.activeCount() - 1}")
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        db.close()
        server.close()

if __name__ == '__main__':
    main()
