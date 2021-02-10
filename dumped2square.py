#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zparteka

parse juicebox matrix to numpy matrix format
"""

import argparse
from scripts.matrix_parsing_operations import read_juicer_dump, beads_to_matr, save_matr


def main():
    parser = argparse.ArgumentParser(description="opis")
    parser.add_argument("dumped_file", help="output matrix file from Juicebox")
    parser.add_argument("-r", "--resolution", help="Dumped heatmap resolution in bp", default=10000, type=int)
    parser.add_argument("-c", "--chromosome", help="Chromosome to label the file", default=None, type=str)
    parser.add_argument("-g", "--genome", help="Genome version: hg19 or hg38", default="hg38", type=str)
    args = parser.parse_args()

    # todo go back to multiple heatmaps idea - need chromosome parameter to create input empty matrix
    """
    if path.isdir(args.dumped_file):
        multiple_juicer_matrices(matrices_dir=args.dumped_file, resolution=args.resolution)
    else:
    """
    #todo to działa tylko dla chromosomów!! bez sensu
    filename = args.dumped_file[:-4] + "_formatted.txt"
    beads = read_juicer_dump(dumpfile=args.dumped_file, resolution=args.resolution)
    matr = beads_to_matr(nonzero_beads=beads, chromosome=args.chromosome, resolution=args.resolution, genome=args.genome)
    save_matr(matr=matr, filename=filename)


if __name__ == '__main__':
    main()
