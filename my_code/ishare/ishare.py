#use mouse copy the RD document  and paste into the txt file.
if __name__ == '__main__':
	f = open('a.txt','r')
	lines = f.readlines()
	f.close()
	
	# each document has 3 rows, and the 0 rows is the document title.
	# file out the unwanted row.
	newlist = []
	for l in lines:
		if l.find('Checked Out') == -1:
			newlist.append(l)
	
	doclist = []
	for i in range(len(newlist)):
		if i%3 == 0:
			doclist.append(newlist[i].strip())
	print len(doclist)
	for l in doclist:
		print l
