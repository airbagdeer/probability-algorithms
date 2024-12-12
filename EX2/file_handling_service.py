class File_handler_service:
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, output_file_name):
        self.output_file_name = output_file_name

    def create_output_file(self):
        with open(self.output_file_name, "w") as file:
            file.write("#Students Eyal Stolov Michael Chernin 324827328 314950668\n")


    def write_output(self, output_number, output_text):
        with open(self.output_file_name, "a") as file:
            file.write(f'#Output{output_number} {output_text}\n')

    def get_only_words_in_train_file(self, train_file_name):
        words_in_file = []
        with open(train_file_name, "r") as file:
            for line in file:
                words_split_by_space = line.split(' ')
                for word in words_split_by_space:
                    if word.isalpha():
                        words_in_file.append(word)
                    else:
                        #TODO: what do we do with the words here
                        print(word)


            return words_in_file