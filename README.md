<div align="center">

# Advent of Code 2019

### Python solutions to the 2019 Advent of Code puzzles

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-000000?style=for-the-badge&logo=python&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logoColor=white)
[![Repo](https://img.shields.io/badge/GitHub-jackinf%2Faoc2019-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/jackinf/aoc2019)

</div>

## Overview

This repository contains my solutions to [Advent of Code 2019](https://adventofcode.com/2019), a yearly set of programming puzzles released daily through December. Each day's puzzle is solved in Python and kept in its own directory alongside the puzzle input. Several days build on a shared [Intcode](https://adventofcode.com/2019/day/5) virtual machine, the recurring computer that powers many of the 2019 challenges.

## Features

- Per-day solutions organized into `dayNN/` folders, each with its own `input.txt` and one or more solution scripts (`part1.py`, `part2.py`, or `solution.py`).
- A reusable Intcode interpreter in `shared/Intcode.py` supporting positional, immediate, and relative addressing modes, used across multiple days (e.g. days 5, 7, 9, 11, 13).
- Visualization-friendly puzzles use `pygame`, `numpy`, and `matplotlib`.
- Test-case fixtures (e.g. `test-case-*.txt`) included for days with worked examples.

## Tech Stack

| Area | Tools |
| --- | --- |
| Language | Python 3 |
| Numerics | NumPy |
| Visualization | Pygame, Matplotlib |
| Graphs | dijkstar |

## Getting Started

### Prerequisites

- Python 3
- `pip` for installing dependencies

### Installation

```bash
git clone https://github.com/jackinf/aoc2019.git
cd aoc2019
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running

Solutions are standalone scripts. Most days read their input from a local `test-case-*.txt` or `input.txt` file, so run them from the repository root so shared imports resolve:

```bash
# Run a single-file day
python day01/part1.py
python day01/part2.py

# Run a day that uses the shared Intcode VM (run as a module from the repo root)
python -m day05.solution
```

> Note: file layout varies slightly between days — some use `part1.py`/`part2.py`, others a single `solution.py`. Check the relevant `dayNN/` directory for the entry point.

## Project Structure

```
aoc2019/
├── day01/ … day24/    # one directory per puzzle day (inputs + solutions)
├── shared/
│   └── Intcode.py      # shared Intcode virtual machine
└── requirements.txt    # Python dependencies
```
