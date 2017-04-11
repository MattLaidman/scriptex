#!/usr/bin/env python3

import os
import time
import sys
from difflib import SequenceMatcher

sys.path.append('../')
sys.path.append('../scriptex')

os.chdir('../scriptex')

import scriptex

results=False
prototype=False
Testall=False
Testone=False
Testmanual=False

os.chdir('../testing')

if len(sys.argv)>1:#for command line arguments
	os.chdir('tests')
	input = os.getcwd()+"/"+sys.argv[1]
	output = os.getcwd()+"/"+input[:-4]+ '.tex'
	os.chdir('../../scriptex')
	scriptex.scriptex_run(input, output)

def file_compare(outfile, expected, resultsfile, results):#file compare function
	comp=open(expected).read()
	output=open(outfile).read()
	if len(output)>=84 and len(comp)>=84:
		output=output[70:len(output)-14]
		comp=comp[70:len(comp)-14]
	elif len(output)<84 and len(comp)>=84:
		comp=comp[70:len(comp)-14]
	elif len(comp)<84 and len(output)>=84:
		output=output[70:len(output)-14]
	thing=''
	thing2=''
	complength=len(comp)
	outlength=len(output)
	start=False
	j=0
	while len(output)>j:
		if output[j]=='\\':
			thing=thing+output[j]
			output=output[:j]+output[j+1:]
			start=True
			j=j-1
		elif start==True and (output[j]==" " or output[j]=="\n"):
			start=False
			output=output[:j]+"1"+output[j:]
		elif start==True:
			thing=thing+output[j]
			output=output[:j]+output[j+1:]
			j=j-1
		j=j+1
	start=False
	j=0
	while len(comp)>j:
		if comp[j]=='\\':
			thing2=thing2+comp[j]
			start=True
			comp=comp[:j]+comp[j+1:]
			j=j-1
		elif start==True and (comp[j]==" " or comp[j]=="\n"):
			start=False
			comp=comp[:j]+"1"+comp[j:]
		elif start==True:
			thing2=thing2+comp[j]
			comp=comp[:j]+comp[j+1:]
			j=j-1
		j=j+1
	splitthing=thing.split("\\")
	splitthing2=thing2.split("\\")
	if len(splitthing)>len(splitthing2):
		n=len(splitthing2)
	else:
		n=len(splitthing)
	j=0
	i=0
	while n>j:
		if SequenceMatcher(None, splitthing[j], splitthing2[j]).ratio()==1:
			i=i+1
		j=j+1
	symbolratio=0
	biggestlength=0
	originallen=0
	if len(output)>len(comp):
		originallen=outlength-(len(thing1))+(len(splitthing)-1)
		symbolratio=(i-1)/originallen
		biggestlength=len(output)
	else:
		originallen=complength-(len(thing2))+(len(splitthing2)-1)
		symbolratio=(i-1)/originallen
		biggestlength=len(comp)
	per=(SequenceMatcher(None, output, comp).ratio()*((biggestlength)/originallen)+symbolratio)*100
	print('The output was '+str('{0:.2f}'.format(per))+'% accurate\n')
	os.chdir('../')
	if results==True:
		resultsfile=open(os.getcwd()+'/results.txt','a')
		resultsfile.write('The output was '+str('{0:.2f}'.format(per))+'% accurate\n')
		resultsfile.close()
		return

