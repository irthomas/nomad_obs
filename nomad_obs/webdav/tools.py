# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:56:19 2024

@author: iant
"""

import os
import sys
import platform
import posixpath
import requests
from requests.auth import HTTPBasicAuth


import smtplib
from email.message import EmailMessage
# from smtplib import SMTP_SSL, SMTP_SSL_PORT


if platform.system() == "Windows":
    sys.path.append(r"X:\projects\NOMAD\Science\nomad-level1-pipeline")
    LOCAL_PATH = r"C:\Users\iant\Documents\DATA\temp\operations_webdav"
elif platform.system() == "Linux":
    sys.path.append(r"/bira-iasb/projects/NOMAD/Science/nomad-level1-pipeline/")
    LOCAL_PATH = r"/bira-iasb/projects/NOMAD/Science/Planning/operations_webdav/"

from nomad_ops.core.tools.passwords import passwords

# SC_FTP_ADR = "ftp-ae.oma.be"
# SC_FTP_USR = "nomad"
# SC_FTP_PWD = passwords["nomad_ftp"]
# FTP_PATH = r"/Operations/nomad_ops"

WEBDAV_USER = "nomad"
WEBDAV_PASSWORD = passwords["webdav_nomad"]
WEBDAV_URL = "https://webdav.aeronomie.be"
WEBDAV_ROOT_PATH = "/guest/nomad/"
WEBDAV_DATA_PATH = "Operations/nomad_ops"


EMAIL_RECIPIENTS = [
    # "ian.thomas@aeronomie.be",
    # "bojan.ristic@aeronomie.be",
    # "claudio.queirolo@aeronomie.be",
    # "nomad@aeronomie.be",
    # "nomad.iops@aeronomie.be",
    "nomad-ops@lists.aeronomie.be",
]
EMAIL_SUBJECT = "New files are available on WebDAV"


# def open_ftp(server_address, username, password):
#     # Open an FTP connection with specified credentials
#     success = False
#     # keep trying until ftp is opened successfully
#     while success is False:
#         ftp_conn = ftplib.FTP(server_address, timeout=90)
#         try:
#             ftp_conn.login(user=username, passwd=password)
#         except ftplib.all_errors as e:
#             print("FTP error:", str(e))
#         else:
#             # break the while loop
#             success = True
#     return ftp_conn


# def dir_list(ftp_conn, path):
#     # Return a list of all files and subdirs in specified path (non-recursive)
#     dirs = []
#     files = []
#     try:
#         dir_cont = ftp_conn.mlsd(path)
#     except ftplib.all_errors as e:
#         print("FTP error ({0})".format(e.message))
#     for i in dir_cont:
#         if i[1]['type'] == "dir":
#             dirs.append(i[0])
#         elif i[1]['type'] == "file":
#             files.append(i[0])
#     return (dirs, files)

def dir_list(path, full_path=False):
    # Return a list of all files and subdirs in specified path (non-recursive)
    search_path = WEBDAV_URL + WEBDAV_ROOT_PATH + path + "/"
    # print(search_path)
    
    dirs = []
    files = []
    headers = {"Depth": "1"}
    response = requests.request(method="PROPFIND", url=search_path, auth=HTTPBasicAuth(WEBDAV_USER, WEBDAV_PASSWORD), headers=headers)
    resp_lines = response.content.decode().split()
    loop = 0
    for resp_line in resp_lines:
        if "<D:href>" in resp_line:
            dir_or_file = resp_line.replace("<D:href>%s" % WEBDAV_ROOT_PATH, "").replace("</D:href>", "")
            if loop > 0: # first result is always current directory
                if dir_or_file[-1] == "/":
                    if full_path:
                        dirs.append(dir_or_file[:-1])
                    else:
                        dirs.append(os.path.basename(dir_or_file[:-1]))
                else:
                    if full_path:
                        files.append(dir_or_file)
                    else:
                        files.append(os.path.basename(dir_or_file))
            loop += 1

    return (dirs, files)


# def ftp_walk(ftp_conn, path):
#     # Recursively scan FTP starting from path
#     (dirs, files) = dir_list(ftp_conn, path)
#     yield (path, dirs, files)
#     for i in dirs:
#         path = posixpath.join(path, i)
#         yield from ftp_walk(ftp_conn, path)
#         path = posixpath.dirname(path)

def webdav_walk(path):
    # Recursively scan WEBDAV starting from path
    (dirs, files) = dir_list(path)
    yield (path, dirs, files)
    for i in dirs:
        path = posixpath.join(path, i)
        yield from webdav_walk(path)
        path = posixpath.dirname(path)


# def get_remote_list(ftp_conn, path):
#     # Return a flat list containing all paths present on the FTP
#     file_list = []
#     # print("Getting list of files on ftp")
#     for i in ftp_walk(ftp_conn, path):
#         if not i[1]:  # if not a directory
#             file_list += [posixpath.join(i[0], j) for j in i[2]]
#     return file_list

def get_remote_list(path, relative=False):
    # Return a flat list containing all paths present on the WEBDAV
    file_list = []
    for i in webdav_walk(path):
        if not i[1]:
            if relative:
                file_list += [posixpath.relpath(posixpath.join(i[0], j), path) for j in i[2]]
            else:
                file_list += [posixpath.join(i[0], j) for j in i[2]]
    return file_list


# def get_ftp_md5(ftp, remote_path):
#     m = hashlib.md5()
#     ftp.retrbinary('RETR %s' % remote_path, m.update)
#     return m.hexdigest()


def make_local_path(remote_path):

    rel_path = remote_path.split(posixpath.sep)
    local_path = os.path.join(os.path.normpath(LOCAL_PATH), *rel_path[2:]) # 2 for webdav, 3 for ftp
    return local_path


# def get_remote_file_info(ftp_conn, remote_paths):
#     file_dict = {}
#     for remote_path in remote_paths:
#         md5 = get_ftp_md5(ftp_conn, remote_path)
#         _type = remote_path.split(posixpath.sep)[3]
#         local_path = make_local_path(remote_path)
#         file_dict[remote_path] = {"type": _type, "local_path": local_path, "remote_md5": md5}
#     return file_dict

def get_remote_file_info(remote_paths):

    file_dict = {}
    for remote_path in remote_paths:
        md5 = "" # no MD5 on webdav
        _type = remote_path.split(posixpath.sep)[2] # 2 for webdav, 3 for ftp
        local_path = make_local_path(remote_path)
        file_dict[remote_path] = {"type": _type, "local_path": local_path, "remote_md5": md5}

    return file_dict


# def get_ftp_file_dict():
#     ftp_conn = open_ftp(SC_FTP_ADR, SC_FTP_USR, SC_FTP_PWD)
#     ftp_filepaths = get_remote_list(ftp_conn, FTP_PATH)
#     ftp_file_dict = get_remote_file_info(ftp_conn, ftp_filepaths)
#     return ftp_file_dict


def get_webdav_file_dict():

    webdav_filepaths = get_remote_list(WEBDAV_DATA_PATH)

    webdav_file_dict = get_remote_file_info(webdav_filepaths)
    return webdav_file_dict


# def copy_file_from_ftp(remote_path, local_path):
#     ftp_conn = open_ftp(SC_FTP_ADR, SC_FTP_USR, SC_FTP_PWD)
#     print("Copying file from %s to %s" % (remote_path, local_path))
#     with open(local_path, 'wb') as f:
#         ftp_conn.retrbinary('RETR %s' % remote_path, f.write)

def make_webdav_path(paths):
    return WEBDAV_URL + posixpath.join(WEBDAV_ROOT_PATH, posixpath.join(*[posixpath.normcase(path) for path in paths]))

def download_file(local_filepath, webdav_path):
    
    webdav_full_path = make_webdav_path([webdav_path])

    print("PUT (download) filepath:", webdav_full_path, "to:", local_filepath)
    response = requests.get(webdav_full_path, auth=HTTPBasicAuth(WEBDAV_USER, WEBDAV_PASSWORD))
    if response.ok:
        with open(local_filepath, 'wb') as f:
            f.write(response.content)
        print("File transferred successfully to webdav")
    else:
        print("Webdav download error:", response)


def get_orbit_plan_path(mtp):

    return os.path.join(LOCAL_PATH, "orbit_plans", mtp, "nomad_%s_plan.csv" % mtp)


def send_bira_email(subject, body, to=EMAIL_RECIPIENTS, print_output=False):

    # write email
    _from = "ian.thomas@aeronomie.be"

    if print_output:
        print("From:", _from)
        print("To:", ",".join(EMAIL_RECIPIENTS))
        print(subject)

    # set up email server
    message = EmailMessage()
    message["From"] = _from
    message["To"] = to
    message["Subject"] = subject

    message.set_content(body, 'html')

    try:

        with smtplib.SMTP_SSL("smtp-proxy.oma.be", port=smtplib.SMTP_SSL_PORT) as server:
            if print_output:
                server.set_debuglevel(1)
            server.login("iant", passwords["hera"])
            server.send_message(message)
            server.quit()
            print("Email sent")
    except Exception as e:
        print("Error sending email", e)


def email_summary(h, to=EMAIL_RECIPIENTS, subject=EMAIL_SUBJECT, print_output=False):
    send_bira_email(subject, h, to=to, print_output=print_output)
