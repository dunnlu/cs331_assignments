# This file implements a Naive Bayes Classifier
import math

class BayesClassifier():
    """
    Naive Bayes Classifier
    file length: file length of training file
    sections: sections for incremental training
    """
    def __init__(self):
        self.postive_word_counts = {}
        self.negative_word_counts = {}
        self.percent_positive_sentences = 0
        self.percent_negative_sentences = 0
        self.file_length = 499
        self.file_sections = [self.file_length // 4, self.file_length // 3, self.file_length // 2]
        self.myTrainingVocab = []


    def train(self, train_data, train_labels, vocab, percent_of_data = 1):
        """
        This function builds the word counts and sentence percentages used for classify_text
        train_data: vectorized text
        train_labels: vectorized labels
        vocab: vocab from build_vocab
        """

        #only use "percent_of_data" of the data
        if percent_of_data != 1:
            removed_elements = int((1-percent_of_data)*len(train_labels)) #number of elements to remove
            train_data = train_data[:-removed_elements] #remove elements
            train_labels = train_labels[:-removed_elements] #remove elements

        self.myTrainingVocab = vocab #save vocab for classify_text

        #initialize word counts
        for word in vocab:
            self.postive_word_counts[word] = 1
            self.negative_word_counts[word] = 1

        train_labels = [int(i) for i in train_labels] #convert labels to ints
        #count words
        for i in range(len(train_data)):
            for j in range(len(vocab)):
                if train_data[i][j] == 1: #if word is in sentence
                    if train_labels[i] == 1: #if sentence is positive
                        self.postive_word_counts[vocab[j]] += 1 #increment positive word count
                    else:
                        self.negative_word_counts[vocab[j]] += 1 #increment negative word count
        
        #count sentences
        self.percent_positive_sentences = 0 #reset sentence counts
        self.percent_negative_sentences = 0
        for i in range(len(train_labels)): #for each sentence
            if train_labels[i] == 1: #if sentence is positive
                self.percent_positive_sentences += 1 #increment positive sentence count
            else:
                self.percent_negative_sentences += 1 #increment negative sentence count

        #return the number of examples, for plotting purposes
        return len(train_labels)


    def classify_text(self, vectors, vocab):
        """
        vectors: [vector1, vector2, ...]
        predictions: [0, 1, ...]
        """
        
        #direchlet priors
        for word in vocab:
            if not word in self.myTrainingVocab: #if word is not in training vocab
                self.postive_word_counts[word] = 1
                self.negative_word_counts[word] = 1


        predictions = [] #list of predictions
        for vector in vectors:
            # initialize probabilities to 0
            positive_probability = 0
            negative_probability = 0

            #working in log space, we add instead of multiply
            positive_probability += math.log(self.percent_positive_sentences) #multiply by positive sentence count
            negative_probability += math.log(self.percent_negative_sentences) #multiply by negative sentence count

            # calculate probabilities
            for i in range(len(vector)):
                if vector[i] == 1: #if word is in sentence
                    #P(word | positive)
                    positive_probability += math.log(self.postive_word_counts[vocab[i]] / (self.percent_positive_sentences)) 
                    #P(word | negative)
                    negative_probability += math.log(self.negative_word_counts[vocab[i]] / (self.percent_negative_sentences)) 
                else: #if word is not in sentence
                    #P(not word | positive)
                    positive_probability += math.log((self.percent_positive_sentences - self.postive_word_counts[vocab[i]]) / (self.percent_positive_sentences)) 
                    #P(not word | negative)
                    negative_probability += math.log((self.percent_negative_sentences - self.negative_word_counts[vocab[i]]) / (self.percent_negative_sentences)) 

            # make prediction
            if positive_probability > negative_probability: 
                predictions.append(1)
            else:
                predictions.append(0)

        return predictions
    