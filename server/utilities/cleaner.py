import os

def clear_temp_folder():
    mydir='static/images/temp'
    filelist = [ f for f in os.listdir(mydir)]
    for f in filelist:
        os.remove(os.path.join(mydir, f))
