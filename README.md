## Introduction

MHSPF(**M**icro**H**omologous **S**equences **P**airs **F**inder) is a simple tool for searching 3-tuples MHS pairs from genome.

## Dependencies

### Software

* Python (>=3.7)

## Installation

```bash
git clone https://github.com/sc-zhang/MHSPF.git
cd MHSPF/bin
chmod +x *.py
# Optional, add follow line to your .bash_profile or .bashrc
export PATH=/path/to/MHSPF/bin:$PATH
```

## Usage

### Step 1. Get MHS positions.

```bash
usage: get_MHS.py [-h] -g GENOME [-l LEFT] [-r RIGHT] -o OUTPUT [-t THREADS]

optional arguments:
  -h, --help            show this help message and exit
  -g GENOME, --genome GENOME
                        Input genome file
  -l LEFT, --left LEFT  Minium size of MHS, default=5
  -r RIGHT, --right RIGHT
                        Maximum size of MHS, default=7
  -o OUTPUT, --output OUTPUT
                        Output directory
  -t THREADS, --threads THREADS
                        Threads count, default=10
```

Example:

```bash
get_MHS.py -g reference.fasta -l 5 -r 7 -o MHS -t 10
```

### Step 2. Get MHS frequency

```bash
usage: most_freq_MHS.py [-h] -i INPUT [-c COUNT] -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input directory
  -c COUNT, --count COUNT
                        Output count of most frequency MHS for each length,
                        default=20
  -o OUTPUT, --output OUTPUT
                        Output statistic
```

Example:

```bash
most_freq_MHS.py -i MHS -c 20 -o MHS.freq
```

**Notice:** MHS which only include one base will be dropped.

### Step 3. Get 3-tuple MHSs

1. Here we got MHSs pairs on genome like:  
   MHS1---MHS2---MHS3---------------------MHS1---MHS2---MHS3  
   (MHSx is a short nucleotide sequence, the threshold of distance between two MHS and between two 3-tuple MHSs can be
   set
   by user)
2. The 3-tuple MHSs are the top 10% combinations of most frequency MHS which got in step 2.
3. For each 3-tuple MHSs, we only retain one order of these MHSs randomly.

```bash
usage: MHS_tuples.py [-h] -f FREQ -m MHS [-l LOWER] [-u UPPER] [-s MHSS_DIS] -o
                     OUTPUT [-t THREADS]

optional arguments:
  -h, --help            show this help message and exit
  -f FREQ, --freq FREQ  Input frequence file
  -m MHS, --mhs MHS     Input MHS directory
  -l LOWER, --lower LOWER
                        Minimum distance between two MHSs tuples, default=500
  -u UPPER, --upper UPPER
                        Maximum distance between two MHSs tuples, default=3000
  -s MHSS_DIS, --mhss_dis MHSS_DIS
                        Maximum distance between two MHSs, default=50
  -o OUTPUT, --output OUTPUT
                        Output directory
  -t THREADS, --threads THREADS
                        Threads, default=10
```

Example:

```bash
MHS_tuples.py -f MHS.freq -m MHS -l 500 -u 3000 -s 50 -o MHSs -t 10
```

### Step 4. Get 3-tuple MHSs pairs table

```bash
usage: construct_table.py [-h] -i INPUT -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input directory of MHS tuples
  -o OUTPUT, --output OUTPUT
                        Output table
```

Example:

```bash
construct_table.py -i MHSs -o MHSs.tbl
```

The output file is a table file seperated by tab, the table file is like below:

| ID | MHS1          | MHS2           | MHS3            |
|----|---------------|----------------|-----------------|
| 1  | AATCC,3923952 | AATGCA,3273232 | TGACCAG,2797233 |
