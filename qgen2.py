import secrets
import string
import word_check
import random


class QGen:

    def __init__(self) -> None:
        self.characters = (
            string.ascii_lowercase,
            string.ascii_uppercase,
            string.digits,
            string.punctuation
        )

        self.simple_punctuation = """!#$%&'()*+,-./:;<=>?@[\\]_}{~"""

        self.lowercase_vowels = list("aoiue")
        self.lowercase_consonants = list("bcdfghjklmnpqrstvwxzy")

        self.cluster_brake_prob = (
            [0, 0, 0, 0, 12, 25, 48, 65, 100],
            [0, 0, 0, 12, 25, 48, 65, 100],
            [0, 0, 25, 67, 100],
            [0, 25, 67, 100]
        )

        self.profanity_checker = word_check.ProfanityCheck()

        self.cluster_separator = "_"

    def weighted_random(self, length: int = 8, flags: list = [100, 0, 60, 0]) -> str:

        number_of_enabled_flags = len([f for f in flags if f != 0])
        
        # TODO: add minimal password length
        # length should not be less than the amount of (enabled) sets
        if length < number_of_enabled_flags:
            return "length is too low"
        
        if number_of_enabled_flags == 0:
            return "all flags are zeros"
        
        len_flags = len(flags)

        # amount of flags should be equal to the amount of character sets
        if len_flags != len(self.characters):
            return "flags error"
        

        # (100, 20) -> (100, 120)
        # continous sum of the flags to form ranges for the rolls
        chances_sum = 0
        flags_ranges = []
        for i in range(len_flags):
            if flags[i]:
                chances_sum += flags[i]
                flags_ranges.append(chances_sum)
            else:
                flags_ranges.append(0)

        generated_string = ""

        # adding a unique forced occurrence index for every non-zero flag
        # so even if this flag never rolls, there will always be one instance
        forced_occurrence_index = []
        for i in range(len_flags):
            if flags[i]:
                is_unique_index = False
                while not is_unique_index:
                    index_roll = secrets.randbelow(length)
                    if index_roll not in forced_occurrence_index:
                        is_unique_index = True
                        forced_occurrence_index.append(index_roll)

            # disabled flags must not occur, hence an index that never happens
            else:
                forced_occurrence_index.append(-1)

        # for each spot of the to be generated string
        for i in range(length):

            # found forced occurrence of a flag on this index
            if i in forced_occurrence_index:
                generated_string += "".join(secrets.choice(self.characters[forced_occurrence_index.index(i)]))

            # standard roll
            else:
                roll = secrets.randbelow(chances_sum)
                for j in range(len_flags):
                    if roll < flags_ranges[j]:
                        generated_string += "".join(secrets.choice(self.characters[j]))
                        break

        return generated_string
    

    def readable_letters(self, length: int = 8, is_upper: bool = False) -> str:

        next_vowel_chance = 0
        is_previous_vowel = True

        generated_string = ""
        
        is_profanity_found = True
        
        while is_profanity_found:

            for _ in range(length):

                # adding a vowel to the string
                if secrets.randbelow(100) < next_vowel_chance:
                    generated_string += "".join(secrets.choice(self.lowercase_vowels))
                    if is_previous_vowel:
                        # vow. + vow. => 100% chance for cons.
                        next_vowel_chance = 0
                    else:
                        # cons. + vow. => 90% chance for cons.
                        next_vowel_chance = 10
                    is_previous_vowel = True

                # adding a consonant to the string
                else:
                    generated_string += "".join(secrets.choice(self.lowercase_consonants))
                    if is_previous_vowel:
                        # vow. + cons. => 70% chance for vow.
                        next_vowel_chance = 70
                    else:
                        # cons. + cons. => 100% chance for vow.
                        next_vowel_chance = 100
                    is_previous_vowel = False

            is_profanity_found = self.profanity_checker.find_occurrence(generated_string)

        if is_upper:
            return generated_string.upper()
        return generated_string

    def random_string_digits(self, length: int = 3, is_punct = False):
        generated_string = ""
        if not is_punct:
            for _ in range(length):
                generated_string += "".join(secrets.choice(self.characters[2]))
        else:
            for _ in range(length):
                generated_string += "".join(secrets.choice(self.simple_punctuation))
        return generated_string
    
    def cluster_gen(self, 
                    length: int = 8, 
                    flags: list = [100, 0, 60, 0],
                    cluster_separation = False,
                    merge_clusters = False) -> str:
        
        number_of_enabled_flags = len([f for f in flags if f != 0])

        # length should not be less than the amount of (enabled) sets
        if length < number_of_enabled_flags:
            return "length is too low"
        
        if number_of_enabled_flags == 0:
            return "all flags are zeros"

        len_flags = len(flags)

        # amount of flags should be equal to the amount of character sets
        if len_flags != len(self.characters):
            return "flags error"
        
        
        # list of pairs: cluster index and cluster length
        active_clusters_holder = []
        archived_clusters = []
        
        # (100, 20) -> (100, 120)
        # continous sum of the flags to form ranges for the rolls
        chances_sum = 0
        flags_ranges = []
        for i in range(len_flags):
            if flags[i]:
                chances_sum += flags[i]
                flags_ranges.append(chances_sum)
            else:
                flags_ranges.append(0)

        # empty fill
        for i in range(len_flags):
            active_clusters_holder.append([i, 0])

        non_zero_amount = 0

        # for every non-zero at least 1 symbol
        for i in range(len_flags):
            if flags[i]:
                # change length of the cluster to 1
                active_clusters_holder[i][1] = 1
                non_zero_amount += 1
            
        length_left = length - non_zero_amount

        # for the length of the password
        for i in range(length_left):
            flag_roll = secrets.randbelow(chances_sum)
            for j in range(len_flags):
                if flag_roll < flags_ranges[j]:
                    active_clusters_holder[j][1] += 1

                    # second roll for braking
                    if (secrets.randbelow(100) < self.cluster_brake_prob[j][active_clusters_holder[j][1]]):
                        archived_clusters.append(active_clusters_holder[j].copy())
                        active_clusters_holder[j][1] = 0

                    break

        # archive all the remaining (active) non-zero clusters
        for i in range(len_flags):
            if active_clusters_holder[i][1]:
                archived_clusters.append(active_clusters_holder[i].copy())

        random.shuffle(archived_clusters)

        generated_string = ""

        for cluster in archived_clusters:

            if cluster_separation:
                generated_string += "".join(self.cluster_separator)

            if cluster[0] == 0:
                generated_string += "".join(self.readable_letters(cluster[1], is_upper=False))
                continue
            if cluster[0] == 1:
                generated_string += "".join(self.readable_letters(cluster[1], is_upper=True))
                continue
            if cluster[0] == 2:
                generated_string += "".join(self.random_string_digits(cluster[1], is_punct=False))
                continue
            if cluster[0] == 3:
                generated_string += "".join(self.random_string_digits(cluster[1], is_punct=True))
                continue
            else:
                generated_string += "".join(".null.")
                continue
        
        return generated_string


if __name__ == '__main__':
    test = QGen()
    print(test.cluster_gen(20))
