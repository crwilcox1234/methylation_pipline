## Need to have a master list of all regions seen before running script. Can achieve this by bedtools --everything or cat then | uniq to get only the uniq master regions.  Then add regions not seen in each individual file from master list with added 0's in each of the three columns.  This is so when you use the merge_sum1.py script you can keep 0s as placeholders for regions not in that individual sample.  
#!/usr/bin/python
import sys
file=open('list_A_abr')
file1=open('merge_A_abr_uniq.txt')
infile=file.readlines()
row1=file1.readlines()


master_regions=set()
for line in row1:
    list=line.strip().split('\t')
    site=list[0]+'\t'+list[1]+'\t'+list[2]
    master_regions.add(site)
#    if site not in master_regions:

#       master_regions[site]=float(list[3])
#    else:
#       master_regions[site]+=float(list[3])
#key1 = master_regions.keys()

#    master_regions[list[0]+':'+list[1]+':'+list[2]]=[]
#print(len(master_regions))
#print(master_regions)

#iterate over files
for i in infile:
    i=i.split('\n')[0]
    a= i+'.consolide.cov'
    b=i+'_addedzeros'
    inputfile=open(a)
    outputfile=open(b,"w")

    regions_seen=set()
    
    for line in inputfile:
       line=line.strip()
       list=line.split('\t')
       site=list[0]+'\t'+list[1]+'\t'+list[2]
       regions_seen.add(site)
       outputfile.write(line+'\n')
#       if site not in regions_seen:
#          regions_seen[site]= float(list[4])
#       else:
#          regions_seen[site]+= float(list[4])
#    key2 = regions_seen.keys()
#    print(len(regions_seen))
#    print(regions_seen)
    not_seen=master_regions-regions_seen
    for x in not_seen:
       # print(x)
        outputfile.write('\t'.join([x,"0","0","0"]) + '\n') 

#   print(not_seen)
    
#    for x in key1:
#        if x in key2:
#           outputfile.write(x + '\t' + str(regions_seen[x]) + '\n')
#        else:
#           outputfile.write(x + '\t' + str(master_regions[x]) + '\n')

    
#    for x in key1:
#       outputfile.write(x +'\t'+ str(regions_seen[x]) + '\n')
    inputfile.close()
    outputfile.close()
#    exit()
#    row.close()   
