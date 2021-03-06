# author: Ulya Bayram
# contact: ulyabayram@gmail.com
#
# Copyright (c) 2015 Trustworthy Systems Laboratory at the University of Cincinnati 
# All rights reserved.
#
# Developed by: 		
#	  		Trustworthy Systems Laboratory
#                      	University of Cincinnati
#                        http://dataengineering.org
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal with the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimers.
#
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimers in the documentation and/or other materials provided with the distribution.
# Neither the names of the Trustworthy Systems Laboratory, the University of Cincinnati, nor the names of its contributors may be used to endorse or promote products derived from this Software without specific prior written permission.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE.

import os
import math
 
# inputs:
#	filenametosave	: filename to save the syndrome numbers and bunch of other things
#	filenametosave2	: same as above, but save only the syndrome numbers
#	actual 		: original test set disk usage list
#	pred 		: predicted test set disk usage list
#	actualdelta	: original delta disk usage list
#	predelta	: predicted delta disk usage list
#	numd		: number of disks in RAID
def SyndromesAndReliabilityCheck(filenametosave, filenametosave2, actual, pred, actualdelta, predelta, numd):
	fo = open(filenametosave, 'w')
	f2 = open(filenametosave2, 'w')
	# max amount of disk usage in the system with a 10% addition, to set as threshold
	dmax = max(actual) + max(actual)*float(0.1) 

	bt = []
	improvement = []
	#numd = int(8)
	tofindmean = []
	#fcheck = open(filenametosave[:-4] + '_dr_check.txt', 'w')

	#averageimp = 0
	for t in range(len(actual)):
		
		dr = (dmax - pred[t])

		if pred[t] < actual[t]:
			dr = (dmax - actual[t])

		if pred[t] > dmax:
			dr = 0
		
		# more detail on these computations are in our DSN2015 paper
		# or contact me
		improvement = (20.4475 / (20.4475*(1-min([ (dr*numd/float(actual[t])), 1])) + (3.4069*min([dr*numd/float(actual[t]), 1]) )))
		y = (1-min([(dr*numd/float(actual[t])), 1]))

		bt.append(actual[t]/float(4096)) # 4 kb
		if t==0:
			dr_rel = 0 # initialization
		else:
			dr_rel = (dr/float(4096))/(float(bt[t-1]/float(numd)))

		#if dr*numd > actual[t]:
		#	print >> fcheck, t, (dr*numd-actual[t])
		tofindmean.append(dr_rel)
		print >> fo, improvement, dr, dmax, actual[t], pred[t], y, dr_rel
		print >> f2, dr_rel
		#averageimp += improvement

	#print str(filenametosave[:-4] + " --> " + str(averageimp/float(len(actual))))
	print  str(filenametosave[:-4] + " mean syndrome numbers --> " + str(sum(tofindmean)/float(len(tofindmean))))
	#print  str(filenametosave[:-4] + " mode --> " + str(findMode(tofindmean)))
	#print  str(filenametosave[:-4] + " median --> " + str(findMedian(tofindmean)))


