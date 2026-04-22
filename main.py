"""Pygame simulation of moving squares with simple steering behavior.

This module demonstrates a compact game-loop architecture with:
- world initialization (``create_squares``)
- per-frame updates (``update_world``)
- drawing (``draw_world``)
- event handling (``handle_events``)

Movement uses delta time (``dt``) so velocity is in pixels per second. Each
square can steer away from the closest larger square, bounce off the window
boundaries, and be respawned after its lifespan expires.
"""

from __future__ import annotations
from typing import List, Tuple
from pygame.math import Vector2

import pygame
import random
import time

SCREEN_WIDTH: int = 1200
SCREEN_HEIGHT: int = 800
FPS:  float = 60.0
SQUARE_COUNT: int = 30
RUNNING_TURN: int = 300
CHASING_TURN: int = 200
BACKGROUND_COLOR = (20, 24, 28)
SQUARE_COLOR = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 165, 0), (255, 20, 147), (0, 255, 127), (255, 69, 0)]

class Square:
    """Represents one moving square in the simulation.

    The square stores position, velocity, size, and lifespan metadata. Steering
    behavior is computed from neighboring squares each frame.
    """

    def __init__(self, color, size: int, x: float, y: float, vx: float, vy: float, max_speed: float, birth_time, life_span, alive):
        """Initialize a square with movement and lifecycle properties."""
        self.color = color
        self.size = size
        self.x = x 
        self.y = y
        self.center = Vector2(self.x + self.size / 2, self.y + self.size / 2)
        self.vx = vx
        self.vy = vy
        self.max_speed = max_speed
        self.moving_vector = Vector2(vx, vy)
        self.boost_multiplier = 1.0
        self.boost_decay = 3.0
        self.birth_time = birth_time
        self.life_span = life_span
        self.alive = alive

    def check_for_bounds(self, bounds: Tuple[int, int]):
        """Clamp position to screen bounds and bounce velocity if needed.

        Returns updated position, moving vector, and whether a bounce happened.
        """
        width, height = bounds
        bounce = False
        if self.x < 0:
            self.x = 0
            self.moving_vector.x *= -1
            bounce = True
        elif self.x > width - self.size:
            self.x = width - self.size
            self.moving_vector.x *= -1
            bounce = True

        if self.y < 0:
            self.y = 0
            self.moving_vector.y *= -1
            bounce = True
        elif self.y > height - self.size:
            self.y = height - self.size
            self.moving_vector.y *= -1
            bounce = True

        if bounce:
            self.boost_multiplier = 2.2

        return self.x, self.y, self.moving_vector, bounce
    
    def larger_square(self, squares: List[Square]) -> List[Square]:
        """Return all squares that are larger than this one."""
        larger = []
        for other in squares:
            if other.size > self.size:
                larger.append(other)
        return larger
    
    def smaller_square(self, squares: List[Square]) -> List[Square]:
        """Return all squares that are smaller than this one."""
        smaller = []
        for other in squares:
            if other.size < self.size:
                smaller.append(other)
        return smaller

    def threat(self, squares: List[Square]):
        """Return nearest larger square, or self if no threat exists."""
        larger = self.larger_square(squares)
        distances = []
        if larger:
            for square in larger:
                distance = self.center.distance_squared_to(square.center)
                distances.append((square, distance))
            threat = min(distances, key=lambda x: x[1])
            return threat[0]
        else:
            return self
        
    def prey(self, squares: List[Square]):
        """Return nearest smaller square, or self if no prey exists."""
        smaller = self.smaller_square(squares)
        distances = []
        if smaller:
            for square in smaller:
                distance = self.center.distance_squared_to(square.center)
                distances.append((square, distance))
            prey = min(distances, key=lambda x: x[1])
            return prey[0]
        else:
            return self
        
    def running(self, squares: List[Square], dt: float):
        """Compute flee steering vector away from nearest larger square."""
        threat = self.threat(squares)
        if threat is self:
            return Vector2(0, 0)
        v = self.center - threat.center
        if v.length_squared() == 0:
            return Vector2(0, 0)
        v = v.normalize()
        v *= RUNNING_TURN * dt
        return v
    
    def chasing(self, squares: List[Square], dt: float):
        """Compute chase steering vector toward nearest smaller square."""
        prey = self.prey(squares)
        if prey is self:
            return Vector2(0, 0)
        v = prey.center - self.center
        if v.length_squared() == 0:
            return Vector2(0, 0)
        v = v.normalize()
        v *= CHASING_TURN * dt
        return v
    
    def clamp_speed(self):
        """Limit velocity magnitude to max_speed."""
        if self.moving_vector.length() > self.max_speed: 
            self.moving_vector.scale_to_length(self.max_speed) 
        return self.moving_vector
    

