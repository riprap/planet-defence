"""
    Source file name: arcadegame.py
    
    Author:  Nolan Knill
    
    Last modified by: Nolan Knill
    
    Date last modified: January 11, 2011
    
    Program description: Arcadegame.py is an arcade adventure game where 
                         the player tries 

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
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.setDX(-speed)
            self.setDY(0)
            self.setRotation(180)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.setDX(speed)
            self.setDY(0)
            self.setRotation(0)      
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            self.setDY(-speed)
            self.setDX(0)
            self.setRotation(90)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.setDY(speed)
            self.setDX(0)
            self.setRotation(270)
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
            self.setSpeed(50)
            """
            getting angle to shoot from spaceship, since gameEngine.dirTo doesn't seem to work
            """
            dy = mouse_pos[1] - self.scene.character.y
            dx = mouse_pos[0] - self.scene.character.x
            angle = -math.degrees(math.atan2(dy,dx))
            #get character x and character y, and mouse_pos[0], mouse_pos[1]
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
        for i in range(0, int(self.planet.getHealth())):
            health += "+"
        self.text = "Score: %d %s" % (self.score, health)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()

class Enemy(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("images/electrode.gif")
        self.start_position()
    
    def reset(self):
        """ change attributes randomly """
        
        #set random position
        x = random.randint(10, self.screen.get_width())
        y = random.randint(10, self.screen.get_height())
        self.setPosition((x, y))
        
        #set random size
        scale = random.randint(10, 40)
        self.setImage("images/electrode.gif")

    def start_position(self):
        quadrant = random.randint(1,4) #top, right, bottom, left
        if quadrant == 1: #(top)
            self.y = 25
            self.x = random.randint(100,700)
        if quadrant == 2:
            self.y = random.randint(100,500)
            self.x = 775
        if quadrant == 3:
            self.y = 575
            self.x = random.randint(100,700) 
        elif quadrant == 4:
            self.y = random.randint(100,500)
            self.x = 25

class Planet(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("images/planet.gif")
        #puts planet in the middle of the screen
        self.x = 375
        self.y = 275
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
            print("ello govna")

        enemyHitPlanet = self.character.collidesWith(self.planet)
        if enemyHitPlanet:
            print ("enemyHitPlanet")

        bulletHitPlanet = self.bullet.collidesWith(self.planet)
        enemyHitPlanet = self.bullet.collidesWith(self.planet)
        if bulletHitPlanet or enemyHitPlanet:
            self.planet.changeHealth(-1)

        bulletHitEnemy = self.bullet.collidesGroup(self.enemies)
        if bulletHitEnemy:
            print("BulletHitEnemy")
            bulletHitEnemy.reset()

    def instructions(self, score):
        print("score")

def main():
    game = Game()
    game.start()



if __name__ == "__main__":
    main()