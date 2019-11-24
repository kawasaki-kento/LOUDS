from constructor import ArrayConstructor
from measure import MeasureMemory
import re
import array

class Trie(object):
    def __init__(self, words, unit_scale=8):
        bit_array, labels = self.create_tree(words)

        self.rank1 = self.get_rank(1)

        self.unit_scale = unit_scale
        self.split_list = BitVector(bit_array, self.unit_scale).split_array()

        self.zero_pos = [0]
        c = 1
        for i, v in enumerate(bit_array):
            if v == 0:
                self.zero_pos.append(i)
                c+=1

        self.zero_pos = array.array('I', self.zero_pos)

        self.bit_array = array.array('B',bit_array)
        self.labels = array.array('u',labels)        

    # Trie木作成
    def create_tree(self, words):
        words = [word.lower() for word in words]
        words.sort()
        constructor = ArrayConstructor()
        for word in words:
            constructor.add(word)
        bit_array, labels = constructor.dump()
        
        return bit_array, labels


    def rank(self, position, target_bit):
        n = 0
        for bit in self.bit_array[:position+1]:
            if(bit == target_bit):
                n += 1
        return n

    def select0(self, n):
        return self.zero_pos[n]


    def sub_rank1(self, position):
        unit_num = int(position / self.unit_scale)
        n = self.split_list[unit_num-1]
        n+=sum(self.bit_array[unit_num * self.unit_scale : position+1])
        
        return n

    def get_rank(self, target_bit):
        return lambda position: self.rank(position, target_bit)
        
    # ノード探索
    def trace_children(self, current_node, character, cnt):
        # ビット列の先頭から見て、n 個目の 0 ビットの次の位置
        index = self.select0(current_node) + 1

        while(self.bit_array[index] == 1):
            # ビット列の先頭から位置 k までに、1 のビットがいくつあるかを返す
            if cnt == 0:
                node = self.rank1(index)
            else:
                node = self.sub_rank1(index)

            if(self.labels[node] == character):
                cnt=1
                return node, cnt
            
            index += 1
        return None, cnt

    # 単語検索
    def search(self, query):
        query = query.lower()
        cnt = 0
        node = 1
        for c in query:
            node, cnt = self.trace_children(node, c, cnt)
            if(node is None):
                return None
        return node

    # 子ノードのindexを取得
    def get_children(self, parent_node_seq):
        return [i for j in parent_node_seq for i in range(self.select0(int(j)), self.select0(int(j+1)))[1:]]


    # 検索ノード以下のwordをすべて取得する
    def get_below_nodes(self, node_list):
        below_nodes = []
        below_nodes.extend(node_list)
        cnt = 0
        
        # 子ノードが存在する限り実行
        while self.get_children(node_list) != []:
            tmp_list = [self.sub_rank1(i) for i in self.get_children(node_list)]
            below_nodes.extend(tmp_list)
            node_list = tmp_list
            cnt+=1

        return below_nodes
           

# rank
class BitVector:
    
    def __init__(self, bit_array, unit_scale):
        self.bit_array = bit_array
        self.splited_array = None
        self.n = 0
        self.split_list = []
        self.unit_scale = unit_scale
        self.split_size = int(len(self.bit_array) / self.unit_scale)
        
    def rank(self, position, target_bit):
        n = 0
        for bit in self.splited_array[:position+1]:
            if(bit == target_bit):
                n += 1
        return n

    def get_rank(self, target_bit):
        return lambda position: self.rank(position, target_bit)
        
    def split_array(self):

        for i in range(self.split_size):
            
            if i == self.split_size-1:
                self.splited_array = self.bit_array[i*self.unit_scale:]
                rank1 = self.get_rank(1)
            else:
                self.splited_array = self.bit_array[i*self.unit_scale:(i+1)*self.unit_scale]
                rank1 = self.get_rank(1)

            self.n+=rank1(len(self.splited_array))
            self.split_list.append(self.n)

            self.split_list = array.array('I', self.split_list)

        return self.split_list