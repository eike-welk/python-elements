#!/usr/bin/python

# adds comments to the reference files
# [[comment [identifier]]]

from sys import argv
from sys import exit
from os import system

from urllib2 import urlopen

testonly = False

if len(argv) < 2:
    print "please add filename of reference html"
    exit(0)

if len(argv) == 3:
	testonly = True

print testonly

blueprint = open("comment_blueprint.html").read().strip()
blueprint_onlyadd = open("comment_blueprint_onlyadd.html").read().strip()

c = open(argv[1]).read().strip()

c_orig = c

comments = []
while "[[comment" in c:
    x = c[c.index("[[comment"):c.index("]]")+2]
    c = c[c.index("]]")+2:]

    # get comments    
    s = x.replace("[[comment", "").replace("]]", "").strip()
    
    if testonly:
        c_arr = []
        comments = ""
    else: 
        url = "http://linuxuser.at/elements/doc/comments.php?action=get_comment&t=%s" % s
        comments = urlopen(url).read().strip()
        c_arr = comments.split("\n")
        if c_arr[0].strip() == "":
            c_arr.pop(0)
        
        comments = ""
        for cc in c_arr:
            cc_arr = cc.split("|||")
            comments = "%s\n<tr><th>%s (%s)</th></tr>\n<tr><td>%s</td></tr>\n" % (comments, cc_arr[0], cc_arr[2], cc_arr[1])

    if len(c_arr) > 0:    
        out = blueprint.replace("##name##", s)
    else:
        out = blueprint_onlyadd.replace("##name##", s)
    
    out = out.replace("##count##", str(len(c_arr)))
    out = out.replace("##comments##", comments)
    #print comments
    
    c_orig = c_orig.replace(x, out)
    c_orig = c_orig.replace("<ul>", "<ul class='ul1'>")
    c_orig = c_orig.replace("<ul>", "<ul class='ul1'>")
    
if testonly:
    f = open("../test.html", "w")
    f.write(c_orig)
    f.close()
    system("firefox-bin ../test.html")
    system("rm ../test.html")
    
else:
    print c_orig
