#!/usr/bin/env python3
import argparse
import os


def get_opts():
    group = argparse.ArgumentParser()
    group.add_argument('-i', '--input', help="Input directory of MHS tuples", required=True)
    group.add_argument('-o', '--output', help="Output table", required=True)
    return group.parse_args()


def construct_table(in_dir, out_fn):
    print("Loading MHS tuples")
    freq_db = {}
    mhss_set = set()
    for fn in os.listdir(in_dir):
        print("\tLoading %s"%fn)
        in_fn = os.path.join(in_dir, fn)
        with open(in_fn, 'r') as fin:
            for line in fin:
                if line[0] == '#':
                    data = line.strip().split()
                    vals = data[1].split(',')
                    if not vals[0].isdigit():
                        mhss = vals
                        mhss_set.add(tuple(mhss))
                    else:
                        freq = list(map(int, vals))
                        for idx in range(3):
                            mhs = mhss[idx]
                            if mhs not in freq_db:
                                freq_db[mhs] = freq[idx]
    
    print("Writing table")
    with open(out_fn, 'w') as fout:
        fout.write("ID\tMHS1\tMHS2\tMHS3\n")
        idx = 1
        for mhss in mhss_set:
            tmp = []
            for mhs in mhss:
                tmp.append("%s,%s"%(mhs, freq_db[mhs]))
            fout.write("%d\t%s\n"%(idx, '\t'.join(tmp)))
            idx += 1
    
    print("Finished")


def main():
    opt = get_opts()
    in_dir = opt.input
    out_fn = opt.output

    construct_table(in_dir, out_fn)


if __name__ == "__main__":
    main()
