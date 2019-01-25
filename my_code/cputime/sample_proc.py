#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'James Liu'




from command import Command
import time
class Sample(object):
	"""
	>>> from command import FakeCommand
	>>> fcmd = FakeCommand()

	>>> fcmd.set_return([1.2,1.3,1.4])
	>>> s = Sample('uc_detection_va2ddd.py',3,1,fcmd)
	>>> s.sample_once()
	1.2
	>>> s.sample_once()
	1.3
	>>> s.sample_once()
	1.4

	>>> fcmd.set_return([1.2,1.3,1.4])
	>>> s = Sample('uc_detection_va2ddd.py',1,3,fcmd)
	>>> s.run()
	1.3

	>>> fcmd.set_return([1.2,1.3,1.4])
	>>> s.run('a.txt')
	1.3
	>>> f = open('a.txt','r')
	>>> f.read()
	'1.3,0'
	>>> f.close()
	"""	
	def __init__(self,pname='',interval=0,count=0,cmdobj=Command()):
		self._pname = pname
		self._intr  = interval
		self._cnt   = count
		self._cmdobj= cmdobj
		self._sdata = []

	def sample_once(self):
		return self._cmdobj.cputime(self._pname)


	def _save_data(self,fname,outputstr):
		if fname is not None:
			f = open(fname,'w')
			f.write(outputstr)
			f.close()

	def run(self,fname=None):
		while self._cnt > 0: 
			self._sdata.append(self.sample_once())
			self._cnt = self._cnt - self._intr
			time.sleep(self._intr)
			self._save_data(fname,'{},{}'.format(self._sdata,self._cnt))
			
		aver = reduce(lambda x,y:x+y,self._sdata)
		self._save_data(fname,'{},{}'.format(aver/len(self._sdata),self._cnt))
		return aver/len(self._sdata)
	
if __name__ == '__main__':
	import doctest
	doctest.testmod()
