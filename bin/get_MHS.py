#!/usr/bin/env python3
import argparse
import os
import multiprocessing


def get_opts():
    group = argparse.ArgumentParser()
    group.add_argument('-g', '--genome', help="Input genome file", required=True)
    group.add_argument('-l', '--left', help="Minium size of MHS, default=5", type=int, default=5)
    group.add_argument('-r', '--right', help="Maximum size of MHS, default=7", type=int, default=7)
    group.add_argument('-o', '--output', help="Output directory", required=True)
    group.add_argument('-t', '--threads', help="Threads count, default=10", type=int, default=10)
    return group.parse_args()


def sub_get_MHS(seq, fn, lbound, ubound):
    MHS_db = {}
    print("\tPID: %d, Starting"%os.getpid())
    
    for mhs_len in range(lbound, ubound+1):
        print("\tPID: %d, Getting with length: %d"%(os.getpid(), mhs_len))
        for _ in range(len(seq)-(mhs_len-1)):
            mhs = seq[_: _+mhs_len]
            if "N" in mhs or len(mhs) != mhs_len:
                continue
            if mhs not in MHS_db:
                MHS_db[mhs] = []
            MHS_db[mhs].append(_+1)
    
    print("\tPID: %d, Writing MHS"%os.getpid())
    with open(fn, 'w') as fout:
        for mhs in sorted(MHS_db):
            if len(MHS_db[mhs]) < 2:
                continue
            fout.write("%s\t%s\n"%(mhs, ','.join(map(str, MHS_db[mhs]))))
    print("\tPID: %d, Finished"%os.getpid())

def get_MHS(in_genome, out_dir, lbound, ubound, threads):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    print("PID: %d, Loading genome"%os.getpid())
    fa_db = {}
    with open(in_genome, 'r') as fin:
        for line in fin:
            if line[0] == '>':
                id = line.strip().split()[0][1:]
                fa_db[id] = []
            else:
                fa_db[id].append(line.strip().upper())
    
    for id in fa_db:
        fa_db[id] = ''.join(fa_db[id])
    
    print("PID: %d, Getting MHS"%os.getpid())
    pool = multiprocessing.Pool(processes=threads)
    res = []
    for id in fa_db:
        fn = os.path.join(out_dir, '%s.mhs'%id)
        r = pool.apply_async(sub_get_MHS, (fa_db[id], fn, lbound, ubound, ))
        res.append(r)
    pool.close()
    pool.join()

    for r in res:
        try:
            r.get()
        except Exception as e:
            print("Error: {}".format(e))
    print("PID: %d, Finished"%os.getpid())


if __name__ == "__main__":
    opts = get_opts()
    in_genome = opts.genome
    out_dir = opts.output
    lbound = opts.left
    ubound = opts.right
    threads = opts.threads
    get_MHS(in_genome, out_dir, lbound, ubound, threads)
