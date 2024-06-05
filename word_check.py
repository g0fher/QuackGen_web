import os

class ProfanityCheck:
    word_set = {}

    def __init__(self) -> None:
        self.word_set = self.load_words_from_file()

    def load_words_from_file(self):
        script_dir = os.path.dirname(__file__)
        rel_path = "resourses/bad-words-mini.txt"
        abs_file_path = os.path.join(script_dir, rel_path)

        try:
            with open(abs_file_path, 'r') as file:
                words = file.read().split()
            return set(words)

        except FileNotFoundError:
            print("File not found.")
            return set()

    def find_occurrence(self, input_string: str):
        for elem in self.word_set:
            if str(elem).lower() in str(input_string).lower():
                return True
        return False


# if __name__ == '__main__':
#     test = "hit123"
#     prof_test = ProfanityCheck()
#     print(prof_test.find_occurrence(test))    
