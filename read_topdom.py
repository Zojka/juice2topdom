#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from scripts.topdom_parser_lib import read_domains_from_topdom_output_bed, save_chromosome_domain_file
from os import path, listdir


def main():
    parser = argparse.ArgumentParser(description="opis")
    parser.add_argument("domain", help="Domains bed file from topdom")
    args = parser.parse_args()

    if path.isdir(args.domain):
        domains = []
        doms = listdir(args.domain)
        outfile = path.join(args.domain, "all_domains.bed")
        for i in sorted(doms):
            if i.endswith('.bed'):
                dom_file = path.join(args.domain, i)
                chromosome_domains = read_domains_from_topdom_output_bed(bedfile=dom_file)
                domains += chromosome_domains
        save_chromosome_domain_file(domains=domains, outfile=outfile)
    else:
        domains = read_domains_from_topdom_output_bed(bedfile=args.domain)
        save_chromosome_domain_file(domains=domains, outfile=args.domains[:-4] + "_domais.bed")


if __name__ == '__main__':
    main()
