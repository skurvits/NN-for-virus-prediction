# Finding existing data and saving them to CSV format (train + test).
#class A: AGGAAG and TGGTTG appear in class. Class label is 0.
#class B: AGGAAG and TGGTTG do not appear in class. Class label is 1.

from collections import defaultdict
import random

# TODO change data_path if reusing code
data_path = "C:/Users/Taavi/Documents/Kool/MA/Neural Networks/project/NN-for-virus-prediction/NN-for-virus-prediction/data/test_data/"

def find_all_classes(sequences, sequence_count, path, limit=-1):
    """
    Parameters
    ----------
    sequences - tuple of strings, e.g. ("AGGAAG", "TGGTTG")
    sequence_count - tuple of ints, number of times the sequence must exist in DNA sequence
    path - string, path to search sequences from (assumes that they are split by comma and the 2nd element is sequence)
    limit - int, optional total number of sequences to find

    Returns
    -------

    """
    data = []
    counter = 0
    for line in open(path).readlines():
        values = line.strip().split(",")
        add = True
        for i, sequence in enumerate(sequences):
            if values[1].count(sequence) != sequence_count[i]:
                add = False
                break
        if add:
            data.append(tuple(values))
            counter += 1
        if limit != -1 and counter > limit:
            break
    return data


def write_to_csv(data, path, delimiter="\t"):
    with open(path, "w+") as file:
        for e in data:
            file.write(delimiter.join(e) + "\n")


def load_csv(path, delimiter=","):
    data = []
    with open(path) as file:
        lines = file.readlines()
        for line in lines:
            data.append(tuple(line.strip().split(delimiter)))
    return data


def count_kmers(sequence, k):
    counts = defaultdict(int)
    for i in range(len(sequence)-k+1):
        kmer = sequence[i:i+k]
        counts[kmer] += 1
    return counts


# TODO change paths if reusing code
full_dataset_train_path = "C:/Users/Taavi/Documents/Kool/MA/Neural Networks/project/NN-for-virus-prediction/NN-for-virus-prediction/data/DNA_data/fullset_train.csv"
full_dataset_test_path = "C:/Users/Taavi/Documents/Kool/MA/Neural Networks/project/NN-for-virus-prediction/NN-for-virus-prediction/data/DNA_data/fullset_test.csv"
class_A_train = find_all_classes(("AGGAAG", "TGGTTG"), (1, 1), full_dataset_train_path)
class_B_train = find_all_classes(("AGGAAG", "TGGTTG"), (0, 0), full_dataset_train_path)
class_A_test = find_all_classes(("AGGAAG", "TGGTTG"), (1, 1), full_dataset_test_path)
class_B_test = find_all_classes(("AGGAAG", "TGGTTG"), (0, 0), full_dataset_test_path)

print("Found {} train entities for class A".format(len(class_A_train)))
print("Found {} test entities for class A".format(len(class_A_test)))
print("Found {} train entities for class B".format(len(class_B_train)))
print("Found {} test entities for class B".format(len(class_B_test)))


### Quick check for mistakes, just to be sure
for a in class_A_train + class_A_test:
    if a[1].count("AGGAAG") != 1 or a[1].count("TGGTTG") != 1:
        print("MISTAKE")

for b in class_B_train + class_B_test:
    if "AGGAAG" in b[1] or "TGGTTG" in b[1]:
        print("MISTAKE")


# Count kmers for classes A and B, train and test sets
class_A_train_kmers = []
for sample in class_A_train:
    class_A_train_kmers.append(count_kmers(sample[1], 3))
class_A_test_kmers = []
for sample in class_A_test:
    class_A_test_kmers.append(count_kmers(sample[1], 3))

class_B_train_kmers = []
for sample in class_B_train:
    class_B_train_kmers.append(count_kmers(sample[1], 3))
class_B_test_kmers = []
for sample in class_B_test:
    class_B_test_kmers.append(count_kmers(sample[1], 3))

# All possible 3mers, ordered
all_kmers = ['AAA', 'AAC', 'AAT', 'AAG', 'ACA', 'ACC', 'ACT', 'ACG', 'ATA', 'ATC', 'ATT', 'ATG', 'AGA', 'AGC', 'AGT',
             'AGG', 'CAA', 'CAC', 'CAT', 'CAG', 'CCA', 'CCC', 'CCT', 'CCG', 'CTA', 'CTC', 'CTT', 'CTG', 'CGA', 'CGC',
             'CGT', 'CGG', 'TAA', 'TAC', 'TAT', 'TAG', 'TCA', 'TCC', 'TCT', 'TCG', 'TTA', 'TTC', 'TTT', 'TTG', 'TGA',
             'TGC', 'TGT', 'TGG', 'GAA', 'GAC', 'GAT', 'GAG', 'GCA', 'GCC', 'GCT', 'GCG', 'GTA', 'GTC', 'GTT', 'GTG',
             'GGA', 'GGC', 'GGT', 'GGG']

# Put the 3mers for each sample in the order specified above, adding zeros where no such 3mer was found.
ordered_class_A_train_3mers = []
for i,sample in enumerate(class_A_train_kmers):
    val = [sample[e] if e in sample.keys() else 0 for e in all_kmers]
    val.append(0)
    val = [str(e) for e in val]
    ordered_class_A_train_3mers.append(val)

ordered_class_B_train_3mers = []
for i,sample in enumerate(class_B_train_kmers):
    val = [sample[e] if e in sample.keys() else 0 for e in all_kmers]
    val.append(1)
    val = [str(e) for e in val]
    ordered_class_B_train_3mers.append(val)

ordered_class_A_test_3mers = []
for i, sample in enumerate(class_A_test_kmers):
    val = [sample[e] if e in sample.keys() else 0 for e in all_kmers]
    val.append(0)
    val = [str(e) for e in val]
    ordered_class_A_test_3mers.append(val)

ordered_class_B_test_3mers = []
for i, sample in enumerate(class_B_test_kmers):
    val = [sample[e] if e in sample.keys() else 0 for e in all_kmers]
    val.append(1)
    val = [str(e) for e in val]
    ordered_class_B_test_3mers.append(val)

# Create train set by adding class A and class B train sets together, then shuffling them
train_set = ordered_class_A_train_3mers[:]
train_set.extend(ordered_class_B_train_3mers)
random.shuffle(train_set)

# Create test set by adding class A and class B test sets together, then shuffling them
test_set = ordered_class_A_test_3mers[:]
test_set.extend(ordered_class_B_test_3mers)
random.shuffle(test_set)

print("Train set size {}, test set size {}".format(len(train_set), len(test_set)))

write_to_csv(train_set, data_path+"classes_AB_3mers_train.csv")
write_to_csv(test_set, data_path+"classes_AB_3mers_test.csv")
