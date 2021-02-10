#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zparteka
"""
import numpy as np
# from chiapet_operations.chiapet_given_region import read_region
from math import ceil
from os import path
from glob import glob
from scripts.config import hg19_chromosomes_dict  as chromosomes_hg19
from scripts.config import hg38_chromosomes_dict as chromosomes_hg38
from scripts.config import mm10_chromosomes_dict as chromosomes_mm10

# --------------------------------------------MATRICES------------------------------------------------------------------


def choose_genome_version(genome_version):
    """Check if chosen genome version is supported."""
    if genome_version == 'hg19':
        chromosomes_dict = chromosomes_hg19
    elif genome_version == 'hg38':
        chromosomes_dict = chromosomes_hg38
    elif genome_version == "mm10":
        chromosomes_dict = chromosomes_mm10
    else:
        print("Genome version not included.")
        raise Exception("Not supported genome version.")
    return chromosomes_dict


def bead_ranges_in_chromosome(chromosome, genome_version, resolution):
    """Return list with bead ranges for given chromosome."""
    chromosomes_dict = choose_genome_version(genome_version=genome_version)
    bead_ranges = []
    for i in range(0, chromosomes_dict[chromosome], resolution):
        bead_ranges.append((i, i + resolution))
    return bead_ranges


def bead_ranges_in_region(region, genome_version, resolution):
    """Return list with bead ranges for given region"""
    bead_ranges_chr = bead_ranges_in_chromosome(chromosome=region[0], genome_version=genome_version,
                                                resolution=resolution)
    if int(region[2]) <= bead_ranges_chr[-1][-1]:
        for i in range(len(bead_ranges_chr)):
            if int(region[1]) in range(bead_ranges_chr[i][0], bead_ranges_chr[i][1]):
                start = i
            if int(region[2]) in range(bead_ranges_chr[i][0], bead_ranges_chr[i][1]):
                end = i

        bead_ranges = bead_ranges_chr[start:end + 1]
    else:
        raise ValueError("Domain boundries exceed chromosome length")
    return bead_ranges


def create_chromosome_empty_matrix(chromosome, resolution, genome):
    """Create empty array based on chromosome length and given resolution"""
    chromosomes_dict = choose_genome_version(genome_version=genome)
    length = chromosomes_dict[chromosome]
    number_of_beads = ceil(length / resolution)
    matr = np.zeros((number_of_beads, number_of_beads))
    return matr


def create_matrix_from_bed(interactions):
    """Create matrix using only interactions"""
    n = len(interactions)
    matr = np.zeros((n, n))
    return matr


def create_empty_region_matrix(region, resolution, genome):
    """Create empty matrix of a region by cutting the empty matrix for whole chromosome"""
    check_region(region=region, genome=genome)
    chrom_beads = bead_ranges_in_chromosome(chromosome=region[0], genome_version=genome, resolution=resolution)
    start_bead, end_bead = 0, 0
    for i in range(len(chrom_beads)):
        if int(region[1]) in range(chrom_beads[i][0], chrom_beads[i][1]):
            start_bead = i
        if int(region[2]) in range(chrom_beads[i][0], chrom_beads[i][1]):
            end_bead = i + 1
    region_len = end_bead - start_bead
    region_matr = np.zeros((region_len, region_len))
    return region_matr


def create_empty_domain_matrix(region, resolution):
    """Create empty matrix of domain region with given resolution"""
    start = region[0]
    end = region[1]
    beads = 0
    while start < end:
        start += resolution
        beads += 1
    return np.zeros((beads, beads))


# todo check if this works
def check_region(region, genome):
    """Check if given error is in requested chromosome"""
    chromosomes_dict = choose_genome_version(genome_version=genome)
    if int(region[2]) > chromosomes_dict[region[0]]:
        raise ValueError("End of region exceeds length od chromosome.")


def save_matr(matr, filename, fileformat="txt"):
    """Save matrix in numpy or txt format."""
    if fileformat == "txt":
        np.savetxt(filename, matr)
    elif fileformat == "npy":
        np.save(filename, matr)


# todo - tests for juicer
# ---------------------------------------------JUICER-------------------------------------------------------------------

# TODO read to pandas
def read_juicer_dump(dumpfile, resolution):
    """read file dumped from juicer straw and return nonzero positions of beads"""
    dumped = open(dumpfile, 'r')
    print("Processing " + dumpfile)
    nonzero_beads = []
    for i in dumped:
        line = i.strip().split()
        nonzero_beads.append(
            ((int(ceil(int(line[0]) / resolution))) - 1, int(ceil((int(line[1]) / resolution))) - 1, float(line[2])))
    nonzero_beads = sorted(nonzero_beads, key=lambda tup: tup[1])
    return nonzero_beads


# todo przetestować!!!!
def beads_to_matr(nonzero_beads, chromosome, resolution, genome):
    """Create a matrix from nonzero beads read from dumped file"""
    matr = create_chromosome_empty_matrix(chromosome=chromosome, resolution=resolution, genome=genome)
    for i in range(len(nonzero_beads)):
        matr[nonzero_beads[i][0]][nonzero_beads[i][1]] = nonzero_beads[i][2]
        matr[nonzero_beads[i][1]][nonzero_beads[i][0]] = nonzero_beads[i][2]
    return matr


def multiple_juicer_matrices(matrices_dir, resolution):
    file_list = glob(path.join(matrices_dir, "*KB.txt"))
    for i in file_list:
        print("Parsing " + i)
        filename = path.join(matrices_dir, i.split(".")[0] + "_matrix.txt")
        fi = path.join(matrices_dir, i)
        bead = read_juicer_dump(dumpfile=fi, resolution=resolution)
        matr = beads_to_matr(nonzero_beads=bead)
        save_matr(matr=matr, filename=filename, fileformat="txt")
    print("All matrices have been saved.")



























































