#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'James Liu'

from command import Command
import time
class Test(object):
    def Test01(self):
        """
        >>> d = DiskSize('boot','m',4)
        >>> d.sample()
        813
        >>> d = UsedDisk('run','m',['lock','shm','user'])
        >>> d.sample()
        2
        """

class Sample(object):
    def __init__(self,sleeptime):
        self._sleeptime = sleeptime
        self._disk = UsedDisk('/var/app_data','m',['VM_ramdisk','ram_mails'])
    def run(self):
        oldsize = 0
        samplelist = []
        while True:
            size = self._disk.sample()
            if oldsize == 0: 
                oldsize = size
            else:
                interval = size - oldsize
                samplelist.append(interval)
                with open('output.txt','a') as f:
                    f.write('{}:({},{}),{},{}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S')
                        ,size
                        ,oldsize
                        ,interval
                        ,reduce(lambda x,y:x+y,samplelist)/len(samplelist))
                    )

                oldsize = size
            time.sleep(self._sleeptime)


class DiskSize(object):
    def __init__(self,partname,unit,idx,skiplist=[]):
        self._unitstr = '-' + unit
        self._idx = idx
        self._partname = partname
        self._cmd = Command()
        self._skiplist = skiplist
    def sample(self):
        if len(self._skiplist) == 0: 
            return int(self._cmd.runcmd([['df',self._unitstr],['grep',self._partname],['awk','-F',' ','{print $%d}'%self._idx]]))
        else:
            greplist = [] 
            for s in self._skiplist:
                greplist.append(['grep','-v',s])

            cmdlist = []
            cmdlist.append(['df',self._unitstr])
            cmdlist.append(['grep',self._partname])
            cmdlist.extend(greplist)
            cmdlist.append(['awk','-F',' ','{print $%d}'%self._idx])

            return int(self._cmd.runcmd(cmdlist))

class UsedDisk(DiskSize):
    def __init__(self,partname,unit,skipstr=[]):
        super(UsedDisk,self).__init__(partname,unit,3,skipstr)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    #s = Sample(10*60)
    #s.run()
