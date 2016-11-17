#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
import os
import shutil

def files_in_dir_with_extension(path, ex):
    pathes = {}
    for root, dirs, files in os.walk(path):
        subfiles = os.listdir(root)
        for fn in subfiles:
            fpath = root + "/" + fn
            fextension = fn[fn.rfind('.'):]
            if os.path.isfile(fpath) and fextension == "." + ex:
                pathes[fn] = fpath
    return pathes

def run_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print(err)
    return out

def self_install(file, des):
    file_path = os.path.realpath(file)

    filename = file_path

    pos = filename.rfind("/")
    if pos:
        filename = filename[pos + 1:]

    pos = filename.find(".")
    if pos:
        filename = filename[:pos]

    to_path = os.path.join(des, filename)

    print("installing [" + file_path + "] \n\tto [" + to_path + "]")
    if os.path.isfile(to_path):
        os.remove(to_path)

    shutil.copy(file_path, to_path)
    run_cmd(['chmod', 'a+x', to_path])

    
def file_equal(f1, f2):
    fp1 = open(f1, "rb")
    c1 = fp1.read()
    fp1.close()
    
    fp2 = open(f2, "rb")
    c2 = fp2.read()
    fp2.close()
    
    if c1 == c2:
        return True
    else:
        return False

def __main__():

    # self_install
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        self_install("cpex.py", "/usr/local/bin")
        return

    if len(sys.argv) < 4:
        print("please use [extension] [src path] [des path] cmd to pass param")
        return
    
    extension = sys.argv[1]
    folder_src = sys.argv[2]
    if not os.path.isdir(folder_src):
        folder_src = os.path.join(os.getcwd(), folder_src)

    folder_des = sys.argv[3]
    if not os.path.isdir(folder_des):
        folder_des = os.path.join(os.getcwd(), folder_des)

    src_files = files_in_dir_with_extension(folder_src, extension)
    # print(src_files)
    
    for root, dirs, files in os.walk(folder_des):
        subfiles = os.listdir(root)
        for fn in subfiles:
            fpath = os.path.join(root, fn)
            src_path = src_files.get(fn, "")
            fextension = fn[fn.rfind('.'):]
            if os.path.isfile(fpath) and fextension == "." + extension:
                if src_path == "":
                    print("src not found: " + fpath[len(folder_des) + 1:])
                elif file_equal(src_path, fpath):
                    pass
                else:
                    print("updating " + fpath[len(folder_des) + 1:])
                    os.remove(fpath)
                    shutil.copy(src_path, fpath)
    
__main__();
