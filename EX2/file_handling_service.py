class File_handler_service:
    def __init__(self, output_file_name):
        self.output_file_name = output_file_name

    def create_output_file(self):
        with open(self.output_file_name, "w", encoding="utf-8") as file:
            file.write('#Students\tEyal Stolov\tMichael Chernin\t324827328\t314950668\n')


    def write_output_number(self, output_number, output_text):
        with open(self.output_file_name, "a") as file:
            if(output_number==29):
                file.write(f'#Output{output_number}\n')
            else:
                file.write(f'#Output{output_number}\t{output_text}\n')

    def write_output_row(self, elements):
        with open(self.output_file_name, "a") as file:
            file.write('\t'.join(map(str, elements)) + '\n')

    def get_only_words_in_file(self, file_name):
        words_in_file = []
        with open(file_name, "r") as file:
            for line in file:
                if '<TRAIN' not in line and '<TEST' not in line:
                    words_split_by_space = line.split(' ')
                    for word in words_split_by_space:
                        if word != '\n':
                            words_in_file.append(word)
            return words_in_file