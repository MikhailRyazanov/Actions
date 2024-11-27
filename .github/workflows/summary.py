"""
Print summary of all pytest results (saved using "--junit-xml=<wheel>.xml").
"""
from glob import glob
from re import findall

# colors
g = lambda v: '' if v else '\x1B[32m'  # green if 0
r = lambda v: '\x1B[31m' if v else ''  # red if not 0
y = lambda v: '\x1B[33m' if v else ''  # yellow if not 0
_ = '\x1B[0m'  # reset

print('Wheel  Pass  Error  Fail  Skip')
print('==============================')

good, bad = 0, 0

for xml in sorted(glob('*.xml')):
    with open(xml, 'rt') as f:
        res = dict(findall(r'(\S+)="(\S+)"', f.readline()))
    T, E, F, S = map(lambda k: int(res[k]),
                     ['tests', 'errors', 'failures', 'skipped'])
    P = T - E - F - S
    if xml[:5] == 'sdist':
        T -= S  # ignore skipped Cython
        s = y
    else:
        s = r
    print(f'{xml[:-4]}\n{"":5}'
          f'  {g(T-P)}{P:4}{_}'
          f'  {r(E)}{E:5}{_}'
          f'  {r(F)}{F:4}{_}'
          f'  {s(S)}{S:4}{_}')
    if P == T:
        good += 1
    else:
        bad += 1

print('==============================')
print(f'{g(bad)}{good} good{_}{f", {r(bad)}{bad} bad{_}" if bad else ""}')
