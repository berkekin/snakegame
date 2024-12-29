import tkinter as tk
import random
import time
import os
import json
from typing import List, Tuple, Set, Dict

# -----------------------------
#      LANGUAGE DICTIONARY
# -----------------------------
LANG_STRINGS: Dict[str, Dict[str, str]] = {
    "en": {
        "SETTINGS_TITLE": "Snake Game - Settings Menu",
        "GAME_TITLE": "Snake Game",
        "GAME_MODE_LABEL": "Game Mode:",
        "GAME_MODES": {
            "classic": "Classic",
            "portal": "Portal",
            "obstacles": "Obstacles",
            "ghost": "Ghost"
        },
        "TIMED_GAME_CHECK": "Timed Game",
        "TIME_LABEL": "Time (seconds):",
        "DIFFICULTY_LABEL": "Difficulty Level:",
        "DIFFICULTIES": {
            "easy": "Easy",
            "medium": "Medium",
            "hard": "Hard"
        },
        "SNAKE_COLOR_LABEL": "Snake Color (e.g. 'lime' or '#00FF00'):",
        "BG_COLOR_LABEL": "Background Color (e.g. 'black' or '#000000'):",
        "SNAKE_SHAPE_LABEL": "Snake Shape (square / circle):",
        "PLAYER_NAME_LABEL": "Player Name:",
        "START_BUTTON": "Start Game",
        "SCORE_LABEL": "Score: ",
        "HIGH_SCORE_LABEL": "High Score: ",
        "LEADERBOARD_LABEL": "Leaderboard (Top 5):",
        "TIME_LEFT_LABEL": "Time Left: {} sec",
        "GAME_OVER_TEXT": "GAME OVER!\nPress Enter to restart.",
        "RESUME_TEXT": "GAME PAUSED\nPress 'P' to resume.",
    },
    "es": {
        "SETTINGS_TITLE": "Juego de la Serpiente - Menú de Opciones",
        "GAME_TITLE": "Juego de la Serpiente",
        "GAME_MODE_LABEL": "Modo de Juego:",
        "GAME_MODES": {
            "classic": "Clásico",
            "portal": "Portal",
            "obstacles": "Obstáculos",
            "ghost": "Fantasma"
        },
        "TIMED_GAME_CHECK": "Juego con Tiempo",
        "TIME_LABEL": "Tiempo (segundos):",
        "DIFFICULTY_LABEL": "Nivel de Dificultad:",
        "DIFFICULTIES": {
            "easy": "Fácil",
            "medium": "Medio",
            "hard": "Difícil"
        },
        "SNAKE_COLOR_LABEL": "Color de la Serpiente (ej. 'lime' o '#00FF00'):",
        "BG_COLOR_LABEL": "Color de Fondo (ej. 'black' o '#000000'):",
        "SNAKE_SHAPE_LABEL": "Forma de la Serpiente (square / circle):",
        "PLAYER_NAME_LABEL": "Nombre de Jugador:",
        "START_BUTTON": "Iniciar Juego",
        "SCORE_LABEL": "Puntuación: ",
        "HIGH_SCORE_LABEL": "Puntuación Máxima: ",
        "LEADERBOARD_LABEL": "Tabla de Clasificación (Top 5):",
        "TIME_LEFT_LABEL": "Tiempo Restante: {} seg",
        "GAME_OVER_TEXT": "¡JUEGO TERMINADO!\nPresiona Enter para reiniciar.",
        "RESUME_TEXT": "JUEGO EN PAUSA\nPresiona 'P' para continuar.",
    },
    "fr": {
        "SETTINGS_TITLE": "Jeu du Serpent - Menu des Paramètres",
        "GAME_TITLE": "Jeu du Serpent",
        "GAME_MODE_LABEL": "Mode de Jeu :",
        "GAME_MODES": {
            "classic": "Classique",
            "portal": "Portail",
            "obstacles": "Obstacles",
            "ghost": "Fantôme"
        },
        "TIMED_GAME_CHECK": "Jeu à Temps",
        "TIME_LABEL": "Temps (secondes) :",
        "DIFFICULTY_LABEL": "Niveau de Difficulté :",
        "DIFFICULTIES": {
            "easy": "Facile",
            "medium": "Moyen",
            "hard": "Difficile"
        },
        "SNAKE_COLOR_LABEL": "Couleur du Serpent (ex. 'lime' ou '#00FF00'):",
        "BG_COLOR_LABEL": "Couleur de Fond (ex. 'black' ou '#000000'):",
        "SNAKE_SHAPE_LABEL": "Forme du Serpent (square / circle):",
        "PLAYER_NAME_LABEL": "Nom du Joueur:",
        "START_BUTTON": "Lancer le Jeu",
        "SCORE_LABEL": "Score : ",
        "HIGH_SCORE_LABEL": "Meilleur Score : ",
        "LEADERBOARD_LABEL": "Classement (Top 5) :",
        "TIME_LEFT_LABEL": "Temps Restant : {} s",
        "GAME_OVER_TEXT": "JEU TERMINÉ !\nAppuyez sur Entrée pour recommencer.",
        "RESUME_TEXT": "JEU EN PAUSE\nAppuyez sur 'P' pour continuer.",
    },
}

