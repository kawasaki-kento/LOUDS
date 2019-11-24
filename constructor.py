class Node(object):

    def __init__(self, value):
        self.value = value # 親ノードの要素
        self.children = [] # 子ノードの要素
        self.visited = False

    def __str__(self):
        return str(self.value)

    def add_child(self, child):
        self.children.append(child)

class ArrayConstructor(object):

    def __init__(self):
        self.tree = Node('_')  # ルートノード

    def add(self, word):
        # 単語を追加
        self.build(self.tree, word)

    def build(self, node, word, depth=0):
        # 木を作成
        # 入力文字列のすべての要素をチェックしたなら処理を抜ける
        if(depth == len(word)):
            return

        for child in node.children:

            # すでに同じ要素（文字）のノードがあれば、再帰呼び出しする
            # 再帰呼び出しが実行された場合は、このレイヤーでノードの作成は行わない
            # 必ず次のレイヤー（再帰呼び出し先）以降でノードの作成が行われる
            if(child.value == word[depth]):
                self.build(child, word, depth+1)
                return

        # ノードの作成を行う
        child = Node(word[depth])
        node.add_child(child)
        self.build(child, word, depth+1)

        return

    def show(self):
        self.show_(self.tree)

    def show_(self, node, depth=0):
        print("{}{}".format('  '*depth, node))
        for child in node.children:
            self.show_(child, depth+1)

    def dump(self):
        # trie木をbit配列にdumpする
        from collections import deque

        bit_array = [1, 0]  # [1, 0] はルートノードを表す
        labels = ['_']

        # 幅優先探索でdumpする
        queue = deque()
        queue.append(self.tree)

        while(len(queue) != 0):
            node = queue.popleft()
            labels.append(node.value)

            bit_array += [1] * len(node.children) + [0]

            for child in node.children:
                child.visited = True
                queue.append(child)
        
        return bit_array, labels
