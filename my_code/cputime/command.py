#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'James Liu'


#>>> cmd.exe_float(['ps','aux','|','grep','uc_detection_va2ddd.py','|','awk','-F',' ','{print $3}'])

import subprocess
class Command(object):
	'''
	>>> cmd = Command()
	>>> type(cmd.cputime('python'))
	<type 'float'>
	>>> print(cmd.exword)
	cputime\|grep
	'''

	def __init__(self):
		self._exword = ''
		pass
        def runcmd(self,cmdlist): 
            proclist = []
            preStdOut = None
            for cmd in cmdlist:
                if len(proclist) == 0:
		    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                else:
                    proc = subprocess.Popen(cmd, stdin=proclist[-1].stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                proclist.append(proc)

            for idx in range(0,len(proclist)-1):
                proclist[idx].stdout.close()

            (stdout,stderr) = proclist[-1].communicate()
            return stdout

	def cputime(self,pname,exword=['cputime']):
		self._exword = ''
		exword.append('grep')
		for w in exword:
			if len(self._exword) == 0: 
				self._exword = w
			else:
				self._exword = self._exword+'\|'+w

		proc1 = subprocess.Popen(['ps','aux'], stdout=subprocess.PIPE)
		proc2 = subprocess.Popen(['grep',pname], stdin=proc1.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		proc3 = subprocess.Popen(['grep','-v',self._exword], stdin=proc2.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		# $3 is cputime $11 is process name
		proc4 = subprocess.Popen(['awk','-F',' ','{print $3}'], stdin=proc3.stdout,stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.	
		proc2.stdout.close()
		proc3.stdout.close()
            	(stdout, stderr) = proc4.communicate()
		retstr = stdout.split('\n')[0]
		return float(retstr)
	@property
	def exword(self):
		return str(self._exword)

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
