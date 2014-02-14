#!/bin/bash -eu

dir=$HOME/shared
success=$HOME/backup/SUCCESS
pidfile=$HOME/backup/pid
upload=$HOME/scratch/backup/upload.py

# Check if backup is already running
if [ -f $pidfile ]; then
    pid=$(cat $pidfile)
    if kill -0 $pid >/dev/null 2>&1; then
	exit 0
    fi
fi

echo $$ > $pidfile

cd $dir
files=$(find . -newer $success -type f -printf "%p\t%k\n")
if [ -z "$files" ]; then
    exit 0
fi

size=$(echo "${files}" \
    | awk -F"	" 'BEGIN { sum=0 } { sum+=$2 } END { print sum }')
size=$(( $size/1024 ))

part=1
while (( $size/$part > 10000 )); do
    part=$(( $part*2 ))
done

echo "Backing up ${size}M of modified files in ${part}M chunks..."
echo "${files}" | awk -F"	" '{print $1}' | tar vc -T - | xz -9 \
    | $upload backup $part "backup $(date)"

touch $success
