#!/usr/bin/env python

import os, sys, re

import argparse

parser = argparse.ArgumentParser(description='Run LameStation games on your desktop!')
parser.add_argument('-L','--library', nargs=1, metavar='PATH', help='Path to Spin library directory')
parser.add_argument('-r','--run', action='store_true', help='Run your freshly compiled game')
parser.add_argument('objects', metavar='OBJECT', nargs='+', help='Spin files to convert to Python syntax')

args = parser.parse_args()

# Filter out non-spin, non-file arguments
filenames = [ i for i in args.objects if os.path.splitext(i)[1] == '.spin' or os.path.splitext(i)[1] == '.py' and os.path.isfile(i) ]

def run_game(filename):
    os.system("PYTHONPATH=sdk python "+filename)


def filter_comments(text):
    text = re.sub("{{(.*?)}}","",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("{(.*?)}","",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("'.*","",text)
    text = "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])

    return text

def filter_operators(text):
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

    # Add parentheses to function calls
    text[1] = re.sub("(\w+\.\w+)(?![.a-zA-Z_\(])","\g<1>()", text[1])

    # eat sub-object hashes
    text[1] = re.sub("(\w+)#(\w+)","\g<1>.\g<2>", text[1])

    # handle inc/dec operators
    text[1] = re.sub("(\w+)\+\+","\g<1> += 1", text[1])
    text[1] = re.sub("(\w+)--","\g<1> -= 1", text[1])

    text[1] = re.sub("(\w+\[.+?\])\+\+","\g<1> += 1", text[1])
    text[1] = re.sub("(\w+\[.+?\])--","\g<1> -= 1", text[1])

    # flow control
    text[1] = re.sub("(\s*)repeat([ \t]*)","\g<1>while True:", text[1])     # repeat


    text[1] = re.sub("(\s*if.*)[ \t]*","\g<1>:", text[1])     # repeat
    text[1] = re.sub("(\s*else.*)[ \t]*","\g<1>:", text[1])     # repeat

    indentlevel = len(text[1].split('\n')[0]) - len(text[1].split('\n')[0].lstrip())
    print indentlevel, text[1]

    # add function header
    header = "def " + title + ":\n"
    for t in temps:
        header += " "*indentlevel + t + " = 0\n"

    text[1] = header + text[1]

    return text[1]

def data(text):
    return ""

def variables(text):
    pat = re.compile('\n[\t\r\n ]*(byte|word|long)[ \t]*(\w+)')
    text = re.sub(pat,"\g<2> = None\n",text)
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

        if os.path.splitext(filename)[1] == '.py':
            run_game(filename)
            continue

        f = open(filename).read()

        f = filter_comments(f)

        textblock = split_into_blocks(f)

        # Zero out and initialize content variable
        content = {}
        for b in spinblocks.keys():
            content[b] = ""

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
        footer = open('footer.py','r').read()
        finalcontent = template + finalcontent + footer

        print "Output!"
        print "------------------------------------------"
        print finalcontent

        newfilename = os.path.basename(filename)+'.py'

        newfile = open(newfilename,'w')
        newfile.write(finalcontent)
        newfile.close()


        if args.run:
            run_game(newfilename)
