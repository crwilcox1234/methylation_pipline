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
