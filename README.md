# Tournament Log Reader Challenge

This project parses a Quake 3 Arena server log file, extracts and organizes game data, and generates a detailed report of player performances and rankings.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)

## Features

- Parses a Quake 3 Arena log file and groups data by match.
- Collects and organizes kill data for each match.
- Generates a report summarizing total kills, players, and player rankings.
- Ensures correct handling of player names, including composed names.
- Orders player rankings by the number of kills in descending order.

## Requirements

- Python 3.8 or higher
- [pip](https://pip.pypa.io/en/stable/)

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/leoanjossantos/tournament_log_reader_challenge.git
    cd tournament_log_reader_challenge
    ```

2. **Create and activate a virtual environment:**

    - On macOS and Linux:

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

    - On Windows:

        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

## Usage

1. **Run the log parser script:**

    ```bash
    python3 parser_game_logs.py
    ```

    The script will parse the log file, generate a report, and print it to the console.

## Running Tests

1. **Ensure the virtual environment is activated:**

    ```bash
    source venv/bin/activate
    ```

2. **Run the unit tests:**

    ```bash
    python3 -m unittest test_parser_game_logs.py
    ```

    This command will execute all the test cases and provide you with a report on the test results.

## Project Structure

```plaintext
tournament_log_reader_challenge/
├── parser_game_logs.py            # Main script for parsing logs and generating the report
├── test_parser_game_logs.py       # Unit tests for the log parser
├── logs.txt                       # Example log file to be parsed
└── README.md                      # This README file 
