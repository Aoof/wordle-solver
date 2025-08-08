# Wordle Solver

A command-line tool to help solve Wordle-style word puzzles by suggesting likely candidate words based on user feedback for each guess.

> ### Author's remarks
> I created this tool because I found myself manually calculating the best guesses during Wordle games. So I thought why not automate it? I ended up spending about two hours building a simple algorithm that uses letter frequency data (sourced from [this chart](https://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html)) to provide solid suggestions.
>
> My manual process was about trying to use the most frequent letters in the first couple of guesses, so I wanted to preserve that strategy for the user. Instead of automating the whole thought process, I focused on removing the tedious parts, specifically, tracking which yellow letters don’t go where, and which green letters stay fixed.
>
> The script generates permutations of valid letters, keeping green letters locked in place and shifting yellow letters into new positions each time, ensuring all hints are respected. This way, you can concentrate on optimizing your next move rather than handling the repetitive logic.
>
> For fun, I also included an optional feature to fetch real word lists from the web, which is enabled by default. You can disable it using the `--disable-fetch` flag.

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
