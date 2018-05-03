#!/bin/bash

#Configuration

nrOfNodes=$1
startPort=9000

counter=0
while [ $counter -le $((nrOfNodes-1)) ]
do
#Node port
    currentPort=$((startPort + counter))
    
    ttab python bully.py "127.0.0.1:$currentPort"
    ((counter++))
done

echo all nodes started