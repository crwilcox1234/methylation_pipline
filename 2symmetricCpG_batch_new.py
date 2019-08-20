import sys
import math
file=open('R1_list_sort')
row=file.readlines()
output1=open('NULL','w')
for line in row:
    name=line.split('\n')[0]
    file1=open(name+'.sort.cov')
    file2=open(name+'.sort.fa')
    output=open(name+'.symmetricCpG.new.txt','w')  
    row1=file1.readlines()
    row2=file2.readlines()
    dict={}
    dict1={}

    i=0
    while i<=len(row2)-1:
        site=row2[i].split('>')[1].split('\n')[0]
        if site not in dict:
            dict[site]=row2[i+1].split('\n')[0]
        i=i+2
    print(len(dict))

    i=0
    while i<len(row1)-1:
        a=row1[i].split('\t')
        b=row1[i+1].split('\t')
        chro1=a[0]
        start1=a[1]
        stop1=a[2]

        chro2=b[0]
        start2=b[1]
        stop2=b[2]

        site1=chro1+':'+start1+'-'+stop1
        site2=chro2+':'+start2+'-'+stop2
        if (chro1==chro2)and(stop1==start2)and(dict[site1]=='c' or dict[site1]=='C') and (dict[site2]=='g'or dict[site2]=='G'):
            output.write(row1[i].split('\n')[0]+'\t'+row1[i+1].split('\n')[0]+'\t'+dict[site1]+':'+dict[site2]+'\n')
            dict1[site1]=site1
            dict1[site2]=site2
        else:
            if site1 not in dict1:
                dict1[site1]=site1
                if (dict[site1]=='c' or dict[site1]=='C'):
                    output.write(row1[i].split('\n')[0]+'\t'+chro1+'\t'+stop1+'\t'+str(int(stop1)+1)+'\t'+'0'+'\t'+'0'+'\t'+'0'+'\t'+dict[site1]+':'+'gFake'+'\n')
                elif (dict[site1]=='g' or dict[site1]=='G'):
                    output.write(chro1+'\t'+str(int(start1)-1)+'\t'+start1+'\t'+'0'+'\t'+'0'+'\t'+'0'+'\t'+row1[i].split('\n')[0]+'\t'+'cFake'+':'+dict[site1]+'\n')
        i=i+1
    c=row1[len(row1)-1].split('\t')
    site=c[0]+':'+c[1]+'-'+c[2]
    if site not in dict1:
        dict1[site]=site
        if (dict[site]=='c' or dict[site]=='C'):
            output.write(row1[len(row1)-1].split('\n')[0]+'\t'+c[0]+'\t'+c[2]+'\t'+str(int(c[2])+1)+'\t'+'0'+'\t'+'0'+'\t'+'0'+'\t'+dict[site]+':'+'gFake'+'\n')
        elif (dict[site]=='g' or dict[site]=='G'):
            output.write(c[0]+'\t'+str(int(c[1])-1)+'\t'+c[1]+'\t'+'0'+'\t'+'0'+'\t'+'0'+'\t'+row1[len(row1)-1].split('\n')[0]+'\t'+'cFake'+':'+dict[site]+'\n')
    print(len(dict1))
    output.close()
output1.close()
