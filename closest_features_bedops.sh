module load bedtools/2.19.1
module load bedops/2.4.14

while read line
do
#sed 's/"$line".*//' list_A_name > "$line"_remove.txt
#done < list_A

cat !{"$line"} *.cov > "$line"_rm.cov
closest-features --delim '\t' --dist "$line" "$line"_rm.cov > "$line"_closest_feature.cov

done < list_A


#bedops --everything file1.bed file2.bed ... fileN.bed \
#    | bedmap --echo-map --fraction-both 0.6 - \
#    | awk '(split($0, a, ";") > 1)' - \
#    | sed 's/\;/\n/g' - \
#    | sort-bed - \
#    | uniq - \
#    > answer.bed
