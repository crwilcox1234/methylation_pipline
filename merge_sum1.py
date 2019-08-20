#!/usr/bin/python
import sys
#outfile = open("merge-file-methyl-cov.bed",'w')
outfile = open("test-file-methyl_heade.bed",'w')
file1=open('list')
row1=file1.readlines()
print(len(row1))
files=[]
for line in row1:
    line=line.split('\n')[0]
    a=line
    files.append(a)
outfile.write(files[0]+'\t'+files[1]+'\t'+files[2]+'\t'+files[3]+'\t'+files[4]+'\t'+files[5]+'\t'+files[6]+'\t'+files[7]+'\t'+files[8]+'\t'+files[9]+'\t'+files[10]+'\t'+files[11]+'\t'+files[12]+'\t'+files[13]+'\t'+files[14]+'\t'+files[15]+'\t'+files[16]+'\t'+files[17]+'\t'+files[18]+'\t'+files[19]+'\t'+files[20]+'\t'+files[21]+'\t'+files[22]+'\t'+files[23]+'\t'+files[24]+'\t'+files[25]+'\t'+files[26]+'\t'+files[27]+'\t'+files[28]+'\t'+files[29]+'\t'+files[30]+'\t'+files[31]+'\t'+files[32]+'\t'+files[33]+'\t'+files[34]+'\t'+files[35]+'\t'+files[36]+'\t'+files[37]+'\t'+files[38]+'\t'+files[39]+'\n')

print(files)



dict={}

#list2='symbol'
#for line in row1:
#    a=line.split('\n')[0]
#    list2=list2+'\t'+a
#list2=list2+'\n'
#outfile.write(list2)
#print(list2)


#testFile=open('merge_sig_diff_cut_8042.seq134.trim43_trimmed_bismark_bt2.bedGraph.gz.bismark.zero.cov','r')
dictfile=open('everything_merge_uniq_addedrows.txt','r') #everything_merge_text is made using bedops --everything.  Use the output file from bedops --everything, do not remove extra columns
for line in dictfile:
    elem = line.strip().split('\t')
    dict[elem[0]+':'+elem[1]+':'+elem[2]]=[]
dictfile.close()

for x in range(len(files)):
    infile=open(files[x],'r')
    for line in infile:
        elem=line.strip().split('\t')
        dict[elem[0]+':'+elem[1]+':'+elem[2]].append(elem[4])
    infile.close()

keys=dict.keys()

for x in keys:
    outfile.write(x)
    counts=dict[x]
#    if len(counts)<10:
#        print ('Warning')
    for i in range(len(counts)):
        outfile.write('\t'+counts[i])
    outfile.write('\n')
outfile.close()

#The output will not have all the columns needed, so to add the columns and replace empty elements with 0, use this code:
#awk -v max=41 -v OFS='\t' '{ for(i=NF+1; i<=max; i++) $i = "0"; print }' test-file-methyl_heade.bed > methylation_matrix_header_test.txt

#to count the number of elements above 0 in each row (i.e. to determine the number of samples methylated the CpG):
#awk '{for(i=1;i<=NF;i++)if($i > 0)x++;print x;x=0}' methylation_matrix_header_test.txt > CpGs_methylated_count.txt
