#!/usr/bin/env python3
import argparse
import os


def get_opts():
    group = argparse.ArgumentParser()
    group.add_argument('-i', '--input', help="Input directory", required=True)
    group.add_argument('-c', '--count', help="Output count of most frequency MHS for each length, "
                                             "default=20", type=int, default=20)
    group.add_argument('-o', '--output', help="Output statistic", required=True)
    return group.parse_args()


def most_freq(in_dir, cnt, out_fn):
    print("Loading MHS files")
    freq_db = {}
    for fn in os.listdir(in_dir):
        print("\tLoading %s" % fn)
        full_fn = os.path.join(in_dir, fn)
        with open(full_fn, 'r') as fin:
            for line in fin:
                data = line.strip().split()
                MHS = data[0]
                mhs_len = len(data[0])
                mhs_cnt = len(data[1].split(','))
                if mhs_len not in freq_db:
                    freq_db[mhs_len] = {}
                if MHS not in freq_db[mhs_len]:
                    freq_db[mhs_len][MHS] = 0
                freq_db[mhs_len][MHS] += mhs_cnt

    print("Getting most frequency ones")
    with open(out_fn, 'w') as fout:
        fout.write("#MHS_len\tMHS_seq\tMHS_cnt\n")
        for mhs_len in sorted(freq_db):
            cur_cnt = 0
            for MHS in sorted(freq_db[mhs_len], key=lambda x: freq_db[mhs_len][x], reverse=True):
                if len(set(list(MHS))) == 1:
                    continue
                cur_cnt += 1
                fout.write("%d\t%s\t%d\n" % (mhs_len, MHS, freq_db[mhs_len][MHS]))
                if cur_cnt > cnt:
                    break

    print("Finished")


def main():
    opt = get_opts()
    in_dir = opt.input
    cnt = opt.count
    out_fn = opt.output
    most_freq(in_dir, cnt, out_fn)


if __name__ == '__main__':
    main()
