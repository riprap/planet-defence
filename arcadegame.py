"""
    Source file name: arcadegame.py
    
    Author:  Nolan Knill
    
    Last modified by: Nolan Knill
    
    Date last modified: January 24, 2013
    
    Program description: Arcadegame.py is an space arcade planet
                         defense game. The player takes control
                         of a spaceship, and must defend his/her
                         planet from incoming self-destructing
                         Electrodes.

    Project: 1 - The Arcade Game
"""
import pygame, gameEngine, time, math, random
pygame.mixer.init() #initialiaze pygame mixer (sound)

class Character(gameEngine.SuperSprite):
    """
    Character class sets up an image of a ship as the user's
    avatar. Initial speed is 0. checkEvents() moves the 
    avatar by 10 in the direction which is pressed. Left click
    shoots a bullet in the direction the mouse is located.
    """
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("images/ship.bmp")
        self.setSpeed(0)
        self.setAngle(0)
    
    def checkEvents(self):
        speed = 10
        #get height of the avatar used (in case we change it)
        #we need this to determine the 
        avatar_width = self.image.get_width()
        avatar_height = self.image.get_height()
        #get pygame events (key or mouse presses)
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            #if key LEFT or A, move the character left
            self.setDY(0)
            self.setRotation(180)
            if self.x > avatar_width: 
                self.setDX(-speed)
            else:
                self.setDX(0)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            #if key RIGHT or D, move the character right
            self.setDY(0)
            self.setRotation(0)
            if self.x < self.screen.get_width() - avatar_width:
                self.setDX(speed)
            else:
                self.setDX(0)
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            #if key UP or S, move the character up
            self.setDX(0)
            self.setRotation(90)
            if self.y > avatar_height:            
                self.setDY(-speed)
            else:
                self.setDY(0)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            #if key DOWN or S, move the character down
            self.setDX(0)
            self.setRotation(270)
            if self.y < self.screen.get_height() - avatar_height:
                self.setDY(speed)
            else:
                self.setDY(0)
        else: #if no recognized key is pressed (or none are pressed)
            #stop all movement
            self.setDX(0)
            self.setDY(0)
        
        if mouse[0]: 
            #shoot the bullet if left mouse is clicked
            self.scene.bullet.fire()

class Bullet(gameEngine.SuperSprite):
    """
    Bullet class sets a bullet image (size 5x5) and a sound when fired.
    When fired, the fire() method checks the time of the last shot,
    and only fires if the last shot was more than 0.5 seconds prior.
    The bullet is fired in the direction of the mouse.
    """
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("images/bullet.gif")
        #scale the bullet image
        self.imageMaster = pygame.transform.scale(self.imageMaster, (5, 5))
        #hide bullet once it goes off screen
        self.setBoundAction(self.HIDE)
        self.reset()
        self.last_shot = 0
        #set fire sound
        self.sndFire = pygame.mixer.Sound("sounds/pew.ogg")
        self.sndFire.set_volume(0.2)

    def fire(self):
        current_time = time.clock()
        """
        check current time vs last shot to see if appropriate time has passed
        in order to shoot the next bullet
        """
        if (current_time > self.last_shot + 0.50) or (self.last_shot == 0):
            self.last_shot = time.clock()
            mouse_pos = pygame.mouse.get_pos()
            self.setPosition((self.scene.character.x, self.scene.character.y))
            self.setSpeed(25)
            #getting angle to shoot from spaceship
            dy = mouse_pos[1] - self.scene.character.y
            dx = mouse_pos[0] - self.scene.character.x
            angle = -math.degrees(math.atan2(dy,dx))
            #shoot the bullet at this angle
            self.setAngle(angle)
            #play bullet sound file
            self.sndFire.play(0)
    
    def reset(self):
        #reset the bullet to off screen for reuse
        self.setPosition ((-100, -100))
        self.setSpeed(0)

