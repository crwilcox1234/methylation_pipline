# this program can generate the batch qsub file for trimG to deal with multiple methylation fastq.gz files.

import sys

infile = open("R1_list")   # the list of the methylation sequence data files

outfile = open("trimG_batch_qsub.sh", "w")

outfile.write("#! /bin/bash\n#$ -N trimG_hg38_qsub\n#$ -q som,sam,bio,pub8i\n#$ -pe openmp 1\n\n")

for line in infile:

	name = line.strip().split('\n')[0]

	out = open(("t_" + name + "trimG_hg38.sh"), "w")

	out.write("#! /bin/bash\n#$ -N t_%strimG_hg38\n#$ -pe openmp 1\n#$ -q sam,som,sam128,bio,pub8i,pub64\n\n"%(name))
	out.write("module load fastx_toolkit/0.0.14\nmodule load fastqc/0.11.5\n") 
	out.write("~/software/trimglore/trim_galore --path_to_cutadapt ~/.local/bin/cutadapt \
		 --fastqc --stringency 5 --rrbs --length 30 --non_directional -o /dfs3/bio/crwilcox/RRBS_TZB/%s \
		/dfs3/bio/crwilcox/RRBS_TZB/%s/%s_R1.fastq.gz"%(name,name,name))
	out.close()
	outfile.write("qsub t_%strimG_hg38.sh\n"%(name))

outfile.close()
