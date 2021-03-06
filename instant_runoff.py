#!/usr/bin/python

import cgi
import email
import email.mime.multipart
import email.mime.text
import os
import re
import subprocess
import sys

def groff_txt(input, grotty_flags="-fc", encoding="ascii"):
    'Convert Groff into plain text'
    p = subprocess.Popen(
        ['groff', '-T%s' % (encoding), '-t', '-ms', '-P', grotty_flags],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate(input)

    if p.returncode != 0:
        raise RuntimeError()

    if stderr:
        raise RuntimeError(repr(stderr))

    return stdout

def groff_html(input):
    'Convert Groff into HTML'
    htxt = groff_txt(input, grotty_flags="-f", encoding="ascii")
    out = _groffToQuoteHTMLUnquote(htxt)
    return out

def _mk_escape_pattern(start, end):
    return r'\x1b\[%s([^\x1b]+)\x1b\[%s' % (start, end)

def _groffToQuoteHTMLUnquote(stdout):
    """Postprocess groff text output to "HTML"."""

    stdout = cgi.escape(stdout)

    quoteHTMLunquote = "<pre>%s</pre>" % (stdout)
    typewriter = [
        (_mk_escape_pattern('1m', '0m'), r'<b>\1</b>'),
        (_mk_escape_pattern('1m', '22m'), r'<b>\1</b>'),
        (_mk_escape_pattern('4m', '24m'), r'<i>\1</i>'),
        (_mk_escape_pattern('4m', '0m'), r'<i>\1</i>')]

    for (pattern, repl) in typewriter:
        quoteHTMLunquote = re.sub(
            pattern, repl, quoteHTMLunquote)

    return quoteHTMLunquote

def sendmail(msg, args=[]):
    p = subprocess.Popen(
        ["/usr/lib/sendmail"] + args,
        stdin=subprocess.PIPE)
    (stdout, stderr) = p.communicate(msg)
    if p.returncode != 0:
        raise RuntimeError()



def compose(body):
    mail = email.message_from_string(body)
    input = mail.get_payload()
    txt = groff_txt(input)
    htxt = groff_txt(input, grotty_flags="-f", encoding="ascii")
    html = _groffToQuoteHTMLUnquote(htxt)

    alt = email.mime.multipart.MIMEMultipart('alternative')
    alt.attach(email.mime.text.MIMEText(txt, 'plain'))
    alt.attach(email.mime.text.MIMEText(html, 'html'))
    alt.attach(email.mime.text.MIMEText(input, 'x-groff-ms'))
    #mail.set_payload(alt)
    #mail.attach(alt)
    #print mail.as_string()

    for fname in mail.keys():
        for fvalue in mail.get_all(fname):
            alt.add_header(fname, fvalue)

    return alt

USAGE = '%s [--help|--preview] sendmail-args' % sys.argv[0]
def main():
    dir = os.path.expanduser('~/.cache/instant-runoff')
    if len(sys.argv) == 1:
        print USAGE
        exit(1)
    elif sys.argv[1] == '--help':
        print USAGE
        exit(0)
    elif sys.argv[1] == "--preview":
        print groff_txt(sys.stdin.read())
        return
    elif sys.argv[1] == "--html":
        print groff_html(sys.stdin.read())
        return

    try:
        os.makedirs(dir)
    except OSError:
        # Fuck you, Python.
        pass

    #input = sys.stdin.read()
    #process(input)

    #save(alt.as_string(), 'out.alt')

    mail = email.message_from_string(sys.stdin.read())

    #tty = file('/dev/tty')
    #print >>tty, 'Really send? [y/n] ',
    #tty.flush()
    #c = tty.readline()
    #print >>tty, c
    #tty.flush()

    input = mail.get_payload()
    txt = groff_txt(input)
    htxt = groff_txt(input, grotty_flags="-f", encoding="ascii")
    html = _groffToQuoteHTMLUnquote(htxt)

    alt = email.mime.multipart.MIMEMultipart('alternative')
    alt.attach(email.mime.text.MIMEText(txt, 'plain'))
    alt.attach(email.mime.text.MIMEText(html, 'html'))
    alt.attach(email.mime.text.MIMEText(input, 'x-groff-ms'))
    #mail.set_payload(alt)
    #mail.attach(alt)
    #print mail.as_string()

    for fname in mail.keys():
        for fvalue in mail.get_all(fname):
            alt.add_header(fname, fvalue)

    sendmail(alt.as_string(), sys.argv[1:])

#if __name__ == '__main__':
#    main()

