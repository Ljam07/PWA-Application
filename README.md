# Game Rating PWA-Application

This is a simple Flask application that allows users to rate games. The application connects to a SQLite database to store game ratings.

## Features

- Submit ratings for games
- Fetch a random game from the database to rate

## Requirements

- Python 3.x
- Flask
- SQLite

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Ljam07/PWA-Application.git
    cd PWA-Application
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    .venv\Scripts\activate.bat  # On Mac, use `source .venv/bin/activate`
    ```

3. Install the required packages:
    - Either run the ```Setup.bat``` file OR
    - Run this in the command line:
        ```bash
        pip install -r requirements.txt
        ```

## Usage

1. Run the Flask application:
    ```bash
    python main.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/` to access the page.

## Code Overview

- `main.py`: The main Flask application file.
- `database/games.db`, `database/users.db`: The SQLite database files.
- `templates/*.html`: The HTML render templates for all pages.
- `static/`: The folder containing all the nice looking stuff.

## License

This project is licensed under the GNU General Public Lisence. See the `LICENSE` file for more details.
