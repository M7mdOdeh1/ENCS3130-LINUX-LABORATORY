# Function to check if a file exists
read_file() {
    echo "Please input the name of the file:"
    read filename

    if [ -f "$filename" ]
    then
        echo "File exists"
        while true
        do
            echo "Do you want to print the file content? (yes/no)"
            read answer
            if [ "$answer" = "yes" ]
            then
                cat "$filename"
                return 0
            elif [ "$answer" = "no" ]
            then
                return 0
            else
                echo "Invalid response, please answer with 'yes' or 'no'."
            fi
        done
    else
        echo "File does not exist"
        return 1
    fi
}
# Function to calculate CPU usage stats
calculate_cpu_usage() {
    if ! read_file; then
        return
    fi

    total=0
    count=0
    max=-1
    min=101

    while IFS= read -r line
    do
        if [[ $line == "CPU usage" ]]; then
            cpu=$(echo $line | awk -F ' ' '{print $3}' | tr -d '%')
            total=$(echo "$total + $cpu" | bc)
            ((count++))

            if (( $(echo "$cpu > $max" | bc -l) )); then
                max=$cpu
            fi
            if (( $(echo "$cpu < $min" | bc -l) )); then
                min=$cpu
            fi
        fi
    done < "$filename"

    if ((count > 0)); then
        average=$(echo "scale=2; $total / $count" | bc)
        echo "Average CPU usage: $average%"
        echo "Maximum CPU usage: $max%"
        echo "Minimum CPU usage: $min%"
    else
        echo "No CPU usage data found in the file."
    fi
}
# Function to calculate received packets stats
calculate_received_packets() {
    if ! read_file; then
        return
    fi

    total=0
    count=0
    max=-1
    min=-1

    while IFS= read -r line
    do
        if [[ $line == "Networks: packets:" ]]; then
            packets_in=$(echo "$line" | awk -F 'packets:|/' '{print $2}' | awk '{print $1}')
            if [[ -n $packets_in && $packets_in =~ ^[0-9]+$ ]]; then
                total=$((total + packets_in))
                ((count++))

                if ((packets_in > max)); then
                    max=$packets_in
                fi
                if ((min == -1)) || ((packets_in < min)); then
                    min=$packets_in
                fi
            fi
        fi
    done < "$filename"

    if ((count > 0)); then
        average=$((total / count))
        echo "Average received packets: $average"
        echo "Maximum received packets: $max"
        echo "Minimum received packets: $min"
    else
        echo "No received packets data found in the file."
    fi
}


calculate_sent_packets() {
    if ! read_file; then
        return
    fi
    sent_packets=$(grep 'Networks:' "$filename" | awk -F'[/ ]' '{print $6}' | sort -n)

    sum=0
    count=0
    for sent in $sent_packets; do
        sum=$((sum + sent))
        count=$((count + 1))
    done
    average=$(printf "%.2f" $(echo "scale=2; $sum / $count" | bc))
    minimum=$(echo "$sent_packets" | awk 'NR==1')
    maximum=$(echo "$sent_packets" | awk 'END{print}')

    echo "Average sent packets: $average"
    echo "Minimum sent packets: $minimum"
    echo "Maximum sent packets: $maximum"
}

