# -*- coding: utf-8 -*-
"""
Created on Tue May  3 11:10:42 2022

@author: iant
"""

import re
import os
import posixpath
import ftplib
import platform

KERNEL_FTP = "spiftp.esac.esa.int"
KERNEL_FTP_PATH = "/data/SPICE/ExoMars2016/kernels"


if platform.system() == "Windows":
    PATH_LOCAL_SPICE_KERNELS = r"C:\Users\iant\Documents\DATA\local_spice_kernels\kernels"

else:
    PATH_LOCAL_SPICE_KERNELS = r"/bira-iasb/data/SATELLITE/TRACE-GAS-ORBITER/NOMAD/kernels"




ops = True #for operations
# ops = False #for planning


class MetakernelParser():

    def __init__(self, ops=False):
        self.ftp_connection = None
        self.remote_path = None
        self.local_path = None
        self.version_regex = None
        self.meta_regex = None
        self.path_regex = None
        self.dsk_regex = None
        self.remote_version = None
        
        self.ops = ops
        
        if ops:
            self.mk_name = "em16_ops.tm"
        else:
            #for planning
            self.mk_name = "em16_plan.tm"

    def openFTP(self, ftp_server):
        # Open an FTP connection with the specified server address.
        # Returns False if the connection failed.
        self.ftp_connection = ftplib.FTP(ftp_server)
        try:
            self.ftp_connection.login() # Anonymous
            return True
        except ftplib.all_errors as e:
            print("FTP error ({0})".format(e.message))
            return False

    def retrieve_FTP_file(self, src, dest):
        try:
            with open(dest, 'wb') as f:
                #folder, base = os.path.split(src)
                #self.ftp_connection.cwd(folder)
                #self.ftp_connection.retrbinary('RETR ' + base, f.write)
                self.ftp_connection.retrbinary('RETR ' + src, f.write)
            return True
        except ftplib.all_errors as e:
            os.remove(dest)
            print("FTP error ({0})".format(e.message))
            return False
        except IOError as e:
            print("IO error ({0})".format(e.message))
            return False

    def closeFTP(self):
        try:
            self.ftp_connection.close()
            print("FTP connection closed.")
        except ftplib.all_errors as e:
            print("FTP error ({0})".format(e.message))

    def set_kernel_remote(self, remote_path):
        # Point to the ExoMars2016 kernels folder on spiftp
        self.remote_path = remote_path

    def set_kernel_local_path(self, local_path):
        self.local_path = local_path

    def set_version_regex(self, regex_string):
        self.version_regex = re.compile(regex_string)

    def set_metakernel_regex(self, regex_string):
        self.meta_regex = re.compile(regex_string)

    def set_dsk_regex(self, regex_string):
        self.dsk_regex = re.compile(regex_string)

    def files_to_dict(self, filenames, regex):
        # Store a list of files in a dictionary, mapped by a key
        # derived from their filename using a regex.
        files_dict = {}
        for filename in filenames:
            res = regex.search(filename)
            if res:
                files_dict[res.group()] = filename
        return files_dict

    def latest_from_dict(self, files_dict):
        if files_dict:
            sorted_keys = sorted(files_dict.keys())
            return sorted_keys[-1]
        else:
            return None

    def get_latest_metakernel(self):
        # Compare the local metakernel version with the remote.
        # When out of date, move the old one to previous_versions and download
        # em16_ops.tm and em16_ops_vXXX_XXXXXXXX_XXX.tm
        # Returns True if the local version was updated.
        if not self.ftp_connection:
            print("No FTP connection.")
            return False
        else:
            print("Connection to {0} established.".format(self.ftp_connection.host))
            try:
                self.ftp_connection.cwd("/")
                self.ftp_connection.cwd(posixpath.join(self.remote_path,"mk"))
                remote_list = self.ftp_connection.nlst()
                rem_filt_dict = self.files_to_dict(remote_list, self.version_regex)
                self.remote_version = self.latest_from_dict(rem_filt_dict)
                print("Remote version is: {0}".format(self.remote_version))
                local_list = os.listdir(os.path.join(self.local_path,"mk"))
                loc_filt_dict = self.files_to_dict(local_list, self.version_regex)
                self.local_version = self.latest_from_dict(loc_filt_dict)
                print("Local version is: {0}".format(self.local_version))

                if (not self.local_version) or (self.remote_version > self.local_version):

                    self.retrieve_FTP_file(posixpath.join(self.remote_path,"mk",rem_filt_dict[self.remote_version]), os.path.join(self.local_path,"mk",rem_filt_dict[self.remote_version]))
                    self.retrieve_FTP_file(posixpath.join(self.remote_path,"mk",self.mk_name), os.path.join(self.local_path,"mk",self.mk_name))

                    if self.local_version:
                        os.rename(os.path.join(self.local_path,"mk",loc_filt_dict[self.local_version]), os.path.join(self.local_path,"mk","previous_versions",loc_filt_dict[self.local_version]))

                    print("Local version updated to {0}".format(self.remote_version))
                    self.replace_path()
                    self.insert_dsk()
                    print("Inserted DSK kernels into metakernel.")
                    return True
                else:
                    print("Local version unchanged. No action needed.")
                    return False

            except ftplib.all_errors as e:
                print("FTP error ({0})".format(e.message))
                return False

    def parse_metakernel(self):
        # Read the local em16_ops.tm copy and return a set kernels
        # in use for this version.
        latest_kernels = set()
        try:
            for line in open(os.path.join(self.local_path,"mk",self.mk_name)):
                res = self.meta_regex.search(line.rstrip('\n'))
                if res:
                    latest_kernels.add(posixpath.normcase(res.group()))
        except IOError as e:
            print("IO error ({0})".format(e.message))
        return set(sorted(latest_kernels))

    def replace_path(self):
        try:
            with open(os.path.join(self.local_path,"mk",self.mk_name)) as f:
                data = f.read()
            os.rename(os.path.join(self.local_path,"mk",self.mk_name), os.path.join(self.local_path,"mk","%s.bak" %self.mk_name))
            with open(os.path.join(self.local_path,"mk",self.mk_name), 'w') as f:
                print("Adding local path to metakernel")
                print 
                f.write(data.replace("( '..' )", "('"+self.local_path+"')")) #re sub doesn't work with windows paths
        except IOError as e:
            print("IO error ({0})".format(e.message))

    def insert_dsk(self):
        dsk_s = []
        dsk_path = os.path.join(self.local_path, "dsk")
        for i in os.scandir(dsk_path):
            if i.name.endswith(".bds"):
                dsk_s.append("                           " + "'" + posixpath.join('$KERNELS/dsk', i.name) + "'")
        dsk_str = '\n'.join(dsk_s) + '\n'
        try:
            # Maybe change to regex/string slicing approach
            f = open(os.path.join(self.local_path,"mk", self.mk_name))
            data_l = list(f)
            f.close()
            insert_pos = [i for i,x in enumerate(data_l) if "KERNELS_TO_LOAD" in x][0] + 1
            data_l.insert(insert_pos, dsk_str)
            f = open(os.path.join(self.local_path,"mk", self.mk_name), 'w')
            f.write("".join(data_l))
            f.close()
        except IOError as e:
            print("IO error ({0})".format(e.message))

    def get_local_tree(self):
        # Returns the directory tree relative to the local kernel path
        # as a set.
        local_files = set()
        try:
            for path, _, files in os.walk(self.local_path):
                for filename in files:
                    rel_path = os.path.relpath(path,self.local_path)
                    local_files.add(os.path.join(rel_path,filename))
        except IOError as e:
            print("IO error ({0})".format(e.message))
        return set(sorted(local_files))

    def update_kernels(self, local_tree, metakernel):
        # Download the missing kernel files to the local tree.
        files_to_download = metakernel.difference([s.replace("\\", "/") for s in local_tree])
        print("There are %i files to download" %len(files_to_download))
        for filename in files_to_download:
            if os.path.exists(os.path.normcase(os.path.join(self.local_path,filename))):
                print("Error: file already exists %s" %os.path.normcase(os.path.join(self.local_path,filename)))
            else:
                print(posixpath.join(self.remote_path,filename)+' --> '+os.path.normcase(os.path.join(self.local_path,filename)))
                self.retrieve_FTP_file(posixpath.join(self.remote_path,filename),os.path.normcase(os.path.join(self.local_path,filename)))

    def check_tree(self, dest):
        # Setup the kernel tree.
        tree = ['ck','ek','fk','ik','lsk','pck','sclk','spk','mk/previous_versions', 'dsk']
        for folder in tree:
            path = os.path.join(dest,folder)
            if not os.path.exists(path):
                print("Missing {0} folder in tree. Creating...".format(folder))
                os.makedirs(path)