class Scoreboard(gameEngine.SuperSprite):
    """
    Scoreboard class sets a scoreboard in the top left corner,
    with health and score counters
    """
    def __init__(self, scene, start_health=5):
        gameEngine.SuperSprite.__init__(self, scene)
        self.score = 0
        #hack to fix start health showing up as one less
        self.health = start_health
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        #updates the scoreboard for each frame based on current
        #health and score
        health = self.health
        self.text = "Score: %d Health: %d" % (self.score, health)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()

    def change(self, d_health, d_score):
        #changes the health and score based on various events
        self.health += d_health
        self.score += d_score

class Enemy(gameEngine.SuperSprite):
    """
    Enemy class sets the image and angle of the incoming
    Electrodes trying to destroy RaspberryPia. 
    Based on the difficulty level, the speed of the enemies 
    will fluctuate, as well as how many are on screen (this is
    changed in the Game class)
    """
    def __init__(self, scene, difficulty):
        gameEngine.SuperSprite.__init__(self, scene)
        self.difficulty = difficulty
        self.reset()

    def reset(self):
        width = self.screen.get_width()
        height = self.screen.get_height()
        #pick a side for the Enemy to come from
        quadrant = random.randint(1,4) #top, right, bottom, left
        """
        based on the quadrant, give a corresponding x and y
        co-ordinate to start from
        """
        if quadrant == 1: 
            x = random.randint(-200,width+200)
            y = 0
        if quadrant == 2:
            x = width
            y = random.randint(-200,height+200)
        if quadrant == 3:
            y = height
            x = random.randint(-200,width+200) 
        elif quadrant == 4:
            y = random.randint(-200,height+200)
            x = 0
        self.setPosition((x,y))
        #enemies move faster based on the difficulty
        if self.difficulty == 1:
            top_speed = 0.6
        elif self.difficulty == 2:
            top_speed = 1.2
        elif self.difficulty == 3:
            top_speed = 2
        #randomized speeds for enemies offers some variant
        self.setSpeed(random.uniform(0.4,top_speed))
        #set direction of the Electrode to attack the planet
        angle=self.dirTo((self.screen.get_width()/2, self.screen.get_height()/2))
        self.setAngle(angle)
        self.setImage("images/electrode.gif")

class HealthPackage(gameEngine.SuperSprite):
    """
    HealthPackage class creates a health package that can be obtained 
    by flying into or letting the package hit the planet.
    """
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("images/health.png")
        self.reset()

    def move(self):
        #let's get this health pack in motion!
        #set direction of the Electrode to attack the planet
        self.setSpeed(1)   
        angle=self.dirTo((self.screen.get_width()/2, self.screen.get_height()/2))
        self.setAngle(angle)

    def reset(self):
        #set it off screen with no speed
        self.setSpeed(0)
        width = self.screen.get_width()
        height = self.screen.get_height()
        quadrant = random.randint(1,4) #top, right, bottom, left
        """
        based on the quadrant, give a corresponding x and y
        co-ordinate to start from
        """
        if quadrant == 1: 
            x = random.randint(-200,width+200)
            y = -25
        if quadrant == 2:
            x = width+25
            y = random.randint(-200,height+200)
        if quadrant == 3:
            y = height+25
            x = random.randint(-200,width+200) 
        elif quadrant == 4:
            y = random.randint(-200,height+200)
            x = -25
        self.setPosition((x,y))

class Planet(gameEngine.SuperSprite):
    """
    Planet class sets the Home Planet in the middle 
    of the screen based on its height and width
    """
    def __init__(self, scene):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("images/planet.gif")
        """
        Avatar is 75x75, making 37.5 the distance from
        the edge of the avatar to the middle of it
        """
        avatar_width = 37.5
        avatar_height = 37.5
        center_x = self.screen.get_width()/2
        center_y = self.screen.get_height()/2
        self.x = center_x - avatar_width
        self.y = center_y - avatar_height

