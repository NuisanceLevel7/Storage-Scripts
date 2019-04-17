#!/usr/bin/python

import re,os,time,datetime,subprocess,sys,base64,random
import os.path, datetime
from shutil import copyfile
import requests
import json
import yaml
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DateString:

    def __init__(self):
        self.yesterday = str(datetime.date.fromtimestamp(time.time() - (60*60*24) ).strftime("%Y-%m-%d"))
        self.today = str(datetime.date.fromtimestamp(time.time()).strftime("%Y-%m-%d"))
        self.tomorrow = str(datetime.date.fromtimestamp(time.time() + (60*60*24) ).strftime("%Y-%m-%d"))
        self.now = str(time.strftime('%X %x %Z'))


class Files:

    def __init__(self):
        self.dir = ''
        self.data = []
        self.file_exists = 0

    def mkdir(self,dir):
        if not os.path.isdir(dir):
            subprocess.call(["mkdir", dir])
        if os.path.isdir(dir):
            return True
        return False

    def write_file(self,filename,list):
        f = open(filename,'w')
        for line in list:
            f.write(line + '\n')
        f.close()

    def write_file_append(self,filename,list):
        f = open(filename,'a')
        for line in list:
            f.write(line)
        f.close()

    def write_log(self,logfile,logentry):
        f = open(logfile,'a')
        reportDate =  str(time.strftime("%x - %X"))
        f.write(reportDate + " :" + logentry)
        f.close()

    def read_file(self,filename):
        self.data = []
        self.file_exists = 1
        # Testing if file exists.
        if os.path.isfile(filename):
            try:
                f = open(filename,'r')
            except IOError:
                print("Failed opening ", filename)
                sys.exit(2)
            for line in f:
                line = line.strip()
                self.data.append(line)
                f.close()
            return self.data     
        else:
            # Set the file_exists flag in case caller cares.
            self.file_exists = 0

    def copy_file(self,src, dest):
        try:
            copyfile(src, dest)
        except IOError:
            print("Failed file copy ", src,dest)
            sys.exit(2)

    
    def stat_file(self,fname):
        blocksize = 4096
        hash_sha = hashlib.sha256()
        f = open(fname, "rb")
        buf = f.read(blocksize)
        while 1:
            hash_sha.update(buf)
            buf = f.read(blocksize)
            if not buf:
                break    
        checksum =  hash_sha.hexdigest()
        filestat = os.stat(fname)
        filesize = filestat[6]
        return checksum,filesize



class Tools:

    def __init__(self):
        self.version = '1'    
        self.today = datetime.datetime.today().strftime('%Y-%m-%d-%H%M-%S')

    def decode_vmax(self,naa):
        ldev = naa[-8:]
        sn   = naa[-16:]
        ser  = sn[0:4]
        a = self.hex_decode(ldev[0:2])
        b = self.hex_decode(ldev[2:4])
        c = self.hex_decode(ldev[4:6])
        d = self.hex_decode(ldev[6:8])
        ldev = a + b + c + d
        return 'Symm' + ser + '_' + ldev

    def hex_decode(self,code):
        key = code[0:1]
        key = int(key.strip())
        bit = code[-1:]
        bit = bit.strip()
        if key > 3:
            bit = int(bit)
            bit += 9
            bit = hex(bit)
            bit = bit[-1:]
        return bit

    def archive_file(self,datafile):
        archive = datafile + '_' + self.today + '.old'
        if os.path.isfile(datafile):
            os.rename(datafile, archive)


