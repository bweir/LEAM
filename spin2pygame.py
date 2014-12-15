#!/usr/bin/env python

import os, sys, re

import argparse
import getpass

import xmlrpclib


parser = argparse.ArgumentParser(description='Generate Confluence API listing from Spin files.')
parser.add_argument('-L','--library', nargs=1, metavar='PATH', help='Path to Spin library directory')
parser.add_argument('objects', metavar='OBJECT', nargs='+', help='Spin files to convert to Python syntax')

args = parser.parse_args()

# Filter out non-spin, non-file arguments
filenames = [ i for i in args.objects if os.path.splitext(i)[1] == '.spin' and os.path.isfile(i) ]

def filter_comments(text):
#    text = re.sub("{{.*?}}","",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("{{(.*?)}}","",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("{(.*?)}","",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("'.*","",text)
    text = "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])

    return text

def filter_operators(text):
#    text = re.sub("=(?![=\w ])",":=",text)
    text = re.sub(":=","=",text)

    return text

def function(text):
    text = text.split('\n',1)
    prototype = text[0]
    if ':' in prototype:
        if '|' in prototype:
            title = prototype.split('[:|]')[0]
            alias=  prototype.split('[:|]')[1]
            temp =  prototype.split('[:|]')[2]
        else:
            title = prototype.split(':')[0]
            alias = prototype.split(':')[1]
            temp =  ""
    else:
        alias = ""
        if '|' in prototype:
            title = prototype.split('|')[0]
            temp =  prototype.split('|')[1]
        else:
            temp = ""
            title = prototype
    temps = re.findall(r"[\w]+",temp)


    title = title.strip()
    alias = alias.strip()

    print title
    print "  ",alias
    print "  ",temps

    # Fix aliases
    if not alias == "":
        text[1] = re.sub(alias,"result",text[1])
    text[1] = filter_operators(text[1])

    # Fix parameters
    if not re.search("\(.*\)", title):
        title += '()'

    #text[1] = "def " + title + ":\n" + text[1]
    text[1] = "def " + title + ":\n" + "    return true"

    return text[1]

def data(text):
    return ""

def variables(text):
    return text

def constants(text):
    text = re.sub("\n[\t\r\n ]*","\n",text)
    return text

def objects(text):
    print text
    text = re.sub("\n[\t ]*(.*)[\t ]*:[ \t]*\"(.+?)\"","\nimport \g<2> as \g<1>",text)
    text = re.sub("/",".",text)
    return text

spinblocks = {
    'PUB' : function,
    'PRI' : function,
    'DAT' : data,
    'VAR' : variables,
    'CON' : constants,
    'OBJ' : objects,
}
 


def split_into_blocks(text):
    return filter(None, re.split('(\nPUB)|(\nDAT)|(\nPRI)|(\nVAR)|(\nCON)|(\nOBJ)',text))


# Only do anything if files are valid
if not filenames:
    print "No valid files selected"
else:

    for filename in filenames:

        f = open(filename).read()

        f = filter_comments(f)

        textblock = split_into_blocks(f)


        # Zero out and initialize content variable
        content = {}
        for b in spinblocks.keys():
            content[b] = ""

        print spinblocks.keys()

        # See if code starts with named block or comments
#        if textblock[0].split('\n')[1] in spinblocks.keys():
#            startpoint = 0
#        else:
#            startpoint = 1

        # Process and render output for individual sections
        n = len(textblock)
        r = range(n)

        ## This code assumes that there is code before your main code
        for i in r[1::2]:
            label = textblock[i].split('\n')[1]

            print label
            if label in spinblocks.keys():
                content[label] += spinblocks[label](textblock[i+1])
                content[label] += "\n\n"

            
            
        # Final Formatting

        # Assemble pieces into final page for upload
        finalcontent = ""
        finalcontent += content['OBJ']
        finalcontent += content['CON']
        finalcontent += content['VAR']
        finalcontent += content['PRI']
        finalcontent += content['PUB']
        finalcontent += content['DAT']


        # add boiler plate
        template = open('template.py','r').read()
        finalcontent = template + finalcontent

        print "Output!"
        print "------------------------------------------"
        print finalcontent

        newfile = open(os.path.basename(filename)+'.py','w')
        newfile.write(finalcontent)
        newfile.close()
