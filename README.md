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

In the current logic, each square can try to turn away from the closest larger
square while still bouncing on screen edges. Squares are removed after their
lifespan ends and respawned so the simulation stays populated.

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
- Updates each square every frame using delta time.
- Applies steering away from the nearest larger square.
- Reflects velocity when a square hits a window boundary.
- Removes expired squares and respawns new ones to keep the count stable.
- Draws all squares and a small text overlay each frame.

## Notes

- This project is intentionally simple and learning-oriented.
- Use it as a base for experimenting with movement, collision, and AI behavior.
- The `CODE_EXPLORER.html` dashboard summarizes the architecture and major patterns in the code.
