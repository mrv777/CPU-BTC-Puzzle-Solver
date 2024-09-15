# Bitcoin Puzzle Solver (Cython Version)

This project contains Python/Cython scripts that attempt to solve Bitcoin Puzzles by searching for private keys that generate specific Bitcoin addresses. It includes a CPU-based multiprocessing version optimized with Cython.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- A C compiler (e.g., GCC, Clang, or MSVC)

## Installation

1. Clone this repository or download the files:
   - `main.py`
   - `bitcoin_utils.pyx`
   - `setup.py`
   - `README.md`

2. Install the required Python packages:

   ```
   pip3 install -r requirements.txt
   ```

3. Build the Cython extension:

   ```
   python setup.py build_ext --inplace
   ```

## Usage

### CPU-based Solver

1. Open a terminal and navigate to the directory containing the script files.

2. Run the main script:

   ```
   python main.py --puzzle <puzzle_number> [--start <start_range>] [--end <end_range>]
   ```

   Example:
   ```
   python main.py --puzzle 67
   ```

3. The script will start running and display progress information:
   - Number of CPU cores being used
   - Total execution time and keys checked per second upon completion



```
python3 -m venv btcpuzzle1
source btcpuzzle1/bin/activate
pip3 install -r requirements.txt
```

## Benchmark

On an M1 Max Macbook Pro, does ~350K keys per second.

## Important Notes

- This script performs a computationally intensive task and may run for a very long time without finding a solution.
- Ensure your computer is well-ventilated and connected to a power source if you plan to run it for extended periods.
- The script is designed to utilize all available CPU cores, which may cause high CPU usage and increased power consumption.
- There is no guarantee that a solution will be found within the given range.

## Disclaimer

This script is for educational and research purposes only. Please use responsibly and ethically.

## Python Environment
```
python3 -m venv btcpuzzle1
source btcpuzzle1/bin/activate
pip3 install -r requirements.txt
```

## Benchmark

On an M1 Max Macbook Pro, this Cython version achieves approximately 280k keys per second.
Total execution time:
Puzzle 22: 3.5 seconds
Puzzle 24: 23 seconds
Puzzle 25: 49 seconds

## Important Notes

- This script performs a computationally intensive task and may run for a very long time without finding a solution.
- Ensure your computer is well-ventilated and connected to a power source if you plan to run it for extended periods.
- The script is designed to utilize all available CPU cores, which may cause high CPU usage and increased power consumption.
- There is no guarantee that a solution will be found within the given range.

## Files

- `main.py`: The main script that manages the multiprocessing and overall execution.
- `bitcoin_utils.pyx`: Cython file containing optimized utility functions for Bitcoin address generation.
- `setup.py`: Build script for compiling the Cython extension.
- `requirements.txt`: List of Python package dependencies.
- `README.md`: This file, containing instructions and information about the project.

## Disclaimer

This script is for educational and research purposes only. Please use responsibly and ethically.

