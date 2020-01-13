#!/usr/bin/python
# -*- coding:utf-8 -*-
# # auth: zeyu.yang@datavisor.com 2019-07-04
import random


class ReservoirSample(object):

    def __init__(self, size=0):
        self.size = size
        self._size = self.size
        self._counter = 0
        self._sample = []

    def feed(self, item):
        if self._size == 0:
            return -1

        self._counter += 1
        # 第i个元素（i <= k），直接进入池中
        if len(self._sample) < self._size:
            self._sample.append(item)

        # 第i个元素（i > k），以k / i的概率进入池中
        rand_int = random.randint(1, self._counter)
        if rand_int <= self._size:
            self._sample[rand_int - 1] = item
        return self._counter

    def get_sample(self):
        return self._sample

    def set_size(self, size):
        self._size = size
        return size

    def white_to_file(self, filename="sample_file"):
        try:
            fout = open(filename, 'w')
            fout.write("".join(self._sample))
            fout.close()
        except:
            print ("Erro: write to sample")
