"""
    Source file name: arcadegame.py
    
    Author:  Nolan Knill
    
    Last modified by: Nolan Knill
    
    Date last modified: January 11, 2011
    
    Program description: Arcadegame.py is an arcade adventure game where 
                         the player tries 

    Project: 1 - The Arcade Game
"""
import pygame, gameEngine, time

class Character(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("images/character.bmp")
        self.setSpeed(0)
        self.setAngle(0)

    def shoot(self):
        current_time = time.clock()
        if 'last_shot' not in vars():
            last_shot = 0
        if last_shot < (current_time - 1):
            print("shoot em", pygame.mouse.get_pos())
            last_shot = current_time
        else:
            print("cant shoot")
    def checkEvents(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_LEFT]:
            self.setDX(-3)
            self.setDY(0)
            self.setRotation(180)
        elif keys[pygame.K_RIGHT]:
            self.setDX(3)
            self.setDY(0)
            self.setRotation(0)      
        elif keys[pygame.K_UP]:
            self.setDY(-3)
            self.setDX(0)
            self.setRotation(90)
        elif keys[pygame.K_DOWN]:
            self.setDY(3)
            self.setDX(0)
            self.setRotation(270)
        else:
            self.setDX(0)
            self.setDY(0)
        if mouse[0]:
            """
            put the below in the 
            character.shoot() method
            """
            self.shoot()

class Game(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self)
        self.character = Character(self)
        self.sprites = [self.character]

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
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = startScreen(score)
    game = Game()
    game.start()

if __name__ == "__main__":
    main()