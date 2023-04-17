#!/bin/bash

DATASET_DIR="Engagement/FaceEngageDataset"
file_count=$(find $DATASET_DIR -name "*.mp4" -type f | wc -l)
counter=0

find Engagement -name "*.mp4" -type f | while read file; do
  counter=$(($counter + 1))
  perc=$((counter * 100 / file_count))
  echo "Processing file $counter of $file_count [$perc%]: $file"
  python process_video.py "$file"
  if [ $? -ne 0 ]; then
    echo "Error processing file: $file"
    continue
  fi
done
