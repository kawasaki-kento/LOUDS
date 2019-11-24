from trie import Trie
from measure import MeasureTime, MeasureMemory
from words import Words
from nltk.corpus import wordnet
import sys


# 辞書読み込み
t = Words(sys.argv[1]) # ./data/origin/wordnet_words.csv
words_dict = t.words_dict
words = t.words

# Trie木作成
print("=========================== 使用メモリ ===========================")
trie = Trie(words)

m = MeasureMemory()
# bit配列のメモリ使用量、ラベル配列のメモリ使用量
print("bit_array:", m.convert_bytes(m.compute_object_size(trie.bit_array)), "labels:", m.convert_bytes(m.compute_object_size(trie.labels)))

# selectのメモリ使用量
print("select:", m.convert_bytes(m.compute_object_size(trie.zero_pos)))

# rankのメモリ使用量
print("rank:", m.convert_bytes(m.compute_object_size(trie.split_list)))

x = input("Input search word:")

# 単語検索
print("=========================== 単語検索 ===========================")
while True:
    # 完全一致検索の実行時間測定インスタンス作成
    es = MeasureTime(trie.search)
    # プレフィックス検索の実行時間測定インスタンス作成
    pr = MeasureTime(trie.get_below_nodes)

    if x in words:

        # ノード番号取得
        node = es.exe_func(x)

        # 単語に紐づく属性情報取得
        syns = wordnet.synsets(x)
        print("\n")
        print('------ 検索結果 ------')
        print("result:", x)
        print("node_unmber:", node)
        print("definition_of_result:", syns[0].definition())
        print("Prediction candidate:")

        # プレフィックス検索
        for i in pr.exe_func([node]):
            try:
                print(i, words_dict[i])
            except:
                pass

        print('------ 実行時間 ------')
        print("完全一致検索:", es.exe_time, "sec")
        print("プレフィックス検索:", pr.exe_time, "sec")
        
        x = "This word is all nonsense."
        continue
    else:
        x = input("Input another words:")
