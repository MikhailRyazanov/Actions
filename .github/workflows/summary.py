"""
Print summary of all pytest results (saved using "--junit-xml=<wheel>.xml").
Without arguments -- ANSI-colored terminal,
with "md" argument -- markdown,
with "msg" argument -- gitHub notice/warning message (only for skip/warn).
"""
import sys
from glob import glob
from re import findall

# output type
if len(sys.argv) > 1:
    out = sys.argv[1]
else:
    out = 'term'


# formatter for ANSI/markdown
def fmt(val, cond, style):  # style: "ok"/"warn"/"err"
    if not cond:
        return val
    if out == 'md':
        val = val.strip()
        if style in ['ok', 'err']:
            return '**' + val + '**'  # bold
        else:
            return '*' + val + '*'  # italic
    if style == 'ok':
        return f'\x1B[32m{val}\x1B[0m'  # green
    elif style == 'err':
        return f'\x1B[31m{val}\x1B[0m'  # red
    else:
        return f'\x1B[33m{val}\x1B[0m'  # yellow


# table header
if out == 'md':
    print('| Wheel | Pass | Error | Fail | Skip |')
    print('| --- | --- | --- | --- | --- |')
    sep = ' | '
elif out == 'term':
    print('Wheel  Pass  Error  Fail  Skip')
    print('==============================')
    sep = '  '

# count runs
good, bad = 0, 0

for xml in sorted(glob('*.xml')):
    with open(xml, 'rt') as f:
        res = dict(findall(r'(\S+)="(\S+)"', f.readline()))
    T, E, F, S = map(lambda k: int(res[k]),
                     ['tests', 'errors', 'failures', 'skipped'])
    P = T - E - F - S
    if 'no-cython' in xml:
        T -= S  # ignore skipped Cython
    ok = P == T

    if out == 'msg':
        msg = 'notice' if ok else 'warning'
        if S:
            print(f'::{msg} title={xml[:-4]}::{S} skipped')
    else:
        row = sep.lstrip()
        row += xml[:-4]
        if out != 'md':
            row += '\n' + ' ' * 5
        row += sep + fmt(f'{P:4}', P == T, 'ok')
        row += sep + fmt(f'{E:5}', E, 'err')
        row += sep + fmt(f'{F:4}', F, 'err')
        row += sep + fmt(f'{S:4}', S, 'warn' if ok else 'err')
        row += sep.rstrip()
        print(row)
        if ok:
            good += 1
        else:
            bad += 1

# table footer and run counts
if out != 'msg':
    print('' if out == 'md' else '==============================')
    tot = fmt(f'{good} good', not bad, 'ok')
    if bad:
        tot += ', ' + fmt(f'{bad} bad', True, 'err')
    print(tot)
