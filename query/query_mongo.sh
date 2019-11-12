#!/bin/bash

start=$(date +%s%N)
time_couter=0
x=1
number_repeat=10


function execute_mongo
{
  echo "db.btlhqt.find().limit($1)" | mongo data
}

while [ $x -le $number_repeat ]
do
  current=$(date +%s%N)
  echo "========================================== $x times"
  execute_mongo $number_limit
  time_loop=$((($(date +%s%N) - $current)/1000000))
  echo "Current loop time: $time_loop"
  x=$(( $x + 1 ))
done

end=$((($(date +%s%N) - $start)/1000000))
echo "total loop time: $end"
echo "Avg time: $(($end/$number_repeat))"