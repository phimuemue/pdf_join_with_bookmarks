import sys
import os
import re

from pyPdf import PdfFileReader


def countPages(filename):
    f = PdfFileReader(file(filename, "rb"))
    return f.getNumPages()

## retrieve information about all the single pdf files
pagenumbers = []
parts = []
for f in sys.argv[1:]:
    print "Opening %s"%(f)
    os.system("./mbtPdfAsm -M%s -gO > %s.outline"%(f,f))
    ## format: auto-increment no., parent, some reference (?!), page no.
    parts.append([])
    currentpart = parts[-1]    
    ol = open(f+".outline")
    for l in ol:
        if (l.strip() != ";"):
            currentpart.append(l.split(" ", 4))
            currentpart[-1][-1] = currentpart[-1][-1].strip()    
    print "counting pages in %s"%(f)
    pnr = countPages(f)
    print "%s has %d pages"%(f, pnr)
    pagenumbers.append(pnr)

## adjust bookmark numbers
bookmarkcount = 0
pagecount = 0
for (i,p) in enumerate(parts):
    for bm in p:
        ## auto-increment
        bm[0] = str(int(bm[0]) + bookmarkcount) 
        ## parent
        if (bm[1] != "0"):
            bm[1] = str(int(bm[1]) + bookmarkcount) 
        ##bm[2] = str(int(bm[2]) + bookmarkcount) 
        bm[3] = str(int(bm[3]) + pagecount)
    bookmarkcount = bookmarkcount + len(p)
    pagecount = pagecount + pagenumbers[i]

## export outline in appropriate format
f = open("outline.outline", "w")
for p in parts:
    for bm in p:
        f.write(" ".join(bm)+"\n")
f.close()

## combine pdf files ...
print "Combining single files into one file."
os.system("pdfjoin --rotateoversize 'false' --outfile complete.pdf " + str(" ".join(sys.argv[1:])))

## and apply bookmarks
os.system("./mbtPdfAsm -mcomplete.pdf -dcomplete_with_bookmarks.pdf -ooutline.outline")

## print parts
