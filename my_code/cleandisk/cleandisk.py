import time
import os
import traceback
#C:\Windows\SoftwareDistribution\Download delete all
#C:\Windows\System32\catroot


DAY1 = 24 * 60 * 60
DAY2 = 2 * DAY1
HALFDAY = DAY1 * 0.5

def CleanDisk(pname,ts,include):
    try:
        tmp = os.listdir(pname)
    except OSError as e:
        traceback.print_exc()
        return
    else:
        files = [os.path.join(pname,x) for x in tmp] 
        for f in files:
            try:
                curtime = os.path.getmtime(f)
            except WindowsError as e:
                traceback.print_exc()
                continue
            if os.path.isfile(f) and curtime<ts:
                if len(include) == 0:
                    os.remove(f)
                    print 'Delete %s' % f
                else:
                    for i in include:
                        if i in f:
                            os.remove(f)
                            print 'Delete %s' % f
                            break

if __name__ == '__main__':
    while True:
        CleanDisk(os.path.join('C:\\','Windows','Temp'),time.time()-HALFDAY,['cab_','.tmp'])
        CleanDisk(os.path.join('C:\\','Users','James_Liu','AppData','Local','Google','Chrome','User Data'),time.time()-HALFDAY,['.tmp'])
        CleanDisk(os.path.join('C:\\','Users','James_Liu','AppData','Local','Google','Chrome','User Data','Default'),time.time()-HALFDAY,['.tmp'])
        time.sleep(60)
