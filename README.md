# NLP-Assignments
Natural Language Processing Assignments

###### Execution:
	1. calculate_bigrams.py
	   Packages Needed: Pandas (sudo apt-get install python3-pandas)

	   python3 calculate_bigrams.py NLPCorpusTreebank2Parts-CorpusA-Unix.txt
	   python3 calculate_bigrams.py NLPCorpusTreebank2Parts-CorpusA-Unix.txt > output.txt

	2. pos.py (parts of speech tagging)
	   python3 pos.py HW2_F16_NLP6320_POSTaggedTrainingSet-Unix.txt

	3. viterbi.py
	   python3 viterbi.py <input_sequence>
       Sample: python3 viterbi.py "331123312"
       Note: Input sequence state should be in observation space i.e., [1, 2, 3] 

    4. simplified_lesk.py
       Packages Needed:
       	   nltk 3.2.1
		   averaged_perception_tagger and punkt from nltk library needs to be downloaded.
		   To download, open python3 interpretor:
		   		> import nltk
		   		> nltk.download('averaged_perception_tagger')
		   		> nltk.download('punkt')

	   python3 simplified_lesk.py
