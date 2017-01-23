import sys

#*******************************************************************************
#                           INPUT STATES AND MATRICES
#*******************************************************************************

observation_space = ['1', '2', '3']
state_space       = ['hot', 'cold']

transition_matrix = {
	'hot' : {
		'start' : 0.8,
		'hot'   : 0.7,
		'cold'  : 0.4
	},
	'cold' : {
		'start' : 0.2,
		'hot'   : 0.3,
		'cold'  : 0.6
	}
}

emission_matrix   = {
	'hot' : {
		'1' : 0.2,
		'2' : 0.4,
		'3' : 0.4
	},
	'cold' : {
		'1' : 0.5,
		'2' : 0.4,
		'3' : 0.1
	}
}

#*******************************************************************************
#                           IO METHODS
#*******************************************************************************

# Method to check whether user has passed input
def is_args():
    if (len(sys.argv) == 2):
        return list(sys.argv[1].replace(' ', ''))
    else:
        print('Please provide input as an argument')
        sys.exit(1)

# Method to verify whether given input sequence is in observaton space
def verify_input(seq, obs_space):
	for i in seq:
		if i not in obs_space:
			print('Sequence should be a permutation of 1, 2, 3.')
			print('Please provide a valid sequence')
			sys.exit(1)

#*******************************************************************************
#                           INTERNAL METHODs
#*******************************************************************************

# Implementation of Viterbi algorithm
def viterbi(states, trans_mat, emis_mat, seq):
	v = [];
	bp = [];
	sl = len(seq)

	v.append({})

	for s in states:
		v[0][s] = trans_mat[s]['start'] * emis_mat[s][seq[0]]
		bp.append('')

	for t in range(1, sl):
		v.append({})
		for s in states:
			v[t][s] = 0
			bp.append('')
			for i in states:
				temp = v[t-1][i] * trans_mat[i][s] * emis_mat[s][seq[t]]
				if(temp > v[t][s]):
					v[t][s] = temp
					bp[t] = i

	bp.append('')
	high_v = 0

	for s in states:
		if(v[sl - 1][s] > high_v):
			high_v = v[sl - 1][s]
			bp[sl] = s

	return bp

# Print the output sequence.
def print_output(bp):
	print('The most likely weather sequence for the given observation is:')
	print(' '.join(list(filter(None, bp))))

#*******************************************************************************
#                           INTERNAL METHOD CALLS
#*******************************************************************************

sequence = is_args()
verify_input(sequence, observation_space)
bp = viterbi(state_space, transition_matrix, emission_matrix, sequence)
print_output(bp)
