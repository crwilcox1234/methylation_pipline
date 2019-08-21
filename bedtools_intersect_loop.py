import sys
file=open('list_B')
row=file.readlines()

peaklist=[]
for line in row:
    peaklist.append(line.split('\n')[0])
print(len(peaklist))

for line in row:
    sample=line.split('.')[0]
    output=open("bedtools_"+sample+".sh","w")
    a=""
    for elem in peaklist:
        if sample not in elem:
            a=a+"\t"+elem
    b=a.split("\t")
#    if len(b)>27:
#        print("STOP!")    
    output.write("module load bedtools/2.25.0\n\n")
    output.write("bedtools intersect -c -a "+line.split('\n')[0]+" -b"+a+" > "+sample+"_intersect.txt")
    output.close()
