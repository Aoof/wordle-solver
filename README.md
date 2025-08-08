# Wordle Solver

A command-line tool to help solve Wordle-style word puzzles by suggesting likely candidate words based on user feedback for each guess.

## Features

* Dynamically updates suggestions based on **green**, **yellow**, and **gray** letter feedback.
* Optionally fetches a live word list from [Meaningpedia](https://meaningpedia.com).
* Supports custom word lengths and attempt counts.
* Ranks suggestions by letter frequency for optimal guesses.

## Installation

Make sure you have **Python 3.6+** installed.

Clone the repository:

```bash
git clone https://github.com/aoof/wordle-solver.git
cd wordle-solver
```

Install required dependencies (only `requests` is needed for fetching the word list):

```bash
pip install requests
```

## Usage

```bash
python solver.py [--word-length N] [--attempts N] [--disable-fetch] [--suggestions-count N]
```

### Options

* `--word-length`: Number of letters in the target word (default: 5)
* `--attempts`: Number of attempts allowed (default: 6)
* `--disable-fetch`: Disables fetching a word list from the internet (uses random suggestions instead)
* `--suggestions-count`: Number of word suggestions to display at a time (default: 20)

### Example

```bash
python solver.py --word-length 5 --attempts 6
```

## How It Works

1. You enter your guessed word.
2. You provide:

   * **Green letters**: letters in the correct position.
   * **Yellow letters**: letters in the word but wrong position (repeat if they appear more than once).
3. The tool filters and ranks possible words.
4. Suggestions are displayed, and you can ask for more by confirming when prompted.

## Example Interaction

```
Round 1
Enter the first guessed word (5 letters): trace
Enter yellow letters (repeat if needed): a
Enter green letters: e

Calculating suggestions...
Do you want to see the suggestions? (y/N): y
  - eater
  - slate
  - table
  ...
```

## Notes

* Gray letters are inferred automatically based on green/yellow inputs.
* Word suggestions are sorted based on the frequency of letters in English.

## License

This project is licensed under the MIT License.
