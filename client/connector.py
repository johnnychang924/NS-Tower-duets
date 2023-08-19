import socket
import threading
import json

class Connector(threading.Thread):
    def __init__(self, address, port, player_name) -> None:
        threading.Thread.__init__(self)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (address, port)
        self.buffer = ""
        self.running = True
        self.player_name = player_name
        self.option_list = []
        self.game_start = False
        self.player_dict = dict()
        self.player_x = 0
        self.player_y = 0
        self.player_velocity_x = 0
        self.player_velocity_y = 0
        self.setup_x = 0
        self.setup_y = 0
        self.floor = []

    def run(self):
        self.server.connect(self.server_address)
        self.server.send((self.player_name + '$').encode('utf-8'))
        while self.running:
            self.receive_option()
            self.handle_option()
            self.send_pos()

    def send_pos(self):
        pack = "json$" + json.dumps((self.player_x, self.player_y, self.player_velocity_x, self.player_velocity_y)) + '$'
        self.server.send(pack.encode('utf-8'))

    def handle_option(self):
        is_json = False
        is_floor = False
        is_change_pos = False
        option_length = len(self.option_list)
        for i, option in enumerate(self.option_list):
            if option == "start":
                self.game_start = True
            elif option == "json":
                if i == option_length - 1:
                    option = option[-1:]
                    return
                else:
                    is_json = True
            elif is_json:
                self.player_dict = json.loads(option)
                is_json = False
            elif option == "floor":
                if i == option_length - 1:
                    option = option[-1:]
                    return
                else:
                    is_floor = True
            elif is_floor:
                new_floor = json.loads(option)
                is_floor = False
                if len(self.floor) == 0 or new_floor[1] > self.floor[-1][1]:
                    self.floor.append(new_floor)
            elif option == "changePos":
                if i == option_length - 1:
                    option = option[-1:]
                    return
                else:
                    is_change_pos = True
            elif is_change_pos:
                is_change_pos = False
                new_pos = json.loads(option)
                self.setup_x, self.setup_y = new_pos

    def receive_option(self):
        in_data = self.server.recv(1024).decode('utf-8')
        self.buffer += in_data
        while '$' in self.buffer:
            option = ""
            for i, char in enumerate(self.buffer):
                if char != '$':
                    option += char
                else:
                    self.buffer = self.buffer[i + 1:]
                    break
            self.option_list.append(option)
        
    def send_now_pos(self, x, y):
        self.server.send((f"x:{x} y:{y} ").encode('utf-8'))

if __name__ == "__main__":
    conn = Connector("192.168.129.1", 7000, "johnny")
    conn.start()
    if conn.game_start:
        print("start")