import os
import sys
from pathlib import Path
from py_compile import compile
from argparse import ArgumentParser
from zipfile import ZipFile, ZIP_DEFLATED
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.__stdout__)

    parser = ArgumentParser(description='The tool to make and create zip file to release')
    parser.add_argument('-i', help='the file or dist to ignore', action='store', nargs='*',metavar='FILES|DISTS')
    parser.add_argument('-o', help='the path to save zip file', action='store', default='.',metavar='FILE')
    parser.add_argument('-t', help='temp dist name', action='store', default='./dist',metavar='DIST')
    parser.add_argument('-z', help='zip file path', action='store',metavar='FILE')
    parser.add_argument('-c', help='the paths that need to be created', nargs='*',metavar='DISTS')
    parser.add_argument('dist', help='the path of projects')
    args = parser.parse_args()

    logging.warning(f'忽略文件 {args.i} 输出目录 {args.o}')

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
        logging.info(f'Compiling {output_pyc}')
        compile(file, output_pyc)
    if args.z:
        logging.info(f'ZipFile to {args.z}')
        with ZipFile(args.z, 'w', ZIP_DEFLATED) as zip_file:
            for i in temp_dist.glob("**/*"):
                logging.info(f'Zipping {i.relative_to(temp_dist)}')
                zip_file.write(i, i.relative_to(temp_dist))
