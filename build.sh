#!bin/bash

#build executable
echo "Building..."

if [ ! -d "bin" ]; then
    mkdir bin
else
	rm bin/*
fi
g++ -g -O0 -I . -o bin/interrupts interrupts.cpp
echo "build finished!" 

#call executable with proper files
echo "executing..."
./bin/interrupts trace.txt device_table.txt vector_table.txt
echo "execution complete!"

#print results to console
echo "results:"
cat ./execution.txt

python analyze_result.py execution.txt