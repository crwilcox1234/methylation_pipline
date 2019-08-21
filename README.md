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

  * inputs are the two (c and g) .fa files and the output from symetric CpGs

```
import sys
import math
file=open('list_loop')
row=file.readlines()
output1=open('NULL','w')
for line in row:
    name=line.split('\n')[0]
    file1=open('c_'+name+'.fa')
    file2=open('g_'+name+'.fa')
    file3=open(name)
    output=open(name+'.real.txt','w')  
    row1=file1.readlines()
    row2=file2.readlines()
    row3=file3.readlines()
    c={}
    g={}

    i=0
    while i<=len(row1)-1:
        site=row1[i].split('>')[1].split('\n')[0]
        if site not in c:
            c[site]=row1[i+1].split('\n')[0]
        i=i+2
    print(len(c))
    i=0
    while i<=len(row2)-1:
        site=row2[i].split('>')[1].split('\n')[0]
        if site not in g:
            g[site]=row2[i+1].split('\n')[0]
        i=i+2
    print(len(g))

    i=0
    count=0
    while i<=len(row3)-1:
        a=row3[i].split('\t')
        csite=a[0]+':'+a[1]+'-'+a[2]
        gsite=a[6]+':'+a[7]+'-'+a[8]
        if (csite in c) and (gsite in g):
            output.write(row3[i].split('\n')[0]+'\t'+c[csite]+':'+g[gsite]+'\n')
            count=count+1
        i=i+1
    print(str(count))
    output.close()
output1.close()
```
  * Script also finds the how many CpGs are methylated on each strand (c vs g), and that the c and g sites match.

### Example of output file (.real.txt):

```
chr1    778873  778874  0       0       11      chr1    778874  778875  0       0       0       C:gFake C:G
chr1    778877  778878  0       0       11      chr1    778878  778879  3.7037037037037 1       26      C:G     C:G
chr1    778880  778881  4.54545454545455        1       21      chr1    778881  778882  0       0       27      C:G     C:G
chr1    778883  778884  4.54545454545455        1       21      chr1    778884  778885  3.7037037037037 1       26      C:G     C:G
chr1    778896  778897  4.54545454545455        1       21      chr1    778897  778898  0       0       26      C:G     C:G
chr1    778911  778912  4.54545454545455        1       21      chr1    778912  778913  0       0       27      C:G     C:G
chr1    779066  779067  0       0       0       chr1    779067  779068  0       0       21      cFake:G C:G
chr1    779074  779075  0       0       0       chr1    779075  779076  0       0       21      cFake:G C:G
chr1    779095  779096  0       0       0       chr1    779096  779097  0       0       26      cFake:G C:G
chr1    779099  779100  0       0       0       chr1    779100  779101  0       0       25      cFake:G C:G
```

5. filter unmatch

  * This script counts the number of hemimethylated sites (but does not delete them). Make sure to capture the numbers, the script below only outputs them to the screen. Also, the script removes the labels for hemimethylation (labeled by previous scripts as fake) and replaces them with the correct base.

  * input .real.txt
  * output .realmatch.txt

```
import sys
import math
file=open('list_real')
row=file.readlines()
output1=open('NULL','w')
for line in row:
    name=line.split('\n')[0]
    file=open(name)
    output=open(name+'.realmatch.txt','w')  
    row=file.readlines()
    pair={}
    unpair={}
    for line in row:
        a=line.split('\t')
        if a[12]==a[13].split('\n')[0]:
            pair[line]=line
        else:
            if 'gFake' in a[12]:
                a[13]=a[13].split('\n')[0]
                if (a[13]==a[12].split(':')[0]+':'+'G') or (a[13]==a[12].split(':')[0]+':'+'g'):
                    unpair[line]=line
            elif 'cFake' in a[12]:
                a[13]=a[13].split('\n')[0]
                if (a[13]=='C'+':'+a[12].split(':')[1]) or (a[13]=='c'+':'+a[12].split(':')[1]):
                    unpair[line]=line
    sum=len(pair)+len(unpair)
    print(name+'pair is'+':'+str(len(pair)))
    print(name+'unpair is'+':'+str(len(unpair)))
    print(name+'total is'+':'+str(sum))

    for x in pair:
        output.write(pair[x].split('\n')[0]+'\n')
    for x in unpair:
        output.write(unpair[x].split('\n')[0]+'\n') 
        
    output.close()
output1.close()
``` 

### Example of output (.realmatch.txt)

