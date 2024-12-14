import argparse
import math
from file_handling_service import File_handler_service

#TODO: in file handler service change the delimiter to tab not new line
parser = argparse.ArgumentParser()

parser.add_argument("train_file_name")
parser.add_argument("test_file_name")
parser.add_argument("input_word")
parser.add_argument("output_file_name")

args = parser.parse_args()

#assume:
V = 300000

file_handling_service = File_handler_service(args.output_file_name)
file_handling_service.create_output_file()

def lidstone_smoothing(c_x, _lambda, S_size):
    return (c_x + _lambda) / (S_size + _lambda * V)

def perplexity_measure(s_validation_set, training_words_probabilities, p_unseen_word):
    perplexity = 0

    for word in s_validation_set:
        if word in training_words_probabilities:
            perplexity = perplexity + math.log(training_words_probabilities[word])
        else:
            perplexity = perplexity + math.log(p_unseen_word)

    perplexity = math.pow(2, (-1/len(s_validation_set))*perplexity)

    return perplexity

def lidstone_smoothing_model(training_set, training_events, _lambda):
    training_words_probabilities = {}

    for word in training_set:
        training_words_probabilities[word] = lidstone_smoothing(training_events[word], _lambda, len(training_set))

    return training_words_probabilities

def main():
    file_handling_service.write_output(1, args.train_file_name)
    file_handling_service.write_output(2, args.test_file_name)
    file_handling_service.write_output(3, args.input_word)
    file_handling_service.write_output(4, args.output_file_name)
    file_handling_service.write_output(5, V)
    file_handling_service.write_output(6, 1/V)

    S = file_handling_service.get_only_words_in_file(args.train_file_name)
    S_size = len(S)
    file_handling_service.write_output(7, S_size)

    training_set_size = round(0.9 * S_size)
    s_validation_set = S[training_set_size:]
    s_training_set = S[:training_set_size]
    s_training_set_size = len(s_training_set)

    file_handling_service.write_output(8, len(s_validation_set))
    file_handling_service.write_output(9, len(s_training_set))

    training_words_unique_values = {}

    for word in s_training_set:
        if word in training_words_unique_values:
            training_words_unique_values[word] +=1
        else:
            training_words_unique_values[word] = 1

    file_handling_service.write_output(10, len(training_words_unique_values.keys()))

    if(args.input_word in training_words_unique_values):
        c_input_word = training_words_unique_values[args.input_word]
    else:
        c_input_word = 0

    file_handling_service.write_output(11, c_input_word)

    p_input_words_mle = c_input_word / len(s_training_set)
    file_handling_service.write_output(12, p_input_words_mle)

    p_unseen_word = 0 / len(s_training_set) #can write immidiatly 0
    file_handling_service.write_output(13, p_unseen_word)

    _lambda = 0.10
    p_lid_input_word = lidstone_smoothing(c_input_word, _lambda, s_training_set_size)

    file_handling_service.write_output(14, p_lid_input_word)

    c_unseen_word = 0
    p_lid_unseen_word = lidstone_smoothing(c_unseen_word, _lambda, s_training_set_size)
    file_handling_service.write_output(15, p_lid_unseen_word)

    _lambdas = [0.01, 0.10, 1.00]

    for index, _lambda in enumerate(_lambdas):
        model = lidstone_smoothing_model(s_training_set, training_words_unique_values, _lambda)
        p_lid_unseen_word = lidstone_smoothing(c_unseen_word, _lambda, s_training_set_size)
        perplexity = perplexity_measure(s_validation_set, model, p_lid_unseen_word)
        file_handling_service.write_output(16+index, perplexity)

    all_possible_lambdas = [i / 100 for i in range(1, 201)]
    perplexities = []

    for index, _lambda in enumerate(all_possible_lambdas):
        model = lidstone_smoothing_model(s_training_set, training_words_unique_values, _lambda)
        p_lid_unseen_word = lidstone_smoothing(c_unseen_word, _lambda, s_training_set_size)
        perplexity = perplexity_measure(s_validation_set, model, p_lid_unseen_word)
        perplexities.append((perplexity, _lambda))

    min_perplexity = min(perplexities, key=lambda x: x[0])
    file_handling_service.write_output(19, min_perplexity[1])
    file_handling_service.write_output(20, min_perplexity[0])
main()