#!/usr/bin/env/python

import sys
import os
import subprocess
from shutil import copy


dataPath=sys.argv[1]
scriptPath=os.path.dirname(os.path.realpath(__file__))


runName=os.path.basename(dataPath)
newdataPath=os.path.join(dataPath, runName+"_trimmed")



def data_prep():
	trim_ans=raw_input("Enter 'P' for paired end sequences OR \nEnter 'U' for unpaired end sequences: \n ")

	print("\nTrimming raw fastq files in: " + dataPath)
	print("\n")
	os.chdir(dataPath)
	try:
		os.makedirs(newdataPath)
	except:
		pass
	for f in os.listdir(dataPath):
		f=os.path.basename(f)
		if '.gz' in f:
			copy(f, newdataPath)
	os.chdir(newdataPath)
	for i in os.listdir(newdataPath):
		sampleID, filetype=i.split('_R')
		adapter="/opt/Trimmomatic-0.36/adapters/TruSeq3-PE.fa"
		R1=(sampleID+"_R1.fastq.gz")
		R2=(sampleID+"_R2.fastq.gz")
		R1P=(sampleID+"_P_R1.fastq.gz")
		R1U=(sampleID+"_U_R1.fastq.gz")
		R2P=(sampleID+"_P_R2.fastq.gz")
		R2U=(sampleID+"_U_R2.fastq.gz")

		prep_command=" ".join(["java -jar /opt/Trimmomatic-0.36/trimmomatic-0.36.jar PE -phred33 -threads 16", R1, R2, R1P, R1U, R2P, R2U, "".join(["ILLUMINACLIP:", adapter, ":2:30:10"]), "LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"])
		subprocess.check_call(prep_command, shell=True)
	if 'P' in trim_ans.upper():    
		for i in os.listdir(newdataPath):
			if '_U_' in i:
				os.remove(i)
	elif 'U' in trim_ans:
		for i in os.listdir(newdataPath):
			if '_P_' in i:
				os.remove(i)
	elif trim_ans.upper() != 'P' and trim_ans.upper() != 'U':
		for i in os.listdir(newdataPath):
			if '_U_' in i:
				os.remove(i)
	for i in os.listdir(newdataPath):
		if '_P_' not in i and '_U_' not in i:
			os.remove(i)

if dataPath.lower()=='-h' or dataPath.lower()=='--help':
	print("\nRun script as follows: \n python "+scriptPath+"/run_trim.py      /path/to/dataset\n")
else:
	data_prep()