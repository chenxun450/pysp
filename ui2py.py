import os
import os.path

dir = "./"

def list_ui_file():
    list = []
    files = os.listdir(dir)
    for filename in files:
        if os.path.splitext(filename)[1] == ".ui":
            list.append(filename)
    return list

def trans2py(filename):
    return os.path.splitext(filename)[0] + ".py"
    
def main():
    list = list_ui_file()
    for uifile in list:
        pyfile = trans2py(uifile)
        cmd = "pyuic5 -o {pyfile} {uifile}".format(pyfile=pyfile,uifile=uifile)
        os.system(cmd)

if __name__ == "__main__":
    main()