class Explosion(gameEngine.SuperSprite):
    """
    Explosion class sets an image for an explosion, hides it off screen
    and if there is a collision, sets it to the co-ordinates given in
    the parameters for the reset method --> ie.  Explosion.reset((125,13))
    """
    def __init__(self,scene, size):
        gameEngine.SuperSprite.__init__(self, scene)
        self.setImage("images/explosion.png")
        #set the image the size given in the initializer's parameters
        self.imageMaster = pygame.transform.scale(self.imageMaster, (size[0], size[1]))
        self.setBoundAction(self.HIDE)
        self.explosion_time = 0
        self.reset()

    def reset(self, x=-100, y=-100):
        self.setPosition ((x, y))
        self.setSpeed(0)

class Game(gameEngine.Scene):
    """
    Game class. Sets an instance of all the classes needed in the game
    (Bullet, Character, Bullet, Enemies, Explosion, EndExplosion, Planet.
    __init__ accepts a difficulty parameter (1-normal,2-hard,3-insane)
    """
    def __init__(self, difficulty):
        gameEngine.Scene.__init__(self)
        self.difficulty = difficulty
        self.setCaption("Planet Defence")
        #instantiate classes to be used in the game
        self.character = Character(self)
        self.bullet = Bullet(self)
        self.scoreboard = Scoreboard(self)
        #set basic explosion with size (30x30)
        self.explosion = Explosion(self, [30,30])
        #set planet explosion with size (250x250)
        self.endExplosion = Explosion(self, [250,250])
        self.planet = Planet(self)
        # list of enemies based on difficulty level
        self.enemies = []
        #sets a health pack sprite
        self.health = HealthPackage(self)
        if self.difficulty == 1:
            #5 enemies for normal
            number_of_enemies = 5
            self.newHealthTimer = 15
        elif self.difficulty == 2:
            #10 enemies for hard
            number_of_enemies = 10
            self.newHealthTimer = 30
        elif self.difficulty == 3:
            #15 enemies for insane
            number_of_enemies = 15
            self.newHealthTimer = 60
        for i in range(number_of_enemies):
            self.enemies.append(Enemy(self, self.difficulty))
        self.sprites = [self.planet, self.explosion, self.character, self.bullet, self.scoreboard, self.endExplosion, self.health]
        self.enemyGroup = self.makeSpriteGroup(self.enemies)
        self.addGroup(self.enemyGroup)
        #counter is used to check if our ship hits anything (on counter>2, end game)
        self.counter = 0
        #set background soundtrack of the game
        self.sndBackground = pygame.mixer.Sound("sounds/background.ogg")
        #loop background sound
        self.sndBackground.play(-1)
        #set explosion sound
        self.sndPlanetExplosion = pygame.mixer.Sound("sounds/explosion.ogg")
        self.sndExplosion = pygame.mixer.Sound("sounds/shortExplosion.ogg")
        self.sndExplosion.set_volume(0.6)
        #set game over soundf
        self.sndGameOver = pygame.mixer.Sound("sounds/gameOver.ogg")

    def gameEnd(self):
        """
        sets the explosion of the planet, as well as the sounds for the
        explosion and the game over. Stops the game.
        """
        self.endExplosion.reset(self.planet.x, self.planet.y)
        self.sndPlanetExplosion.play(0)
        self.sndBackground.stop()
        time.sleep(1.5)
        self.sndGameOver.play(0)
        self.stop()

    def update(self):
        """
        This method checks for collisions during the game and updates based
        on which collision took place
        """
        #when instatianting, game goes through update, so added this counter
        #to only go through this method after the game begins
        self.counter += 1
        if self.counter>2:
            #if ship hits any enemies or the planet, game over
            shipHitEnemy = self.character.collidesGroup(self.enemies)
            shipHitPlanet = self.character.collidesWith(self.planet)
            if shipHitEnemy or shipHitPlanet:
                self.explosion.reset(self.character.x, self.character.y)
                #move ship off screen to make explosion more realistic
                self.character.x = -100
                self.gameEnd()

            #if enemy explodes on the planet
            enemyHitPlanet = self.planet.collidesGroup(self.enemies)
            if enemyHitPlanet:
                #play explosion sound
                self.sndExplosion.play(0)
                #coordinates where the enemy hit the planet
                enemy = enemyHitPlanet.get_coordinates()
                self.explosion.reset(enemy[0], enemy[1])
                #take away a life, and points
                self.scoreboard.change(-1,-100)
                enemyHitPlanet.reset()
                #if planet's health is at 0, end game
                if self.scoreboard.health == 0:
                    self.gameEnd()

            #if we shoot our own planet
            bulletHitPlanet = self.bullet.collidesWith(self.planet)
            if bulletHitPlanet:
                #play explosion
                self.sndExplosion.play(0)
                self.explosion.reset(self.bullet.x, self.bullet.y)
                #take away health and score
                self.scoreboard.change(-1,-100)
                self.bullet.reset()
                if self.scoreboard.health == 0:
                    #planet is dead
                    self.gameEnd()

            #if we shoot an enemy, eliminate them
            bulletHitEnemy = self.bullet.collidesGroup(self.enemies)
            if bulletHitEnemy:
                #play explosion
                self.sndExplosion.play(0)
                self.explosion.reset(self.bullet.x, self.bullet.y)
                #add points!
                self.scoreboard.change(0,200)
                bulletHitEnemy.reset()
                self.bullet.reset()

            healthHitPlanet = self.health.collidesWith(self.planet)
            healthHitShip = self.health.collidesWith(self.character)
            if healthHitPlanet or healthHitShip:
                self.health.reset()
                self.scoreboard.change(1,50)

            #based on the difficulty, a new health package will appear
            if int(time.time())%self.newHealthTimer == 0:
                self.health.move()
    
    def get_score(self):
        #Returns score to be used on end screen
        return self.scoreboard.score

