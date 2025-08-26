# Python Chess Desktop Application

This project is a desktop chess application built using Python. It allows two players to play chess against each other, integrates game analysis features, and tracks illegal moves. The application provides a graphical user interface (GUI) for an engaging user experience.

## Features

- Two-player chess gameplay
- Integration with Gemini Flash for game analysis
- Start and pause buttons for analysis
- Tracking of illegal moves
- FEN format support for move prompts

## Project Structure

```
python-chess-desktop-app
├── src
│   ├── main.py                # Entry point of the application
│   ├── gui
│   │   └── chess_window.py     # GUI management for the chess game
│   ├── analysis
│   │   └── gemini_flash.py     # Integration with Gemini Flash API
│   ├── chess
│   │   ├── board.py            # Chessboard logic and piece movements
│   │   └── move_tracker.py      # Tracking illegal moves
│   ├── utils
│   │   └── fen.py              # Utility functions for FEN format
│   └── types
│       └── index.py            # Types and constants used in the application
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd python-chess-desktop-app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To start the application, run the following command:
```
python src/main.py
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.