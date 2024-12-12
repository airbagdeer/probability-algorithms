import argparse
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

def q1():
    file_handling_service.write_output(1, args.train_file_name)
    file_handling_service.write_output(2, args.test_file_name)
    file_handling_service.write_output(3, args.input_word)
    file_handling_service.write_output(4, args.output_file_name)
    file_handling_service.write_output(5, V)

    train_file_words = file_handling_service.get_only_words_in_train_file(args.train_file_name)
    words_unique_values = {}

    for word in train_file_words:
        if word in words_unique_values:
            words_unique_values[word] +=1
        else:
            words_unique_values[word] = 1


    if(args.input_word in words_unique_values):
        file_handling_service.write_output(6, words_unique_values[args.input_word]/len(train_file_words))
    # print(file_handling_service.get_only_words_in_train_file(args.train_file_name))

q1()
