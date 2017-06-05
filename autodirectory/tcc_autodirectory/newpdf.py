#!/usr/bin/env python
import sys
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter
import os

# main
def main(args, output_path):
    import getopt
    if not args: 
        return "Pass the directory that you want to parse the files"
    # debug option
    file_titles = [f for f in os.listdir(args) if os.path.isfile(os.path.join(args,f))]
    debug = 0
    # input option
    password = ''
    pagenos = set()
    maxpages = 0
    # output option
    outfile = None
    outtype = None
    imagewriter = None
    rotation = 0
    stripcontrol = False
    layoutmode = 'normal'
    codec = 'utf-8'
    pageno = 1
    scale = 1
    caching = True
    showpageno = True
    laparams = LAParams()
    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFPageInterpreter.debug = debug
    #
    rsrcmgr = PDFResourceManager(caching=caching)

    for fname in file_titles:
        if fname.split('.')[1] == "pdf" and fname.split('.')[0] + '.txt' not in os.listdir(output_path):
            outfile = fname.strip(".pdf")
            if not outtype:
                outtype = 'text'
                if outfile:
                    if outfile.endswith('.htm') or outfile.endswith('.html'):
                        outtype = 'html'
                    elif outfile.endswith('.xml'):
                        outtype = 'xml'
                    elif outfile.endswith('.tag'):
                        outtype = 'tag'
            if outfile:
                print(output_path + "/" + outfile)
                outfp = open(output_path + "/" + outfile + ".txt", 'w')
            else:
                outfp = sys.stdout
            
            if outtype == 'text':
                device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                                       imagewriter=imagewriter)
            else:
                print('else')
                return "Pass the path that you want to parse"

            fp = open(args + "/" + fname, 'rb')
            
            try:
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                for page in PDFPage.get_pages(fp, pagenos,
                                              maxpages=maxpages, password=password,
                                              caching=caching, check_extractable=True):
                    page.rotate = (page.rotate+rotation) % 360
                    interpreter.process_page(page)
            except:
                print("Exception occured on PDF process")
                fp.close()
                device.close()
                outfp.close()                

            fp.close()
            device.close()
            outfp.close()
    return

main('/home/lucas/pdf_files', '/home/lucas/result_files')
