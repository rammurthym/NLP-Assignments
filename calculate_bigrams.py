# Name: Rammurthy Mudimadugula
# Net-ID: rxm163730
# Homework #1

import sys
import pandas
from collections import Counter

pandas.set_option('expand_frame_repr', False)
n = 2 # Set n to calculate ngram counts and probabilities

#*******************************************************************************
#                           INPUT SENTENCES
#*******************************************************************************

s1 = "The president has relinquished his control of the company's board."
s2 = "The chief executive officer said the last year revenue was good."

#*******************************************************************************
#                           IO METHODS
#*******************************************************************************

# Method to read input from a file
def read_input(input_file):
    try:
        f = open(input_file, 'r');
        input_list = f.read().split();
        return input_list
    except IOError:
        print("File '" + input_file + "' does not exist")
        sys.exit(1)

# Method to check whether user has passed corpus file as input
def is_args():
    if (len(sys.argv) == 2):
        return read_input(sys.argv[1])
    else:
        print('Please provide input file as an argument')
        sys.exit(1)

#*******************************************************************************
#                           INTERNAL METHODS
#*******************************************************************************

# Given a list of strings, this method will convert it to list of tuples
def list_to_tuple(input_list):
    s_tuple = []
    for i in input_list:
        for j in input_list:
            s_tuple.append(list(zip([i], [j]))[0])
    return s_tuple

# Method to return a generator used for batch processing
def batch(iterable, n):
    l = len(iterable)
    for m in range(0, l, n):
        yield iterable[m:min(m + n, l)]

# Method to calculate bigram and addone counts
def format_data(ngrams, s_tuple, s_len, ao):
    out_temp = []
    for x in batch(s_tuple, s_len):
        in_temp = []
        for y in x:
            if (ao == 1):
                if(ngrams[y]):
                    in_temp.append(ngrams[y] + 1)
                else:
                    in_temp.append(1)                    
            else:
                if(ngrams[y]):
                    in_temp.append(ngrams[y])
                else:
                    in_temp.append(0)
        out_temp.append(in_temp)
    return out_temp

# Method to calculate bigram probabilities
def calc_prob(wc, s_list, s_count):
    i = 0
    out_temp = []
    for x in s_count:
        in_temp = []
        for y in x:
            if (wc[s_list[i]] == 0):
                in_temp.append(0)
            else:
                in_temp.append(float(y/wc[s_list[i]]))
        i += 1
        out_temp.append(in_temp)
    return out_temp

# Method to calculate addone probabilities
def calc_addone_prob(wc, s_list, s_count):
    i = 0
    out_temp = []
    v = len(wc)
    for x in s_count:
        in_temp = []
        for y in x:
            in_temp.append(y/(wc[s_list[i]] + v))
        i += 1;
        out_temp.append(in_temp)
    return out_temp

# Method to calculate number of times bigrams with a certain count occurred
def calc_ngram_occurences(s_count):
    temp = {}
    for x in s_count:
        for y in x:
            if y in temp:
                temp[y] += 1;
            else:
                temp[y] = 1;
    return temp

# Method to calculate good turing counts
def calc_gt_count(s_count):
    out_temp = []
    temp_dict = calc_ngram_occurences(s_count)
    for x in s_count:
        in_temp = []
        for y in x:
            if y in temp_dict:
                if y+1 in temp_dict:
                    in_temp.append((temp_dict[y+1] + 1)*temp_dict[y+1]/temp_dict[y])
                else:
                    in_temp.append(0)
            else:
                in_temp.append(0)
        out_temp.append(in_temp)
    return out_temp

# Method to calculate good turing probabilities
def calc_gt_prob(N, s_count):
    i = 0
    out_temp = []
    temp_dict = calc_ngram_occurences(s_count)
    for x in s_count:
        in_temp = []
        for y in x:
            if y in temp_dict:
                if y+1 in temp_dict:
                    in_temp.append(temp_dict[y+1]/N)
                else:
                    in_temp.append(0)
        i += 1;
        out_temp.append(in_temp)
    return out_temp

# Method to calculate a sentence probability
def probability(ngram_prob):
    i = 0;
    p = 1;
    for x in ngram_prob:
        j = 0;
        for y in x:
            if (j - i == 1):
                p = float(p*y)
            j += 1
        i += 1
    return p

# Method to calculate word count from a given corpus
def word_count(input_list):
    counter = Counter()
    for i in input_list:
        counter[i] += 1
    return counter

# Method to calculate bigrams of a given corpus
def calc_ngrams(input_list, n):
    if (len(input_list) > n):
        ngrams = list(zip(*[input_list[i:] for i in range(n)]))
        counter = Counter()
        for tuple in ngrams:
            counter[tuple] += 1
        return counter
    else:
        print('Inadequate input')
        return None

