# this program can generate the batch qsub file for Bismark_methylation_extractor to deal with the mapped Bismark data.

import sys

infile = open("list")   # the list of A and B samples that need extraction

outfile = open("bismark_extract_batch_qsub.sh", "w")

outfile.write("#! /bin/bash\n#$ -N extract_hg38_qsub\n#$ -q sam,sam128,som,bio,pub8i,pub64\n#$ -pe openmp 1\n\n")

for line in infile:

        name = line.strip().split('\n')[0]

        out = open(("t_" + name + "extract_hg38.sh"), "w")

        out.write("#! /bin/bash\n#$ -N t_%sextract_hg38\n#$ -pe openmp 8\n#$ -q bio,sam,som,pub64,pub8i\n"%(name))
        out.write("module load bowtie2/2.2.7\nmodule load samtools/1.0\n")
        out.write("~/software/Bismark/bismark_methylation_extractor --multicore 8 -s --bedGraph --zero_based  /share/samdata/crwilcox/MLSS2pooled/TZB/methylation/Combined_202019/%s/%s_R1_trimmed_bismark_bt2.sam -o /share/samdata/crwilcox/MLSS2pooled/TZB/methylation/Combined_202019/%s/"%(name,name,name))
        out.close()
        outfile.write("qsub t_%sextract_hg38.sh\n"%(name))

outfile.close()
