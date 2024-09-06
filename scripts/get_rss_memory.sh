#!/bin/bash

# Usage: call the script in HGCTPGValidation/scripts/produceData_multiconfiguration.py immediately after cmsRun
# get_rss_memory.sh $! interval limit
# 1rst argument: "$!" is the PID of python produceData_multiconfiguration.py process
# 2nd argument: interval in seconds
# 3th argument: memory limit

echo "Starts ger_rss_memory.sh script!"

# Check if the PID of the last process is provided
if [ -z "$1" ]; then
    echo "Usage: $0 PID INTERVALL RSS_LIMIT"
    exit 1
fi

# Check if the limit RSS is provided
if [ -z "$2" ]; then
    echo "Usage: $0 PID INTERVALL RSS_LIMIT"
    exit 1
fi

# Check if the Interval (in s) is provided
if [ -z "$3" ]; then
    echo "Usage: $0 PID INTERVALL RSS_LIMIT"
    exit 1
fi

# Get the PID of the process
INTERVAL=$2
RSS_limit=$3

# Wait the process cmsRun starts running
sleep 20

while true; do
    echo "LastProcess PID= " $1
    
    ps
    
    # Get PID for the process "cmsRun" and the user "jenkins"
    p_all=$(ps -eo pid,user,comm | grep cmsRun | grep jenkins | awk '{print}')
    echo "=== > Information about the process (PID user name_process): " $p_all
    
    PID=$(ps -eo pid,user,comm | grep cmsRun | grep jenkins | awk '{print $1}')
    echo "PID=" $PID
    
    if [ -z "$PID" ] || [ ! -e /proc/$PID/status ] ; then
        echo "Process $PID not found."
        exit 1;
    else
        # Get the RSS (Resident Set Size) memory usage
        RSS=$(grep -i vmrss /proc/$PID/status | awk '{print $2}')
        echo "Free memory (RSS) for process PID=$PID: ${RSS} kB"
        
        if [ "${RSS}" -gt "${RSS_limit}" ]; then
            echo "===> RSS memory ${RSS} > RSS limit ${RSS_limit}";
            kill -9 $PID;
            exit 1;
        fi
        
    fi
    
    sleep $INTERVAL
done
