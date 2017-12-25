from os.path import basename
from os.path import splitext
import sys, argparse, os

parser = argparse.ArgumentParser()
parser.add_argument("--input-file", "-f", type=argparse.FileType('rb'), help="input file")

# # now you can call it directly with basename
# print(basename("/a/b/c.txt"))

if __name__ == '__main__':
    args = parser.parse_args()
    print(args.input_file)
    print(args.input_file.name)
    print(basename(args.input_file.name))
    print(splitext(basename(args.input_file.name))[0])
    args.input_file.close()
    print(2 % 2)