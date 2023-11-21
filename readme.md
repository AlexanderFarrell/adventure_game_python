# Adventure Game in Pygame & Python

This game is a tile-based 2D adventure game created with Pygame. The video for this step can be found here [Tiles and Sprites in Pygame - Adventure Game Part 1](https://www.youtube.com/watch?v=w8i5sizgVNs)


## Setup

1. Open a terminal at the project location. In VSCode, go to the top where it says **Terminal**, and click **New Terminal**. If you don't see terminal, you may see three dots near the top left, click those and see if **Terminal** is under those.
2. Create a virtual environment. Run `python3 -m venv venv`. If you get an error, try `python -m venv venv`. If this still does not work, ensure [Python is installed on your system](https://www.python.org/downloads/). 
3. Activate the virtual environment. **On MacOS, Linux and Unix**, run `source venv/bin/activate`. **On Windows**, run `venv/Scripts/activate`.
4. Install Pygame by typing `pip install pygame`.
5. Run the game by typing `python3 main.py`. If this doesn't succeed, try `python main.py`.


## Navigation

|             Item             |  Description  |
|------------------------------|---------------|
| [images](./images)           | Sprites and tiles in the game. |
| [input.py](./input.py)       | Helper code for User Input |
| [main.py](./main.py)         | Brings everything together. Run this to start the game. |
| [player.py](./player.py)     | The player, which can move around. |
| [sprite.py](./sprite.py)     | An image which can be drawn to the screen. |


