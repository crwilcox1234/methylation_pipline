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
