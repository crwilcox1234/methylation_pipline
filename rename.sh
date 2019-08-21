while read line
do
  mv "$line"_S*_R1.fastq.gz "$line"_R1.fastq.gz
done < R1_list