# for printing to results file
while True:
	results=False
	prototype=False
	Testall=False
	Testone=False
	Testmanual=False
	while True:
		valid=True
		a=input('Would you like to have a file to store test results?\n1. Yes\n2. No\n0. Quit\n')
		try:
			if int(a)==1:
				results=True
				break
			elif int(a)==0:
				exit(0)
			elif int(a)==2:
				break
			else:
				print('That is not an acceptable input')
		except ValueError:
			print('That is not an acceptable input')
	#the actual harness
	while True:
		if Testone==True or Testall==True:
			break
		try:
			dir=input('How would you like to test the system?\n1. Automated\n2. Manual\n0. Quit\n')
			if int(dir)==0:
				exit(0)
			elif int(dir)==1:#Automatic input
				dir=input('Would you like to test: \n1. One\n2. All\n0. Quit\n')
				if int(dir)==1:
					Testone=True
				elif int(dir)==2:#Testing everything
					Testall=True
				elif int(dir)==0:
					exit(0)
				else:
					print('That is not an acceptable input')
			elif int(dir)==2:#Manual input
				Testone=True
				Testmanual=True
				break
			else:
				print('That is not an acceptable input')
		except ValueError:
			print('That is not an acceptable input')
		
	if Testall==True:#Test everything
		i=1
		resultsfile=open('results.txt','a')
		while i<=4:
			os.chdir('tests')
			filenum=str(i)
			testdoc=os.getcwd()+'/test'+filenum+'.png'
			comp=open('compoutput'+filenum+'.tex','r')
			output=os.getcwd()+'/out.tex'
			start = time.time()
			os.chdir('../../scriptex')
			scriptex.run_scriptex(testdoc, output)
			end = time.time()
			print('The time to completion is: '+str(end-start)+' seconds\n')
			os.chdir('../testing')
			if results==True:
				resultsfile.write('The time to completion is: '+str(end-start)+' seconds\n')
				resultsfile.close()
			os.chdir('tests')
			file_compare(output,comp.name,resultsfile,results)
			i=i+1
	elif Testone==True:#test one thing
		testdoc=''
		os.chdir('tests')
		if Testmanual==True:
			while True:
				filename=input('What is the name of the file you would wish to use?(Remember to put the file in the tests folder)\n')
				compname=input('What is the name of the comparison file you would wish to use?(Remember to put the file in the tests folder)\n')
				if os.path.exists(filename) and os.path.exists(compname):
					testdoc=os.getcwd()+'/'+filename
					comp=open(compname,'r')
					output=os.getcwd()+'/out.tex'
					start = time.time()
					os.chdir('../../scriptex')
					scriptex.run_scriptex(testdoc, output)
					end = time.time()
					print('The time to completion is: '+str(end-start)+' seconds\n')
					os.chdir('../testing')
					if results==True:
						resultsfile=open('results.txt','a')
						resultsfile.write('The time to completion is: '+str(end-start)+' seconds\n')
						resultsfile.close()
					os.chdir('tests')
					file_compare(output,comp.name,resultsfile,results)
					break
				elif os.path.exists(filename):
					print("The comparison output is not in the tests folder\n")
				elif os.path.exists(compname):
					print("The test file is not in the tests folder\n")
				else:
					print("The test file and comparison output were not found\n")
		else:
			testdoc=''
			while True:
				while True:
					try:
						filenum=input('Which test would you like to use?(Enter a number between 1 and 5)\n')
						if int(filenum)>4 or int(filenum)<1:
							print('That is not an acceptable input')
						else:
							break
					except ValueError:
						print('That is not an acceptable input')
				while True:
					try:
						dir=input('Would you like to test with:\n1. A .PNG file?\n2. A .TIFF file?\n3. A .JPG file?\n0. Quit\n')
						if int(dir)==1:
							testdoc=os.getcwd()+'/test'+filenum+'.png'
						elif int(dir)==2:
							testdoc=os.getcwd()+'/test'+filenum+'.tiff'
						elif int(dir)==3:
							testdoc=os.getcwd()+'/test'+filenum+'.jpg'
						else:
							print('That is not an acceptable input')
					except ValueError:
							print('That is not an acceptable input')
					comp=open('compoutput'+filenum+'.tex','r')
					output=os.getcwd()+'/out.tex'
					start = time.time()
					os.chdir('../../scriptex')
					scriptex.run_scriptex(testdoc, output)
					end = time.time()
					print('The time to completion is: '+str('{0:.2f}'.format(end-start))+' seconds\n')
					os.chdir('../testing')
					resultsfile=open('results.txt','a')
					if results==True:
						resultsfile.write('The time to completion is: '+'{0:.2f}'.format(end-start)+' seconds\n')
						resultsfile.close()
					os.chdir('tests')
					file_compare(output,comp.name,resultsfile,results)
					break
				else:
					print('That is not an acceptable input')
				break
		# comp.close()