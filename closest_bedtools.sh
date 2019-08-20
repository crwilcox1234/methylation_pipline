module load bedtools/2.19.1
module load bedops/2.4.14
while read line
do
bedtools closest [OPTIONS] -a "$line" \
                           -b <FILE1, FILE2, ..., FILEN> -d 

while read line
do
    sort -k1,1 -k2,2n /share/samdata/crwilcox/MLSS2pooled/TZB/methylation/Combined_202019/coverage_above10CpGs/"$line".cov > "$line".sort.cov
    bedtools getfasta -fi /share/samdata/jiangs2/Dr_TZB/humanRRBS/hg38/hg38.fa -bed "$line".sort.cov -fo "$line".sort.fa
done < R1_list_sort


bedops --everything file1.bed file2.bed ... fileN.bed \
    | bedmap --echo-map --fraction-both 0.6 - \
    | awk '(split($0, a, ";") > 1)' - \
    | sed 's/\;/\n/g' - \
    | sort-bed - \
    | uniq - \
    > answer.bed
