# Sam-Analyzer-task
This is the final task for a bioINF course by AprendeCSIC platform. The main objective is to create a workflow in NextFlow which uses a Python script that reads and analyzes a 'sam' file, and calculating the percentage of the reads that has MAPQ = 60 among the total reads. 

First, the program checks if **uv** is installed, and, if not, **tries to install it**. 

This project uses the following **dependencies**:

  - Python 3.8
  - uv
  - rich
  - NextFlow 23
 
**Install and initialize the environment with uv**

$ curl -LsSf https://astral.sh/uv/install.sh | sh

$ uv init project-sam

$ uv add rich

**The command line should look like this:**

$ nextflow run sam_Analyzer.nf --sam /path/to/file.sam --script /path/to/main.py

The workflow generates two files: 
/work/resultado.txt   # Clean analysis output
/work/log.txt         # Warnings and stderr messages. 

**Test SAM File**

A small SAM file is included for testing, called "example.sam".
It contains:

- Valid reads
- Reads with MAPQ = 60
- Reads with MAPQ ≠ 60
- Corrupted lines
- Non-numeric MAPQ values

The program has 4 main files besides the example and README: 

- main.py. This is the Python script which checks uv and analyzes the sam file.
- pyproject.toml. This is the information for uv to use its dependencies.
- sam_Analyzer.nf. Script in NextFlow using the main.py.
- memoria_final_Task.odt. A document explaining the program for the course.

