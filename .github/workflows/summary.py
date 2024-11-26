"""
Print summary of all pytest results (saved using "--junit-xml=<wheel>.xml").
"""
from glob import glob
from re import findall

print('Wheel  Pass  Error  Fail  Skip')
print('==============================')

for xml in glob('*.xml'):
    with open(xml, 'rt') as f:
        res = dict(findall(r'(\S+)="(\S+)"', f.readline()))
    T, E, F, S = map(lambda k: int(res[k]),
                     ['tests', 'errors', 'failures', 'skipped'])
    P = T - E - F - S
    g = lambda v: '' if v else '\x1B[32m'  # green if 0
    r = lambda v: '\x1B[31m' if v else ''  # red if not 0
    print(f'{xml[:-4]}\n{"":5}'
          f'  {g(T-P)}{P:4}\x1B[0m'
          f'  {r(E)}{E:5}\x1B[0m'
          f'  {r(F)}{F:4}\x1B[0m'
          f'  {r(S)}{S:4}\x1B[0m')
