import os
from os.path import join,getsize
import time
import json

def getdirsize(dir):
    size = 0L
    for root,dirs,files in os.walk(dir):
        try:
            size += sum([getsize(join(root,name)) for name in files ])
        except WindowsError as e:
            print e
            size += 0
    return size

def getsize_safe(fname):
    size = 0
    try:
        size = getsize(fname)
    except WindowsError as e:
        print e
        size = 0
    return size

def get_subdir_size(dirname,dirsize_data,isUpdate=False):
    totalsize = 0
    dirs = os.listdir(dirname)
    for each_dir in dirs:
        subdir = os.path.join(dirname,each_dir)
        if os.path.isdir(subdir):
            #if no record size , add it.
            if dirsize_data.has_key(subdir):
                orisize = dirsize_data.get(subdir)
            else:
                dirsize_data[subdir] = 0
                orisize = 0
            
            size = getdirsize(subdir)
            #if no size record, we need update the size
            if isUpdate:
                dirsize_data[subdir] = size
            totalsize += size
            if size != orisize:
                print 'There are %.3f' % ((size-orisize)/1024/1024), 'Mbytes in %s'%(subdir)
    return totalsize,dirsize_data

#KeyboardInterrupt


if __name__ == '__main__':
    dirsize_data = {}

    if os.path.exists('dirdata.json') is not True:
        w,dirsize_data = get_subdir_size(r'c:\windows',dirsize_data,True)
        w,dirsize_data = get_subdir_size(r'c:\users',dirsize_data,True)
        w,dirsize_data = get_subdir_size(r'c:\Program Files',dirsize_data,True)
        w,dirsize_data = get_subdir_size(r'c:\Program Files (x86)',dirsize_data,True)
        w,dirsize_data = get_subdir_size(r'c:\ProgramData',dirsize_data,True)
        output = json.dumps(dirsize_data)
        with open('dirdata.json','w') as f:
            f.write(output)
    else:
        with open('dirdata.json','r') as f:
            output = f.read()
            dirsize_data = json.loads(output)

    while True:
        w,dirsize_data = get_subdir_size(r'c:\windows',dirsize_data)
        u,dirsize_data = get_subdir_size(r'c:\users',dirsize_data)
        h = getsize_safe(r'c:\hiberfil.sys')
        pfiles,dirsize_data = get_subdir_size(r'c:\Program Files',dirsize_data)
        pfiles86,dirsize_data = get_subdir_size(r'c:\Program Files (x86)',dirsize_data)
        pdata,dirsize_data  = get_subdir_size(r'c:\ProgramData',dirsize_data)
        print '======summary======='
        print 'There are %.3f' % (w/1024/1024), 'Mbytes in c:\\windows'
        print 'There are %.3f' % (u/1024/1024), 'Mbytes in c:\\users'
        print 'There are %.3f' % (h/1024/1024), 'Mbytes in c:\\hiberfil.sys'
        print 'There are %.3f' % (pfiles/1024/1024), 'Mbytes in c:\\Program Files'
        print 'There are %.3f' % (pfiles86/1024/1024), 'Mbytes in c:\\Program Files (x86)'
        print 'There are %.3f' % (pdata/1024/1024), 'Mbytes in c:\\ProgramData' 
        print '============='
        time.sleep(60)

