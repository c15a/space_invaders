# Space Invaders by c15a

# This is my Final Project in Python

# Thank you Codedex !!!

# Import necessary modules
import math
import random
import pygame # imports all pygame components
from pygame import mixer # classes for loading sound objects and playback

# Initialize the pygame
pygame.init()

# Initialize the clock - This is in order to change the Frames per second
clock = pygame.time.Clock()

# create the screen display - Resolution of the game
screen = pygame.display.set_mode((1000, 1000))

# background of the game
background = pygame.image.load('space_background.jpg')

# sound - soundtrack
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player - this is the ship of the player
playerImg = pygame.image.load('player.png')
playerX = 900 # player's X coordinate
playerY = 900 # Player's Y coordinate
playerX_change = 0 # Set the player change X coordinate

# Enemies
# Empty lists as enemies coordinations
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 25

# Initialize enemies
# for loop for number of enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png')) # Load the enemy image
    enemyX.append(random.randint(0,900)) # Random X axis position
    enemyY.append(random.randint(50,150)) # Random Y axis position 
    enemyX_change.append(4) # Set the enemy's change position in X coordinate
    enemyY_change.append(40) # Set the enemy's change position to Y cordinate 

# Bullet
# Ready - You cannot see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png') # Load the bullet image
bulletX = 0 # Bullet's position in X axis 
bulletY = 0 # Bullet's position in Y axis
bulletX_change = 0  # Set the bullet tp change position to X coordinate
bulletY_change = 10 # Set the bullet to change position to Y coordinate
bullet_state = "ready" # Set the bullet's initial state

# Score 
score_value = 0 
font = pygame.font.SysFont("urwbookman", 32) # Setting the font to a SystemFont(Ubuntu)
scoreX = 10 # Score's X coordinate
scoreY = 10 # Score's Y coordinate

# Game Over
# Initialize the game over state - I added this option in order proceed with the Restart after the end of the game
game_over = False 
# Setting the font to a SystemFont(Ubuntu)
over_font = pygame.font.SysFont("urwbookman", 64)

# Function to display score
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255,255,255)) # using render function of the pygame font object - create a text surface object
    screen.blit(score, (x,y)) # this method instructs us to draw the backdrop surface 

# Function to draw enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y)) # Draw the enemy

# Function to display game over text
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200,250)) # Display the "GAME OVER" text

# Function to draw player
def player(x, y):
    screen.blit(playerImg, (x, y)) # Draw the player

# Function to fire a bullet
def fire_bullet(x, y):
    global bullet_state, bulletX, bulletY
    if bullet_state == "ready":
        bullet_state = "fire" # Set the bullet's state to "fire"
        bulletX = x + 16
        bulletY = y - 32 # Adjust bullet's Y position
    if bullet_state == "fire":
        screen.blit(bulletImg, (bulletX, bulletY))
        bulletY -= bulletY_change
        print("Bullet fired at X:", bulletX, "Y:", bulletY)

# Function to check the collision between the enemy and the bullet
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2))) # Calculation of distance by applying the distance formula
    if distance < 27: # If distance is less that 27 -> collision threshold
        return True # Collision detected
    else:
        return False # No collision detected

# Main Game Loop
running = True
while running:

    # Limit the frame rate
    clock.tick(60) # Adjust the frame rate as needed - 60 frames per second

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0)) # This indicates the black color. if it was ( 255, 255, 255 ) would be white

    # Background Image
    screen.blit(background, (0, 0)) # Draw the background image

    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Quit the game if the window is closed
        # If keystroke is pressed, check whether it's right or left
        if event.type == pygame.KEYDOWN: # Check if a key is pressed down
            if event.key == pygame.K_a: # Check if the pressed key is 'a'
                playerX_change = -5 # Change the player's X coordinate to the left (-5)
            if event.key == pygame.K_d:
                playerX_change = 5 # Change the player's X coordinate to the right (5)
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play() # Plays the bullet sound
                    # Get the current X coordinate of the Spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0 # Stop player movement when 'a' or 'd' key is released

    # Update player's position
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0 # Prevent player from moving beyond left edge of the screen
    elif playerX >= 900:
        playerX = 900 # Prevent player from moving beyond right edge of the screen

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 850: # If enemy reaches a certain Y coordinate / the Player's coordinates
            for j in range(num_of_enemies):
                enemyY[j] = 2000 # Move all enemies off the screen
            game_over_text()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: # Check if 'Return' key is pressed
                # Reset the game
                game_over = False
                score_value = 0
                playerX = 850
                # Reset the enemies position
                for i in range(num_of_enemies):
                    enemyX[i] = random.randint(0, 900)
                    enemyY[i] = random.randint(50, 150)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 900:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 900 # Reset bullet's Y coordinate
            bullet_state = "ready" # Set the state of the bullet to ready
            score_value += 1 # Increment the score on collision
            enemyX[i] = random.randint(0, 900) # Randomize enemy's X coordinate
            enemyY[i] = random.randint(50, 150) # Randomize enemy's Y coordinate
        enemy(enemyX[i], enemyY[i], i) # Draw the enemy again

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 900 # Reset bullet's Y coordinate
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY <= 0:
            bullet_state = "ready"

    # Draw player after enemies to ensure it's on top
    player(playerX, playerY) # Draw the player
    show_score(scoreX, scoreY) # Displays the score
    pygame.display.update() # updates the display
