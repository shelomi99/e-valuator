from nltk.corpus import stopwords
from nltk import pos_tag
from math import sqrt
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averagwheed_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

similarity_benchmark = 0.8


def total_magnitude(vector):
    total = 0
    for num in vector:
        total += (num * num)
    total = sqrt(total)
    return total


def similarityVectors(postag1, postag2):
    # Creating a similarity vectors for the two given sentences. Calculate the max similarity for each word in pos1.
    # This is accomplished by using WordNet definitions of pos tags and determining the path similarity between them.
    global similarity_benchmark
    similarity_vec = []
    for word1 in postag1:
        max_similarity = 0
        for word2 in postag2:
            if max_similarity >= similarity_benchmark:
                break
            # matching parts of speech
            if word1[1] == word2[1]:
                definition1 = wn.synsets(word1[0])
                definition2 = wn.synsets(word2[0])
                for def1 in definition1:
                    if max_similarity >= similarity_benchmark:
                        break
                    for def2 in definition2:
                        if def1.pos != def2.pos:
                            continue
                        sim = def1.path_similarity(def2)
                        if sim and sim > max_similarity:
                            max_similarity = sim
                        if max_similarity >= similarity_benchmark:
                            break
        similarity_vec.append(max_similarity)
    return similarity_vec


def wordSimilarity(tag1, tag2):
    # Compare the shortest path between the words in sentences
    postag1 = pos_tag(tag1)
    postag2 = pos_tag(tag2)
    similarity_vec1 = similarityVectors(postag1, postag2)
    similarity_vec2 = similarityVectors(postag2, postag1)
    return similarity_vec1, similarity_vec2


# Calculating the similarity of words in the sentences.
def stringSimilarity(model_answer, student_answer):
    global similarity_benchmark
    tokens1 = word_tokenize(model_answer)
    tokens2 = word_tokenize(student_answer)
    tokens1 = [word for word in tokens1 if word not in stopwords.words('english')]
    tokens2 = [word for word in tokens2 if word not in stopwords.words('english')]
    stemmer = PorterStemmer()
    tokens1 = [stemmer.stem(t) for t in tokens1]
    tokens2 = [stemmer.stem(t) for t in tokens2]
    sim_vec1, sim_vec2 = wordSimilarity(tokens1, tokens2)
    sim_mag1 = total_magnitude(sim_vec1)
    sim_mag2 = total_magnitude(sim_vec2)
    sim_mag = sim_mag1 * sim_mag2
    sim_constant = 1.8
    above_bench1, above_bench2 = 0, 0
    for sim in sim_vec1:
        if sim > similarity_benchmark:
            above_bench1 += 1
    for sim in sim_vec2:
        if sim > similarity_benchmark:
            above_bench2 += 1
    above_bench = above_bench1 + above_bench2
    above_bench /= sim_constant
    if above_bench > 0:
        similarity = sim_mag / above_bench
    else:
        m = max(len(tokens1), len(tokens2)) / 2
        similarity = sim_mag / m

    string_matching_similarity = "{:.2f}".format(similarity * 40)
    # 20% of the total score is allocated for the keyword similarity score
    return float(string_matching_similarity)


# # testing method
# model_answer = 'It\'s a huge black eye, said publisher Arthur Ochs Sulzberger Jr., whose family has controlled the paper since 1896.'
# student_answer = 'It\'s a huge black eye, said publisher Arthur '
# similarity = semanticSimilarity(model_answer, student_answer)
# print(similarity, "/10")
