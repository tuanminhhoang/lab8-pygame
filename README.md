# Lab 8 - Pygame

Small pygame simulation where multiple squares move, steer, and bounce inside
an 800x600 window.

## Overview

The project focuses on core real-time programming concepts:

- Game loop structure (`init -> update -> draw -> quit`)
- Delta-time-based motion (`dt`) for frame-rate independence
- Basic steering behavior with vectors
- Boundary collision handling

In the current logic, each square can try to turn away from the closest larger
square while still bouncing on screen edges.

## Project Structure

- `main.py`: simulation model, update logic, rendering, and main loop
- `requirements.txt`: Python dependency list
- `README.md`: project setup and behavior notes
- `REPORT.md`: assignment/report notes
- `JOURNAL.md`: chronological work log

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

- Close the pygame window to exit.

## Behavior Summary

- Creates `SQUARE_COUNT` squares with random size, position, and velocity.
- Updates each square every frame.
- Applies turn-limited steering away from nearest larger square.
- Reflects velocity when a square hits a window boundary.
- Draws all squares each frame.

## Notes

- This project is intentionally simple and learning-oriented.
- Use it as a base for experimenting with movement, collision, and AI behavior.
