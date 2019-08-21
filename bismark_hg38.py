# this program can generate the batch qsub file for STAR to deal with the single cell data.

import sys

infile = open("R1_list")   # the list of the single cell sequence data files

outfile = open("bismark_batch_qsub.sh", "w")

outfile.write("#! /bin/bash\n#$ -N bismark_hg38_qsub\n#$ -q sam,bio,pub8i\n#$ -pe openmp 1\n\n")

for line in infile:

	name = line.strip().split('\n')[0]

	out = open(("t_" + name + "bismark_hg38.sh"), "w")

	out.write("#! /bin/bash\n#$ -N t_%sbismark_hg38\n#$ -pe openmp 8\n#$ -q som,sam,bio,pub64\n\n"%(name))
	out.write("module load bowtie2/2.2.7\nmodule load samtools/1.0\n") 
	out.write("~/software/Bismark/bismark -p 8 --sam --non_directional /share/samdata/jiangs2/Dr_TZB/humanRRBS/hg38/ /dfs3/bio/crwilcox/RRBS_TZB/%s/%s_R1_trimmed.fq.gz -o /dfs3/bio/crwilcox/RRBS_TZB/%s/"%(name,name,name))
	out.close()
	outfile.write("qsub t_%sbismark_hg38.sh\n"%(name))

outfile.close()
