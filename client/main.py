import pygame
import time
import random
from GameObject import GameObject
from PhysicalEngine import PhysicalEngine
from connector import Connector

default_height, default_width = 700, 1000 # screen size
server_address = '192.168.128.1'
server_port = 7000
player_name = "johnny"

def create_floor(x, y, length):   #(x, y) is the position of first block, length is the number of blocks
    global gameObjects, physicalEngine
    collider = GameObject(x, y, 50, length * 50)
    gameObjects.append(collider)
    physicalEngine.add(collider)
    for i in range(length):
        floor = GameObject(x + 50 * i - (length - 1) * 50 / 2, y, 50, 50, sprite = "ground.png")
        gameObjects.append(floor)

def floor_check():
    global camera, gameObjects, highest_floor, floor_gap
    while camera.transform.y + camera.transform.height / 2  + 1000 > highest_floor:
        length = random.randrange(4, 8)
        x = random.randrange(int(- camera.transform.width / 2), int(camera.transform.width / 2))
        create_floor(x, highest_floor + floor_gap, length)
        highest_floor += floor_gap

def draw_gameObjects():
    global screen_scale, windows, camera
    windows.fill((255, 255, 255))
    for thing in gameObjects:
        if thing.sprite:
            fixed_image = pygame.transform.scale(img_dict[thing.sprite], (thing.transform.width * screen_scale, thing.transform.height * screen_scale))
            x = camera.transform.width / 2 + (thing.transform.x - camera.transform.x) - thing.transform.width / 2
            y = camera.transform.height / 2 - (thing.transform.y - camera.transform.y) - thing.transform.height / 2
            windows.blit(fixed_image, (x * screen_scale, y * screen_scale))
        if thing.text:
            head_font = pygame.font.SysFont(None, int(thing.font_size * screen_scale))
            text = head_font.render(thing.text, True, (0, 0, 0))
            rect = text.get_rect()
            x = camera.transform.width / 2 + (thing.transform.x - camera.transform.x) - rect.width / 2
            y = camera.transform.height / 2 - (thing.transform.y - camera.transform.y) - rect.height / 2
            windows.blit(text, (x * screen_scale, y * screen_scale))
    pygame.display.update()

def move_camera_auto():
    global camera, camera_speed, camera_timer
    now_time = time.time()
    camera.transform.y += camera_speed * (now_time - camera_timer)
    camera_timer = now_time

def move_camera_player():
    global camera, player
    camera.transform.x, camera.transform.y = player.transform.x, player.transform.y

def check_alive():
    global player, camera, current_mode
    if current_mode == "waiting":
        return
    if player.transform.y < camera.transform.y - camera.transform.height / 2 - 100:
        current_mode = "dead"
        gameObjects.clear()
        gameObjects.append(GameObject(0, 0, 0, 0, text = "You Lose", font_size=300))
        camera.transform.x = 0
        camera.transform.y = 0

floor_has_been_draw = 0

def main_loop():
    global running, screen_scale, physicalEngine, current_mode, conn, hint, other_player, gameObjects, start_floor
    left, right = False, False
    first = True
    while running:
        draw_gameObjects()
        if conn.game_start and first:
            first = False
            current_mode = "alive"
            gameObjects.remove(hint)
            del hint
            #gameObjects.remove(start_floor)
            player.transform.x, player.transform.y = conn.setup_x, conn.setup_y
        current_mode = "alive" if conn.game_start else "waiting"
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
            elif current_mode == "waiting":
                pass
            elif event.type == pygame.VIDEORESIZE:
                camera.transform.height = event.h
                camera.transform.width = event.w
                screen_scale = min(event.h / default_height, event.w / default_width)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left = True
                elif event.key == pygame.K_RIGHT:
                    right = True
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if player.touch[2]:
                        player.force.y += 10000000
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                elif event.key == pygame.K_RIGHT:
                    right = False
        if left:
            player.force.x -= 100000
        if right:
            player.force.x += 100000
        if current_mode == "alive":
            check_alive()
            move_camera_auto()
            #move_camera_player()
            global floor_has_been_draw
            while len(conn.floor) > floor_has_been_draw:
                create_floor(conn.floor[floor_has_been_draw][0], conn.floor[floor_has_been_draw][1], conn.floor[floor_has_been_draw][2])
                floor_has_been_draw += 1
            #floor_check()
            #conn.send_now_pos(player.transform.x, player.transform.y)
        for i, (other_name, value) in enumerate(conn.player_dict.items()):
            if len(other_player) <= i:
                new_player = GameObject(0, 0, 100, 100, sprite = "other_player.png", text = "other player", font_size = 40)
                other_player.append(new_player)
                gameObjects.append(new_player)
                physicalEngine.add(new_player)
            other_player[i].transform.x, other_player[i].transform.y = value[0], value[1]
            other_player[i].rect.centerx = value[0]
            other_player[i].rect.centery = value[1]
            other_player[i].text = other_name
            if len(value) <= 2:
                print("load other player failed")
                continue
            other_player[i].velocity.x = value[2]
            other_player[i].velocity.y = value[3]
        physicalEngine.calculate()
        conn.player_x, conn.player_y = player.transform.x, player.transform.y
        conn.player_velocity_x, conn.player_velocity_y = player.velocity.x, player.velocity.y
        #player.transform.x = camera.transform.x
        #player.transform.y = camera.transform.y


if __name__ == "__main__":
    server_address = input("server address:")
    player_name = input("Your Name:")
    pygame.init()
    physicalEngine = PhysicalEngine()
    height, width = default_height, default_width
    screen_scale = 1
    camera_speed = 10
    windows = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    img_dict = dict()
    img_dict["ground.png"] = pygame.image.load("ground.png")
    img_dict["other_player.png"] = pygame.image.load("other_player.png")
    img_dict["player.png"] = pygame.image.load("player.png")
    pygame.display.set_caption("NS-TOWER")
    gameObjects = []
    camera = GameObject(x = 0, y = 0, height = default_height, width = default_width)
    player = GameObject(0, 0, 100, 100, mass = 50, sprite = "player.png", text = player_name, font_size = 40, moveable = True)
    other_player = []
    physicalEngine.add(player)
    gameObjects.append(player)
    running = True
    camera_timer = time.time()
    highest_floor = -250
    floor_gap = 300
    current_mode = "waiting"
    hint = GameObject(0, 300, 0, 0, text = "Waiting Server connect", font_size = 100)
    gameObjects.append(hint)
    start_floor = create_floor(0, highest_floor, 15)
    conn = Connector(server_address, server_port, player_name)
    conn.start()
    main_loop()