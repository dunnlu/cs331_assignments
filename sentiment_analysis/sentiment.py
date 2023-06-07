# CS331 Sentiment Analysis Assignment 3
# This file contains the processing functions

import string
import re
import unicodedata
from classifier import BayesClassifier

def process_text(text):
    """
    Preprocesses the text: Remove apostrophes, punctuation marks, etc.
    Returns a list of text
    """
    translator = str.maketrans('','',string.punctuation) #create punctuation translator table
    preprocessed_text = text.translate(translator).lower()  #remove punctuation, then convert to lowercase
    preprocessed_text = unicodedata.normalize('NFKD', preprocessed_text)  # Normalize using NFKD
    preprocessed_text = ''.join(c for c in preprocessed_text if not unicodedata.combining(c))
    return preprocessed_text #a string with no punctuation, in all lowercase


def build_vocab(preprocessed_text):
    """
    Builds the vocab from the preprocessed text
    preprocessed_text: output from process_text
    Returns unique text tokens
    """
    words = re.sub(r'\d+','',preprocessed_text).split()  #removes numbers, returns a list of the words
    vocab = sorted(list(set(words))) #sorts the list, then converts to a set
    return vocab 


def vectorize_text(text, vocab): 
    """
    Converts the text into vectors
    text: preprocess_text from process_text
    vocab: vocab from build_vocab
    Returns the vectorized text and the labels
    """
    n = len(vocab) #for later use
    vectorized_text = [] #this is going to be a list of featurized vectors (which are themselves a list)
    labels = [] #one label for each sentence

    lines = text.splitlines() #lines is a list of the lines in the preprocessed text
    for line in lines:
        words = line.split()
        #create an array of size n
        vector = [0 for i in range(n)] #initialize the vector to all 0s

        #go through the vector and for each word, see if it is in the line, if so give it value 1
        for i in range(n):
            if vocab[i] in words:
                vector[i] = 1 
        
        labels.append(line[len(line)-2]) #add the label to the list of labels
        vectorized_text.append(vector) #add the vector to the list of vectors
    return vectorized_text, labels


def accuracy(predicted_labels, true_labels):
    """
    predicted_labels: list of 0/1s predicted by classifier
    true_labels: list of 0/1s from text file
    return the accuracy of the predictions
    """
    accuracy_score = 0
    #for i,j in predicted_labels, true_labels:
    #    if(i == j):
    #        accuracy_score += 1

    predicted_labels = [int(i) for i in predicted_labels]
    true_labels = [int(i) for i in true_labels]
    for i in range(len(predicted_labels)):
        if(predicted_labels[i] == true_labels[i]):
            accuracy_score += 1
    accuracy_score /= len(predicted_labels)
    return accuracy_score

def process(input_file,output_file):
    with open(input_file, 'r',encoding='utf-8') as file:
        text = file.read()
    pre_processed_text = process_text(text) #preprocess the text

    vocab = build_vocab(pre_processed_text) #build the vocab

    vectorized_text,labels = vectorize_text(pre_processed_text,vocab) #vectorize the text

    n = len(labels)
    with open(output_file,'w',encoding='utf-8') as file: #write the vectorized text to a file
        first_line = ",".join(vocab) + ",classlabel\n" #first line is the vocab
        file.write(first_line)
        for i in range(n):
            feature_vector = [str(num) for num in vectorized_text[i]] #convert the vector to a list of strings
            subsequent_line = ",".join(feature_vector) + "," + labels[i] + "\n" #add the label to the end
            file.write(subsequent_line)

    return vectorized_text, vocab, labels


def main():
    # Take in text files and outputs sentiment scores
    training_vectorized_text, training_vocab, training_labels = process("trainingSet.txt","preprocessed_train.txt") #process training set and output to "preprocessed_train.txt"
    test_vectorized_text, test_vocab, test_labels = process("testSet.txt","preprocessed_test.txt") #process test set and output to "preprocessed_test.txt"

    classifier = BayesClassifier()
    with open("sentiment.csv",'w',encoding='utf-8') as file: #write the vectorized text to a file
        print("alpha,example size,test accuracy,training accuracy")
        file.write("alpha,example size,test accuracy,training accuracy\n")
        for i in range(1, 5):
            example_size = classifier.train(training_vectorized_text, training_labels, training_vocab, .25*i)
            training_predicted_labels = classifier.classify_text(training_vectorized_text, training_vocab)
            test_predicted_labels = classifier.classify_text(test_vectorized_text, test_vocab)
            print(i*.25, ",",example_size, ",", accuracy(training_predicted_labels, training_labels), ",", accuracy(test_predicted_labels, test_labels))
            file.write(str(i*.25) + "," + str(example_size) + "," + str(accuracy(training_predicted_labels, training_labels)) + "," + str(accuracy(test_predicted_labels, test_labels)) + "\n")
        

    return 1


if __name__ == "__main__":
    main()