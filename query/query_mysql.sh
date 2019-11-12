#!/bin/bash

start=$(date +%s%N)
time_couter=0
x=1
# number_repeat=100


function execute_mysql
{
  #query
}

while [ $x -le $number_repeat ]
do
  current=$(date +%s%N)
  echo "========================================== $x times"
  execute_mysql
  time_loop=$((($(date +%s%N) - $current)/1000000))
  echo "Current loop time: $time_loop"
  x=$(( $x + 1 ))
done

end=$((($(date +%s%N) - $start)/1000000))
echo "total loop time: $end"
avg_time=$(($end/$number_repeat))
echo "Avg time: $avg_time"
echo "$number_repeat times, limit: $number_limit,avg time: $avg_time" >> mysql_logs.txt