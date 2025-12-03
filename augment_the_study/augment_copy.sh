#!/bin/bash

# Loop over all test case files
for file in test_cases/*; do
    echo "Running $file..."

    # GNU date required for ms timing (macOS)
    start_time=$(gdate +%s%3N)
    
    echo ">>> Running 1-tree lower bound"
    python3 augment.py < "$file"
    
    echo ">>> Running approximation solver"
    python3 ../approx_solution/cs412_tsp_approx.py < "$file"

    end_time=$(gdate +%s%3N)

    elapsed_time=$((end_time - start_time))

    echo "Complete in ${elapsed_time} ms"
    echo "----------------------------"
done
