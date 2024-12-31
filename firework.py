import pygame
import sys
import random
import math
from pygame.locals import *

# Window dimensions and configurations
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
FPS = 60

# Firework properties
SIZE = 5.0  # Size of the exploding bullet
SCALE_FACTOR = 10  # Scaling factor for the heart size
SCALE_FACTOR_SMALL = 5  # Scaling factor for smaller explosions
SPEED_CHANGE_SIZE = 0.05  # Rate at which the bullet size decreases upon explosion
CHANGE_SPEED = 0.07  # Rate at which the bullet speed decreases
RAD = math.pi / 180  # Conversion from degrees to radians
A_FALL = 1.5  # Acceleration due to gravity
NUM_BULLET = 300  # Number of bullets in one firework explosion (adjusted for heart shape)
TIME_CREAT_FW = 100  # Time interval between consecutive fireworks
NUM_FIREWORKS_MAX = 3  # Maximum number of fireworks launched at once
NUM_FIREWORKS_MIN = 1  # Minimum number of fireworks launched at once
SPEED_FLY_UP_MAX = 12  # Maximum speed of the upward-moving bullet before explosion
SPEED_FLY_UP_MIN = 8  # Minimum speed of the upward-moving bullet before explosion
MAX_GENERATIONS = 2  # Maximum number of explosion generations
FADE_RATE = 3  # Rate at which the heart fades

class Dot:
    """Trailing dots following each exploding bullet."""
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def update(self):
        """Decrease the size of the dot."""
        if self.size > 0:
            self.size -= SPEED_CHANGE_SIZE * 5
        else:
            self.size = 0

    def draw(self):
        """Draw a single dot."""
        if self.size > 0:
            pygame.draw.circle(DISPLAYSURF, self.color,
                               (int(self.x), int(self.y)), int(self.size))


class BulletFlyUp:
    """Bullet moving upwards before exploding."""
    def __init__(self, speed, x):
        self.speed = speed
        self.x = x
        self.y = WINDOWHEIGHT
        self.dots = []  # List of trailing dots
        self.size = SIZE / 2
        self.color = (255, 255, 100)

    def update(self):
        """Update the bullet's position and its trailing dots."""
        # Add a new trailing dot
        self.dots.append(Dot(self.x, self.y, self.size, self.color))
        # Update the bullet's position
        self.y -= self.speed
        self.speed -= A_FALL * 0.1
        # Update each dot
        for dot in self.dots:
            dot.update()
        # Remove dots that have disappeared
        self.dots = [dot for dot in self.dots if dot.size > 0]

    def draw(self):
        """Draw the bullet and its trailing dots."""
        pygame.draw.circle(DISPLAYSURF, self.color, (int(
            self.x), int(self.y)), int(self.size))  # Draw the bullet
        for dot in self.dots:
            dot.draw()


class Bullet:
    """Bullet after explosion (forming part of the heart shape or radial particles)."""
    def __init__(self, x, y, speed, angle, color, apply_gravity=True, generation=1):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle  # Angle with the horizontal
        self.size = SIZE
        self.color = color
        self.apply_gravity = apply_gravity  # Determines if gravity affects this bullet
        self.generation = generation  # Explosion generation

    def update(self):
        """Update the bullet's position and size."""
        # Calculate speed in both directions
        speedX = self.speed * math.cos(self.angle * RAD)
        speedY = self.speed * math.sin(self.angle * RAD)
        # Update bullet's position
        self.x += speedX
        self.y -= speedY
        if self.apply_gravity:
            self.y += A_FALL  # Apply gravity
        # Decrease the size of the bullet
        if self.size > 0:
            self.size -= SPEED_CHANGE_SIZE
        else:
            self.size = 0
        # Decrease the speed of the bullet
        if self.speed > 0:
            self.speed -= CHANGE_SPEED
        else:
            self.speed = 0

    def draw(self, alpha=255):
        """Draw a single bullet with alpha transparency."""
        if self.size > 0:
            # Create a surface for the bullet with alpha
            bullet_surface = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(bullet_surface, (*self.color, alpha),
                               (int(self.size), int(self.size)), int(self.size))
            DISPLAYSURF.blit(bullet_surface, (int(self.x - self.size), int(self.y - self.size)))


