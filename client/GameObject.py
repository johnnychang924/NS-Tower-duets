from __future__ import annotations
import pygame

class Transform:
    def __init__(self, x = 0, y = 0, height = 1, width = 1):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

class vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GameObject():
    def __init__(self, x, y, height, width, mass = 1, sprite = None, text = None, font_size = 0, moveable = False, scale = (1, 1), bounce_rate = 0) -> None:
        # main define
        self.transform = Transform(x, y, height, width)
        self.mass = mass
        self.sprite = sprite
        self.text = text
        self.font_size = font_size
        self.moveable = moveable
        self.scale = vector(scale[0], scale[1])
        self.bounce_rate = bounce_rate
        self.child = []
        # support calculate
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.rect.centerx = x
        self.rect.centery = y
        self.force = vector(0, 0)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.touch = [False] * 4
