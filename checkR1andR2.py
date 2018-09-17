#!/usr/bin/env python2.7

import glob
import os
import sys

dataPath=sys.argv[1]

fastqFiles=[]
IDs=[]
for i in glob.glob(os.path.join(dataPath, '*')):
	j=os.path.basename(i).split('_R')
	IDs.append(j[0])
	fastqFiles.append(os.path.basename(i))


oddOne=[]
for i in IDs:
	if "".join([i, "_R1.fastq.gz"]) in fastqFiles and "".join([i, "_R2.fastq.gz"]) in fastqFiles:
		pass
	else:
		oddOne.append(i)

print("\n")

for i in oddOne:
	print(i + " is missing its complementary sequence")

print("\n")
