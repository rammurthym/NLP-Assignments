# Name: Rammurthy Mudimadugula
# Net-ID: rxm163730
# Homework #2

import re
import sys
from collections import Counter
from collections import OrderedDict

#*******************************************************************************
#                           IO METHODS
#*******************************************************************************

# Method to read input from a file
def read_input(input_file):
    try:
        f = open(input_file, 'r');
        input_pos = f.read();
        return input_pos
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

def remove_pos_tags(input_pos):
	temp = re.sub(r'_[^\s]+', '', input_pos)
	f = open('POSRemovedTrainingSet.txt', 'w')
	f.write(temp)
	return temp.split()

#*******************************************************************************
#                           INTERNAL METHODS
#*******************************************************************************

# Given a list of strings, this method will convert it to list of tuples
def list_to_tuple(input_list):
    s_tuple = []
    for i in input_list:
        temp = i.split('_')
        s_tuple.append(list(zip([temp[0]], [temp[1]]))[0])
    return s_tuple


def calc_tag_count(input_list):
	counter = Counter()
	for i in input_list:
		counter[i] += 1
	return counter

# Method to calculate word count from a given corpus
def word_count(input_list):
    counter = Counter()
    for i in input_list:
        counter[i] += 1
    return counter

def calc_prob(wc, tuples, c):
    probabilities = OrderedDict()
    for i in tuples:
        probabilities[i] = (c[i]/wc[i[0]])
    return probabilities

# def retag(tuples, t5):
#     rt_list = []

#     for t in t5:
#         for key in t:
#             if prob[i] < 0.5:

#                 for key in prob:
#                     if i[0] in key:
#                         if prob[key] >= 0.5:
#                             rt_list.append('_'.join([str(i[0]), str(key[1])]))
#             else:
#                 rt_list.append('_'.join(str(j) for j in i))
#     return rt_list

def top_five(prob):
    s = [(k, prob[k]) for k in sorted(prob, key=prob.get, reverse=True)]

    t5 = []

    i = 0
    for m in s:
        if m[1] < 0.5:
            t5.append({m[0] : m[1]})
            if i == 4:
                break
            i += 1
    return t5

def print_t5(t5):
    print("Word \t\t\t Incorrect_Tag \t\t\t Error_Rate")
    for t in t5:
        for key in t:
            print(key[0] + '\t\t\t' + key[1] + '\t\t\t' + str(t[key]*100))

def make_file(rtlist):
    temp = ' '.join(rtlist)
    f = open('POSRetaggedTrainingSet.txt', 'w')
    f.write(temp)
    f.close()

#*******************************************************************************
#                           INTERNAL METHOD CALLS
#*******************************************************************************

input_pos = is_args()
rpt = remove_pos_tags(input_pos)
wc = word_count(rpt)
# print(wc)
input_list = input_pos.split()
# print(input_list[0].split("_")[0])
tuples = list_to_tuple(input_list)

# print(tuples)

c = calc_tag_count(tuples)


prob = calc_prob(wc, tuples, c)

t5 = top_five(prob)

# rtlist = retag(tuples, t5)
# print(rtlist)

# make_file(rtlist)

print_t5(t5)
