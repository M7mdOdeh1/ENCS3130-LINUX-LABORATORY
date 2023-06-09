# Function to check if a file exists
# return 0 if exist and 1 if not
file_exists() {
  if [ -e "$1" ]; then
    return 0
  else
    return 1
  fi
}

# extract_cpu_usage from the file
cpu_usage_info() {

# it gathers the CPU usage percentages, removes the '%' sign, extracts the numerical values, and sorts them in ascending order
cpuUsages=$( grep 'CPU usage' "$1" | tr -s '%' ':' | cut -d: -f2 | sort -n)
sum=0
count=0

# it calculates the average CPU usage by adding all the values and dividing by the number of values
for usage in $cpuUsages; do
  sum=$(awk "BEGIN{printf \"%f\", $sum + $usage}")
  count=$((count + 1))
done
average=$(awk "BEGIN{printf \"%.2f\", $sum / $count}")

# it prints the average, minimum, and maximum CPU usage
echo "Average CPU usage: $average%"
echo "Minimum CPU usage:$(echo "$cpuUsages" | head -n 1)%"
echo "Maximum CPU usage:$(echo "$cpuUsages" | tail -n 1)%"
#echo "$cpuUsages"

}

# extract received packets from the file
rcv_packets_info() {

# it gathers the packets received, removes the '/' sign, extracts the numerical values, and sorts them in ascending order
rcv_packets=$( grep 'Networks:' "$1" | tr -s '/' ':' | cut -d: -f3 | sort -n)
sum=0
count=0

# it calculates the average CPU usage by adding all the values and dividing by the number of values
for rcv in $rcv_packets; do
  sum=$(awk "BEGIN{printf \"%f\", $sum + $rcv}")
  count=$((count + 1))
done
average=$(awk "BEGIN{printf \"%.2f\", $sum / $count}")

# it prints the average, minimum, and maximum recieved packets
echo "Average received packets: $average"
echo "Minimum received packets:$(echo "$rcv_packets" | head -n 1)"
echo "Maximum received packets:$(echo "$rcv_packets" | tail -n 1)"
#echo "$rcv_packets"

}

# extract sent packets from the file
sent_packets_info() {

# it gathers the sent packets, removes the '/' sign, extracts the numerical values, and sorts them in ascending order
sent_packets=$( grep 'Networks:' "$1" | tr -s '/ ' ':' | cut -d: -f6 | sort -n)
sum=0
count=0

# it calculates the average CPU usage by adding all the values and dividing by the number of values
for sent in $sent_packets; do
  sum=$(awk "BEGIN{printf \"%f\", $sum + $sent}")
  count=$((count + 1))
done
average=$(awk "BEGIN{printf \"%.2f\", $sum / $count}")

# it prints the average, minimum, and maximum sent packets
echo "Average sent packets: $average"
echo "Minimum sent packets:$(echo "$sent_packets" | head -n 1)"
echo "Maximum sent packets:$(echo "$sent_packets" | tail -n 1)"
#echo "$sent_packets"
}

# function to extract all commands from the file
extract_commands() {
  read="false"
  pid_lines=""

  IFS=$'\n'  # setting IFS (Internal Field Separator) to a newline character

# Loop through the file line by line
# loop to extract the lines between the lines starting with "PID" and "Processes"
for line in $(cat "$1"); do

  if [[ $line == Processes* ]]; then    
    read="false"  # Stop reading when line starts with "Processes"
  fi

  if [[ $read == "true" ]]; then
    pid_lines+="$line"$'\n'  # Append the line to the variable
  fi

  if [[ $line == PID* ]]; then
    read="true" # Start reading when line starts with "PID"
  fi
  
done

}

# function to extract commands with the maximum average CPU and sort them in descending order and print the first m lines
commands_with_max_cpu() {
# extract the column with the CPU time
cpuColumn=$(echo "$pid_lines" | awk '{ for (i=1; i<=NF; i++) { if ($i ~ /^[0-9]+\.[0-9]+$/) { print $i; break } } }')
# print number of lines of cpuColumn

# add cpuColumn to the first column of pid_lines
pid_lines=$(paste <(echo "$cpuColumn") <(echo "$pid_lines"))

# sort the lines in descending order according to the CPU time
pid_lines=$(echo "$pid_lines" | sort -nrk1)

count=0
# print the first 3 columns of pid_lines (PID, USER, and COMMAND) and print the first column untill find an integer (CPU time)
pid_lines=$(echo "$pid_lines" | awk '{count=0; for (i=2; i<=NF; i++) { if ($i ~ /^[0-9]+(\.[0-9]+)?$/ && count < 2) { printf " %s  ", $i; count++ } else if (count == 2) { print ""; break } else{ printf "%s ", $i } } }')

# extract the first m lines
pid_lines=$(echo "$pid_lines" | head -n "$1")

echo " ---------------------------------"
echo " PID   Command          CPU Time"
echo " ---   -------          --------"
echo "$pid_lines"
echo " ---------------------------------"
}

