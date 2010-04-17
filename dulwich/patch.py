from difflib import SequenceMatcher
import rfc822
from dulwich.objects import (
    Commit,
    )
def unified_diff(a, b, fromfile='', tofile='', n=3, lineterm='\n'):
    """difflib.unified_diff that doesn't write any dates or trailing spaces.

    Based on the same function in Python2.6.5-rc2's difflib.py
    """
    started = False
    for group in SequenceMatcher(None, a, b).get_grouped_opcodes(3):
        if not started:
            yield '--- %s\n' % fromfile
            yield '+++ %s\n' % tofile
            started = True
        i1, i2, j1, j2 = group[0][1], group[-1][2], group[0][3], group[-1][4]
        yield "@@ -%d,%d +%d,%d @@\n" % (i1+1, i2-i1, j1+1, j2-j1)
        for tag, i1, i2, j1, j2 in group:
            if tag == 'equal':
                for line in a[i1:i2]:
                    yield ' ' + line
                continue
            if tag == 'replace' or tag == 'delete':
                for line in a[i1:i2]:
                    yield '-' + line
            if tag == 'replace' or tag == 'insert':
                for line in b[j1:j2]:
                    yield '+' + line


                f.write("old mode %o\n" % old_mode)
            f.write("new mode %o\n" % new_mode) 
            f.write("deleted mode %o\n" % old_mode)
    f.writelines(unified_diff(old_contents, new_contents, 


def git_am_patch_split(f):
    """Parse a git-am-style patch and split it up into bits.

    :param f: File-like object to parse
    :return: Tuple with commit object, diff contents and git version
    """
    msg = rfc822.Message(f)
    c = Commit()
    c.author = msg["from"]
    c.committer = msg["from"]
    if msg["subject"].startswith("[PATCH"):
        subject = msg["subject"].split("]", 1)[1][1:]
    else:
        subject = msg["subject"]
    c.message = subject
    for l in f:
        if l == "---\n":
            break
        c.message += l
    diff = ""
    for l in f:
        if l == "-- \n":
            break
        diff += l
    version = f.next().rstrip("\n")
    return c, diff, version