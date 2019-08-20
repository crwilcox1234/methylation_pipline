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

        
