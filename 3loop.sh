module load bedtools/2.19.1
while read line
do
    awk -F"\t" '{print$1"\t"$2"\t"$3}' "$line" > c_"$line"
    bedtools getfasta -fi /share/samdata/jiangs2/Dr_TZB/humanRRBS/hg38/hg38.fa -bed c_"$line" -fo c_"$line".fa
    awk -F"\t" '{print$1"\t"$3"\t"($3+1)}' "$line" > g_"$line"
    bedtools getfasta -fi /share/samdata/jiangs2/Dr_TZB/humanRRBS/hg38/hg38.fa -bed g_"$line" -fo g_"$line".fa
    rm c_"$line"
    rm g_"$line"
done < list_loop
