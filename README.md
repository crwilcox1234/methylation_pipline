# methylation_pipline

1. sort

```bash

module load bedtools/2.19.1
while read line
do
    sort -k1,1 -k2,2n /share/samdata/crwilcox/MLSS2pooled/TZB/methylation/Combined_202019/coverage_above10CpGs/"$line".cov > "$line".sort.cov
    bedtools getfasta -fi /share/samdata/jiangs2/Dr_TZB/humanRRBS/hg38/hg38.fa -bed "$line".sort.cov -fo "$line".sort.fa
done < R1_list_sort

```
  * Extracts sequences (ATGC) from FASTA file for each of the methylation sites defined in .bed format file

2. Symetric CpGs

[View code](2symmetricCpG_batch_new.py)

  * Symmetric CpG batch new takes the sort.cov file and sort.fa file from the sort script above and ***marks*** the sites that are not c's or g's in the .fa file as ***"fake"*** sites or hemimethylated sites.

3. loop script

  * Splits the output files from 2 above (2symmetricCpG_batch_new.py) into separate files (both c and g) .fa files



