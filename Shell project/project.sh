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
rcv_packets=$( grep 'Networks:' "$1" | tr -s '/' ':' | cut -d: -f5 | sort -n)
sum=0
count=0

# it calculates the average CPU usage by adding all the values and dividing by the number of values
for sent in $sent_packets; do
  sum=$(awk "BEGIN{printf \"%f\", $sum + $sent}")
  count=$((count + 1))
done
average=$(awk "BEGIN{printf \"%.2f\", $sum / $count}")

# it prints the average, minimum, and maximum sent packets
echo "Average received packets: $average"
echo "Minimum received packets:$(echo "$sent_packets" | head -n 1)"
echo "Maximum received packets:$(echo "$sent_packets" | tail -n 1)"
echo "$sent_packets"

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
        echo "File does not exist"
      fi
      ;;

  c) cpu_usage_info "$filename";;

  i) rcv_packets_info "$filename";;
  o) sent_packets_info "$filename";;
  u);;
  a);;
  b);;
  e) exit 0;;
  *) echo "Please enter one of the choices only!!!";;
esac
done
exit 0
