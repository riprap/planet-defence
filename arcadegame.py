"""
    Source file name: arcadegame.py
    
    Author:  Nolan Knill
    
    Last modified by: Nolan Knill
    
    Date last modified: January 11, 2011
    
    Program description: Arcadegame.py is an arcade adventure game where 
                         the player tries 

    Project: 1 - The Arcade Game
"""
import pygame, gameEngine, time, math

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
        if (current_time > self.last_shot + 0.25) or (self.last_shot == 0):
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
        self.health = 3
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        health = ""
        for i in range(0, int(self.health)):
            health += "+"
        self.text = "Score: %d %s" % (self.score, health)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()


class Planet(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("images/planet.gif")
        #puts planet in the middle of the screen
        self.x = 375
        self.y = 275

class Game(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self)
        self.character = Character(self)
        self.bullet = Bullet(self)
        self.scoreboard = Scoreboard(self)
        self.planet = Planet(self)
        self.sprites = [self.character, self.bullet, self.scoreboard, self.planet]

def startScreen(score):
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    instructions = (
    "Instructions"
    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 0))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    return donePlaying
       

def main():
    game = Game()
    game.start()



if __name__ == "__main__":
    main()