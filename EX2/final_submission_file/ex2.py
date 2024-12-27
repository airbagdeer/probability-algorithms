import argparse
import math
from file_handling_service import File_handler_service

parser = argparse.ArgumentParser()

parser.add_argument("train_file_name")
parser.add_argument("test_file_name")
parser.add_argument("input_word")
parser.add_argument("output_file_name")

args = parser.parse_args()

# assume:
V = 300000

file_handling_service = File_handler_service(args.output_file_name)
file_handling_service.create_output_file()


def count_words(words_set):
    words_unique_values = {}

    for word in words_set:
        if word in words_unique_values:
            words_unique_values[word] += 1
        else:
            words_unique_values[word] = 1

    return words_unique_values

def count_frequencies(words_frequency):
    frequencies_count = {}

    for word in words_frequency.keys():
        if words_frequency[word] in frequencies_count:
            frequencies_count[int(words_frequency[word])] = frequencies_count[words_frequency[word]] + [word]
        else:
            frequencies_count[int(words_frequency[word])] = [word]

    return frequencies_count

def lidstone_smoothing(c_x, _lambda, S_size):
    return (c_x + _lambda) / (S_size + _lambda * V)


def perplexity_measure(s_validation_set, training_words_probabilities, p_unseen_word):
    if len(s_validation_set) == 0:
        return float('inf')  # Perplexity is undefined for empty sets

    perplexity = 0

    for word in s_validation_set:
        if word in training_words_probabilities:
            perplexity = perplexity + math.log2(training_words_probabilities[word])
        else:
            perplexity = perplexity + math.log2(p_unseen_word)

    perplexity = math.pow(2, (-1 / len(s_validation_set)) * perplexity)

    return perplexity


def lidstone_smoothing_model(training_set, training_events, _lambda):
    training_words_probabilities = {}

    for word in training_set:
        training_words_probabilities[word] = lidstone_smoothing(training_events[word], _lambda, len(training_set))

    return training_words_probabilities