class FireWork:
    """Firework explosion forming a heart shape."""
    def __init__(self, x, y, generation=1):
        self.x = x
        self.y = y
        self.color = Random.color()
        self.bullets = self.create_bullets(generation)
        self.dots = []  # List of trailing dots for all bullets
        self.timer = 0  # Timer to trigger secondary explosions
        self.generation = generation  # Current explosion generation
        self.alpha = 255  # Transparency level

    def create_bullets(self, generation):
        """Generate bullets forming a heart shape or radial particles."""
        bullets = []
        scale = SCALE_FACTOR if generation == 1 else SCALE_FACTOR_SMALL
        for t in range(0, 360, 1):  # Degree step for smoothness
            rad = math.radians(t)
            if generation == 1:
                # Heart shape parametric equations
                x = scale * (16 * math.sin(rad)**3)
                y = scale * (13 * math.cos(rad) - 5 * math.cos(2 * rad) -
                            2 * math.cos(3 * rad) - math.cos(4 * rad))
                # Offset to center the heart at (self.x, self.y)
                bullet_x = self.x + x
                bullet_y = self.y - y  # Negative to flip the heart upwards
                # For initial generation, bullets are static and don't apply gravity
                apply_gravity = False
                speed = 0
                angle = 0
            else:
                # Radial particles emitting in all directions
                bullet_x = self.x
                bullet_y = self.y
                apply_gravity = True
                speed = random.uniform(2, 6)
                angle = t  # Spread uniformly in all directions
            bullets.append(Bullet(bullet_x, bullet_y, speed, angle,
                                  self.color, apply_gravity=apply_gravity, generation=generation))
        return bullets

    def update(self):
        """Update all bullets and their trailing dots, and handle secondary explosions."""
        self.timer += 1
        self.alpha = max(0, self.alpha - FADE_RATE)  # Fade out the heart

        for bullet in self.bullets:
            bullet.update()
            # Only add dots for moving bullets (speed > 0)
            if bullet.speed > 0:
                self.dots.append(Dot(bullet.x, bullet.y, bullet.size, bullet.color))
        for dot in self.dots:
            dot.update()
        # Remove dots that have disappeared
        self.dots = [dot for dot in self.dots if dot.size > 0]

        # Trigger secondary explosions after a certain time
        if self.generation < MAX_GENERATIONS and self.timer == FPS // 2:  # Half a second delay
            self.spawn_secondary_explosions()

    def spawn_secondary_explosions(self):
        """Spawn smaller particles moving outward in all directions."""
        global explosion_bullets
        for bullet in self.bullets:
            if self.generation < MAX_GENERATIONS and bullet.size > SIZE * 0.5:
                # Only for heart shape bullets
                if self.generation == 1 and bullet.speed == 0:
                    # Spawn radial bullets from heart shape
                    explosion_bullets.append(Bullet(
                        bullet.x, bullet.y,
                        speed=random.uniform(2, 6),
                        angle=random.uniform(0, 360),
                        color=self.color,
                        apply_gravity=True,
                        generation=self.generation + 1
                    ))

    def draw(self):
        """Draw all bullets and their trailing dots with fading."""
        for bullet in self.bullets:
            bullet.draw(self.alpha)
        for dot in self.dots:
            dot.draw()


class Random:
    """Utility class for generating random attributes."""
    @staticmethod
    def color():
        """Generate a random bright color."""
        color1 = random.randint(128, 255)
        color2 = random.randint(128, 255)
        color3 = random.randint(128, 255)
        colorList = [color1, color2, color3]
        random.shuffle(colorList)
        return colorList

    @staticmethod
    def num_fireworks():
        """Number of fireworks launched at once."""
        return random.randint(NUM_FIREWORKS_MIN, NUM_FIREWORKS_MAX)

    @staticmethod
    def randomBulletFlyUp_speed():
        """Speed of the upward-moving bullet."""
        return random.uniform(SPEED_FLY_UP_MIN, SPEED_FLY_UP_MAX)

    @staticmethod
    def randomBulletFlyUp_x():
        """X-position of the upward-moving bullet."""
        return random.randint(int(WINDOWWIDTH * 0.2), int(WINDOWWIDTH * 0.8))


def main():
    """Main function to run the firework simulation."""
    global FPSCLOCK, DISPLAYSURF, fireWorks, explosion_bullets
    pygame.init()
    pygame.display.set_caption('FIREWORKS - Heart Shape with Secondary Explosions')
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    fireWorks = []
    explosion_bullets = []
    time = TIME_CREAT_FW
    bulletFlyUps = []

    while True:
        DISPLAYSURF.fill((0, 0, 0))  # Clear the screen
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Create new upward-moving bullets after a certain time interval
        if time == TIME_CREAT_FW:
            for _ in range(Random.num_fireworks()):
                bulletFlyUps.append(BulletFlyUp(
                    Random.randomBulletFlyUp_speed(), Random.randomBulletFlyUp_x()))

        # Update and draw all upward-moving bullets
        for bulletFlyUp in bulletFlyUps[:]:
            bulletFlyUp.draw()
            bulletFlyUp.update()

        # Update and draw all fireworks
        for fireWork in fireWorks[:]:
            fireWork.draw()
            fireWork.update()

        # Update and draw all explosion bullets
        for explosion_bullet in explosion_bullets[:]:
            explosion_bullet.draw()
            explosion_bullet.update()
            if explosion_bullet.size <= 0:
                explosion_bullets.remove(explosion_bullet)

        # Check if upward-moving bullets have reached their peak to explode into fireworks
        for bulletFlyUp in bulletFlyUps[:]:
            if bulletFlyUp.speed <= 0:  # Bullet has reached maximum height
                fireWorks.append(FireWork(bulletFlyUp.x, bulletFlyUp.y))
                bulletFlyUps.remove(bulletFlyUp)  # Remove the bullet

        # Remove fireworks that have fully exploded (all bullets have disappeared)
        for fireWork in fireWorks[:]:
            if fireWork.alpha <= 0:
                fireWorks.remove(fireWork)

        # Increment the timer
        if time <= TIME_CREAT_FW:
            time += 1
        else:
            time = 0

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    main()
    #hello