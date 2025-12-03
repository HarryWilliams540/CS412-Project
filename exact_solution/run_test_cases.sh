for file in $(ls test_cases | sort -V); do
    file="test_cases/$file"
    filename=$(basename "$file")

    echo "Running $filename..."

    input_size=$(head -n 1 "$file" | awk '{print $1}')

    start_time=$(date +%s%3N)
    python3 cs412_tsp_exact.py < "$file" > /dev/null
    end_time=$(date +%s%3N)

    elapsed_time=$((end_time - start_time))

    echo "Complete in $elapsed_time ms"
    echo "----------------------------"

    echo "$filename,$input_size,$elapsed_time" >> tsp_runtime_results.csv
done
