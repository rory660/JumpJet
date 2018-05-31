# JumpJet (working title)
![screenshot](https://user-images.githubusercontent.com/30571778/40794783-18333c7c-64f8-11e8-92fa-c9b667f0a3d2.png)
Platformer game made with Pygame

## Requirements
- Python 3
- pygame module

## Main game
Run game.py with Python 3. You will be prompted to choose a level id. Enter a number corresponding to any level in the "levels" folder. Once a level has been chosen, the game will run.

### Controls
- `a` and `d` keys to move left and right
- `space` to jump
- `←→↑↓` to 'boost' in any cardinal direction. This is a WIP feature that will be used to navigate levels, and the number of boosts available per jump will be limited, but currently is not.

## Editor
Run editor.py with Python 3. You will be prompted to either load a level by id, or create a new level. You can define a width and height for the level. Once running, the editor will display a green box representing the play area. In the actual game, the camera is locked to this area. In order to be ran, the level must have an entrance and exit, currently represented by white and green platforms.

### Controls
- `wasd` to move the camera.
- `z` and `x` to switch placement mode. Current placement modes include walls, hazards, entrance and exit.
- `q` and `e` to switch object within a placement mode.
- `ctrl-s` to save the level. If a level has been loaded, it will be overwritten with a save. Otherwise, a new file will be created for the level.
