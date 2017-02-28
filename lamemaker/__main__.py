import click

import os
import re
import stat
import sys
import sh

firstfunction = None

def write_game(text, filename):
    f = open(filename,'w')
    f.write(text)
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IEXEC)
    f.close()

def run_game(libraries, filename):
    libraries = ":".join(libraries)
    os.system("PYTHONPATH="+libraries+" python "+filename)

def match_log(level, line):
    return re.match(r'^\w+:\s*\d+\s+'+level, line)

def color_log(app, line):
    line = app+": "+line.rstrip()
    if match_log('INFO',line):
        return click.style(line, bold=True, fg='green')
    elif match_log('WARNING',line):
        return click.style(line, bold=True, fg='yellow')
    elif match_log('ERROR',line):
        return click.style(line, bold=True, fg='red')
    else:
        return click.style(line, fg='green')

def build_game(libraries, filename):
    paths = []
    for library in libraries:
        paths += ['-p',library]
    for line in sh.pyinstaller(paths+[filename,'--onefile'],
            _err_to_out=True, _iter=True):
        click.echo(color_log('pyinstaller', line))

    os.remove(os.path.join(os.getcwd(), os.path.basename(os.path.splitext(filename)[0]+'.spec')))

def filter_comments(text):
    text = re.sub("{{(.*?)}}","",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("{(.*?)}","",text, flags=re.MULTILINE|re.DOTALL)
    text = re.sub("'.*","",text)
    text = re.sub("(?<=\d)_(?=\d)","",text)                           # remove underscores in numbers
    text = "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])
    text = "\n" + text

    return text

def filter_operators(text):
    text = re.sub(":=","=",text)
    text = re.sub("//","%",text)
    text = re.sub("=>",">=",text)
    text = re.sub("=<","<=",text)
    text = re.sub("@","",text)

    return text

def function(text, label):
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

    if label == 'PUB':
        global firstfunction
        if firstfunction == None:
            firstfunction = title

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
    text[1] = re.sub("(\s*)repeat[ \t]*\n","\g<1>while True:\n", text[1])    # repeat
    text[1] = re.sub("(\s*)repeat[ \t]+(\w+)[ \t]+from[ \t]+(.+)[ \t]+to[ \t]+(.+)[ \t]*\n","\g<1>for \g<2> in range(\g<3>, \g<4>):\n", text[1])    # repeat from to
    text[1] = re.sub("(\s*)until[ \t]+(.*)[ \t]*\n","\g<1>    if \g<2>\g<1>        break\n", text[1])   # until


    text[1] = re.sub("(\s*if.*)[ \t]*","\g<1>:", text[1])     # repeat
    text[1] = re.sub("(\s*else.*)[ \t]*","\g<1>:", text[1])     # repeat

    # miscellaneous
    text[1] = re.sub("(\w+)\?","random.getrandbits(32)",text[1])        # random
    text[1] = re.sub("\$([0-9A-Fa-f]+)","int(\"0x\g<1>\",0)",text[1])   # hex
    text[1] = re.sub("string\((.*?)\)","\g<1>",text[1])                 # string
    text[1] = re.sub("\",[ \t]*10[ \t]*,\"","\\\n",text[1])             # newlines

    text[1] = re.sub("cnt","0",text[1])


    indentlevel = len(text[1].split('\n')[0]) - len(text[1].split('\n')[0].lstrip())
#    print indentlevel, text[1]

    # add function header
    header = "def " + title + ":\n"
    for t in temps:
        header += " "*indentlevel + t + " = 0\n"

    text[1] = header + text[1]

    return text[1]

def data(text, label):
    return ""

def variables(text, label):
    pat = re.compile('\n[\t ]*(byte|word|long)[ \t]+(\w+)\[(.+?)\].*')
    text = re.sub(pat,"\n\g<2> = [0]*\g<3>",text)
    pat = re.compile('\n[\t ]*(byte|word|long)[ \t]+(\w+).*')
    text = re.sub(pat,"\n\g<2> = None",text)

    return text

def constants(text, label):
    text = re.sub("[\t ]*(.*)","\g<1>",text)

    text = re.sub("[\t ]*_clkmode(.*)","",text)
    text = re.sub("[\t ]*_xinfreq(.*)","",text)
    return text

def objects(text, label):
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

def compile(libraries, filename, run=False):

    f = open(filename).read()

    f = filter_comments(f)

    textblock = split_into_blocks(f)

    # Zero out and initialize content variable
    content = {}
    for b in spinblocks.keys():
        content[b] = ""

    ## This code assumes that there is code before your main code
    for i in xrange(0,len(textblock)-1,2):
        label = textblock[i].split('\n')[1]
        #print label
        if label in spinblocks.keys():
            content[label] += spinblocks[label](textblock[i+1], label)
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
    templatedir = os.path.join(os.path.dirname(__file__),'templates')
    template = open(os.path.join(templatedir, 'game.py'),'r').read()
    footer = open(os.path.join(templatedir,'footer.py'),'r').read()
    out =  template
    out += finalcontent 
    out += "\n" + firstfunction + "()\n"
    out += footer

    return out

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--library', '-L', metavar='PATH', multiple=True, type=str, help='path to spin library directory')
@click.option('--dump', '-d', is_flag=True, help='print generated file')
@click.option('--run', '-r', is_flag=True, help='run compiled game')
@click.option('--build', '-b', is_flag=True, help='build standalone binary')
@click.option('--output','-o',metavar='PATH', type=click.Path(), default=os.path.join(os.getcwd(),'out'), help='output directory of resulting game')
@click.argument('filename', type=click.Path(exists=True))
def cli(library, dump, run, build, output, filename):
    """Run LameStation games on the desktop."""

    libraries = list(library)
    libraries.insert(0, u'.')
    out = compile(libraries, filename, True)

    output = os.path.realpath(output)

    print output
    if os.path.exists(output):
        click.confirm("Are you sure you want to overwrite this directory?")

    if dump:
        print out

    newfilename = os.path.splitext(filename)[0]+'.py'
    write_game(out, newfilename)

    if run:
        run_game(libraries, newfilename)

    if build:
        build_game(libraries, newfilename)

    os.remove(newfilename)

if __name__ == '__main__':
    cli()
