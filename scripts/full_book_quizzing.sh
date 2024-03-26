#!/bin/zsh

# Check if exactly two arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <chapters> <number_of_blocks> <starting_block> <epub_file_name>"
    exit 1
fi

# total number of chapters
chapters=$1

#total number of blocks
blocks=$2

#starting block
starting_block=$3
((block_stop=blocks + starting_block))
# file name for epub
book_file=$4
book_filename_without_extension="${book_file%.*}"

# make directory for output files
mkdir -p "$book_filename_without_extension"
mkdir -p "$book_filename_without_extension/output_files"

# get learning objectives and quiz questions for all chapters
for ((i=$starting_block; i<=$block_stop; ++i))
do
    block_tag=$(python3 main.py dump-block-tag --block_id=$i)
    if [[ $block_tag =~ ^ch[0-9]{2} ]]; then
        block_tag_without_extension="${block_tag%.*}"
        directory="$book_filename_without_extension"
        counter=1
        file_path="$directory/$block_tag_without_extension"
        #prompt for lo
        python3 main.py prompt --block_id=$i --msg="$block_tag_without_extension lo" --prompt=prompts/block-learning-objective.jinja
        # check if file exists and add suffix if necessary
        while [[ -e "$file_path" ]]; do
            file_path="${directory}/$block_tag_without_extension-${counter}"
            ((counter++))
        done
        python3 main.py dump-prompts --block_id=$i >> $file_path.txt
        python3 main.py dump-blocks --block_id=$i >> $file_path.txt
    fi
done

for ((i=1; i<=$chapters; ++i))
do
    A=$i
    A=$( printf '%02d' $A )

    python3 main.py dump-prompts --tag="*ch$A lo*" >> "$book_filename_without_extension"/output_files/ch$A\_objectives.txt
done


# get all files from directory
target_directory="${book_filename_without_extension%/}/"
files=("${(@f)$(find "$target_directory" -maxdepth 1 -type f | sort -rV)}")


# load files into promptlab
python3 main.py load --fn="$book_filename_without_extension/*.txt"


for file in "${files[@]}"; do
    filename_without_extension=$(basename "$file" .txt)
    first_four="${filename_without_extension:0:4}"
    echo "$first_four"
    # get quizzing for all segments
    python3 main.py prompt --tag="*$first_four*" --msg="$first_four quiz" --prompt=prompts/generate-questions-plaintext-2.jinja

    python3 main.py dump-prompts --tag="*$first_four quiz*" >> "$book_filename_without_extension"/output_files/$first_four\_quiz".txt
done





# for (( i=1; i<=chapters; ++i))
# do
#     A=$i
#     A=$( printf '%02d' $A )
#     base_name="ch$A.txt"
#     directory="$book_filename_without_extension"
#     counter=1
#     file_path="$directory/$base_name"
#     # check if file exists and add suffix if necessary
#     while [[ -e "$file_path" ]]; do
#         file_path="${directory}/ch${A}-${counter}.txt"
#         ((counter++))
#     done
#     # learning objectives for each chapter
#     python3 main.py prompt --tag="ch$A.html" --msg="ch$A lo" --prompt=prompts/block-learning-objective.jinja

#     # generate questions for each chapter
#     python3 main.py prompt --tag="ch$A.html" --msg="ch$A quiz" --prompt=prompts/generate-questions-plaintext-1.jinja
#     python3 main.py prompt --tag="ch$A.html" --msg="ch$A quiz" --prompt=prompts/generate-questions-plaintext-2.jinja

#     # output quiz questions to files for each chapter
#     python3 main.py dump-prompts --tag="*ch$A lo*" >> "$book_filename_without_extension"/ch$A.txt
#     python3 main.py dump-prompts --tag="*ch$A quiz*" >> "$book_filename_without_extension"/ch$A.txt
# done

# # get all files from directory
# target_directory="${book_filename_without_extension%/}/"
# files=("${(@f)$(find "$target_directory" -maxdepth 1 -type f | sort -rV)}")

# # iterate over all files
# for file in "${files[@]}"; do
#     filename_without_extension=$(basename "$file" .txt)
#     echo "$filename_without_extension"
#     # get quizzing for all segments
#     python3 main.py prompt --tag="*$filename_without_extension*" --msg="$filename_without_extension quiz" --prompt=prompts/generate-questions-plaintext-1.jinja
#     python3 main.py prompt --tag="*$filename_without_extension*" --msg="$filename_without_extension quiz" --prompt=prompts/generate-questions-plaintext-2.jinja

#     python3 main.py dump-prompts --tag="*$filename_without_extension quiz*" >> "$book_filename_without_extension"/"$filename_without_extension".txt
#     file_path=$file
#     cp "$file_path" "$file_path.bak"
#     sed '/===/,/===/d' "$file_path.bak" > "$file_path"
# done






# block_total=$1
# starting_block=$2
