# TournamentLab

TournamentLab is a Python command-line tournament management system designed to manage a local football league.

The application allows users to register teams, generate a single round-robin fixture schedule, record match results, calculate league standings, and determine the tournament champion.

The project focuses on applying Python programming concepts, modular development, data validation, file handling, and automated testing.

## Features

### 1. Team Registration
- Register between 4 and 8 teams for a tournament.
- Team names must contain between 2 and 30 characters.
- Team names are trimmed before registration.
- Duplicate team names are rejected, regardless of letter casing.
- Every team receives a unique ID.

### 2. Fixture Generation
- Automatically generate a single round-robin schedule.
- Every team plays every other team exactly once.
- Prevent duplicate fixture generation.
- Generate unique fixture IDs.
- Each fixture stores its home team, away team, status, and scores.

### 3. Fixture Management
- Display all generated fixtures.
- Show fixture IDs, participating teams, and match status.
- Distinguish between pending and played fixtures.

### 4. Result Recording
- Record results for existing fixtures.
- Accept only nonnegative whole-number scores.
- Reject invalid scores.
- Prevent a fixture from receiving results more than once.
- Save valid results to the tournament data file.

### 5. League Standings
Automatically calculate:
- Matches played
- Wins
- Draws
- Losses
- Points
- Goals for
- Goals against
- Goal difference

Points system:
- Win: 3 points
- Draw: 1 point
- Loss: 0 points

Teams are ranked using the following rules:
1. Points (highest first).
2. Goal difference (highest first).
3. Goals scored (highest first).
4. Team name (alphabetical order).

The champion is announced only after every fixture has been played.

### 6. Data Storage
- Store tournament information in a JSON file.
- Load previously saved tournament data.
- Validate loaded data before accepting it.
- Reject malformed or inconsistent tournament data.

### 7. Tournament Simulation
The project also includes a simulation feature intended to generate reproducible demonstration results without requiring manual entry for every fixture.

Simulation must be explicitly selected by the user and must not secretly modify tournament records.

## Technologies

- Python 3
- JSON
- Python Standard Library
- `unittest` for automated testing

No external Python packages are required.

## Project Structure

```text
tournament__lab/
│
├── main.py
├── README.md
│
├── tournament/
│   ├── __init__.py
│   ├── teams.py
│   ├── fixtures.py
│   ├── results.py
│   ├── standings.py
│   ├── storage.py
│   └── simulation.py
│
├── tests/
│   ├── test_teams.py
│   ├── test_fixtures.py
│   ├── test_results.py
│   ├── test_standings.py
│   ├── test_storage.py
│   ├── test_simulation.py
│   └── test_main.py
│
├── docs/
│   ├── design-decisions.md
│   └── ai-learning-log.md
│
│
└── tournament.json
```

## Installation and Setup

Clone or download the project.

Navigate into the project directory:

```bash
cd tournament__lab
```

No external dependencies need to be installed.

## Running the Application

Run the application using:

```bash
python3 main.py
```

## Running Tests

The project uses Python's built-in `unittest` framework.

Run the complete test suite:

```bash
python3 -m unittest discover -s tests -v
```

The `-v` option displays the individual test names and their results.

## Data Model

### Team

Each team is represented as a dictionary:

```python
{
    "id": "TM001",
    "name": "Red Comets"
}
```

### Fixture

Each fixture is represented as a dictionary:

```python
{
    "id": "M001",
    "home_id": "TM001",
    "away_id": "TM002",
    "status": "pending",
    "home_score": None,
    "away_score": None
}
```

When a result is recorded, the fixture's status changes to `played`, and both scores are stored as integers.

## Testing

Automated tests are organised according to the application's modules.

Current testing coverage includes:

- Team registration and validation.
- Round-robin fixture generation.
- Result validation and recording.
- Standings calculation and ranking.
- Tournament data validation and persistence.

Additional testing for simulation and the main application flow is planned.

## Project Goals

TournamentLab is a learning project intended to demonstrate practical Python development skills, including:

- Functions and modular programming.
- Lists and dictionaries.
- Loops and conditional statements.
- Exception handling.
- File handling and JSON.
- Data validation.
- Automated testing.
- Software design and problem-solving.

---
**Project:** TournamentLab  
**Language:** Python  
**Application Type:** Command-Line Interface (CLI)