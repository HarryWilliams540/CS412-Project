# John Henry Adams
# 11/18/2025

#!/bin/bash

OUTPUT_FILE="tsp_runtime_results.csv"

# Write CSV header
echo "test_case,input_size,runtime_ms" > "$OUTPUT_FILE"

# Sort files numerically (case_1, case_2, ..., case_20)
for filename in $(ls test_cases | sort -V); do
    file="tsp_test_cases/$filename"

    echo "Running $file..."

    # Extract input size (first number in file)
    input_size=$(head -n 1 "$file" | awk '{print $1}')

    start_time=$(date +%s%3N)
    python3 cs412_tsp_exact.py < "$file" > /dev/null
    end_time=$(date +%s%3N)

    elapsed_time=$((end_time - start_time))

    echo "Complete in $elapsed_time ms"
    echo "----------------------------"

    # Append to CSV
    echo "$filename,$input_size,$elapsed_time" >> "$OUTPUT_FILE"
done

echo "Results saved to $OUTPUT_FILE"
