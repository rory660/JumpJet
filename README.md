# Spectrum Platformer (temporary title)
![screenshot](https://user-images.githubusercontent.com/30571778/40951368-7ac13762-686e-11e8-88ab-851114373dbb.png)
Platformer game made with Pygame

## Requirements
- Python 3
- pygame module

## Main game
Run game.py with Python 3. You will be prompted to choose a level id. Enter a number corresponding to any level in the "levels" folder. Once a level has been chosen, the game will run. Get to the exit of each level to progress to the next level.

### Controls
- `a` and `d` keys to move left and right
- `space` to jump

## Editor
Run editor.py with Python 3. You will be prompted to either load a level by id, or create a new level. You can define a width and height for the level. Once running, the editor will display a green box representing the play area. In the actual game, the camera is locked to this area. In order to be ran, the level must have an entrance and exit, currently represented by white and green platforms.

### Controls
- `wasd` to move the camera.
- `z` and `x` to switch placement mode. Current placement modes include walls, hazards, entrance and exit.
- `q` and `e` to switch object within a placement mode.
- `ctrl-s` to save the level. If a level has been loaded, it will be overwritten with a save. Otherwise, a new file will be created for the level.
- `ctrl-z` to undo previous edit.
