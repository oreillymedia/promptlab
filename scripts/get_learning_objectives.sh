#!/bin/bash

run_module(){
    local block_id=$1
    local module_file=$2

    python3 main.py load --fn=$module_file
    python3 main.py prompt --prompt=prompts/block-learning-objective.jinja 

    echo LEARNING OBJECTIVE >> $module_file
    python3 main.py dump-prompts --block_id=$block_id >> $module_file
}

run_module 1736 "ckad_video_course/mod3_jobs_cronjobs.txt"
run_module 1737 "ckad_video_course/mod4_volumes.txt"
run_module 1738 "ckad_video_course/mod5_multicontainer_pods.txt"
run_module 1739 "ckad_video_course/mod6_labels_annotations.txt"

echo Finished Learning Objectives