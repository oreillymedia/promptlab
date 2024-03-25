#!/bin/zsh


# Check if exactly three arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <block_total> <starting_block> <course_name_with_underscores>"
    exit 1
fi


# total number of blocks
block_total=$1
# starting block number
starting_block=$2
# course name with underscores (no spaces)
course_name=$3
# make course folder
mkdir -p "$course_name"


# get learning objectives and quizzes for all segments
for (( i=$starting_block; i<=$block_total; ++i))
do
    segment_name=$(python3 main.py dump-blocks --block_id=$i | sed -nE 's/^(#|##)\s*//p')
    # get LOs for each block
    python3 main.py prompt --block_id=$i  --msg="$segment_name lo" --prompt=prompts/block-learning-objective.jinja
    
    
    # output objectives and quizzing for each segment
    echo "$i - $segment_name" >> "$course_name"/"$i - $segment_name".txt
    python3 main.py dump-prompts --block_id=$i --tag="*$segment_name lo*" >> "$course_name"/"$i - $segment_name".txt
    echo "===" >> "$course_name"/"$i - $segment_name".txt
    python3 main.py dump-blocks --block_id=$i >> "$course_name"/"$i - $segment_name".txt
    echo "===" >> "$course_name"/"$i - $segment_name".txt
    
done

# get all files from directory
target_directory="${course_name%/}/"
files=("${(@f)$(find "$target_directory" -maxdepth 1 -type f | sort -rV)}")


# load files into promptlab
python3 main.py load --fn="$course_name/*.txt"

# iterate over all files
for file in "${files[@]}"; do
    filename_without_extension=$(basename "$file" .txt)
    echo "$filename_without_extension"
    # get quizzing for all segments
    python3 main.py prompt --tag="*$filename_without_extension*" --msg="$filename_without_extension quiz" --prompt=prompts/generate-questions-plaintext-1.jinja
    python3 main.py prompt --tag="*$filename_without_extension*" --msg="$filename_without_extension quiz" --prompt=prompts/generate-questions-plaintext-2.jinja

    python3 main.py dump-prompts --tag="*$filename_without_extension quiz*" >> "$course_name"/"$filename_without_extension".txt
    file_path=$file
    cp "$file_path" "$file_path.bak"
    sed '/===/,/===/d' "$file_path.bak" > "$file_path"
done
