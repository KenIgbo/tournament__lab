# TournamentLab — Design Decisions

This document records the major technical decisions made during the development of TournamentLab and explains why each decision was chosen.

## 1. Programming Language

**Decision:** Python.

**Reason:**

Python was selected because of its readability, simplicity, and suitability for building command-line applications.

It also provides built-in modules for JSON handling, mathematical operations, random number generation, and automated testing.

## 2. Application Type

**Decision:** Command-Line Interface (CLI).

**Reason:**

The project focuses on application logic, data management, validation, and Python programming rather than web development.

A command-line interface provides a straightforward way to interact with the tournament system.

## 3. Modular Architecture

**Decision:** Divide the application into separate modules.

**Reason:**

Instead of placing all application logic inside `main.py`, responsibilities are separated into different modules.

| Module | Responsibility |
|---|---|
| `teams.py` | Team registration and team-related operations |
| `fixtures.py` | Fixture generation and listing |
| `results.py` | Result validation and recording |
| `standings.py` | League statistics and ranking |
| `storage.py` | JSON persistence and data validation |
| `simulation.py` | Tournament result simulation |
| `main.py` | Application menu and coordination |

This approach improves readability, maintainability, and testability.

## 4. Data Structures

**Decision:** Use dictionaries to represent teams and fixtures.

**Reason:**

Dictionaries allow related information to be grouped using meaningful keys.

Team example:

```python
{
    "id": "TM001",
    "name": "Red Comets"
}
```

Fixture example:

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

Lists are used to store multiple teams and fixtures.

## 5. Team Identification

**Decision:** Generate unique team IDs using the format `TM001`, `TM002`, and so on.

**Reason:**

Team IDs provide a consistent way to identify teams independently of their names.

Fixtures store team IDs instead of duplicating team names.

This reduces unnecessary data duplication and makes it easier to retrieve team information.

## 6. Team Registration Rules

**Decision:** Allow between 4 and 8 teams.

**Reason:**

The tournament requires at least four teams to generate a meaningful round-robin competition.

The maximum limit of eight keeps the tournament within the project's specified requirements.

Additional rules:
- Names must contain 2–30 characters after trimming.
- Names must be unique regardless of letter casing.
- Team registration is locked once fixtures have been generated.

Locking registration prevents changes to the team list from invalidating an existing fixture schedule.

## 7. Round-Robin Fixture Generation

**Decision:** Use Python's `itertools.combinations()`.

**Reason:**

A single round-robin tournament requires every team to play every other team exactly once.

The number of fixtures is calculated using:

```python
n * (n - 1) // 2
```

For example:

| Teams | Fixtures |
|---:|---:|
| 4 | 6 |
| 5 | 10 |
| 6 | 15 |
| 7 | 21 |
| 8 | 28 |

Using combinations avoids manually writing fixture pairings and prevents duplicate unordered matchups.

Fixtures are generated only once per tournament.

## 8. Fixture Status

**Decision:** Use two fixture statuses: `pending` and `played`.

**Reason:**

A pending fixture has not received a result.

A played fixture has valid home and away scores.

This distinction makes it possible to determine which fixtures can accept results and whether the tournament is complete.

## 9. Score Validation

**Decision:** Accept only nonnegative whole-number scores.

**Reason:**

Football scores cannot be negative or fractional.

Since Python's `input()` function returns strings, scores are first validated as strings before being converted into integers.

The `str.isdecimal()` method is used to check that the input contains decimal digits only.

Both scores are validated before either score is assigned to the fixture.

This prevents invalid input from partially modifying tournament data.

## 10. Preventing Duplicate Results

**Decision:** Only fixtures with `pending` status can receive results.

**Reason:**

Once a fixture has been played, its result must not be submitted again.

This prevents duplicate result entries and ensures that teams do not receive points more than once for the same fixture.

## 11. Standings Calculation

**Decision:** Calculate standings dynamically from played fixtures instead of storing standings separately.

**Reason:**

Storing standings independently could lead to inconsistencies between match results and league statistics.

By calculating standings from fixture records, the application always derives its statistics from the available match data.

Only fixtures with `played` status contribute to standings.

## 12. Ranking Rules

**Decision:** Rank teams using the following order:

1. Points.
2. Goal difference.
3. Goals scored.
4. Team name in alphabetical order.

**Reason:**

This provides predictable ranking when teams have equal points.

The final alphabetical comparison ensures deterministic ordering when all numerical tie-breakers are equal.

## 13. Tournament Completion

**Decision:** Announce the champion only when all generated fixtures have been played.

**Reason:**

Announcing a champion while fixtures remain pending would produce an incomplete tournament result.

When matches remain, the standings are displayed as being in progress.

## 14. JSON Persistence

**Decision:** Use JSON for storing tournament information.

**Reason:**

JSON is lightweight, human-readable, and supported by Python's built-in `json` module.

The file stores teams and fixtures.

Standings are not stored because they are calculated from fixture results.

## 15. Data Validation During Loading

**Decision:** Validate tournament data before loading it into the application's working lists.

**Reason:**

A JSON file can contain syntactically valid JSON but still have invalid tournament information.

Validation checks the structure, team records, fixture records, IDs, references, scores, and fixture pairings.

Invalid data must be rejected without replacing the application's existing in-memory tournament data.

## 16. Automated Testing

**Decision:** Use Python's built-in `unittest` framework.

**Reason:**

Automated testing makes it possible to verify application behaviour without manually repeating every operation.

Tests are separated according to module responsibilities.

Mocking is used where appropriate to prevent tests from unnecessarily modifying the actual tournament data file.

## 17. AI Assistance

**Decision:** Use AI as a learning assistant and code reviewer rather than as an external service inside the application.

**Reason:**

The purpose of the project is to develop Python programming and software engineering skills.

AI assistance is used to explain concepts, review code, identify potential problems, and help design tests.

The application does not depend on an AI API.