module load bedtools/2.19.1
while read line
do
    sort -k1,1 -k2,2n /share/samdata/crwilcox/MLSS2pooled/TZB/methylation/Combined_202019/coverage_above10CpGs/"$line".cov > "$line".sort.cov
    bedtools getfasta -fi /share/samdata/jiangs2/Dr_TZB/humanRRBS/hg38/hg38.fa -bed "$line".sort.cov -fo "$line".sort.fa
done < R1_list_sort