def main():
    file_handling_service.write_output_number(1, args.train_file_name)
    file_handling_service.write_output_number(2, args.test_file_name)
    file_handling_service.write_output_number(3, args.input_word)
    file_handling_service.write_output_number(4, args.output_file_name)
    file_handling_service.write_output_number(5, V)
    file_handling_service.write_output_number(6, 1 / V)

    S = file_handling_service.get_only_words_in_file(args.train_file_name)
    S_size = len(S)
    file_handling_service.write_output_number(7, S_size)

    training_set_size = round(0.9 * S_size)
    s_validation_set = S[training_set_size:]
    s_training_set = S[:training_set_size]
    s_training_set_size = len(s_training_set)

    file_handling_service.write_output_number(8, len(s_validation_set))
    file_handling_service.write_output_number(9, len(s_training_set))

    training_words_unique_values = count_words(s_training_set)

    file_handling_service.write_output_number(10, len(training_words_unique_values.keys()))

    if (args.input_word in training_words_unique_values):
        c_input_word = training_words_unique_values[args.input_word]
    else:
        c_input_word = 0

    file_handling_service.write_output_number(11, c_input_word)

    p_input_words_mle = c_input_word / len(s_training_set)
    file_handling_service.write_output_number(12, p_input_words_mle)

    p_unseen_word = 0 / len(s_training_set)  # can write immidiatly 0
    file_handling_service.write_output_number(13, p_unseen_word)

    _lambda = 0.10
    p_lid_input_word = lidstone_smoothing(c_input_word, _lambda, s_training_set_size)

    file_handling_service.write_output_number(14, p_lid_input_word)

    c_unseen_word = 0
    p_lid_unseen_word = lidstone_smoothing(c_unseen_word, _lambda, s_training_set_size)
    file_handling_service.write_output_number(15, p_lid_unseen_word)

    _lambdas = [0.01, 0.10, 1.00]

    for index, _lambda in enumerate(_lambdas):
        model = lidstone_smoothing_model(s_training_set, training_words_unique_values, _lambda)
        p_lid_unseen_word = lidstone_smoothing(c_unseen_word, _lambda, s_training_set_size)
        perplexity = perplexity_measure(s_validation_set, model, p_lid_unseen_word)
        file_handling_service.write_output_number(16 + index, perplexity)

    all_possible_lambdas = [i / 100 for i in range(1, 201)]
    perplexities = []

    for index, _lambda in enumerate(all_possible_lambdas):
        model = lidstone_smoothing_model(s_training_set, training_words_unique_values, _lambda)
        p_lid_unseen_word = lidstone_smoothing(c_unseen_word, _lambda, s_training_set_size)
        perplexity = perplexity_measure(s_validation_set, model, p_lid_unseen_word)
        perplexities.append((perplexity, _lambda))

    [best_perplexity, best_lambda] = min(perplexities, key=lambda x: x[0])
    file_handling_service.write_output_number(19, best_lambda)
    file_handling_service.write_output_number(20, best_perplexity)

    S_t = S[:S_size // 2]
    S_h = S[S_size // 2:]
    S_t_size = len(S_t)
    S_h_size = len(S_h)

    file_handling_service.write_output_number(21, S_t_size)
    file_handling_service.write_output_number(22, S_h_size)

    S_t_words_count = count_words(S_t)
    S_h_words_count = count_words(S_h)

    S_t_frequencies_count = count_frequencies(S_t_words_count)
    S_h_frequencies_count = count_frequencies(S_h_words_count)

    held_out_model = {}

    for r, words in S_t_frequencies_count.items():
        t_rs = 0
        for word in words:
            if word in S_h_words_count:
                t_rs += S_h_words_count[word]

        probability = (t_rs)/((len(words)) * S_h_size)

        for word in words:
            held_out_model[word]=probability

    sum_unseen = 0
    N_0 = V - len(S_t_words_count.keys())
    for words in S_h_frequencies_count.values():
        for word in words:
            if word not in S_t_words_count:
                sum_unseen += S_h_words_count[word]

    p_heldout_unseen_word = sum_unseen/(N_0*S_h_size)

    file_handling_service.write_output_number(23, held_out_model[args.input_word])
    file_handling_service.write_output_number(24, p_heldout_unseen_word)

    S_test = file_handling_service.get_only_words_in_file(args.test_file_name)
    file_handling_service.write_output_number(25, len(S_test))

    best_lid_model = lidstone_smoothing_model(s_training_set, training_words_unique_values, best_lambda)
    best_p_lid_unseen_word = lidstone_smoothing(c_unseen_word, best_lambda, s_training_set_size)

    test_perplexity_lid = perplexity_measure(S_test, best_lid_model, best_p_lid_unseen_word)
    test_perplexity_heldout = perplexity_measure(S_test, held_out_model, p_heldout_unseen_word)

    file_handling_service.write_output_number(26, test_perplexity_lid)
    file_handling_service.write_output_number(27, test_perplexity_heldout)

    file_handling_service.write_output_number(28, 'H' if test_perplexity_heldout < test_perplexity_lid else 'L')

    lid_training_frequencies_count = count_frequencies(training_words_unique_values)

    f_lambda = [round(best_p_lid_unseen_word*training_set_size, 5)]
    f_H = [round(p_heldout_unseen_word*S_t_size, 5)]
    N_T_rs = [V-len(S_t_words_count.keys())]
    t_rs = []

    t_r = 0
    for word in S_h_words_count:
        if word not in S_t_words_count:
            t_r += S_h_words_count[word]

    t_rs.append(t_r)

    for r in range(1,10):
        words_appearing_r_times_in_lidstone_training = lid_training_frequencies_count[r]
        words_appearing_r_times_in_heldout_training = S_t_frequencies_count[r]

        f_lambda.append(round(best_lid_model[words_appearing_r_times_in_lidstone_training[0]]*training_set_size, 5))
        f_H.append(round(held_out_model[words_appearing_r_times_in_heldout_training[0]]*S_t_size, 5))
        N_T_rs.append(len(words_appearing_r_times_in_heldout_training))

        t_r = 0
        for word in words_appearing_r_times_in_heldout_training:
            if word in S_h_words_count:
                t_r += S_h_words_count[word]

        t_rs.append(t_r)

    file_handling_service.write_output_number(29,'')

    for values in zip(range(10),f_lambda, f_H, N_T_rs, t_rs):
        file_handling_service.write_output_row(values)


    #debugging as requested, to check the sum of probabilities is equal to one:
    # print(sum(best_lid_model.values()) + best_p_lid_unseen_word*(V-len(best_lid_model.values())))
    # print(sum(held_out_model.values()) + p_heldout_unseen_word*N_0)

main()
