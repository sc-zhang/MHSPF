#!/usr/bin/env python3
import argparse
import os
import itertools
import multiprocessing
import random


def get_opts():
    group = argparse.ArgumentParser()
    group.add_argument('-f', '--freq', help="Input frequency file", required=True)
    group.add_argument('-m', '--mhs', help="Input MHS directory", required=True)
    group.add_argument('-l', '--lower', help="Minimum distance between two MHSs tuples, default=500",
                       type=int, default=500)
    group.add_argument('-u', '--upper', help="Maximum distance between two MHSs tuples, default=3000",
                       type=int, default=3000)
    group.add_argument('-s', '--mhss_dis', help="Maximum distance between two MHSs, default=50",
                       type=int, default=50)
    group.add_argument('-o', '--output', help="Output directory", required=True)
    group.add_argument('-t', '--threads', help="Threads, default=10", type=int, default=10)
    return group.parse_args()


def rev_seq(seq):
    base_db = {"A": "T", "T": "A", "G": "C", "C": "G"}
    r_seq = ""
    for base in seq[::-1]:
        r_seq += base_db[base]
    return r_seq


def get_mhss(freq_file: str, lbound: int, ubound: int, max_mhss_dis: int, mhs_file: str, out_file: str):
    print("\tPID: %d, Loading most frequency MHS" % (os.getpid()))
    most_freq_mhs = []
    freq_db = {}
    with open(freq_file, 'r') as fin:
        for line in fin:
            if line[0] == '#':
                continue
            data = line.strip().split()
            if len(set(list(data[1]))) == 1:
                continue
            most_freq_mhs.append(data[1])
            freq_db[data[1]] = int(data[2])

    pos_db = {}
    with open(mhs_file, 'r') as fin:
        for line in fin:
            data = line.strip().split()
            mhs = data[0]
            pos_db[mhs] = list(map(int, data[1].split(',')))

    all_mhss = [mhss for mhss in itertools.combinations(most_freq_mhs, 3)]
    random.shuffle(all_mhss)
    sel_mhss = 10 if len(all_mhss) // 10 < 10 else len(all_mhss) // 10
    sel_idx = 0
    with open(out_file, 'w') as fout:
        for mhss in all_mhss[:sel_mhss]:
            sel_idx += 1
            pmhss = list(mhss)
            random.shuffle(pmhss)
            pmhss = tuple(pmhss)
            pmhss_list = list(pmhss)
            print("\tPID: %d, [%d/%d] Dealing %s with (%s)" % (
                os.getpid(), sel_idx, sel_mhss, mhs_file, ','.join(pmhss_list)))
            tmp_mhss = []
            pos_size1 = len(pos_db[pmhss_list[0]])
            pos_start2 = 0
            pos_size2 = len(pos_db[pmhss_list[1]])
            pos_start3 = 0
            pos_size3 = len(pos_db[pmhss_list[2]])
            for idx1 in range(pos_size1):
                pos1 = pos_db[pmhss_list[0]][idx1]
                for idx2 in range(pos_start2, pos_size2):
                    pos2 = pos_db[pmhss_list[1]][idx2]
                    if pos2 - pos1 < len(pmhss_list[0]):
                        pos_start2 += 1
                        continue
                    if pos2 - pos1 > max_mhss_dis:
                        break
                    for idx3 in range(pos_start3, pos_size3):
                        pos3 = pos_db[pmhss_list[2]][idx3]
                        if pos3 - pos2 < len(pmhss_list[1]):
                            pos_start3 += 1
                            continue
                        if pos3 - pos2 > max_mhss_dis:
                            break
                        tmp_mhss.append([pos1, pos2, pos3])

            if len(tmp_mhss) == 0:
                continue

            mhss_pair = []
            mhss_regions_count = len(tmp_mhss)
            for i in range(mhss_regions_count - 1):
                for j in range(i + 1, mhss_regions_count):
                    if tmp_mhss[j][0] - tmp_mhss[i][-1] < lbound:
                        continue
                    if tmp_mhss[j][0] - tmp_mhss[i][-1] > ubound:
                        break
                    mhss_pair.append([tmp_mhss[i], tmp_mhss[j]])
                    break

            if len(mhss_pair) == 0:
                continue

            fout.write("# %s\n" % (','.join(pmhss_list)))
            fout.write("# %s\n" % (','.join(map(str, [freq_db[_] for _ in pmhss_list]))))
            for mhss1, mhss2 in mhss_pair:
                fout.write("%s\t%s\n" % (','.join(map(str, mhss1)), ','.join(map(str, mhss2))))

    print("\tPID: %d, Finished" % os.getpid())


def main():
    opt = get_opts()
    freq_file = opt.freq
    mhs_dir = opt.mhs
    lbound = opt.lower
    ubound = opt.upper
    max_mhss_dis = opt.mhss_dis
    out_dir = opt.output
    threads = opt.threads

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    print("PID: %d, Starting" % os.getpid())
    pool = multiprocessing.Pool(processes=threads)
    res = []
    for fn in os.listdir(mhs_dir):
        full_fn = os.path.join(mhs_dir, fn)
        out_fn = os.path.join(out_dir, "%ss" % fn)
        r = pool.apply_async(get_mhss, (freq_file, lbound, ubound, max_mhss_dis, full_fn, out_fn,))
        res.append(r)
    pool.close()
    pool.join()

    for r in res:
        try:
            r.get()
        except Exception as e:
            print("Error: {}".format(e))
    print("PID: %d, Finished" % os.getpid())


if __name__ == "__main__":
    main()
