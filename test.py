from trie import Trie
from measure import MeasureTime, MeasureMemory
from words import Words
from nltk.corpus import wordnet
import numpy as np
import random
import time
import sys



# 元辞書読み込み
o = Words(sys.argv[1]) # ./data/origin/wordnet_words.csv 元データ
words_dict = o.words_dict
words = o.words

# テストデータ読み込み
t = Words(sys.argv[2]) # ./data/test/wordnet_words_****.csv テストデータ
test_dict = t.words_dict

# テスト回数
trial = int(sys.argv[3])
# 分割ユニットサイズ
unit_scale = 8

# ランダムサンプリング サンプルサイズ（検索単語数）

f = open("./results/result_of_"+sys.argv[2].split('/')[3].split('.')[0]+".txt", 'w')

print("=========================== 使用データ ===========================", file=f)
print("PATH：",sys.argv[2], file=f)
print("サンプルサイズ：", len(test_dict), file=f)
print("テスト回数：",trial, file=f)

# Trie木作成
print("=========================== 使用メモリ ===========================", file=f)
trie = Trie(words, unit_scale)

m = MeasureMemory()
# bit配列のメモリ使用量、ラベル配列のメモリ使用量
print("bit_array:", m.convert_bytes(m.compute_object_size(trie.bit_array)), "labels:", m.convert_bytes(m.compute_object_size(trie.labels)), file=f)

# selectの使用メモリ
print("select:", m.convert_bytes(m.compute_object_size(trie.zero_pos)), file=f)

# rankの使用メモリ
print("rank:", m.convert_bytes(m.compute_object_size(trie.split_list)), file=f)


# 実行時間計測
print("============================ 実行時間 ============================", file=f)
exact_search = []
prefix_search = []




for j in range(trial):
    
    # word検索の実行時間測定インスタンス作成
    es = MeasureTime(trie.search)
    # prefix検索の実行時間測定インスタンス作成
    pr = MeasureTime(trie.get_below_nodes)
    
    c = 0
    pr_c = 0
    
    # 検索を実行
    for answer, query in test_dict.items():
        # 単語検索
        node = es.exe_func(query)
        if node == answer:
            c+=1

        # プレフィックス検索
        pr_c+=len(pr.exe_func([node]))


    print("--",  j+1, "回目", file=f)
    print(" ・完全一致検索:", " time:"+str(round(es.exe_time, 4))+"秒", " 検索件数："+"{:,d}".format(c)+"件", file=f)
    print(" ・プレフィックス検索:", " time:"+str(round(pr.exe_time, 4))+"秒", " prefix件数："+"{:,d}".format(pr_c)+"件", file=f)
    exact_search.append(es.exe_time)
    prefix_search.append(pr.exe_time)
    
print("============================ 平均実行時間 ============================", file=f)
print("完全一致検索：", str(round(np.mean(exact_search), 4))+"秒", file=f)
print("プレフィックス検索：", str(round(np.mean(prefix_search), 4))+"秒", file=f)
print("プレフィックス検索（１件当たり）：", str(np.mean(prefix_search)/pr_c)+"秒", file=f)

f.close()

print("Test is done.")