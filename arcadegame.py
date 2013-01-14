"""
    Source file name: arcadegame.py
    
    Author:  Nolan Knill
    
    Last modified by: Nolan Knill
    
    Date last modified: January 11, 2011
    
    Program description: Arcadegame.py is an arcade adventure game where 
                         the player tries 

    Project: 1 - The Arcade Game
"""
import pygame, gameEngine


class Character(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("images/character.bmp")
        self.setSpeed(0)
        self.setAngle(0)
    
    def checkEvents(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.setDX(-3)
            self.setDY(0)
        elif keys[pygame.K_RIGHT]:
            self.setDX(3)
            self.setDY(0)
        elif keys[pygame.K_UP]:
            self.setDY(-3)
            self.setDX(0)
        elif keys[pygame.K_DOWN]:
            self.setDY(3)
            self.setDX(0)
        else:
            self.setDX(0)
            self.setDY(0)

class Game(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self)
        self.character = Character(self)
        self.sprites = [self.character]

def main():
    game = Game()    
    game.start()

if __name__ == "__main__":
    main()