def alive(squares: List[Square]) -> List[Square]:
    """Remove expired squares based on lifespan."""
    squares[:] = [square for square in squares if time.time() - square.birth_time < square.life_span]
    return squares

def reborn(squares: List[Square]) -> List[Square]:
    """Respawn squares until the world reaches SQUARE_COUNT."""
    while len(squares) < SQUARE_COUNT:
        color = random.choice(SQUARE_COLOR)
        size = random.randint(20, 40)
        x = random.randint(0, SCREEN_WIDTH - size)
        y = random.randint(0, SCREEN_HEIGHT - size)
        vx = random.choice([-2200, 2200]) * 1/size
        vy = random.choice([-2200, 2200]) * 1/size
        max_speed= 2200 * 1/size
        birth_time = time.time()
        life_span = random.randint(30, 60)
        alive = False
        squares.append(Square(color, size, x, y, vx, vy, max_speed, birth_time, life_span, alive))
    return squares    

def create_squares() -> List[Square]:
    """Create the initial set of random squares."""
    squares = []
    for _ in range(SQUARE_COUNT):
        color = random.choice(SQUARE_COLOR)
        size = random.randint(20, 40)
        x = random.randint(0, SCREEN_WIDTH - size)
        y = random.randint(0, SCREEN_HEIGHT - size)
        vx = random.choice([-2200, 2200]) * 1/size
        vy = random.choice([-2200, 2200]) * 1/size
        max_speed= 2200 * 1/size
        birth_time = time.time()
        life_span = random.randint(30, 60)
        alive = True
        squares.append(Square(color, size, x, y, vx, vy, max_speed, birth_time, life_span, alive))
    return squares


def update_square(square: Square, squares: List[Square], bounds: Tuple[int, int], dt: float):
    """Advance one square by one frame using dt-based movement."""
    if not square.alive:
        if time.time() - square.birth_time > 2:
            square.alive = True
    else:
        square.x, square.y, square.moving_vector, bounce = square.check_for_bounds(bounds)
        
        if not bounce:
            square.moving_vector += square.running(squares, dt) + square.chasing(squares, dt)
        if square.moving_vector.length_squared() > square.max_speed ** 2:
            square.moving_vector = square.clamp_speed()
        
        velocity = square.moving_vector * square.boost_multiplier

        square.x += velocity.x * dt
        square.y += velocity.y * dt

        if square.boost_multiplier > 1.0:
            square.boost_multiplier -= square.boost_decay * dt
        if square.boost_multiplier < 1.0:
            square.boost_multiplier = 1.0
        
        square.center = Vector2(square.x + square.size / 2, square.y + square.size / 2)
    

def update_world(squares: List[Square], bounds: Tuple[int, int], dt: float):
    """Update all simulation entities for one frame."""
    squares = alive(squares)
    squares = reborn(squares)
    for square in squares:
        update_square(square, squares, bounds, dt)

def draw_world(screen: pygame.Surface, squares: List[Square]):
    """Render all alive squares to the screen."""
    screen.fill(BACKGROUND_COLOR)
    for square in squares:
        if square.alive:
            pygame.draw.rect(screen, square.color, pygame.Rect(square.x, square.y, square.size, square.size))

def draw_text(text: str, font: pygame.font.Font, text_col, x: int, y: int, screen: pygame.Surface):
    """Render a single text label at the given screen position."""
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def handle_event() -> bool:
    """Handle input events and return False when the app should exit."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            return False
    return True

def run():
    """Initialize pygame and execute the main game loop."""
    pygame.init()
    pygame.display.set_caption("Random Squares")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    text_font = pygame.font.Font(None, 30) 
    squares = create_squares()
    running = True
    bounds = [SCREEN_WIDTH, SCREEN_HEIGHT]

    while running:
        dt = clock.tick(FPS) / 1000.0
        running = handle_event()
        update_world(squares, bounds, dt)
        draw_world(screen, squares)
        draw_text(f"FPS: {int(clock.get_fps())}", text_font, (255, 255, 255), 20, 10, screen)
        draw_text("Press q to exit", text_font, (255, 255, 255), 20, 40, screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run()
