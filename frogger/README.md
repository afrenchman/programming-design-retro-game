# Overview

A replica of the classic Frogger arcade game, rebuilt using Python and Pygame. Dodge cars, jump on turtles, and race against time to reach your lily pads safely.

## Instructions

1. Run the `main.py` and select Frogger from the menu.
2. Alternatively, run `frogger.py` directly.

## Controls

Key | Action
---|---
D-Pad Up | Move Up
D-Pad Down | Move Down
D-Pad Left | Move Left
D-Pad Right | Move Right
START Button | Exit to main menu
A Button | Restart after Game Over

## Features

- Multi-lane traffic with moving enemies (cars)
- River with dynamic platforms (logs and turtles)
- High score tracking
- Time-limited levels and life system
- Retro visuals and sound effects
- Integrated gamepad support

## Algorithms Used

Category | Description
---|---
Collision Detection | Rect-based collisions between frog and enemies/platforms
Game State Management | Finite state machine to control menu, game, and Game Over transitions
Time Management | Countdown timer for each level
Object Pooling | Lists to manage dynamic creation and cleanup of enemies/platforms
Animation System | Frame-based sprite animation for frog movement

## Next Plan of Action

* Game complete and integrated into multi-game system

## Assets

Asset | Credits
---|---
Fonts | bit5x3.ttf
Sound Effects | Public domain resources
Background and Sprites | Edited by Said Castro using open game art and custom pixel art
