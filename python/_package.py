import zipfile
import os
import re

ARCHIVENAME = "../aws_aseag_py.zip"

corefiles = ['aseag_api',
             'aseag_data', 
             'bus_appdef', 
             'bus_gui', 
             'bus_handler',
             'bus_nlg', 
             'bus_response',
             'bus_userprofile'
            ]

myaskdir = "./myask"
myaskfiles = ['__init__', 
              'myask_alexaout', 
              'myask_appdef', 
              'myask_dynamodb',
              'myask_localtest',
              'myask_log', 
              'myask_slots'
            ]

libs = ['requests'] 


def addFolderToZip(zipfile,folder,directory):
    path=os.path.join(directory,folder)
    file_list=os.listdir(path)
    for file_name in file_list:
        file_path=os.path.join(path,file_name)
        if os.path.isfile(file_path):
            addfile(zipfile, file_path)
        elif os.path.isdir(file_path):
            print "----> sub directory found '"+ file_path + "'----"
            addFolderToZip(zipfile,file_name,path)
        else:
            print "!!!! other found!!!!"
            addFolderToZip(zipfile,file_name,path)
           

def addfile(archive, filename, archive_name=""):
    
    if archive_name == "": archive_name= filename
    if re.match(".*\.pyc$", filename):
        print "  --ignoring '" + filename +"'"
    else:
        print "  ++adding '" + filename+"' as '"+archive_name+"'"
        archive.write(filename, arcname=archive_name)
   
print 'creating archive '  +ARCHIVENAME
zf = zipfile.ZipFile(ARCHIVENAME, mode='w')
try:
    for filename in corefiles:
        addfile(zf, filename+'.py')

    for filename in myaskfiles:
        addfile(zf, myaskdir+'/'+filename+'.py','myask/'+filename+'.py')

    for libdir in libs:
        print "Adding library folder " + libdir
        addFolderToZip(zf, libdir,".")
finally:
    print 'closing'
    zf.close()

