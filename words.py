from trie import Trie
from nltk.corpus import wordnet
import random
import csv
import sys

class Words:
    # 辞書読み込み
    def __init__(self, dict_path):
        self.dict_path = dict_path # ./data/origin/wordnet_words.csv
        self.words_dict = None
        self.words = None

        with open(self.dict_path, "r", encoding="utf-8") as f:
            data = f.read()

        self.words_dict = dict([(int(i.split(",")[0]), i.split(",")[1]) for i in data.split("\n") if i != ""])
        self.words = [i for i in self.words_dict.values()]

    # 計測用のテストデータ作成
    def create_test_words(self, size):
        test_dict = {}
        while len(test_dict.keys()) < size:
            w = random.choice(list(self.words_dict.items()))
            test_dict.setdefault(w[0], w[1])

        return test_dict


class CreateWords:
    # wordnetから辞書作成
    def __init__(self, dict_path):
        self.dict_path = dict_path # ./data/origin/wordnet_words.csv
        words = list(set([i.lemmas()[0].name() for i in wordnet.all_synsets()]))
        trie = Trie(words)
        with open(dict_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for k in words:
                writer.writerow([trie.search(k), k])



if __name__ == "__main__":

    # テストデータ作成
    t = Words(sys.argv[1])
    words_dict = t.words_dict
    words = t.words

    dict_path = "./data/test/wordnet_words_"
    for s in sys.argv[2].split(','):
        test_dict = t.create_test_words(int(s))
        with open(dict_path+str(s)+".csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for k, v in test_dict.items():
                writer.writerow([k, v])

    print("Test data is created.")