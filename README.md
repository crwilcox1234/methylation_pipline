# methylation_pipline

### Before sorting the **.zero.cov** file output from bismark's methyl extractor, you must decide how much coverage you want as a cutoff, we started with a cutoff at 10

```
while read line
do
    awk -F " " '{if(($5+$6)>10){print$0}}' "$line"/"$line"_R1_trimmed_bismark_bt2.bedGraph.gz.bismark.zero.cov > "$line"_above10_R1_trimmed_bismark_bt2.bedGraph.gz.bismark.zero.cov
done < R1_list
```

1. sort

```bash
module load bedtools/2.19.1
while read line
do
    sort -k1,1 -k2,2n "$line".cov > "$line".sort.cov
    bedtools getfasta -fi hg38.fa -bed "$line".sort.cov -fo "$line".sort.fa
done < R1_list_sort
```
  * Extracts sequences (ATGC) from FASTA file for each of the methylation sites defined in .bed format file

### Example of the **sort.cov** file:

```
chr1    778878  778879  3.7037037037037 1       26
chr1    778880  778881  4.54545454545455        1       21
chr1    778881  778882  0       0       27
chr1    778883  778884  4.54545454545455        1       21
chr1    778884  778885  3.7037037037037 1       26
chr1    778896  778897  4.54545454545455        1       21
chr1    778897  778898  0       0       26
chr1    778911  778912  4.54545454545455        1       21
chr1    778912  778913  0       0       27
```

### Example of the **sort.fa** file:

```
>chr1:778873-778874
C
>chr1:778877-778878
C
>chr1:778878-778879
G
>chr1:778880-778881
C
>chr1:778881-778882
G
```

2. Symetric CpGs

[View code](2symmetricCpG_batch_new.py)

  * Symmetric CpG batch new takes the sort.cov file and sort.fa file from the sort script above and ***marks*** the sites that are not c's or g's in the .fa file as ***"fake"*** sites or hemimethylated sites.

### Example of the output file (symmetricCpG.new.txt):

```
chr1    778873  778874  0       0       11      chr1    778874  778875  0       0       0       C:gFake
chr1    778877  778878  0       0       11      chr1    778878  778879  3.7037037037037 1       26      C:G
chr1    778880  778881  4.54545454545455        1       21      chr1    778881  778882  0       0       27      C:G
chr1    778883  778884  4.54545454545455        1       21      chr1    778884  778885  3.7037037037037 1       26      C:G
chr1    778896  778897  4.54545454545455        1       21      chr1    778897  778898  0       0       26      C:G
chr1    778911  778912  4.54545454545455        1       21      chr1    778912  778913  0       0       27      C:G
chr1    779066  779067  0       0       0       chr1    779067  779068  0       0       21      cFake:G
```

3. loop script

  * Splits the output files from 2 above (2symmetricCpG_batch_new.py) into separate files (both c and g) .fa files

```
module load bedtools/2.19.1
while read line
do
    awk -F"\t" '{print$1"\t"$2"\t"$3}' "$line" > c_"$line"
    bedtools getfasta -fi hg38.fa -bed c_"$line" -fo c_"$line".fa
    awk -F"\t" '{print$1"\t"$3"\t"($3+1)}' "$line" > g_"$line"
    bedtools getfasta -fi hg38.fa -bed g_"$line" -fo g_"$line".fa
    rm c_"$line"
    rm g_"$line"
done < list_loop
```

### Example of one of the output files (c_...symmetricCpG.new.txt.fa):

```
>chr1:827327-827328
C
>chr1:827550-827551
c
>chr1:827552-827553
c
>chr1:869946-869947
C
```

4. Check symmetric CpGs

  * inputs are the two (c and g) .fa files and the combined 


