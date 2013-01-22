"""
    Source file name: arcadegame.py
    
    Author:  Nolan Knill
    
    Last modified by: Nolan Knill
    
    Date last modified: January 22, 2013
    
    Program description: Arcadegame.py is an space arcade planet
                         defense game. The player takes control
                         of a spaceship, and must defend his/her
                         planet from incoming self-destructing
                         Electrodes.

    Project: 1 - The Arcade Game
"""
import pygame, gameEngine, time, math, random

class Character(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("images/ship.bmp")
        self.setSpeed(0)
        self.setAngle(0)
    
    def checkEvents(self):
        speed = 10
        
        avatar_width = self.image.get_width()
        avatar_height = self.image.get_height()

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.setDY(0)
            self.setRotation(180)
            if self.x > avatar_width: 
                self.setDX(-speed)
            else:
                self.setDX(0)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.setDY(0)
            self.setRotation(0)
            if self.x < self.screen.get_width() - avatar_width:
                self.setDX(speed)
            else:
                self.setDX(0)
        
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            self.setDX(0)
            self.setRotation(90)
            if self.y > avatar_height:            
                self.setDY(-speed)
            else:
                self.setDY(0)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.setDX(0)
            self.setRotation(270)
            if self.y < self.screen.get_height() - avatar_height:
                self.setDY(speed)
            else:
                self.setDY(0)
        
        else:
            self.setDX(0)
            self.setDY(0)
        
        if mouse[0]:
            self.scene.bullet.fire()


class Bullet(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("images/bullet.gif")
        self.imageMaster = pygame.transform.scale(self.imageMaster, (5, 5))
        self.setBoundAction(self.HIDE)
        self.reset()
        self.last_shot = 0

    def fire(self):
        current_time = time.clock()
        if (current_time > self.last_shot + 0.50) or (self.last_shot == 0):
            self.last_shot = time.clock()
            mouse_pos = pygame.mouse.get_pos()
            self.setPosition((self.scene.character.x, self.scene.character.y))
            self.setSpeed(25)
            """
            getting angle to shoot from spaceship, since gameEngine.dirTo doesn't seem to work
            """
            dy = mouse_pos[1] - self.scene.character.y
            dx = mouse_pos[0] - self.scene.character.x
            angle = -math.degrees(math.atan2(dy,dx))
            self.setAngle(angle)
    
    def reset(self):
        self.setPosition ((-100, -100))
        self.setSpeed(0)


class Scoreboard(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        health = ""
        for i in range(0,3):
            health += "+"
        self.text = "Score: %d %s" % (self.score, health)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()

class Enemy(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.reset()
    
    def reset(self):
        quadrant = random.randint(1,4) #top, right, bottom, left
        if quadrant == 1: #(top)
            x = random.randint(100,700)
            y = 25
        if quadrant == 2:
            x = 775
            y = random.randint(100,500)
        if quadrant == 3:
            y = 575
            x = random.randint(100,700) 
        elif quadrant == 4:
            y = random.randint(100,500)
            x = 25
        self.setPosition((x,y))
        self.setSpeed(random.uniform(1,2.8))

        #self.getAngle(self.x,self.y)
        self.setImage("images/electrode.gif")


class Planet(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("images/planet.gif")
        avatar_width = 37.5
        avatar_height = 37.5
        center_x = self.screen.get_width()/2
        center_y = self.screen.get_height()/2
        self.x = center_x - avatar_width
        self.y = center_y - avatar_height
        self.health = 5

    def changeHealth(self, amount):
        self.health += amount

    def getHealth(self):
        return self.health

class Game(gameEngine.Scene):
    def __init__(self, score=0):
        gameEngine.Scene.__init__(self)
        keepGoing = True
        self.instructions(score)
        self.character = Character(self)
        self.bullet = Bullet(self)
        self.scoreboard = Scoreboard(self)
        self.planet = Planet(self)
        self.enemies = []
        for i in range(5):
            self.enemies.append(Enemy(self))
        self.enemyGroup = self.makeSpriteGroup(self.enemies)
        self.addGroup(self.enemyGroup)
        self.sprites = [self.character, self.bullet, self.scoreboard, self.planet]

    def update(self):
        shipHitEnemy = self.character.collidesGroup(self.enemies)
        if shipHitEnemy:
            shipHitEnemy.reset()
            self.

        enemyHitPlanet = self.planet.collidesGroup(self.enemies)
        if enemyHitPlanet:
            enemyHitPlanet.reset()

        bulletHitPlanet = self.bullet.collidesWith(self.planet)
        if bulletHitPlanet:
            #explosion
            #reduce health
            self.bullet.reset()

        bulletHitEnemy = self.bullet.collidesGroup(self.enemies)
        if bulletHitEnemy:
            bulletHitEnemy.reset()
            self.bullet.reset()

    def instructions(self, score):
        print("score")

def main():
    game = Game()
    game.start()



if __name__ == "__main__":
    main()