# This file implements a Naive Bayes Classifier


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


    def train(self, train_data, train_labels, vocab):
        """
        This function builds the word counts and sentence percentages used for classify_text
        train_data: vectorized text
        train_labels: vectorized labels
        vocab: vocab from build_vocab
        """
        #initialize word counts
        for word in vocab:
            self.postive_word_counts[word] = 1
            self.negative_word_counts[word] = 1

        #count words
        for i in range(len(train_data)):
            for j in range(len(vocab)):
                if train_data[i][j] == 1: #if word is in sentence
                    if train_labels[i] == 1: #if sentence is positive
                        self.postive_word_counts[vocab[j]] += 1 #increment positive word count
                    else:
                        self.negative_word_counts[vocab[j]] += 1 #increment negative word count

        #count sentences
        train_labels = [int(i) for i in train_labels] #convert labels to ints
        for i in range(len(train_labels)): #for each sentence
            if train_labels[i] == 1: #if sentence is positive
                self.percent_positive_sentences += 1 #increment positive sentence count
            else:
                self.percent_negative_sentences += 1 #increment negative sentence count

        print("Positive sentences: ", self.percent_positive_sentences)
        print("Negative sentences: ", self.percent_negative_sentences)

        #calculate percentages
        self.percent_positive_sentences /= len(train_labels)
        self.percent_negative_sentences /= len(train_labels)

        #print results
        print("Percent positive sentences: ", self.percent_positive_sentences)
        print("Percent negative sentences: ", self.percent_negative_sentences)
        return 1


    def classify_text(self, vectors, vocab):
        """
        vectors: [vector1, vector2, ...]
        predictions: [0, 1, ...]
        """
        #There is a problem here, since the training vocab and test vocab are not equivalent, but the code assumes that they are
        #We need to implement direchlet priors, and find the correct way to call the correct vocab word's word counts
        
        predictions = [] #list of predictions
        for vector in vectors:
            # initialize probabilities
            positive_probability = 1
            negative_probability = 1

            # calculate probabilities
            for i in range(len(vector)):
                if vector[i] == 1: #if word is in sentence
                    positive_probability *= (self.postive_word_counts[vocab[i]] / (self.postive_word_counts[vocab[i]] + self.negative_word_counts[vocab[i]])) #multiply by positive word count
                    negative_probability *= (self.negative_word_counts[vocab[i]] / (self.postive_word_counts[vocab[i]] + self.negative_word_counts[vocab[i]])) #multiply by negative word count
            positive_probability *= self.percent_positive_sentences #multiply by positive sentence count
            negative_probability *= self.percent_negative_sentences #multiply by negative sentence count
            if positive_probability > negative_probability:
                predictions.append(1)
            else:
                predictions.append(0)

            # print results
            #print("Positive probability: ", positive_probability)
            #print("Negative probability: ", negative_probability)
            #print("Prediction: ", predictions[-1])
        return predictions
    