# -----------------------------
#     GLOBAL GAME CONSTANTS
# -----------------------------
GAME_WIDTH = 500         # The width of the playable area (pixels)
GAME_HEIGHT = 500        # The height of the playable area (pixels)
SNAKE_SIZE = 20          # Each cell of the grid is 20x20 pixels

BG_COLOR_DEFAULT = "black"   # Default background color
SNAKE_COLOR_DEFAULT = "lime" # Default snake color
FOOD_COLOR = "red"           # Normal food color
BONUS_FOOD_COLOR = "gold"    # Bonus food color
OBSTACLE_COLOR = "yellow"    # Obstacles color

BONUS_FOOD_DURATION = 5000   # Bonus food remains on the screen for this many ms
NUM_OBSTACLES = 10           # Number of obstacles to generate (if obstacles mode is chosen)

# Speeds & difficulty increments
DIFFICULTY_SPEED = {
    "easy": 130,
    "medium": 100,
    "hard": 70
}
DIFFICULTY_SPEED_INC = {
    "easy": 5,
    "medium": 7,
    "hard": 10
}

# JSON file for storing multiple players' top scores
HIGH_SCORES_JSON = "highscores.json"


def generate_all_cells() -> Set[Tuple[int, int]]:
    """
    Generate a set of all valid cells on the grid. Each cell corresponds
    to a coordinate (x, y) multiple of SNAKE_SIZE, within the game’s dimensions.
    """
    cells = set()
    x_cells = (GAME_WIDTH // SNAKE_SIZE)
    y_cells = (GAME_HEIGHT // SNAKE_SIZE)
    for ix in range(x_cells):
        for iy in range(y_cells):
            cells.add((ix * SNAKE_SIZE, iy * SNAKE_SIZE))
    return cells


class SnakeGame:
    """
    Main game class for handling logic, drawing, modes (classic, portal, obstacles, ghost),
    timed play, and multiple player high scores in a JSON file.
    """

    def __init__(
        self,
        master: tk.Toplevel,
        language: str = "en",
        game_mode: str = "classic",
        timed_mode: bool = False,
        game_time: int = 30,
        difficulty: str = "medium",
        snake_color: str = SNAKE_COLOR_DEFAULT,
        bg_color: str = BG_COLOR_DEFAULT,
        snake_shape: str = "square",
        player_name: str = "Player"
    ) -> None:
        """
        Initializes a new SnakeGame instance.

        Args:
            master: Parent Tkinter widget or Toplevel window.
            language: The UI language code ("en", "es", or "fr").
            game_mode: "classic", "portal", "obstacles", or "ghost".
            timed_mode: If True, the game is limited to 'game_time' seconds.
            game_time: The total seconds allowed if timed_mode is True.
            difficulty: "easy", "medium", or "hard" (affects speed).
            snake_color: The color of the snake segments.
            bg_color: The canvas background color.
            snake_shape: Shape of the snake segments ("square" or "circle").
            player_name: The player's displayed name for the high score table.
        """
        self.master = master
        self.master.focus_set()  # Ensure focus for key events

        # Store settings
        self.language = language
        self.game_mode = game_mode.lower().strip()
        self.timed_mode = timed_mode
        self.game_time = max(game_time, 1)
        self.difficulty = difficulty.lower().strip()
        self.snake_color = snake_color
        self.bg_color = bg_color
        self.snake_shape = snake_shape.lower()
        self.player_name = player_name.strip() or "Player"

        # Fallback if invalid difficulty
        if self.difficulty not in DIFFICULTY_SPEED:
            self.difficulty = "medium"

        # Text dictionary for this language
        self.texts = LANG_STRINGS.get(self.language, LANG_STRINGS["en"])
        self.master.title(self.texts["GAME_TITLE"])

        # Score & multiple high scores
        self.score = 0
        self.high_scores = self.load_high_scores()  # retrieve list of top {player, score} dicts
        self.high_score = max([d["score"] for d in self.high_scores], default=0)

        # UI elements
        self.score_label = tk.Label(
            self.master,
            text=f"{self.texts['SCORE_LABEL']}{self.score}",
            font=("Arial", 14),
            bg="gray20", fg="white"
        )
        self.score_label.pack(fill=tk.X)

        # Display highest score (single best)
        self.high_score_label = tk.Label(
            self.master,
            text=f"{self.texts['HIGH_SCORE_LABEL']}{self.high_score}",
            font=("Arial", 12),
            bg="gray20", fg="white"
        )
        self.high_score_label.pack(fill=tk.X)

        # Display top 5 leaderboard
        self.leaderboard_label = tk.Label(
            self.master,
            text=self.texts["LEADERBOARD_LABEL"],
            font=("Arial", 12, "bold"),
            bg="gray20", fg="white"
        )
        self.leaderboard_label.pack(fill=tk.X)
        self.leaderboard_frame = tk.Frame(self.master, bg="gray20")
        self.leaderboard_frame.pack(fill=tk.X)
        self.show_leaderboard()

        # Create canvas
        self.canvas = tk.Canvas(
            self.master,
            bg=self.bg_color,
            height=GAME_HEIGHT,
            width=GAME_WIDTH
        )
        self.canvas.pack()

        # Game state
        self.game_over = False
        self.paused = False
        self.current_speed = DIFFICULTY_SPEED[self.difficulty]
        self.all_cells = generate_all_cells()

        # Define snake's initial body (3 segments near the center)
        self.snake_body: List[Tuple[int, int]] = [(240, 240), (220, 240), (200, 240)]
        self.direction = "right"
        self.occupied_cells = set(self.snake_body)

        # Food
        self.food_position = (0, 0)  # assigned below
        # Bonus food
        self.bonus_food_position = None
        self.bonus_food_active = False
        self.bonus_food_appeared_time = 0

        # Obstacles
        self.obstacles: List[Tuple[int, int]] = []
        if self.game_mode == "obstacles":
            self.create_obstacles(NUM_OBSTACLES)

        # Place the initial food
        self.food_position = self.place_food()

        # Timed mode setup
        if self.timed_mode:
            self.time_left = self.game_time
            self.time_label = tk.Label(
                self.master,
                text="",
                font=("Arial", 14),
                bg="gray20", fg="white"
            )
            self.time_label.pack(fill=tk.X)
            self.update_timer()

        # Draw initial items
        self.draw_snake()
        self.draw_food()
        if self.game_mode == "obstacles":
            self.draw_obstacles()

        # Key bindings
        self.master.bind("<Left>", self.go_left)
        self.master.bind("<Right>", self.go_right)
        self.master.bind("<Up>", self.go_up)
        self.master.bind("<Down>", self.go_down)
        self.master.bind("p", self.toggle_pause)
        self.master.bind("<Return>", self.restart_game)

        # Pause automatically if window loses focus
        self.master.bind("<FocusOut>", self.on_focus_out)

        # Start the main loop
        self.move_snake()

    # ----------------------------------------------------------------
    #                  LEADERBOARD & UI
    # ----------------------------------------------------------------

    def show_leaderboard(self) -> None:
        """
        Display the top 5 {player, score} entries in the self.leaderboard_frame.
        """
        for widget in self.leaderboard_frame.winfo_children():
            widget.destroy()

        top_five = self.high_scores[:5]  # top 5
        for idx, entry in enumerate(top_five, start=1):
            lbl = tk.Label(
                self.leaderboard_frame,
                text=f"{idx}. {entry['player']} - {entry['score']}",
                font=("Arial", 10),
                bg="gray20", fg="white",
                anchor="w"
            )
            lbl.pack(fill=tk.X, padx=10)

    def on_focus_out(self, event) -> None:
        """
        Automatically pause the game when the window loses focus.
        """
        if not self.game_over and not self.paused:
            self.toggle_pause(None)

    # ----------------------------------------------------------------
    #                  DRAWING & CANVAS UPDATES
    # ----------------------------------------------------------------

    def draw_snake(self) -> None:
        """
        Clear any existing snake drawing and redraw the snake body
        segments in their current positions.
        """
        self.canvas.delete("snake")
        for (x, y) in self.snake_body:
            if self.snake_shape == "circle":
                self.canvas.create_oval(
                    x, y, x + SNAKE_SIZE, y + SNAKE_SIZE,
                    fill=self.snake_color,
                    tag="snake"
                )
            else:  # default to square
                self.canvas.create_rectangle(
                    x, y, x + SNAKE_SIZE, y + SNAKE_SIZE,
                    fill=self.snake_color, tag="snake"
                )

    def draw_food(self) -> None:
        """
        Clear any existing food drawings (normal & bonus) and
        redraw them at their current positions.
        """
        self.canvas.delete("food")
        fx, fy = self.food_position
        self.canvas.create_rectangle(
            fx, fy, fx + SNAKE_SIZE, fy + SNAKE_SIZE,
            fill=FOOD_COLOR, tag="food"
        )

        # Bonus food
        self.canvas.delete("bonus_food")
        if self.bonus_food_active and self.bonus_food_position:
            bx, by = self.bonus_food_position
            self.canvas.create_oval(
                bx, by, bx + SNAKE_SIZE, by + SNAKE_SIZE,
                fill=BONUS_FOOD_COLOR, tag="bonus_food"
            )

    def draw_obstacles(self) -> None:
        """
        Clear any existing obstacle drawings, then draw each obstacle
        as a rectangle on the canvas.
        """
        self.canvas.delete("obstacle")
        for (ox, oy) in self.obstacles:
            self.canvas.create_rectangle(
                ox, oy, ox + SNAKE_SIZE, oy + SNAKE_SIZE,
                fill=OBSTACLE_COLOR, tag="obstacle"
            )

    # ----------------------------------------------------------------
    #                     FOOD & OBSTACLE PLACEMENT
    # ----------------------------------------------------------------

    def place_food(self) -> Tuple[int, int]:
        """
        Randomly place normal food in a free cell not occupied by
        the snake or obstacles.
        """
        free_cells = self.all_cells - self.occupied_cells
        if free_cells:
            return random.choice(list(free_cells))
        return 0, 0  # fallback

    def place_bonus_food(self) -> Tuple[int, int]:
        """
        Randomly place bonus food in a free cell not occupied by
        the snake, normal food, or obstacles.
        """
        temp_occupied = self.occupied_cells.union({self.food_position})
        free_cells = self.all_cells - temp_occupied
        if free_cells:
            return random.choice(list(free_cells))
        return 0, 0

    def create_obstacles(self, count: int) -> None:
        """
        Create a given number of obstacles in unoccupied cells.

        Args:
            count: How many obstacles to place on the board.
        """
        free_cells = list(self.all_cells - self.occupied_cells)
        random.shuffle(free_cells)
        placed = 0
        self.obstacles.clear()

        while placed < count and free_cells:
            cell = free_cells.pop()
            if cell != self.food_position:
                self.obstacles.append(cell)
                placed += 1

        self.occupied_cells.update(self.obstacles)

    # ----------------------------------------------------------------
    #                        GAME LOOP
    # ----------------------------------------------------------------

    def move_snake(self) -> None:
        """
        Main game loop function:
        1. Calculate the new head position based on current direction.
        2. Check collisions (unless in ghost mode).
        3. Move the snake segments.
        4. Possibly spawn or remove bonus food.
        5. Redraw everything and schedule the next move.
        """
        if self.game_over:
            return

        if self.paused:
            # If the game is paused, just wait 100ms and check again
            self.master.after(100, self.move_snake)
            return

        head_x, head_y = self.snake_body[0]

        # Adjust the head based on direction
        if self.direction == "left":
            head_x -= SNAKE_SIZE
        elif self.direction == "right":
            head_x += SNAKE_SIZE
        elif self.direction == "up":
            head_y -= SNAKE_SIZE
        elif self.direction == "down":
            head_y += SNAKE_SIZE

        # "portal" mode wraps around edges
        if self.game_mode == "portal":
            head_x %= GAME_WIDTH
            head_y %= GAME_HEIGHT
        else:
            # "classic", "obstacles", "ghost": check boundary collision
            if head_x < 0 or head_x >= GAME_WIDTH or head_y < 0 or head_y >= GAME_HEIGHT:
                self.end_game()
                return

        new_head = (head_x, head_y)

        # Check collision with obstacles
        if self.game_mode == "obstacles" and new_head in self.obstacles:
            self.end_game()
            return

        # Check self-collision (unless "ghost" mode)
        if self.game_mode != "ghost":
            if new_head in self.snake_body[1:]:
                self.end_game()
                return

        # Move the snake depending on whether we ate something
        if new_head == self.food_position:
            # Ate normal food
            self.snake_body.insert(0, new_head)
            self.occupied_cells.add(new_head)
            self.score += 1
            self.score_label.config(text=f"{self.texts['SCORE_LABEL']}{self.score}")

            # Make the old food cell free
            self.occupied_cells.discard(self.food_position)
            # Place new food somewhere else
            self.food_position = self.place_food()

            # Increase speed slightly every 5 points
            if self.score % 5 == 0:
                inc = DIFFICULTY_SPEED_INC[self.difficulty]
                self.current_speed = max(30, self.current_speed - inc)
        else:
            # Check if we ate bonus food
            if self.bonus_food_active and new_head == self.bonus_food_position:
                self.score += 3
                self.score_label.config(text=f"{self.texts['SCORE_LABEL']}{self.score}")
                self.bonus_food_active = False
                self.occupied_cells.discard(self.bonus_food_position)
                self.bonus_food_position = None
            else:
                # Normal movement: remove tail
                tail = self.snake_body.pop()
                self.occupied_cells.discard(tail)

            # Now add new head
            self.snake_body.insert(0, new_head)
            self.occupied_cells.add(new_head)

        # Possibly spawn bonus food with a small probability
        if not self.bonus_food_active and random.random() < 0.01:
            self.bonus_food_position = self.place_bonus_food()
            self.bonus_food_active = True
            self.bonus_food_appeared_time = time.time()
            self.occupied_cells.add(self.bonus_food_position)

        # Bonus food expiration
        if self.bonus_food_active:
            elapsed = (time.time() - self.bonus_food_appeared_time) * 1000
            if elapsed > BONUS_FOOD_DURATION:
                if self.bonus_food_position in self.occupied_cells:
                    self.occupied_cells.discard(self.bonus_food_position)
                self.bonus_food_active = False
                self.bonus_food_position = None

        # Redraw the snake, food, obstacles
        self.draw_snake()
        self.draw_food()
        if self.game_mode == "obstacles":
            self.draw_obstacles()

        # Schedule the next movement step
        self.master.after(self.current_speed, self.move_snake)

    # ----------------------------------------------------------------
    #                        TIMED MODE
    # ----------------------------------------------------------------

    def update_timer(self) -> None:
        """
        Decrements the time_left each second in timed mode
        and ends the game when it reaches zero.
        """
        if self.timed_mode and not self.game_over and not self.paused:
            self.time_left -= 1
            if hasattr(self, "time_label"):
                # Update the time label text in the chosen language
                self.time_label.config(text=self.texts["TIME_LEFT_LABEL"].format(self.time_left))

            if self.time_left <= 0:
                self.end_game()
                return

        self.master.after(1000, self.update_timer)

    # ----------------------------------------------------------------
    #                   END / RESTART GAME
    # ----------------------------------------------------------------

    def end_game(self) -> None:
        """
        Sets the game_over flag, updates high scores, and displays a
        game-over message on the canvas.
        """
        self.game_over = True
        self.update_high_scores()
        self.canvas.create_text(
            GAME_WIDTH / 2,
            GAME_HEIGHT / 2,
            text=self.texts["GAME_OVER_TEXT"],
            fill="white",
            font=("Arial", 20, "bold")
        )

    def restart_game(self, event) -> None:
        """
        Resets the entire game state (snake, food, score, etc.)
        and starts a new round without closing the window.
        """
        if not self.game_over:
            return

        self.game_over = False
        self.paused = False
        self.score = 0
        self.score_label.config(text=f"{self.texts['SCORE_LABEL']}{self.score}")

        # Recalculate the best score among current top scores
        self.high_score = max((d["score"] for d in self.high_scores), default=0)
        self.high_score_label.config(text=f"{self.texts['HIGH_SCORE_LABEL']}{self.high_score}")

        # Reset snake
        self.snake_body = [(240, 240), (220, 240), (200, 240)]
        self.direction = "right"
        self.current_speed = DIFFICULTY_SPEED[self.difficulty]

        # Reset sets
        self.all_cells = generate_all_cells()
        self.occupied_cells = set(self.snake_body)
        self.obstacles.clear()

        # Reset food/bonus
        self.bonus_food_position = None
        self.bonus_food_active = False
        self.food_position = (0, 0)

        # Recreate obstacles if needed
        if self.game_mode == "obstacles":
            self.create_obstacles(NUM_OBSTACLES)

        # Place the initial food again
        self.food_position = self.place_food()

        # Clear canvas and redraw
        self.canvas.delete("all")
        self.draw_snake()
        self.draw_food()
        if self.game_mode == "obstacles":
            self.draw_obstacles()

        # Reset timer
        if self.timed_mode:
            self.time_left = self.game_time
            if hasattr(self, "time_label"):
                self.time_label.config(text=self.texts["TIME_LEFT_LABEL"].format(self.time_left))

        # Resume loop
        self.move_snake()

    # ----------------------------------------------------------------
    #                  KEYBOARD CONTROLS
    # ----------------------------------------------------------------

    def go_left(self, event) -> None:
        """Change the direction to left if not currently going right."""
        if self.direction != "right":
            self.direction = "left"

    def go_right(self, event) -> None:
        """Change the direction to right if not currently going left."""
        if self.direction != "left":
            self.direction = "right"

    def go_up(self, event) -> None:
        """Change the direction to up if not currently going down."""
        if self.direction != "down":
            self.direction = "up"

    def go_down(self, event) -> None:
        """Change the direction to down if not currently going up."""
        if self.direction != "up":
            self.direction = "down"

    def toggle_pause(self, event) -> None:
        """
        Pauses or resumes the game if it's not over.
        Displays a pause message on the canvas.
        """
        if self.game_over:
            return

        self.paused = not self.paused
        if self.paused:
            self.canvas.create_text(
                GAME_WIDTH / 2,
                GAME_HEIGHT / 2,
                text=self.texts["RESUME_TEXT"],
                fill="white",
                font=("Arial", 18, "bold"),
                tag="pause_msg"
            )
        else:
            self.canvas.delete("pause_msg")

    # ----------------------------------------------------------------
    #        MULTIPLE HIGH SCORES (JSON-based)
    # ----------------------------------------------------------------

    def load_high_scores(self) -> List[Dict[str, any]]:
        """
        Load multiple scores from the JSON file, if it exists,
        returning a list of dicts: [{"player": str, "score": int}, ...].
        Sorted descending by "score".
        """
        if not os.path.exists(HIGH_SCORES_JSON):
            return []

        try:
            with open(HIGH_SCORES_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

        # Sort by score descending
        data.sort(key=lambda d: d["score"], reverse=True)
        return data

    def save_high_scores(self, data: List[Dict[str, any]]) -> None:
        """
        Persists the updated list of {player, score} dicts into the JSON file.
        """
        with open(HIGH_SCORES_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def update_high_scores(self) -> None:
        """
        Insert the current {player_name, score} into the leaderboard,
        keep only the top 5, and update displayed high scores.
        """
        data = self.load_high_scores()
        data.append({"player": self.player_name, "score": self.score})
        data.sort(key=lambda d: d["score"], reverse=True)
        data = data[:5]  # keep top 5
        self.save_high_scores(data)
        self.high_scores = data

        # Update the displayed "high_score" if the new top is greater
        best_score = data[0]["score"] if data else 0
        if best_score > self.high_score:
            self.high_score = best_score
        self.high_score_label.config(text=f"{self.texts['HIGH_SCORE_LABEL']}{self.high_score}")

        # Refresh the leaderboard display
        self.show_leaderboard()


class SettingsMenu:
    """
    A settings menu for configuring:
    - Language (en, es, fr)
    - Player Name
    - Game mode (classic, portal, obstacles, ghost)
    - Timed mode and duration
    - Difficulty (easy, medium, hard)
    - Snake color / background color
    - Snake shape (square / circle)
    """

    def __init__(self, master: tk.Tk) -> None:
        """
        Sets up the settings menu with default values for
        language, game mode, timing, difficulty, shapes, and colors.
        """
        self.master = master
        self.language_var = tk.StringVar(value="en")

        # Start with English as default text
        self.texts = LANG_STRINGS["en"]
        self.master.title(self.texts["SETTINGS_TITLE"])

        # Create the menu layout
        self.create_widgets()
        # After widgets are created, set up language radio buttons
        self.create_language_widgets()

    def create_widgets(self) -> None:
        """Create all main widgets using the currently selected language text."""
        # Player name
        tk.Label(self.master, text=self.texts["PLAYER_NAME_LABEL"]).pack()
        self.player_name_entry = tk.Entry(self.master)
        self.player_name_entry.insert(0, "Player")
        self.player_name_entry.pack()

        # Frame for game mode
        self.game_mode_var = tk.StringVar(value="classic")
        tk.Label(self.master, text=self.texts["GAME_MODE_LABEL"]).pack()
        modes_frame = tk.Frame(self.master)
        modes_frame.pack()

        for mode_key in ["classic", "portal", "obstacles", "ghost"]:
            text_label = self.texts["GAME_MODES"][mode_key]
            rb = tk.Radiobutton(
                modes_frame,
                text=text_label,
                variable=self.game_mode_var,
                value=mode_key
            )
            rb.pack(side=tk.LEFT, padx=5)

        # Timed mode checkbox
        self.timed_var = tk.BooleanVar()
        tk.Checkbutton(self.master, text=self.texts["TIMED_GAME_CHECK"], variable=self.timed_var).pack()

        # Game time input
        tk.Label(self.master, text=self.texts["TIME_LABEL"]).pack()
        self.time_entry = tk.Entry(self.master)
        self.time_entry.insert(0, "30")  # default
        self.time_entry.pack()

        # Difficulty selection
        self.diff_var = tk.StringVar(value="medium")
        tk.Label(self.master, text=self.texts["DIFFICULTY_LABEL"]).pack()
        diff_frame = tk.Frame(self.master)
        diff_frame.pack()

        for diff_key in ["easy", "medium", "hard"]:
            text_label = self.texts["DIFFICULTIES"][diff_key]
            rb = tk.Radiobutton(
                diff_frame,
                text=text_label,
                variable=self.diff_var,
                value=diff_key
            )
            rb.pack(side=tk.LEFT, padx=5)

        # Snake color
        tk.Label(self.master, text=self.texts["SNAKE_COLOR_LABEL"]).pack()
        self.snake_color_entry = tk.Entry(self.master)
        self.snake_color_entry.insert(0, SNAKE_COLOR_DEFAULT)
        self.snake_color_entry.pack()

        # Background color
        tk.Label(self.master, text=self.texts["BG_COLOR_LABEL"]).pack()
        self.bg_color_entry = tk.Entry(self.master)
        self.bg_color_entry.insert(0, BG_COLOR_DEFAULT)
        self.bg_color_entry.pack()

        # Snake shape
        tk.Label(self.master, text=self.texts["SNAKE_SHAPE_LABEL"]).pack()
        self.snake_shape_entry = tk.Entry(self.master)
        self.snake_shape_entry.insert(0, "square")
        self.snake_shape_entry.pack()

        # Start button
        self.start_button = tk.Button(self.master, text=self.texts["START_BUTTON"], command=self.start_game)
        self.start_button.pack(pady=10)

    def create_language_widgets(self) -> None:
        """
        Create radio buttons for language selection.
        Whenever the language changes, re-run the translation of the UI.
        """
        lang_frame = tk.Frame(self.master)
        lang_frame.pack(pady=5)

        # A label for "Language:"
        lang_label = tk.Label(lang_frame, text="Language:")
        lang_label.pack(side=tk.LEFT, padx=5)

        for lang_code in ["en", "es", "fr"]:
            rb = tk.Radiobutton(
                lang_frame,
                text=lang_code.upper(),
                variable=self.language_var,
                value=lang_code,
                command=self.change_language
            )
            rb.pack(side=tk.LEFT, padx=5)

    def change_language(self) -> None:
        """
        Called when user selects a different language radio button.
        This will update all widget texts to the newly selected language.
        """
        new_lang = self.language_var.get()
        self.texts = LANG_STRINGS[new_lang]
        self.master.title(self.texts["SETTINGS_TITLE"])

        # Destroy all widgets and rebuild in the new language
        for widget in self.master.winfo_children():
            widget.destroy()

        self.create_widgets()
        self.create_language_widgets()
        self.language_var.set(new_lang)

    def start_game(self) -> None:
        """
        Validate user input, then create a new Toplevel window
        and launch the SnakeGame with chosen settings.
        """
        game_mode = self.game_mode_var.get()
        timed_mode = self.timed_var.get()

        # Validate the game time
        try:
            game_time = int(self.time_entry.get())
        except ValueError:
            game_time = 30

        difficulty = self.diff_var.get()
        snake_color = self.snake_color_entry.get()
        bg_color = self.bg_color_entry.get()
        snake_shape = self.snake_shape_entry.get().lower().strip()
        player_name = self.player_name_entry.get()

        # Create a new top-level window for the actual game
        game_window = tk.Toplevel(self.master)
        SnakeGame(
            master=game_window,
            language=self.language_var.get(),
            game_mode=game_mode,
            timed_mode=timed_mode,
            game_time=game_time,
            difficulty=difficulty,
            snake_color=snake_color,
            bg_color=bg_color,
            snake_shape=snake_shape,
            player_name=player_name
        )


def main() -> None:
    """
    The main entry point that creates the Tk root window,
    sets up the SettingsMenu, and starts the GUI event loop.
    """
    root = tk.Tk()
    SettingsMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()
