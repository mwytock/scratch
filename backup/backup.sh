#!/bin/bash -eu

dir=$HOME/shared
success=$HOME/backup/SUCCESS
upload=$HOME/scratch/backup/upload.py

desc="Backup archive from $(date)"

cd $dir
files=$(find . -newer $success -type f)

if [ -z "$files" ]; then
    exit 1
fi

echo "Backing up modified files"
echo "${files}"

echo "${files}" | tar c -T - | xz -9 | $upload backup "$desc"
touch $success
