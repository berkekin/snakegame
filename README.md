# snakegame

Snake Game
Welcome to the Snake Game repository! This project is a modernized take on the classic Snake game, built in Python using the Tkinter library for the GUI. It supports multiple game modes, difficulty levels, bonus items, and an evolving leaderboard stored in JSON.

Features
Multiple Game Modes

Classic – Standard Snake gameplay with boundary collisions.
Portal – Wrap around the screen edges to appear on the opposite side.
Obstacles – Randomly generated obstacles that you must avoid.
Ghost – Pass through yourself without collision.
Timed Mode

Optionally limit each game to a certain number of seconds.
Perfect for quick sessions or “speed run” challenges.
Difficulties & Speed

Choose Easy, Medium, or Hard—each modifies the movement speed and the speed-up increments earned through scoring.
Bonus Food

Occasionally appears on the board for a limited time. Eat it quickly to gain extra points.
Leaderboard & JSON Storage

Stores high scores in a JSON file.
Each record associates a player name with a score.
Automatically shows the Top 5 scores in the game’s UI.
Multiple Languages

Built-in support for English (en), Spanish (es), and French (fr).
Easily extendable by adding more language entries in the dictionary.
Customizable Snake Appearance

Change the snake color and canvas background.
Choose between square or circle snake segments.
Automatic Pause

The game will pause whenever it loses focus, and you can also manually toggle pause with the p key.
Getting Started
Clone the Repo:



git clone https://github.com/YourUsername/snake-game.git
cd snake-game
Install Python Dependencies (optional if you are already on a standard Python 3.x environment):



pip install --upgrade pip
pip install --user tk
Note: Tkinter often comes pre-installed with Python on most systems.

Run the Game:


python snakegame.py
A Settings Menu will appear allowing you to configure the game (language, difficulty, timed mode, colors, etc.). Click Start Game to launch a new Snake game window.

Enjoy & Contribute!

Folder Structure
snakegame.py
Main Python file containing both the settings menu (GUI) and the Snake game logic.
highscores.json
Automatically created JSON file storing top scores and player names.
Contributing
Fork this repository.
Create a feature branch (git checkout -b feature/new-mode).
Commit your changes (git commit -m "Add a new stealth mode").
Push to the branch (git push origin feature/new-mode).
Create a Pull Request.
