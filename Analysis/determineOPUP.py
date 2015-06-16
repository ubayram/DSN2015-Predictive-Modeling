# author: Ulya Bayram
# contact: ulyabayram@gmail.com
# inputs are real and predicted overall results
# selected quartile % (or no quartile) to indicate which result is from which q
# and fres, the file to write the results on
def underOverCalculator(real, pred, q, fres):

	opflag = 0
	upflag = 0
	sumOp = 0
	sumUp = 0

	# for each test data
	for i in range(len(pred)):
		# if predicted delta is larger than original delta
		if pred[i] >= real[i]: 
			opflag += 1 # overprediction detected
			sumOp += (pred[i]-real[i]) # amount of overprediction
		else: # underprediction detected
			upflag += 1
			sumUp += (real[i]-pred[i]) # amount of underprediction
	

	opRate = opflag / float(len(pred)) # overprediction occurrence rate
	upRate = upflag / float(len(pred)) # underprediction occurrence rate

	# average overprediction within whole test set (single value)
	avgOP = sumOp/ float(opflag) 

	if upflag > 0:
		# average underprediction within whole test set (single value)
		avgUP = sumUp / float(upflag) 
	else:
		avgUP = 0

	# result = [float(q/float(100)), opRate, upRate, avgOP, avgUP, upflag, sumUp]
	 
	# write to the file fres opened in main_.py file the following
	# quartile %, over prediction rate, 
	# under prediction rate, 
	# average over prediction amount, average underprediction amount
	# how many times underprediction occurred
	# sum of underprediction amount
	print >> fres, float(q/float(100)), opRate, upRate, avgOP, avgUP, upflag, sumUp