calculate_max_avg_cpu_commands() {
    echo "Please input an integer number:"
    read m

    # check if the input is an integer
    if ! [[ "$m" =~ ^[0-9]+$ ]]
    then
        echo "Error: Input is not an integer."
        return
    fi

    # check if the file exists and can be read
    if ! read_file; then
        return
    fi

    declare -A cpu_usage_counts
    declare -A cpu_usage_totals

    while IFS= read -r line
    do
        # assuming that command is in the 12th field and CPU% is in the 9th field in 'top' output
        command=$(echo $line | awk '{print $12}')
        cpu=$(echo $line | awk '{print $9}' | tr -d '%')

        if [[ -n $command && $cpu =~ ^[0-9\.]+$ ]]
        then
            cpu_usage_totals[$command]=$(echo "${cpu_usage_totals[$command]:-0} + $cpu" | bc)
            cpu_usage_counts[$command]=$((cpu_usage_counts[$command] + 1))
        fi
    done < "$filename"

    # calculate average CPU usage for each command and sort
    results=()
    for command in "${!cpu_usage_counts[@]}"
    do
        average_cpu=$(echo "scale=2; ${cpu_usage_totals[$command]} / ${cpu_usage_counts[$command]}" | bc)
        results+=("$average_cpu $command")
    done

    IFS=$'\n' results=($(sort -rn <<<"${results[*]}")) unset IFS

    # print the top m commands with the highest average CPU usage
    for ((i=0; i<m && i<${#results[@]}; i++))
    do
        echo "${results[$i]}"
    done
}
calculate_max_avg_mem_commands() {
    echo "Please input an integer number:"
    read m

    # check if the input is an integer
    if ! [[ "$m" =~ ^[0-9]+$ ]]
    then
        echo "Error: Input is not an integer."
        return
    fi

    # check if the file exists and can be read
    if ! read_file; then
        return
    fi

    declare -A mem_usage_counts
    declare -A mem_usage_totals

    while IFS= read -r line
    do
        # assuming that command is in the 12th field and MEM% is in the 10th field in 'top' output
        command=$(echo $line | awk '{print $12}')
        mem=$(echo $line | awk '{print $10}' | tr -d '%')

        if [[ -n $command && $mem =~ ^[0-9\.]+$ ]]
        then
            mem_usage_totals[$command]=$(echo "${mem_usage_totals[$command]:-0} + $mem" | bc)
            mem_usage_counts[$command]=$((mem_usage_counts[$command] + 1))
        fi
    done < "$filename"

    # calculate average MEM usage for each command and sort
    results=()
    for command in "${!mem_usage_counts[@]}"
    do
        average_mem=$(echo "scale=2; ${mem_usage_totals[$command]} / ${mem_usage_counts[$command]}" | bc)
        results+=("$average_mem $command")
    done

    IFS=$'\n' results=($(sort -rn <<<"${results[*]}")) unset IFS

    # print the top m commands with the highest average MEM usage
    for ((i=0; i<m && i<${#results[@]}; i++))
    do
        echo "${results[$i]}"
    done
}
calculate_min_avg_mem_commands() {
    echo "Please input an integer number:"
    read m

    # check if the input is an integer
    if ! [[ "$m" =~ ^[0-9]+$ ]]
    then
        echo "Error: Input is not an integer."
        return
    fi

    # check if the file exists and can be read
    if ! read_file; then
        return
    fi

    declare -A mem_usage_counts
    declare -A mem_usage_totals

    while IFS= read -r line
    do
        # assuming that command is in the 12th field and MEM% is in the 10th field in 'top' output
        command=$(echo $line | awk '{print $12}')
        mem=$(echo $line | awk '{print $10}' | tr -d '%')

        if [[ -n $command && $mem =~ ^[0-9\.]+$ ]]
        then
            mem_usage_totals[$command]=$(echo "${mem_usage_totals[$command]:-0} + $mem" | bc)
            mem_usage_counts[$command]=$((mem_usage_counts[$command] + 1))
        fi
    done < "$filename"

    # calculate average MEM usage for each command and sort
    results=()
    for command in "${!mem_usage_counts[@]}"
    do
        average_mem=$(echo "scale=2; ${mem_usage_totals[$command]} / ${mem_usage_counts[$command]}" | bc)
        results+=("$average_mem $command")
    done

    IFS=$'\n' results=($(sort -n <<<"${results[*]}")) unset IFS

    # print the top m commands with the lowest average MEM usage
    for ((i=0; i<m && i<${#results[@]}; i++))
    do
        echo "${results[$i]}"
    done
}
# Main menu loop
while true
do
    echo "Select an option to run the top statistics project:"
    echo "r) read top output file"
    echo "c) average, minimum, and maximum CPU usage"
    echo "i) average, minimum, and maximum received packets"
    echo "o) average, minimum, and maximum sent packets"
    echo "u) commands with the maximum average CPU"
    echo "a) commands with the maximum average memory usage"
    echo "b) commands with the minimum average memory usage"
    echo "e) exit"
    
    read option

    case "$option" in
        r) read_file ;;
        c) calculate_cpu_usage ;;
        i) calculate_received_packets ;;
        o) calculate_sent_packets ;;
        u) calculate_max_avg_cpu_commands ;;
        a) calculate_max_avg_mem_commands ;;
        b) calculate_min_avg_mem_commands ;;
        e) 
            echo "Are you sure you want to exit? (yes/no)"
            read confirm_exit
            if [ "$confirm_exit" == "yes" ]; then
                exit 0
            fi
            ;;
        *) echo "Invalid option. Please select a valid one." ;;
    esac
done