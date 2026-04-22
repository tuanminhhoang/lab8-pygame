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
FPS: int = 60
SQUARE_COUNT: int = 30
BACKGROUND_COLOR = (20, 24, 28)
SQUARE_COLOR = (230, 230, 240)


class Square:
    """One moving square in the simulation.

    Attributes:
    - x, y: top-left position in screen coordinates.
    - moving_vector: velocity in pixels per second.
    - size: side length of the square in pixels.
    - center: derived center point used for distance and steering logic.
    """

    def __init__(
        self,
        x: float,
        y: float,
        vx: float,
        vy: float,
        size: int,
        birth_time: float,
        lifespan: int,
    ):
        """Initialize position, velocity, size, and lifetime tracking."""

        self.x = x
        self.y = y
        self.moving_vector = Vector2(vx, vy)
        self.size = size
        self.center = Vector2(self.x + (self.size / 2), self.y + (self.size / 2))
        self.birth_time = birth_time
        self.lifespan = lifespan

    def larger_squares(self, others: List[Square]) -> List[Square]:
        """Return all squares from `others` with a strictly larger size."""
        larger = []
        for square in others:
            if square.size > self.size:
                larger.append(square)
        return larger
    
    def smaller_squares(self, others: List[Square]) -> List[Square]:
        smaller = []
        for square in others:
            if square.size > self.size:
                smaller.append(square)
        return smaller
    

    def threat(self, others: List[Square]) -> Square:
        """Return the nearest larger square, or self when none exist."""
        larger = self.larger_squares(others)
        distances = []
        if larger:
            for square in larger:
                distance = self.center.distance_squared_to(square.center)
                distances.append((square, distance))
            closest_square = min(distances, key=lambda x: x[1])
            return closest_square[0]
        else:
            return self

    def run_away(self, others: List[Square], dt: float) -> Vector2:
        """Rotate current velocity away from the nearest larger square.

        The rotation amount is clamped by a per-frame turn rate so steering is
        smooth and frame-rate independent.
        """
        threat = self.threat(others)
        if threat is self:
            return self.moving_vector
        v = Vector2(self.center - threat.center)
        if v.length_squared() == 0:
            return self.moving_vector
        v = v.normalize()
        avoid_speed = 200
        self.moving_vector += v * avoid_speed * dt
        max_speed = 100
        if self.moving_vector.length() > max_speed:
            self.moving_vector.scale_to_length(max_speed)
        return self.moving_vector


def create_squares(count: int) -> List[Square]:
    """Create random squares with valid initial position, velocity, and lifespan."""
    squares: List[Square] = []
    for _ in range(count):
        size = random.randint(20, 40)
        x = random.randint(0, SCREEN_WIDTH - size)
        y = random.randint(0, SCREEN_HEIGHT - size)
        vx = random.choice([-1500, 1500]) * size
        vy = random.choice([-1500, 1500]) * size
        birth_time = time.time()
        lifespan = random.randint(30, 180)
        squares.append(
            Square(
                x=x,
                y=y,
                vx=vx,
                vy=vy,
                size=size,
                birth_time=birth_time,
                lifespan=lifespan,
            )
        )
    return squares

def reborn(squares: List[Square]) -> List[Square]:
    """Add new squares until the world reaches the target population."""
    while len(squares) < SQUARE_COUNT:
        size = random.randint(20, 40)
        x = random.randint(0, SCREEN_WIDTH - size)
        y = random.randint(0, SCREEN_HEIGHT - size)
        vx = random.uniform(-100, 100)
        vy = random.uniform(-100, 100)
        birth_time = time.time()
        lifespan = random.randint(30, 180)
        squares.append(
            Square(
                x=x,
                y=y,
                vx=vx,
                vy=vy,
                size=size,
                birth_time=birth_time,
                lifespan=lifespan,
            )
        )
    return squares

def death(squares: List[Square]) -> List[Square]:
    """Remove squares whose lifespan has expired."""
    squares[:] = [s for s in squares if time.time() - s.birth_time < s.lifespan]
    return squares

def check_for_bounds(square: Square, bounds: Tuple[int, int]) -> Tuple[float, float, Vector2]:
    """Clamp square to bounds and reflect velocity when a wall is hit."""
    if square.x < 0:
        square.x = 0
        square.moving_vector[0] *= -1

    elif square.x > bounds[0] - square.size:
        square.x = bounds[0] - square.size
        square.moving_vector[0] *= -1

    if square.y < 0:
        square.y = 0
        square.moving_vector[1] *= -1

    elif square.y > bounds[1] - square.size:
        square.y = bounds[1] - square.size
        square.moving_vector[1] *= -1

    return square.x, square.y, square.moving_vector

def free_from_border(square: Square, bounds: Tuple[int, int]) -> Vector2:
    """Nudge a square away from borders when its speed becomes too low."""
    if square.x <= 1 or square.x >= bounds[0] - square.size - 1:
        if abs(square.moving_vector.x) < 30:
            if square.x <= 1:
                square.moving_vector.x += 100
            else:
                square.moving_vector.x -= 100

    if square.y <= 1 or square.y >= bounds[1] - square.size - 1:
        if abs(square.moving_vector.y) < 30:
            if square.y <= 1:
                square.moving_vector.y += 100
            else:
                square.moving_vector.y -= 100
    return square.moving_vector

def update_square(
    square: Square, squares: List[Square], bounds: Tuple[int, int], dt: float
):
    """Advance one square by one frame.

    Update order:
    1. steer velocity using nearby larger squares
    2. integrate position from velocity and dt
    3. refresh derived center position
    4. resolve boundary collisions
    """
    square.moving_vector = square.run_away(squares, dt)

    square.x += float(square.moving_vector[0]) * dt
    square.y += float(square.moving_vector[1]) * dt

    square.x, square.y, square.moving_vector = check_for_bounds(square, bounds)

    square.moving_vector = free_from_border(square, bounds)

    square.center = Vector2((square.x + square.size) / 2, (square.y + square.size) / 2)

def update_world(squares: List[Square], bounds: Tuple[int, int], dt: float) -> None:
    """Update the full simulation state for one frame."""
    squares = death(squares)
    squares = reborn(squares)
    for square in squares:
        update_square(square, squares, bounds, dt)


def draw_world(screen: pygame.Surface, squares: List[Square]) -> None:
    """Clear the screen and draw each square as a filled rectangle."""
    screen.fill(BACKGROUND_COLOR)
    for square in squares:
        pygame.draw.rect(
            screen,
            SQUARE_COLOR,
            pygame.Rect(square.x, square.y, square.size, square.size),
        )

def handle_events() -> bool:
    """Process pygame events and report whether the app should keep running."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            return False
    return True

def draw_text(text: str, font: pygame.font.Font, text_col, x: int, y: int, screen: pygame.Surface) -> None:
    """Render a text label onto the screen at the given position."""
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def run() -> None:
    """Initialize pygame and run the main loop until quit."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Random Squares (Skeleton)")
    clock = pygame.time.Clock()
    text_font = pygame.font.Font(None, 30)
    squares = create_squares(SQUARE_COUNT)
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        running = handle_events()

        update_world(squares, (SCREEN_WIDTH, SCREEN_HEIGHT), dt)
        draw_world(screen, squares)
        draw_text(f"FPS: {FPS}", text_font, (255, 255, 255), 20, 10, screen)
        draw_text("Press q to exit", text_font, (255, 255, 255), 20, 40, screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()
