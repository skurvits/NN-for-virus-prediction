import random
import numpy as np
from numpy.random import choice
import argparse
import pandas as pd

def count_kmers(read, k):
    """Count kmer occurrences in a given read.

    Parameters
    ----------
    read : string
        A single DNA sequence.
    k : int
        The value of k for which to count kmers.

    Returns
    -------
    counts : dictionary, {'string': int}
        A dictionary of counts keyed by their individual kmers (strings
        of length k).

    Examples
    --------
    >>> count_kmers("GATGAT", 3)
    {'ATG': 1, 'GAT': 2, 'TGA': 1}
    """
    # Start with an empty dictionary
    counts = {}
    # Calculate how many kmers of length k there are
    num_kmers = len(read) - k + 1
    # Loop over the kmer start positions
    for i in range(num_kmers):
        # Slice the string to get the kmer
        kmer = read[i:i+k]
        # Add the kmer to the dictionary if it's not there
        if kmer not in counts:
            counts[kmer] = 0
        # Increment the count for this kmer
        counts[kmer] += 1
    # Return the final counts
    return counts

def generate_random_sequence(length):
	sequence = ""
	for i in range(length):
		sequence += random.choice("CGTA")
	return sequence


def gen_dataset(filename_A, length_A, filename_B, length_B):
	df = pd.DataFrame()
	d = {}
	with open(filename_A) as f:
		for line in f:
			(key, val) = line.split(":")
			d[str(key)] = val
	keys, values = zip(*d.items())
	for i in range(length_A):
		my_lst = np.random.choice(keys, 100, p=values)
		kmers = count_kmers(''.join(map(str, my_lst)),4)
		#print(kmers)
		kmers["class"] = 0
		df = df.append(pd.DataFrame(kmers, index = [i]))
		#print(str("seqA_" + str(i) + "," + ''.join(map(str, my_lst)) + ",0"))
		final_i = i + 1

	d = {}
	with open(filename_B) as f:
		for line in f:
			(key, val) = line.split(":")
			d[str(key)] = val
	keys, values = zip(*d.items())
	for i in range(length_B):
		my_lst = np.random.choice(keys, 100, p=values)
		kmers = count_kmers(''.join(map(str, my_lst)),4)
		#print(kmers)
		kmers["class"] = 1
		df = df.append(pd.DataFrame(kmers, index = [final_i + i]))

		#print(str("seqB_" + str(i) + "," + ''.join(map(str, my_lst)) + ",1"))
	df = df.fillna(0)
	np.savetxt('OutPut_T.csv', df, delimiter='\t', fmt='%i')
	#df.to_csv('OutPut_T.csv', index=False)
	return df

#gen_dataset("codonfile_A.txt", 300, "codonfile_B.txt", 300)

# Create the parser
my_parser = argparse.ArgumentParser(description='Input files and output lenghts')

# Add the arguments
my_parser.add_argument('file_A',
                       metavar='file_A',
                       type=str,
                       help='File with codon:probability dictionary of class A')

my_parser.add_argument('length_A',
                       metavar='length_A',
                       type=int,
                       help='Number of 300 nucleotid long sequences generated form file A')

my_parser.add_argument('file_B',
                       metavar='file_B',
                       type=str,
                       help='File with codon:probability dictionary of class B')

my_parser.add_argument('length_B',
                       metavar='length_B',
                       type=int,
                       help='Number of 300 nucleotid long sequences generated form file B')

# Execute the parse_args() method
args = my_parser.parse_args()

print(gen_dataset(args.file_A, args.length_A, args.file_B, args.length_B))

#Source:  http://claresloggett.github.io/python_workshops/improved_kmers.html

