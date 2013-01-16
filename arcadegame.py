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
        self.setImage("images/character.bmp")
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
            getting angle to shoot from spaceship
            """
            dy = mouse_pos[1] - self.scene.character.y
            dx = mouse_pos[0] - self.scene.character.x
            angle = -math.degrees(math.atan2(dy,dx))
            print(angle)
            #get character x and character y, and mouse_pos[0], mouse_pos[1]
            self.setAngle(angle)
        else:
            print("Cant fire that quickly")
    def reset(self):
        self.setPosition ((-100, -100))
        self.setSpeed(0)

class Game(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self)
        self.character = Character(self)
        self.bullet = Bullet(self)
        self.sprites = [self.character, self.bullet]

def startScreen(score):
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    instructions = (
    "Mail Pilot.     Last score: %d" % score ,
    "Instructions:  You are a mail pilot,",
    "delivering mail to the islands.",
    "",
    "Fly over an island to drop the mail,",
    "but be careful not to fly too close",    
    "to the clouds. Your plane will fall ",
    "apart if it is hit by lightning too",
    "many times. Steer with the mouse.",
    "",
    "good luck!",
    "",
    "click to start, escape to quit..."
    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 0))
        insLabels.append(tempLabel)
    
    donePlaying = True
    keepGoing = True
    clock = pygame.time.Clock()   
    pygame.mouse.set_visible(True)
    return donePlaying
        

def main():
    """ gotta fix this part

    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = startScreen(score)
    """

    game = Game()
    game.start()

if __name__ == "__main__":
    main()