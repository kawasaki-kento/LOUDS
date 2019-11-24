# LOUDS
PythonとLOUDSによるTRIE木の実装

# requirements
nltk==3.4

# プログラム
 - trie.py：TRIE木
 - constructor.py：ビット配列
 - words.py：辞書データの作成・読み込み
 - measure.py：メモリと検索時間の測定
 - search_word.py：単語検索
 - test.py：検索時間の測定

# 実行手順

### 辞書データ用のディレクトリ作成
~~~
mkdir data
cd data
mkdir orign
mkdir test
~~~

### 辞書データ作成
~~~
from words import CreateWords
CreateWords("./data/origin/wordnet_words.csv")
~~~

### テストデータ作成
~~~
python words.py 辞書データPATH サンプル数1,サンプル数2,サンプル数3,…
~~~

### 単語検索
~~~
python search_word.py 辞書データPATH
~~~

### 速度計測
~~~
python test.py 辞書データPATH テストデータPATH テスト回数
~~~