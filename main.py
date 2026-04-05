"""Pygame scaffold for animating 10 moving squares.

This module is intentionally incomplete. The current structure is meant to help
you practice using pygame, working with a small data model, and filling in the
missing movement logic yourself.

The main ideas are:
- create a list of square objects
- update each square every frame
- draw each square to the screen
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import pygame
import random


# TODO: Tune these values while testing your simulation.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
SQUARE_COUNT = 10
SQUARE_SIZE = 24
BACKGROUND_COLOR = (20, 24, 28)
SQUARE_COLOR = (230, 230, 240)


@dataclass
class Square:
	"""Represents one square in the simulation.

	The x and y values store the top-left corner of the square. The vx and vy
	values store its movement speed in pixels per frame or pixels per second,
	depending on how you choose to structure the update step.
	"""

	x: float
	y: float
	vx: float
	vy: float
	size: int = SQUARE_SIZE


def create_squares(count: int, dt: float) -> List[Square]:
	"""Create the initial list of squares.

	TODO:
	- Choose a valid starting position for each square.
	- Give each square a random velocity.
	- Keep the motion readable while you test the animation.
	"""
	squares: List[Square] = []
	# Placeholder values only. Replace with real random initialization logic.
	for _ in range(count):
		squares.append(Square(x=random.randint(0, SCREEN_WIDTH - SQUARE_SIZE), y=random.randint(0, SCREEN_HEIGHT - SQUARE_SIZE), vx=random.randint(-50.0,50.0) * dt, vy=random.randint(-50.0, 50.0) * dt))
	return squares


def update_square(square: Square, bounds: Tuple[int, int]) -> None:
	"""Update one square's position and boundary behavior.

	TODO:
	- Move the square using its velocity.
	- Reverse direction when it hits a boundary.
	- Keep the square fully visible inside the window.
	"""
	# TODO: Implement movement and wall-bounce behavior.
	if square.x < 0:
		square.x = 0
	if square.y < 0:
		square.y = 0
	if square.x > bounds[0] - square.size:
		square.x = bounds[0] - square.size
	if square.y > bounds[1] - square.size:
		square.y = bounds[1] - square.size
	if square.y == 0 or square.y == bounds[1] - square.size:
		square.vy = float(square.vy) * -1.0
	if square.x == 0 or square.x == bounds[0] - square.size:
		square.vx = float(square.vx) * -1.0
	square.x = float(square.x) + float(square.vx)
	square.y = float(square.y) + float(square.vy)
    
    


def update_world(squares: List[Square], dt: float, bounds: Tuple[int, int]) -> None:
	"""Update all squares each frame.

	TODO:
	- Call update_square for every square.
	- Decide whether dt belongs in the square state or in the update step.
	"""
	for square in squares:
		update_square(square, bounds)


def draw_world(screen: pygame.Surface, squares: List[Square]) -> None:
	"""Draw all game objects.

	TODO:
	- Draw each square as a filled rectangle.
	- Optionally give each square a different color.
	"""
	screen.fill(BACKGROUND_COLOR)

	# TODO: Replace this placeholder draw logic with a loop that uses square data.
	for _square in squares:
		pygame.draw.rect(screen, SQUARE_COLOR, pygame.Rect(_square.x, _square.y, _square.size, _square.size))


def handle_events() -> bool:
	"""Process pygame events.

	Returns False when the user closes the window.
	"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return False
	return True


def run() -> None:
	"""Application entry point for the pygame loop."""
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Random Squares (Skeleton)")
	clock = pygame.time.Clock()
	dt = clock.tick(FPS) / 1000.0

	squares = create_squares(SQUARE_COUNT, dt)
	running = True

	while running:
		running = handle_events()

		update_world(squares, dt, (SCREEN_WIDTH, SCREEN_HEIGHT))
		draw_world(screen, squares)

		pygame.display.flip()

	pygame.quit()


if __name__ == "__main__":
	run()
