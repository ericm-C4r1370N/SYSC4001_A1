# SYSC4001_A1


# Contents:
  - trace.txt: program execution trace
  - device_table.txt: table of hardcoded IO times for corresponding device #'s
  - vector_table.txt: table of memory addressses containing ISR locations for each IO device.
  - analyze_result.py: matplotlib script to plot gantt chart

# Supported Platforms:
  - x86-64 based Linux

# Build dependencies:
  - gcc/g++ 

# Result analysis dependencies:
  - python3+
  - matplotlib

# Usage (scripted):
  - clone repo
  - cd into repo
  - run "source build.sh"
  - program will be compiled to ./bin/interrupts 
  - program will execute and output to ./execution.txt
  - python script will run on execution.txt and display results in a gantt chart of simulation results

# Usage (manual):
  - clone repo
  - cd into repo
  - compile interrupts.cpp with interrupts.hpp using your preferred compiler
  - run compiled binary
  - optional: interpret results with additional program 