#*******************************************************************************
#                           INTERNAL METHOD CALLS
#*******************************************************************************

input_list = is_args()

wc = word_count(input_list)
V = len(wc)

bigrams = calc_ngrams(input_list, n)
N = len(bigrams)

s1_list = s1.split()
s2_list = s2.split()

s1_len = len(s1_list)
s2_len = len(s2_list)

s1_tuple = list_to_tuple(s1.split())
s2_tuple = list_to_tuple(s2.split())

s1_count = format_data(bigrams, s1_tuple, s1_len, 0)
s2_count = format_data(bigrams, s2_tuple, s2_len, 0)

s1_count_addone = format_data(bigrams, s1_tuple, s1_len, 1)
s2_count_addone = format_data(bigrams, s2_tuple, s2_len, 1)

s1_count_gt = calc_gt_count(s1_count)
s2_count_gt = calc_gt_count(s2_count)

s1_count_prob = calc_prob(wc, s1_list, s1_count)
s2_count_prob = calc_prob(wc, s2_list, s2_count)

s1_addone_prob = calc_addone_prob(wc, s1_list, s1_count_addone)
s2_addone_prob = calc_addone_prob(wc, s2_list, s2_count_addone)

s1_gt_prob = calc_gt_prob(N, s1_count_gt)
s2_gt_prob = calc_gt_prob(N, s2_count_gt)

s1_p = probability(s1_count_prob)
s2_p = probability(s2_count_prob)

s1_addone_p = probability(s1_addone_prob)
s2_addone_p = probability(s2_addone_prob)

s1_gt_p = probability(s1_count_gt)
s2_gt_p = probability(s2_count_gt)


print("***********************************************************************")
print("                        S1: BIGRAM COUNTS                              ")
print("***********************************************************************")

print()
print("                        WITHOUT SMOOTHING                              ")
print(pandas.DataFrame(s1_count, s1_list, s1_list))
print()

print()
print("                        WITH ADDONE SMOOTHING                          ")
print(pandas.DataFrame(s1_count_addone, s1_list, s1_list))
print()

print()
print("                        GOOD TURING SMOOTHING                          ")
print(pandas.DataFrame(s1_count_gt, s1_list, s1_list))
print()

print("***********************************************************************")
print("                        S2: BIGRAM COUNTS                              ")
print("***********************************************************************")

print()
print("                        WITHOUT SMOOTHING                              ")
print(pandas.DataFrame(s2_count, s2_list, s2_list))
print()

print()
print("                        WITH ADDONE SMOOTHING                          ")
print(pandas.DataFrame(s2_count_addone, s2_list, s2_list))
print()

print()
print("                        GOOD TURING SMOOTHING                          ")
print(pandas.DataFrame(s2_count_gt, s2_list, s2_list))
print()

print("***********************************************************************")
print("                        S1: BIGRAM PROBABILITIES                       ")
print("***********************************************************************")

print()
print("                        WITHOUT SMOOTHING                              ")
print(pandas.DataFrame(s1_count_prob, s1_list, s1_list))
print()

print()
print("                        WITH ADDONE SMOOTHING                          ")
print(pandas.DataFrame(s1_addone_prob, s1_list, s1_list))
print()

print()
print("                        GOOD TURING SMOOTHING                          ")
print(pandas.DataFrame(s1_gt_prob, s1_list, s1_list))
print()

print("***********************************************************************")
print("                        S2: BIGRAM PROBABILITIES                       ")
print("***********************************************************************")

print()
print("                        WITHOUT SMOOTHING                              ")
print(pandas.DataFrame(s2_count_prob, s2_list, s2_list))
print()

print()
print("                        WITH ADDONE SMOOTHING                          ")
print(pandas.DataFrame(s2_addone_prob, s2_list, s2_list))
print()

print()
print("                        GOOD TURING SMOOTHING                          ")
print(pandas.DataFrame(s2_gt_prob, s2_list, s2_list))
print()

print("***********************************************************************")
print("                        S1: PROBABILITY                                ")
print("***********************************************************************")

print("Probability without Smoothing: ", s1_p)
print()

print("Probability with Addone Smoothing: ", s1_addone_p) 
print()

print("Probability with Good-Turing Smoothing: ", s1_gt_p) 
print()

print("***********************************************************************")
print("                        S2: PROBABILITY                                ")
print("***********************************************************************")

print("Probability without Smoothing: ", s2_p)
print()

print("Probability with Addone Smoothing: ", s2_addone_p) 
print()

print("Probability with Good-Turing Smoothing: ", s2_gt_p) 
print()

sys.exit(0)
