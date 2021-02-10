#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: zparteka
"""
from os import path


# TopDom

def create_topdom_matrix(matrix, resolution, chromosome, outfile):
    """parse HiC matrix file  """
    out = open(outfile, 'w')
    counter = 0
    with open(matrix) as f:
        for line in f:
            new_line = chromosome + "\t" + str(counter) + "\t" + str(counter + resolution) + "\t" + line.replace(" ",
                                                                                                                 "\t")
            out.write(new_line)
            counter += resolution
    f.close()
    out.close()


def create_outfile(infile, format):
    """Create output file in input location."""
    dire = path.dirname(infile)
    name = path.basename(infile)[:-4] + format
    outfile = path.join(dire, name)
    return outfile


# ----------------------------------------------------Output------------------------------------------------------------


def read_domains_from_topdom_output_bed(bedfile):
    """Read domains from topdom output"""
    with open(bedfile) as bed:
        line = bed.readline()
        domains = []
        counter = 0
        while line:
            lline = line.strip().split()
            if lline[-1] == "domain":
                counter += 1
                domains.append(lline)
            line = bed.readline()
    print("{} domains found".format(str(counter)))
    return domains


def read_domains_from_bedfile(bedfile):
    """Read domains from bed with three first columns "chr start end" file
    and return as a list [[chr, start1, end1], ...]"""
    with open(bedfile) as bed:
        line = bed.readline()
        domains = []
        while line:
            lline = line.strip().split()
            domains.append((lline[0], int(lline[1]), int(lline[2])))
            line = bed.readline()
    return domains


def save_chromosome_domain_file(domains, outfile):
    """Save domains found in single chromosome file"""
    output = open(outfile, "w")
    for i in domains:
        output.write(i[0] + "\t" + i[1] + "\t" + i[2] + "\n")
    print("{} saved.".format(outfile))
    output.close()


def dict_domains_in_chromosomes(domains_list):
    """Given a list of domains (chr start end) return a dictionary of with chromosomes as keys and list of domains
    as values"""
    chromosomes = {}
    for i in domains_list:
        chrom = i[0]
        if chrom not in chromosomes.keys():
            chromosomes[chrom] = [(i[1], i[2])]
        else:
            chromosomes[chrom].append((i[1], i[2]))
    return chromosomes
