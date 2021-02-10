#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zparteka
"""
from os import path, listdir
import argparse
from scripts.topdom_parser_lib import create_topdom_matrix, create_outfile


def main():
    parser = argparse.ArgumentParser(
        description="This script parses Hi-C interaction matrix to TopDom file format (n x n+3 matrix with fist three "
                    "columns: chromosome, from.coord, to.coord.)")
    parser.add_argument("matrix", help="Contact matrix or directory to multiple matrices.")
    parser.add_argument("-c", "--chromosome",
                        help="Chromosome number. Example: chr1, chr13, chrX. Only if matrix is a file not a directory.",
                        default="chr22",
                        type=str)
    parser.add_argument("-r", "--resolution", help="Matrix resolution in base pairs", default=10000, type=int)
    parser.add_argument("-o", "--outfile",
                        help="Your result file. Only if matrix is a file, otherwise output is saved in input directory.",
                        default=None)
    args = parser.parse_args()

    if path.isfile(args.matrix):
        if not args.outfile:
            outfile = create_outfile(args.matrix, "_topdom.txt")
        else:
            outfile = args.outfile

        create_topdom_matrix(matrix=args.matrix, resolution=args.resolution, chromosome=args.chromosome,
                             outfile=outfile)
    else:
        files = listdir(args.matrix)
        for i in files:
            if not i.endswith('png'):
                #chromosome = i.split(".")[2]
                #print(chromosome)
                matr = path.join(args.matrix, i)
                outfile = create_outfile(matr, "_topdom.txt")
                print("Parsing " + matr)
                create_topdom_matrix(matrix=matr, resolution=args.resolution, chromosome=args.chromosome,
                                     outfile=outfile)
                print("Saved " + outfile)


if __name__ == '__main__':
    main()