# this code main_code was created when building this code, for test purposes
# ignore
def main_code():
	# main
	qlist = [int(-1), float(95), float(99), float(99.9)]

	k = [7, 9, 11]

	h = range(1, 11) #[2, 4, 8]
	fplot = open('plotReliabilitydelete.gp', 'w')

	# add statistical here
	for clusterMethodChoice in range(1, 3): # 1=km, 2=meanshift
		overunderrates = []
		#clusterMethodChoice = 1
		if clusterMethodChoice == 1: # kmeans
			print "Kmeans"
			for iik in range(len(k)):
				folder = str("kmeans/kmeans"+str(k[iik]))
				folder2 = str("kmeans"+str(k[iik]))
				print >> fplot, "set terminal postscript enhanced color\n"
				print >> fplot, "set ylabel \"Improvement\""
				print >> fplot, "set xlabel \"Time\""
				print >> fplot, "set grid x y"
				print >> fplot, "set key left top"
				print >> fplot, "set gri"
				print >> fplot, "set title \"Reliability Analysis " + folder + "\""
				print >> fplot, "set output \'| ps2pdf - Reliability_" + folder + ".pdf\'"
				print >> fplot, "plot",
				for q in qlist:
					tmpactual = []
					tmppred = []
					tmpactualdelta = []
					tmppreddelta = []
					filenametosave = "reliabili_" + folder2 + str(q) + ".txt"
				
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmpactual = [float(line.split()[1]) for line in fx]
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmppred = [float(line.split()[2]) for line in fx]
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmpactualdelta = [float(line.split()[3]) for line in fx]
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmppreddelta = [float(line.split()[4]) for line in fx]
					doReliabilityCheck(filenametosave, tmpactual, tmppred, tmpactualdelta, tmppreddelta)
					if q == qlist[len(qlist)-1]:
						print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines") #title " + "\"" + "q " + str(math.fabs(q)) + "\"")
					elif q == -1:
						print >> fplot, str("\"" + filenametosave + "\" using 0:1 with linestitle " + "\"" + "centroids" + "\","),
					else:
						print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines title " + "\"" + "q" + str(math.fabs(q)) + "\","),

		else: #meanshift
			print "MSSSSS"
			for iim in range(1, 11):
				folder = str("meanshift/meanshift"+str(iim))
				folder2 = str("meanshift"+str(iim))
				print >> fplot, "set terminal postscript enhanced color\n"
				print >> fplot, "set ylabel \"Improvement\""
				print >> fplot, "set xlabel \"Time\""
				print >> fplot, "set grid x y"
				print >> fplot, "set key left top"
				print >> fplot, "set gri"
				print >> fplot, "set title \"Reliability Analysis " + folder + "\""
				print >> fplot, "set output \'| ps2pdf - Reliability_" + folder + ".pdf\'"
				print >> fplot, "plot",

				for q in qlist:
					tmpactual = []
					tmppred = []
					tmpactualdelta = []
					tmppreddelta = []
					filenametosave = "reliabili_" + folder2 + str(q) + ".txt"
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmpactual = [float(line.split()[1]) for line in fx]
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmppred = [float(line.split()[2]) for line in fx]
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmpactualdelta = [float(line.split()[3]) for line in fx]
					with open(str(folder+'/HMM_predictions_q_' + str(math.fabs(q)) + '.txt'), 'r') as fx:
						tmppreddelta = [float(line.split()[4]) for line in fx]	
					doReliabilityCheck(filenametosave, tmpactual, tmppred, tmpactualdelta, tmppreddelta)
					if q == qlist[len(qlist)-1]:
						print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines title " + "\"" + "q" + str(math.fabs(q)) + "\"")
					elif q == -1:
						print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines title " + "\"" + "centroids" + "\","),
					else:
						print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines title " + "\"" + "q" + str(math.fabs(q)) + "\","),

	folder = 'statistical'
	print >> fplot, "set terminal postscript enhanced color\n"
	print >> fplot, "set ylabel \"Improvement\""
	print >> fplot, "set xlabel \"Time\""
	print >> fplot, "set grid x y"
	print >> fplot, "set gri"
	print >> fplot, "set key left top"
	print >> fplot, "set title \"Reliability Analysis " + folder + "\""
	print >> fplot, "set output \'| ps2pdf - Reliability_" + folder + ".pdf\'"
	print >> fplot, "plot",
	for q in qlist:
		tmpactual = []
		tmppred = []
		tmpactualdelta = []
		tmppreddelta = []

		filenametosave = "reliabili_" + folder + str(q) + ".txt"

		with open(str(folder+'/statisticalPredictions' + str(q) + '.txt'), 'r') as fx:
			tmpactual = [float(line.split()[1]) for line in fx]
		with open(str(folder+'/statisticalPredictions' + str(q) + '.txt'), 'r') as fx:
			tmppred = [float(line.split()[2]) for line in fx]
		with open(str(folder+'/statisticalPredictions' + str(q) + '.txt'), 'r') as fx:
			tmpactualdelta = [float(line.split()[3]) for line in fx]
		with open(str(folder+'/statisticalPredictions' + str(q) + '.txt'), 'r') as fx:
			tmppreddelta = [float(line.split()[4]) for line in fx]
		doReliabilityCheck(filenametosave, tmpactual, tmppred, tmpactualdelta, tmppreddelta)

		if q == qlist[len(qlist)-1]:
			print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines title " + "\"" + str(math.fabs(q)) + "\"")
		elif q == -1:
			print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines title " + "\"" + "centroids" + "\","),
		else:
			print >> fplot, str("\"" + filenametosave + "\" using 0:1 with lines title " + "\"" + "q" + str(math.fabs(q)) + "\","),


	#os.system('gnuplot plotReliability.gp')
