import socket
import threading
import time
import json
import random

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 7000
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
max_player_num = 2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

screen_width, screen_height = 700, 1000
timer = 0
camera_speed = 10
highest_floor = -250
floor_gap = 250
floor = []

def floor_check():
    global highest_floor, floor_gap
    while (time.time() - timer) * camera_speed  + 1000 > highest_floor:
        length = random.randrange(4, 8)
        x = random.randrange(int(- screen_width / 2), int(screen_width / 2))
        y = highest_floor + floor_gap
        floor.append((x, y, length))
        highest_floor += floor_gap

def handle_client(conn, index):
    global player_dict
    name = conn.recv(1024).decode(FORMAT)
    name = name[:-1]
    if name in player_dict:
        name += '*'
    player_dict[name] = (0, 0)
    print(name, "join the game")
    global game_start, s
    buffer = ""
    option_list = []
    while not game_start:
        pass
    conn.send("start$".encode(FORMAT))
    conn.send(("changePos$" + json.dumps((screen_width / (max_player_num + 1) * (index + 1) - screen_width / 2, 0)) + '$').encode(FORMAT))
    floor_has_been_send = 0
    global floor
    while True:
        while len(floor) > floor_has_been_send:
            conn.send(("floor$" + json.dumps(floor[floor_has_been_send]) + '$').encode(FORMAT))
            floor_has_been_send += 1
        new_player_dict = dict(player_dict)
        del new_player_dict[name]
        conn.send(("json$" + json.dumps(new_player_dict) + '$').encode(FORMAT))
        in_data = conn.recv(1024).decode(FORMAT)
        buffer += in_data
        while '$' in buffer:
            option = ""
            for i, char in enumerate(buffer):
                if char != '$':
                    option += char
                else:
                    buffer = buffer[i + 1:]
                    break
            option_list.append(option)
        is_json = False
        option_length = len(option_list)
        for i, option in enumerate(option_list):
            if option == "json":
                if i == option_length - 1:
                    option = option[-1:]
                    return
                else:
                    is_json = True
            elif is_json:
                is_json = False
                player_dict[name] = json.loads(option)
        time.sleep(0.1)

def start_server():
    global game_start, player_num, threads, timer
    print("server started at: ", socket.gethostbyname(socket.gethostname()))
    connect = True
    i = 0
    s.listen()
    while connect:
        conn, addr = s.accept()
        thread = threading.Thread(target = handle_client, args = (conn, i))
        thread.start()
        threads.append(thread)
        i += 1
        player_num += 1
        if player_num < max_player_num:
            print(f"need {max_player_num - player_num} more player")
        else:
            print("game start")
            game_start = True
            connect = False
            timer = time.time()
    while True:
        floor_check()
        time.sleep(10)
    
    
if __name__ == "__main__":
    threads = []
    game_start = False
    player_num = 0
    player_dict = dict()
    start_server()
    for thread in threads:
        thread.join()