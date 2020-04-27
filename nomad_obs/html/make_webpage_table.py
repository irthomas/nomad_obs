# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:38:48 2020

@author: iant
"""
import os
    

def writeHtmlTable(html_page_name, html_title, html_header, html_rows, paths, linkNameDesc="", extraComments=[]):
    """make html observation file"""
#    global HTML_PATHS

    h = r""
    h += r"<h1>%s</h1>" %html_title +"\n"
    if linkNameDesc != "":
        pagename = linkNameDesc[0]
        desc = linkNameDesc[1]
        h += r"<p><a href=%s>%s</a> - %s</p>" %(pagename, pagename, desc) +"\n"

    for extraComment in extraComments:
        h += r"<p>%s</p>" %(extraComment) +"\n"

    h += r"<div style='white-space:pre;overflow:auto;width:2000px;padding:10px;'>"
    h += r"<table border=1 style='width:2000px;'>"+"\n"

    h += r"<tr>"+"\n"
    for headerColumn in html_header:
        h += r"<th>%s</th>" %headerColumn +"\n"
    h += r"</tr>"+"\n"

    for row in html_rows:
        if row[-1] == "":
            h += r"<tr>"+"\n"
        else:
            h += r"<tr bgcolor='#%s'>" %row[-1]+"\n"

        for element in row[0:-1]:
            h += r"<td>%s</td>" %(element) +"\n"
        h += r"</tr>"+"\n"
    h += r"</table>"+"\n"
    h += r"</div>"

    f = open(os.path.join(paths["HTML_MTP_PATH"], html_page_name+".html"), 'w')
    f.write(h)
    f.close()


