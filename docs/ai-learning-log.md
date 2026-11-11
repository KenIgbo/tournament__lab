# TournamentLab — AI Learning Log

## Project Overview

**Project:** TournamentLab

**Programming Language:** Python

**Project Type:** Command-Line Application

**Purpose of AI Assistance:**

AI was used as a programming tutor and development assistant throughout the project.

The objective was to understand the programming concepts, design decisions, and testing strategies rather than simply copy and paste code.

No AI API is integrated into the application.

---

## Learning and Development Log

### 1. Project Architecture

**Topics explored:**
- Modular programming.
- Separating application responsibilities.
- Organising Python packages.
- Importing functions and variables between modules.

**What I learned:**

A project becomes easier to maintain when related functionality is separated into modules.

For example, team registration belongs in `teams.py`, while fixture generation belongs in `fixtures.py`.

The `main.py` file should coordinate the application rather than contain all the business logic.

### 2. Team Registration

**Topics explored:**
- Lists and dictionaries.
- Unique identifiers.
- String methods.
- Input validation.
- Case-insensitive comparisons.

**What I learned:**

The `strip()` method removes unnecessary whitespace from team names.

The `casefold()` method allows names to be compared without treating uppercase and lowercase letters as different names.

Team IDs provide a consistent way to reference teams in fixtures.

### 3. Round-Robin Fixture Generation

**Topics explored:**
- The `itertools` module.
- Combinations.
- Nested data structures.
- Mathematical fixture calculations.

**What I learned:**

The `itertools.combinations()` function can generate every unique pair of teams.

For a single round-robin tournament, the number of fixtures is:

```python
n * (n - 1) // 2
```

This eliminates the need to manually create fixture pairings.

### 4. Result Validation

**Topics explored:**
- The `input()` function.
- String validation.
- Type conversion.
- Boolean and integer relationships in Python.
- Preventing partial data modification.

**What I learned:**

Python's `input()` function returns a string, even when the user enters a number.

The `isdecimal()` method can be used to validate nonnegative whole-number input.

I also learned that `bool` is a subclass of `int` in Python.

Therefore, validation must consider the actual data type when accepting numeric values.

An important lesson was to validate both home and away scores before modifying the fixture.

### 5. Standings Calculation

**Topics explored:**
- Iterating through lists of dictionaries.
- Calculating statistics.
- Sorting with lambda functions.
- Sorting using multiple criteria.

**What I learned:**

Standings should be derived from played fixtures rather than stored separately.

The `sort()` method can accept a key function that defines ranking priorities.

A tuple can be used to apply multiple sorting conditions.

### 6. JSON Storage

**Topics explored:**
- The `json` module.
- Reading and writing files.
- JSON decoding errors.
- Data validation.
- Exception handling.
- Preserving application state.

**What I learned:**

Valid JSON does not necessarily mean valid application data.

A JSON file can be syntactically correct while containing invalid team IDs, fixture references, scores, or statuses.

The application must validate loaded information before updating its working data.

### 7. Automated Testing

**Topics explored:**
- The `unittest` framework.
- Test classes and test methods.
- `setUp()` and `tearDown()`.
- Mocking with `unittest.mock.patch`.
- Testing functions with different inputs.
- Testing expected failures.
- Capturing printed output.

**What I learned:**

Tests help identify problems that may not be obvious during manual testing.

I learned to use mocks to prevent functions such as `save_tournament()` from modifying the actual JSON file during tests.

I also learned that a test failure does not always mean the application code is incorrect. Sometimes the problem is in the test itself.

### 8. Testing and Debugging Results

**Milestone:** 48 automated tests passed.

The tests covered:

- Team registration.
- Fixture generation.
- Result recording.
- Standings calculation.
- JSON storage and validation.

Several issues were discovered and corrected during testing.

Examples included:
- Rejecting Boolean and floating-point values as scores.
- Preventing partial fixture updates when the away score is invalid.
- Validating fixture IDs before converting their numeric portions.
- Correcting a misspelled variable in a test.

**What I learned:**

Testing is not just about confirming that code works.

It also helps reveal weaknesses in application logic and encourages safer programming practices.

---

## AI Usage Principles

During development, AI assistance followed these principles:

1. Understand the problem before implementing a solution.
2. Ask for explanations of unfamiliar Python concepts.
3. Review suggested code rather than accepting it blindly.
4. Test changes before considering them complete.
5. Understand why a particular solution works.
6. Keep the application independent of AI services.

---

## Future Learning Goals

The following areas will receive further attention:

- Strengthening JSON validation tests.
- Testing the tournament simulation module.
- Testing the main application flow.
- Improving integration testing.
- Reviewing the overall project architecture.
- Improving error handling and edge-case coverage.

---

## Final Reflection

TournamentLab provides an opportunity to apply Python concepts to a practical software development project.

The development process focuses not only on writing working code but also on understanding program behaviour, validating data, handling errors, organising modules, and writing automated tests.

AI assistance supports the learning process by providing explanations, feedback, and testing guidance while keeping the development and understanding of the project as the primary responsibility of the developer.