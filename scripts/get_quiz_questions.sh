#!/bin/bash

run_quiz(){
    local block_id=$1
    local module_file=$2

    python3 main.py load --fn=$module_file
    python3 main.py prompt --prompt=prompts/generate-questions.jinja 

    echo QUIZ  >> $module_file
    echo ===============  >> $module_file
    python3 main.py dump-prompts --block_id=$block_id >> $module_file
}

run_quiz 1740 "ckad_video_course/mod1_container_fundamentals.txt"
run_quiz 1741 "ckad_video_course/mod2_pod_namespaces.txt"
run_quiz 1742 "ckad_video_course/mod3_jobs_cronjobs.txt"
run_quiz 1743 "ckad_video_course/mod4_volumes.txt"
run_quiz 1744 "ckad_video_course/mod5_multicontainer_pods.txt"
run_quiz 1745 "ckad_video_course/mod6_labels_annotations.txt"

echo Finished Quizzes