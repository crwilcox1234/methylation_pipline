while read line
do
    awk -F " " '{if(($5+$6)>10){print$0}}' /dfs3/bio/crwilcox/RRBS_TZB/"$line"/"$line"_R1_trimmed_bismark_bt2.bedGraph.gz.bismark.zero.cov > "$line"_above10_R1_trimmed_bismark_bt2.bedGraph.gz.bismark.zero.cov
done < R1_list
