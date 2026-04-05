# Lab 8 - Pygame

Simple Pygame project scaffold for animating squares on screen.

This project is intentionally kept small so you can focus on core pygame ideas:
window setup, event handling, drawing rectangles, and updating motion over time.

## Project Files

- `main.py` contains the pygame scaffold and the square simulation logic.
- `requirements.txt` tracks Python dependencies.
- `.venv` is the local virtual environment used for development.

## Prerequisites

- Python 3.11+
- A PowerShell terminal on Windows

## Setup (Windows PowerShell)

1. Create virtual environment:

   ```powershell
   py -m venv .venv
   ```

2. Activate virtual environment:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

If the environment is already created, activate it and install dependencies again only if needed.

## Run

```powershell
python main.py
```

## What the Program Does

- Opens a pygame window.
- Creates a small collection of square objects.
- Updates and draws those squares each frame.

## Notes

- The current code is a learning scaffold, not a finished game.
- Some logic is intentionally left as TODOs so you can complete it yourself.

## Dependencies

Tracked in `requirements.txt`.