```
chr1    904893  904894  0       0       23      chr1    904894  904895  0       0       15      C:G     C:G
chr1    904898  904899  14.2857142857143        4       24      chr1    904899  904900  31.8181818181818        7       15      C:G     C:G
chr1    904912  904913  0       0       24      chr1    904913  904914  0       0       16      C:G     C:G
chr1    904914  904915  0       0       24      chr1    904915  904916  0       0       16      C:G     C:G
chr1    904922  904923  0       0       24      chr1    904923  904924  0       0       16      C:G     C:G
chr1    904932  904933  4.16666666666667        1       23      chr1    904933  904934  6.25    1       15      C:G     C:G
chr1    904935  904936  0       0       24      chr1    904936  904937  0       0       16      C:G     C:G
chr1    904938  904939  75      9       3       chr1    904939  904940  6.66666666666667        1       14      C:G     C:G
```

  * **NOTE:** After this script is finished you need to consolidate strands (A and B samples treated separately) using [consolidate_over3.py](consolidate_over3.py) into coverage and ratios in order to make matrices of each sample with relevant information (i.e. coverage and methylation ratio) and CpG sites not found in that sample. Then use bedops --everything or cat to concatinate all of the (A or B) .realmatch.txt files and pipe (|) into uniq -c which prints only uniq regions and counts how many times that region occurred (which can be used to make a histogram of how many CpGs are found in multiple samples).  After making a uniq list of master regions for As and Bs separately, can now run the [premerge_files.py](premerge_files.py) to add CpGs (can also do this with regions or DMRs when you get there) from the master list (either from all As or all Bs) that are not present in individual sample files.  This [premerge_files.py](premerge_files.py) script will output consolide.cov files (these .cov files include all the CpGs found in at least one sample in the group (either A group or B group)).  A following step of the pipline will generate output files with CpGs found only in that individual (found in both A and B for that individual). Now can run the [merge_sum1.py](merge_sum1.py) or [merge_ratio.py](merge_ratio.py) script using the outputs from premerge. Can also use similar scripts after step 6. 

6. Overlay

  * only outputs CpGs that are in both samples (A and B).

```
import sys
file=open('list_realmatch1')
row=file.readlines()
i=0
while i<=len(row)-1:
    A=row[i].split('\n')[0]
    B=row[i+1].split('\n')[0]
    file1=open(A+'_trimmed_bismark_bt2.bedGraph.gz.bismark.zero.symmetricCpG.new.txt.real.txt.realmatch.txt')
    file2=open(B+'_trimmed_bismark_bt2.bedGraph.gz.bismark.zero.symmetricCpG.new.txt.real.txt.realmatch.txt')
    row1=file1.readlines()
    row2=file2.readlines()
    output1=open(A+'.overlay.consolide.cov','w')
    output2=open(B+'.overlay.consolide.cov','w')

    dict={}
    dict1={}

    for line in row1:
        a=line.split('\t')
        site=a[0]+'\t'+a[1]+'\t'+a[2]
        c=int(a[4])+int(a[10])
        t=int(a[5])+int(a[11])
        sum1=c+t
        if (site not in dict) and (sum1>10):
            dict[site]=site
    print(len(dict))

    for line in row2:
        a=line.split('\t')
        site=a[0]+'\t'+a[1]+'\t'+a[2]
        c=int(a[4])+int(a[10])
        t=int(a[5])+int(a[11])
        sum1=c+t
        if (site in dict) and (sum1>10):
            dict1[site]=site
    print(len(dict1))

    for line in row1:
        a=line.split('\t')
        site=a[0]+'\t'+a[1]+'\t'+a[2]
        c=int(a[4])+int(a[10])
        t=int(a[5])+int(a[11])
        sum1=c+t
        if (site in dict1):
            ratio=str(100*float(c)/sum1)
            output1.write(site+'\t'+ratio+'\t'+str(c)+'\t'+str(t)+'\n')

    for line in row2:
        a=line.split('\t')
        site=a[0]+'\t'+a[1]+'\t'+a[2]
        c=int(a[4])+int(a[10])
        t=int(a[5])+int(a[11])
        sum1=c+t
        if (site in dict1):
            ratio=str(100*float(c)/sum1)
            output2.write(site+'\t'+ratio+'\t'+str(c)+'\t'+str(t)+'\n')
    output1.close()
    output2.close()
    i=i+2
```

  * Can now use methylKit to determine DMRs (See Mandy's paper). After determining DMRs make a matrix of common DMRs and filter for DMRs only in 2 or more samples. Now can make heatmaps and PCAs based on DMRs.
 


