#!/bin/bash

# This script is called in HGCTPGValidation/scripts/produceData_multiconfiguration.py immediately after running cmsDriver.py
# It checks periodically the rss memory of the cmsRun process, if the memory becomes greater than a given limit value, the cmsRun process is killed
# Usage: 
# get_rss_memory.sh $! interval limit
# 1rst argument: "$!" is the PID of python produceData_multiconfiguration.py process
# 2nd argument: interval in seconds
# 3th argument: memory limit

DEBUG=1

# Check if the PID of the last process is provided
if [ -z "$1" ]; then
    echo "Usage: $0 PID INTERVAL RSS_LIMIT"
    exit 1
fi

# Check if the Interval (in s) is provided
if [ -z "$2" ]; then
    echo "Usage: $0 PID INTERVAL RSS_LIMIT"
    exit 1
fi

# Check if the limit RSS is provided
if [ -z "$3" ]; then
    echo "Usage: $0 PID INTERVAL RSS_LIMIT"
    exit 1
fi

# Get the PID of the process
INTERVAL=$2
RSS_limit=$3

# Wait the process cmsRun starts running
sleep 20

# Get PID for the process "cmsRun" and the user "jenkins"
p_all=$(ps -eo pid,user,comm | grep cmsRun | grep jenkins | awk '{print}')
PID=$(ps -eo pid,user,comm | grep cmsRun | grep jenkins | awk '{print $1}')

if [ "$DEBUG" = "1" ] ; then
    echo "LastProcess PID= " $1
    ps
    echo "=== > Information about the process (PID user name_process): " $p_all
    echo "PID=" $PID
fi
    
if [ -z "$PID" ] ; then
    echo "Process $PID not found!" 1>&2 &&
    exit 1;
fi
    
while true; do
    
    if [ ! -e /proc/$PID/status ] ; then
        echo "Process $PID already finished!"
        break;
    else
        # Get the RSS (Resident Set Size) memory usage
        RSS=$(grep -i vmrss /proc/$PID/status | awk '{print $2}')
        if [ "$DEBUG" = "1" ] ; then
            echo "Free memory (RSS) for process PID=$PID: $(( ${RSS} / 1000 )) MB"
        fi
        
        if [ "${RSS}" -gt "${RSS_limit}" ]; then
            echo "===> RSS memory $(( ${RSS} / 1000 )) MB > RSS limit $(( ${RSS_limit} / 1000 )) MB"  1>&2 &&
            kill -9 $PID &&
            exit 1;
        fi  
    fi    
    sleep $INTERVAL
done
