"""
Print summary of all pytest results (saved using "--junit-xml=<wheel>.xml").
Without arguments -- ANSI-colored terminal, with any argument -- markdown.
"""
import sys
from glob import glob
from re import findall

# markdown or terminal
md = len(sys.argv) > 1  # (any argument)


def fmt(val, cond, style):  # style: "ok"/"warn"/"err"
    if not cond:
        return val
    if md:
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


if md:
    print('| Wheel | Pass | Error | Fail | Skip |')
    print('| --- | --- | --- | --- | --- |')
    sep = ' | '
else:
    print('Wheel  Pass  Error  Fail  Skip')
    print('==============================')
    sep = '  '

good, bad = 0, 0

for xml in sorted(glob('*.xml')):
    with open(xml, 'rt') as f:
        res = dict(findall(r'(\S+)="(\S+)"', f.readline()))
    T, E, F, S = map(lambda k: int(res[k]),
                     ['tests', 'errors', 'failures', 'skipped'])
    P = T - E - F - S
    if 'no-cython' in xml:
        T -= S  # ignore skipped Cython
        s = 'warn'
    else:
        s = 'err'
    row = sep.lstrip()
    row += xml[:-4]
    if not md:
        row += '\n' + ' ' * 5
    row += sep + fmt(f'{P:4}', P == T, 'ok')
    row += sep + fmt(f'{E:5}', E, 'err')
    row += sep + fmt(f'{F:4}', F, 'err')
    row += sep + fmt(f'{S:4}', S, s)
    row += sep.rstrip()
    print(row)
    if P == T:
        good += 1
    else:
        bad += 1

print('' if md else '==============================')
tot = fmt(f'{good} good', not bad, 'ok')
if bad:
    tot += ', ' + fmt(f'{bad} bad', True, 'err')
print(tot)
