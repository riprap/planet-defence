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
pygame.mixer.init() #initialiaze pygame mixer (sound)
global DIFFICULTY
DIFFICULTY = 1

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
        self.sndFire = pygame.mixer.Sound("sounds/pew.ogg")
        self.sndFire.set_volume(0.5)

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
            self.sndFire.play(0)
    
    def reset(self):
        self.setPosition ((-100, -100))
        self.setSpeed(0)


class Scoreboard(gameEngine.SuperSprite):
    def __init__(self, scene, start_health=5):
        gameEngine.SuperSprite.__init__(self, scene)
        self.score = 0
        self.health = start_health + 1
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        health = self.health
        self.text = "Score: %d Health: %d" % (self.score, health)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()

    def change(self, d_health, d_score):
        self.health += d_health
        self.score += d_score

class Enemy(gameEngine.SuperSprite):
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.reset()

    def reset(self):
        width = self.screen.get_width()
        height = self.screen.get_height()
        quadrant = random.randint(1,4) #top, right, bottom, left
        if quadrant == 1: #(top)
            x = random.randint(-100,width+100)
            y = 0
        if quadrant == 2:
            x = width
            y = random.randint(-100,height+100)
        if quadrant == 3:
            y = height
            x = random.randint(-100,width+100) 
        elif quadrant == 4:
            y = random.randint(-100,height+100)
            x = 0

        self.setPosition((x,y))
        self.setSpeed(random.uniform(0.4,0.6))
        angle=self.dirTo((self.screen.get_width()/2, self.screen.get_height()/2))
        self.setAngle(angle)
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

class Explosion(gameEngine.SuperSprite):
    def __init__(self,scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("images/explosion.png")
        self.imageMaster = pygame.transform.scale(self.imageMaster, (30, 30))
        self.setBoundAction(self.HIDE)
        self.explosion_time = 0
        self.reset()

    def reset(self, x=-100, y=-100):
        self.setPosition ((x, y))
        self.setSpeed(0)

    #def 

class Game(gameEngine.Scene):
    def __init__(self):
        gameEngine.Scene.__init__(self)
        self.setCaption("Planet Defence")
        self.character = Character(self)
        self.bullet = Bullet(self)
        self.scoreboard = Scoreboard(self)
        self.planet = Planet(self)
        self.explosion = Explosion(self)
        self.enemies = []
        for i in range(5):
            self.enemies.append(Enemy(self))
        self.enemyGroup = self.makeSpriteGroup(self.enemies)
        self.addGroup(self.enemyGroup)
        self.sprites = [self.explosion, self.character, self.bullet, self.scoreboard, self.planet]
        self.counter = 0
        self.sndBackground = pygame.mixer.Sound("sounds/background.ogg")
        self.sndBackground.play(-1)

    def update(self):
        shipHitEnemy = self.character.collidesGroup(self.enemies)
        shipHitPlanet = self.character.collidesWith(self.planet)
        if shipHitEnemy or shipHitPlanet:
            self.counter += 1
            if self.counter>2:
                ship = self.character.get_coordinates()
                self.explosion.reset(ship[0], ship[1])
                self.stop()


        enemyHitPlanet = self.planet.collidesGroup(self.enemies)
        if enemyHitPlanet:
            enemy = enemyHitPlanet.get_coordinates()
            self.explosion.reset(enemy[0], enemy[1])
            self.scoreboard.change(-1,-100)
            enemyHitPlanet.reset()
            if self.scoreboard.health == 0:
                self.stop()
            

        bulletHitPlanet = self.bullet.collidesWith(self.planet)
        if bulletHitPlanet:
            self.explosion.reset(self.bullet.x, self.bullet.y)
            self.scoreboard.change(-1,-100)
            self.bullet.reset()
            if self.scoreboard.health == 0:
                self.stop()

        bulletHitEnemy = self.bullet.collidesGroup(self.enemies)
        if bulletHitEnemy:
            self.explosion.reset(self.bullet.x, self.bullet.y)
            self.scoreboard.change(0,200)
            bulletHitEnemy.reset()
            self.bullet.reset()

    def get_score(self):
        return self.scoreboard.score

def instructions(score):
    sndIntro = pygame.mixer.Sound("sounds/power.ogg")
    if score == 1: #Post start screen instructions
        sndIntro.play(-1)
        instructions = (
        "Planet Defence.",
        "Instructions:  You are a spaceship pilot",
        "defending our home planet of RaspberryPia.",
        "",
        "Select Difficulty:",
        "Normal = 1",
        "Hard = 2",
        "Insane = 3"
        )
    else:
        instructions = (
        "Your home planet has perished...",
        "",
        "",
        "Your final score: %d" % score
        )
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Planet Defence")
    game = Game()
    plane = Planet(game)
    
    allSprites = pygame.sprite.Group(plane)
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (0, 0, 255))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3]:
                if keys[pygame.K_1]:
                    DIFFICULTY = 1
                elif keys[pygame.K_2]:
                    DIFFICULTY = 2
                elif keys[pygame.K_3]:
                    DIFFICULTY = 3
                keepGoing = False
                donePlaying = False
                sndIntro.stop()
                print(DIFFICULTY)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
    return donePlaying

def main():
    #start = Start()
    #start.start()
    donePlaying = instructions(1)
    while donePlaying == False:
        game = Game()
        game.start()
        donePlaying = instructions(game.get_score())

if __name__ == "__main__":
    main()