def instructions(score):
    """
    Returns difficulty level to main(). The difficulty options are 
    1(normal), 2(hard), and 3(insane). If it returns 0, the game
    will end.
    """
    sndIntro = pygame.mixer.Sound("sounds/power.ogg")
    if score == 1: #Post start screen instructions
        sndIntro.play(-1)
        font_color = (0, 0, 255)
        instructions = (
        "Planet Defence.",
        "Instructions:  You are a spaceship pilot",
        "defending our home planet of RaspberryPia.",
        "Don't let the Electrodes hit our planet.",
        "The planet can take 4 Electrode explosions",
        "before it explodes. If YOU crash into the",
        "Electodes or our planet, you will die, and",
        "the planet will",
        "be history.",
        "",
        "Select Difficulty:",
        "Normal - 1",
        "Hard   - 2",
        "Insane - 3",
        "Or exit: ESC",
        "",
        "Controls:",
        "Move   - Arrow keys",
        "Shoot  - Left mouse",
        "Aim with Mouse pointer"
        )
    else:
        font_color = (200,0,0)
        instructions = (
        "Your home planet has perished...",
        "You gave a valiant effort.",
        "",
        "Your final score: %d" % score,
        ""
        "If you would like to play again",
        "Select a Difficulty:",
        "Normal = 1",
        "Hard = 2",
        "Insane = 3"
        "",
        "",
        "",
        "Or exit: ESC"
        )
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Planet Defence")
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []    
    for line in instructions:
        tempLabel = insFont.render(line, 1, font_color)
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                keepGoing = False
                difficulty = 0
            if keys[pygame.K_1] or keys[pygame.K_2] or keys[pygame.K_3]:
                if keys[pygame.K_1]:
                    difficulty = 1
                elif keys[pygame.K_2]:
                    difficulty = 2
                elif keys[pygame.K_3]:
                    difficulty = 3
                keepGoing = False
                sndIntro.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    difficulty = 0
        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
    return difficulty

def main():
    """
    returns difficulty. (0-done 1-normal 2-hard 3-insane)
    Pass 1 to instructions so that home screen 
    instructions appear.
    Variable difficulty will get back 1,2,3 for difficulty
    or 0 to end game.
    """
    difficulty = instructions(1)
    while difficulty > 0:
        game = Game(difficulty)
        game.start()
        difficulty = instructions(game.get_score())

if __name__ == "__main__":
    main()