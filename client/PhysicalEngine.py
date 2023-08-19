import pygame
import time

class PhysicalEngine:
    def __init__(self, gameobjects = []) -> None:
        self.gameObjects = gameobjects
        self._filterGameObjects()
        self.lastTime = time.time()
    
    def add(self, gameObject):
        self.gameObjects.append(gameObject)
        if gameObject.moveable:
            self.moveableObjects.append(gameObject)
        else:
            self.grounds.append(gameObject)
    
    def calculate(self):
        #collision_torence = 5
        collision_torence = 10
        wind_force = 0.01
        deltaTime = time.time() - self.lastTime
        deltaTime *= 1
        self.lastTime = time.time()
        for object in self.moveableObjects:
            object.force.y -= 800 * object.mass
            object.rect.centerx = object.transform.x
            object.rect.centery = object.transform.y
            for i in range(4):
                object.touch[i] = False
            for collision in self.gameObjects:
                if collision == object:
                    continue
                if pygame.Rect.colliderect(object.rect, collision.rect):
                    x_inter = (object.transform.width + collision.transform.width) / 2 - abs(object.transform.x - collision.transform.x)
                    y_inter = (object.transform.height + collision.transform.height) / 2 - abs(object.transform.y - collision.transform.y)
                    if x_inter > y_inter:
                        if object.transform.y > collision.transform.y:
                            object.touch[2] = True
                        else:
                            object.touch[0] = True
                    else:
                        if object.transform.x > collision.transform.x:
                            if y_inter > collision_torence:
                                object.touch[3] = True
                                if collision.velocity.x > 0:
                                    object.velocity.x = collision.velocity.x
                        else:
                            if y_inter > collision_torence:
                                object.touch[1] = True
                                if collision.velocity.x < 0:
                                    object.velocity.x = collision.velocity.x
                '''if pygame.Rect.colliderect(object.rect, collision.rect):
                    if abs(object.rect.bottom - collision.rect.top) < collision_torence:
                        object.touch[2] = True
                    if abs(object.rect.top - collision.rect.bottom) < collision_torence:
                        object.touch[0] = True
                    if abs(object.rect.right - collision.rect.left) < collision_torence:
                        object.touch[1] = True
                    if abs(object.rect.left - collision.rect.right) < collision_torence:
                        object.touch[3] = True'''
        '''for object in self.moveableObjects:
            if object.touch[1]:
                object.force.x = min(0, object.force.x)
                object.velocity.x = min(0, object.velocity.x)
                #object.velocity.x = object.velocity.x * -0.4 if object.velocity.x > 0 else object.velocity.x
                object.acceleration.x = min(0, object.acceleration.x)
            if object.touch[3]:
                object.force.x = max(0, object.force.x)
                object.velocity.x = max(0, object.velocity.x)
                #object.velocity.x = object.velocity.x * -0.4 if object.velocity.x < 0 else object.velocity.x
                object.acceleration.x = max(0, object.acceleration.x)
            if object.touch[0]:
                object.force.y = min(0, object.force.y)
                object.velocity.y = min(0, object.velocity.y)
                object.acceleration.y = min(0, object.acceleration.y)
            if object.touch[2]:
                object.force.y = max(0, object.force.y)
                object.velocity.y = max(0, object.velocity.y)
                object.acceleration.y = max(0, object.acceleration.y)
                object.force.x = object.force.x - object.velocity.x * 50000 if object.velocity.x * 50000 < object.force.x else 0
            object.force.x -= object.velocity.x * wind_force
            object.force.y -= object.velocity.y * wind_force
            object.transform.x += object.velocity.x * deltaTime
            object.transform.y += object.velocity.y * deltaTime
            object.velocity.x += object.acceleration.x * deltaTime
            object.velocity.y += object.acceleration.y * deltaTime
            object.acceleration.x = object.force.x / object.mass
            object.acceleration.y = object.force.y / object.mass
            object.force.x = 0
            object.force.y = 0'''
        for object in self.moveableObjects:
            if object.touch[1]:
                object.force.x = min(0, object.force.x)
                #object.velocity.x = min(0, object.velocity.x)
                object.velocity.x = object.velocity.x * -0.4 if object.velocity.x > 0 else object.velocity.x
                object.acceleration.x = min(0, object.acceleration.x)
            if object.touch[3]:
                object.force.x = max(0, object.force.x)
                #object.velocity.x = max(0, object.velocity.x)
                object.velocity.x = object.velocity.x * -0.4 if object.velocity.x < 0 else object.velocity.x
                object.acceleration.x = max(0, object.acceleration.x)
            if object.touch[0]:
                object.force.y = min(0, object.force.y)
                object.velocity.y = min(0, object.velocity.y)
                object.acceleration.y = min(0, object.acceleration.y)
            if object.touch[2]:
                object.force.y = max(0, object.force.y)
                object.velocity.y = max(0, object.velocity.y)
                object.acceleration.y = max(0, object.acceleration.y)
                object.force.x -= object.velocity.x * 100
            object.force.x -= object.velocity.x * wind_force
            object.force.y -= object.velocity.y * wind_force
            object.transform.x += object.velocity.x * deltaTime
            object.transform.y += object.velocity.y * deltaTime
            object.velocity.x += object.acceleration.x * deltaTime
            object.velocity.y += object.acceleration.y * deltaTime
            object.acceleration.x = object.force.x / object.mass
            object.acceleration.y = object.force.y / object.mass
            object.force.x = 0
            object.force.y = 0

    def _filterGameObjects(self):
        self.moveableObjects = []
        self.grounds = []
        for object in self.gameObjects:
            if object.moveable:
                self.moveableObjects.append(object)
            else :
                self.grounds.append(object)
                