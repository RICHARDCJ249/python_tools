import os
from pathlib import Path
from py_compile import compile
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser(description='THe tool to make and create zip file to release')
    parser.add_argument('-i', help='the file or dist to ignore', action='store', nargs='*')
    parser.add_argument('-o', help='the path to save zip file', action='store', default='.')
    parser.add_argument('-t', help='temp dist name', action='store', default='./dist')
    parser.add_argument('-c', help='the paths that need to be created', nargs='*')
    parser.add_argument('dist', help='the path of projects')
    args = parser.parse_args()

    print(f'忽略文件 {args.i} 输出目录 {args.o}')

    dist = Path(args.dist)
    temp_dist = dist / args.t if args.t else Path(args.t)
    temp_dist.mkdir(exist_ok=True)
    for i in args.c:
        os.makedirs(temp_dist / i, exist_ok=True)
    if (dist / 'requirements.txt').exists():
        (dist / 'requirements.txt').replace(temp_dist / 'requirements.txt')
    for file in dist.rglob('*.py'):
        if set(args.i) & set(file.parts):
            continue
        output_pyc = temp_dist / file.relative_to(dist).with_suffix('.pyc')
        print(f'Compiling {output_pyc}')
        compile(file, output_pyc)