META_PARSER_REGEX = "(?<=\'\$KERNELS/).*(?=\'$)"

if ops:
    META_VERSION_REGEX = "(?<=em16_ops_)*\d{4}(?:\.|-|_)?\d{2}(?:\.|-|_)?\d{2}(?=_\d{3}.tm$)"
else:
    META_VERSION_REGEX = "(?<=em16_plan_)*\d{4}(?:\.|-|_)?\d{2}(?:\.|-|_)?\d{2}(?=_\d{3}.tm$)"
    
parser = MetakernelParser(ops=ops)
print("Kernel update started.")
parser.check_tree(PATH_LOCAL_SPICE_KERNELS)
parser.set_kernel_local_path(PATH_LOCAL_SPICE_KERNELS)
print("Local path set to %s" %PATH_LOCAL_SPICE_KERNELS)
parser.set_kernel_remote(KERNEL_FTP_PATH)
print("Remote path set to %s on %s" %(KERNEL_FTP_PATH,KERNEL_FTP))

parser.set_version_regex(META_VERSION_REGEX)
parser.set_metakernel_regex(META_PARSER_REGEX)

if not parser.openFTP(KERNEL_FTP):
    print("FTP connection failed, aborting.")
else:
    parser.get_latest_metakernel()
    
    local_tree = parser.get_local_tree()
    print("\n\n")
    metakernel = parser.parse_metakernel()

    # print("##### Local files ####")
    # print([posixpath.normcase(s) for s in local_tree])
    # print("##### Metakernel files ####")
    # print(metakernel)
    
    files_to_download = metakernel.difference([s.replace("\\","/") for s in local_tree])
    
    parser.update_kernels(parser.get_local_tree(), parser.parse_metakernel())
    parser.closeFTP()
