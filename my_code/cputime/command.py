#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'James Liu'


#>>> cmd.exe_float(['ps','aux','|','grep','uc_detection_va2ddd.py','|','awk','-F',' ','{print $3}'])

import subprocess
class Command(object):
	'''
	>>> cmd = Command()
	>>> type(cmd.cputime('uc_detection_va2ddd.py'))
	<type 'float'>
	'''

	def __init__(self):
		pass
	def cputime(self,pname):
		proc1 = subprocess.Popen(['ps','aux'], stdout=subprocess.PIPE)
		proc2 = subprocess.Popen(['grep',pname], stdin=proc1.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		proc3 = subprocess.Popen(['awk','-F',' ','{print $3}'], stdin=proc2.stdout,stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.	
		proc2.stdout.close()
            	(stdout, stderr) = proc3.communicate()
		retstr = stdout.split('\n')[0]
		return float(retstr)

class FakeCommand(Command):
	'''
	>>> fcmd = FakeCommand()
	>>> fcmd.set_return([1.2,1.3,1.4])
	>>> fcmd.cputime("ps aux | grep uc_detection_va2ddd.py | awk -F " " '{print $3}'")
	1.2
	>>> fcmd.cputime("ps aux | grep uc_detection_va2ddd.py | awk -F " " '{print $3}'")
	1.3
	>>> fcmd.cputime("ps aux | grep uc_detection_va2ddd.py | awk -F " " '{print $3}'")
	1.4
	'''

	def __init__(self):
		super(FakeCommand,self).__init__()
		self._ret = []
	def set_return(self,data):
		self._ret = data
	def cputime(self,cmd):
		return self._ret.pop(0)

if __name__ == '__main__':
	import doctest
	doctest.testmod()
