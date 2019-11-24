import time
import math
import sys
from itertools import chain
from collections import deque
import numpy as np
import array

# 時間計測
class MeasureTime:
    def __init__(self, func):
        self.exe_time = 0
        self.func = func
        
    # funcの処理時間を計測
    def exe_func(self, *args,**kargs):
        start = time.time()
        result = self.func(*args,**kargs)
        diff_time = time.time() - start
        self.exe_time += diff_time
        
        return result

# オブジェクトの使用メモリ計測
class MeasureMemory:
    def compute_object_size(self, o, handlers={}):
        dict_handler = lambda d: chain.from_iterable(d.items())
        all_handlers = {tuple: iter,
                        list: iter,
                        deque: iter,
                        dict: dict_handler,
                        set: iter,
                        frozenset: iter,
                        np.ndarray: iter,
                        array.array: iter
                    }
        
        all_handlers.update(handlers)
        # 参照済みオブジェクトのidを格納
        seen = set()                      
        default_size = sys.getsizeof(0)

        def sizeof(o):
            # 既に参照したオブジェクトは確認しない
            if id(o) in seen:       
                return 0
            seen.add(id(o))
            s = sys.getsizeof(o, default_size)

            for typ, handler in all_handlers.items():
                if isinstance(o, typ):

                    # listならばイテレーターにして、再帰的にsizeof関数に適用する
                    # 参照先のオブジェクトのメモリ使用量も含む
                    s += sum(map(sizeof, handler(o)))
                    break
            return s

        return sizeof(o)

    # 数値を小数点第1位で四捨五入して文字列に変換する
    def round_bytes(self, size):
        return str(round(size, 1))

    # ファイルサイズ（Bytes）をKBytes, MBytes, GBytes, TBytes表記の文字列に変換する
    def convert_bytes(self, bytesize):
        if bytesize < 1024:
            return str(bytesize) + ' B'
        elif bytesize < 1024 ** 2:
            return self.round_bytes(bytesize / 1024.0) + ' KB'
        elif bytesize < 1024 ** 3:
            return self.round_bytes(bytesize / (1024.0 ** 2)) + ' MB'
        elif bytesize < 1024 ** 4:
            return self.round_bytes(bytesize / (1024.0 ** 3)) + ' GB'
        elif bytesize < 1024 ** 5:
            return self.round_bytes(bytesize / (1024.0 ** 4)) + ' TB'
        else:
            return str(bytesize) + ' Bytes'