# function to sort the commands in descending order according to the maximum memory usage
sort_command_memory() {
# extract the column with the memory usage


memoryColumn=$(echo "$pid_lines" | tr -d '/+-' | awk '{count=0; for (i=2; i<=NF; i++) { if ($i ~ /^[0-9]+[kKmMgGbB]?$/) { if (count < 3){ count++ } else { print $i; break} } } }')
# print number of lines of memoryColumn

# convert the memory usage to bytes
memoryColumn_bytes=$(echo "$memoryColumn" | awk '{ if ($1 ~ /[kK]$/) { printf "%d\n", $1 * 1024 } else if ($1 ~ /[mM]$/) { printf "%d\n", $1 * 1024 * 1024 } else if ($1 ~ /[gG]$/) { printf "%d\n", $1 * 1024 * 1024 * 1024 } else if ($1 ~ /[bB]$/) { printf "%d\n", $1 }}')
# add memoryColumn and memoryColumn_bytes to the first column of pid_lines
pid_lines=$(paste <(echo "$memoryColumn") <(echo "$pid_lines"))
pid_lines=$(paste <(echo "$memoryColumn_bytes") <(echo "$pid_lines"))

# add memoryColumn_bytes to the first column of memoryColumn_bytes
memoryColumn=$(paste <(echo "$memoryColumn") <(echo "$memoryColumn_bytes"))
#sort the lines in descending order according to the memory bytes
memoryColumn=$(echo "$memoryColumn" | sort -nrk2)

# sort the lines in descending order according to the memory usage
pid_lines=$(echo "$pid_lines" | sort -nrk1)


}

# function to print m lines of the commands with the maximum memory usage
print_commands_with_max_memory() {
count=0
# print the first 3 columns of pid_lines (PID, Command, and Memory) and print the first column untill find an integer 
pid_lines=$(echo "$pid_lines" | awk '{count=1; for (i=3; i<=NF; i++) { if ($i ~ /^[0-9]+(\.[0-9]+)?$/) { if (count < 2) {printf " %s  ", $i; count++} else if (count == 2){ printf " %s", 2; break } }   else{ printf "%s ", $i } } }')
# add only the first column of memoryColumn to the first column of pid_lines
pid_lines=$(paste <(echo "$pid_lines") <(echo "$memoryColumn"))

# extract the first m lines
pid_lines=$(echo "$pid_lines" | head -n "$1")

echo " ---------------------------------"
echo " PID   Command          Memory"
echo " ---   -------          ------"
echo "$pid_lines"
echo " ---------------------------------"
}

# funtion to print m lines of the commands with the minimum memory usage
print_commands_with_min_memory() {
count=0
# print the first 3 columns of pid_lines (PID, Command, and Memory) and print the first column untill find an integer
pid_lines=$(echo "$pid_lines" | awk '{count=1; for (i=3; i<=NF; i++) { if ($i ~ /^[0-9]+(\.[0-9]+)?$/) { if (count < 2) {printf " %s  ", $i; count++} else if (count == 2){ print ""; break } }   else{ printf "%s ", $i } } }')
pid_lines=$(paste <(echo "$pid_lines") <(echo "$memoryColumn"))
# extract the last m lines
pid_lines=$(echo "$pid_lines" | tail -n "$1")

echo " ---------------------------------"
echo " PID   Command          Memory"
echo " ---   -------          ------"
echo "$pid_lines"
echo " ---------------------------------"
}


read_integer() {
  read -p "Please enter an integer: " m
  while [[ ! $m =~ ^[0-9]+$ ]]; do
    echo "Invalid input"
    read -p "Please enter an integer: " m
  done
}
# start menu loop
while [ 1 ]
do
  echo "======================================================="
  echo "Select an option to run the top statistics project:"
  echo "r) read top output file"
  echo "c) average, minimum, and maximum CPU usage"
  echo "i) average, minimum, and maximum received packets"
  echo "o) average, minimum, and maximum sent packets"
  echo "u) commands with the maximum average CPU"
  echo "a) commands with the maximum average memory usage"
  echo "b) commands with the minimum average memory usage"
  echo "e) exit"
  echo "======================================================="

  read -p "Option: " option
  case "$option"
    in
    r)
        read -p "Please input the name of the file: " filename
        if file_exists "$filename" 
        then
          echo "File exists"
        else
          echo "File not found!!!"
        fi
        ;;

    c) # check if the filename exists
        if file_exists "$filename" 
        then
        cpu_usage_info "$filename"
        else
          echo "File not found!!!"
        fi
        ;;

    i)  # check if the filename exists
        if file_exists "$filename" 
        then
        rcv_packets_info "$filename"
        else
          echo "File not found!!!"
        fi
        ;;

    o)  # check if the filename exists
        if file_exists "$filename" 
        then
        sent_packets_info "$filename"
        else
          echo "File not found!!!"
        fi  
        ;;
    u) 

        # check if the filename exists
        if file_exists "$filename" 
        then
        read_integer       
        extract_commands "$filename"
        commands_with_max_cpu "$m"
        else
          echo "File not found!!!"
        fi

        ;;
    a) 
        # check if the filename exists
        if file_exists "$filename" 
        then
        read_integer
        extract_commands "$filename" 
        sort_command_memory
        print_commands_with_max_memory "$m"
        else
          echo "File not found!!!"
        fi
       
        ;;

    b)  # check if the filename exists
        if file_exists "$filename" 
        then
        read_integer
        extract_commands "$filename"
        sort_command_memory
        print_commands_with_min_memory "$m"
        else
          echo "File not found!!!"
        fi

        ;;
    e)  
        # ask the user if he really wants to exit
        read -p "Are you sure you want to exit? (yes/no): " exit_choice  
        while [[ ! $exit_choice =~ ^(yes|no)$ ]]; do
          echo "Invalid input"
          read -p "Are you sure you want to exit? (yes/no): " exit_choice
        done
        if [ "$exit_choice" == "yes" ]
        then
          echo "Exiting..."
          exit 0
        else
          echo "Returning to the main menu..."
        fi
        ;;
    *)  echo "Please enter one of the choices only!!!";;
  esac
done
exit 0
