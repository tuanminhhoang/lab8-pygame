# Lab 8 - Pygame

Small pygame simulation where multiple squares move, steer, bounce, and
respawn inside a 1200x800 window.

## Overview

The project focuses on core real-time programming concepts:

- Game loop structure (`init -> update -> draw -> quit`)
- Delta-time-based motion (`dt`) for frame-rate independence
- Basic steering behavior with vectors
- Boundary collision handling
- Simple lifetime-based respawning

In the current logic, each square continuously balances two goals: chase prey
(smaller nearby square) and run from threat (larger nearby square). The flee
steering force is stronger than the chase force, so survival has higher
priority than pursuit.

When a square hits a border, it bounces back and receives a temporary speed
boost. During this short boost window, its effective speed can exceed
`max_speed` before decaying back to normal.

Each square has a randomized lifespan. After a square expires, it is replaced,
and the replacement becomes active after roughly 2 seconds, keeping population
size stable while introducing a short delay before full participation.

## Project Structure

- `main.py`: simulation model, update logic, rendering, text overlay, and main loop
- `requirements.txt`: Python dependency list
- `README.md`: project setup and behavior notes
- `REPORT.md`: assignment/report notes
- `JOURNAL.md`: chronological work log
- `CODE_EXPLORER.html`: interactive learning dashboard for the project

## Requirements

- Python 3.11+
- Windows PowerShell (or any terminal with Python available)

## Setup (Windows PowerShell)

1. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

2. Activate the virtual environment:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

## Run

```powershell
python main.py
```

## Controls

- Close the pygame window or press `Q` to exit.

## Behavior Summary

- Creates `SQUARE_COUNT` squares with random size, position, velocity, and lifespan.
- Uses size-scaled speed, so smaller squares move faster than larger squares.
- Updates each square every frame using delta time.
- Applies combined steering each frame: chase nearest smaller square and flee nearest larger square.
- Weights flee turning force higher than chase turning force so running away dominates when both apply.
- Reflects movement when a square hits a boundary and applies a temporary bounce boost.
- Allows short-term boosted movement to exceed normal `max_speed`, then decays boost back to baseline.
- Expires squares at end of lifespan, respawns replacements, and activates new squares after about 2 seconds.
- Draws alive squares and a text overlay each frame.

## Notes

- This project is intentionally simple and learning-oriented.
- Use it as a base for experimenting with movement, collision, and AI behavior.
- The `CODE_EXPLORER.html` dashboard summarizes the architecture and major patterns in the code.
