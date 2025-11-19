# John Henry Adams
# 11/18/2025

#!/bin/bash
for file in ../test_cases/*; do
    echo "Running $file..."

    start_time=$(date +%s%3N)

    python3 cs412_tsp_exact.py < "$file"

    end_time=$(date +%s%3N)

    elapsed_time=$((end_time - start_time))
    
    echo "Complete in $elapsed_time ms"
    echo "----------------------------"
done