# coding=utf-8
import unittest
import numpy as np
from util.reservoir_sample import ReservoirSample


# # auth: zeyu.yang@datavisor.com 2019-10-25

class MyTestCase(unittest.TestCase):
    # test ReservoirSample
    def test_rs(self):
        times = 0
        sum = 0
        result_set = {}
        # target test times
        target_times = 50000
        # data size
        test_set_size = 100
        # sampling ratio
        sample_ratio = 0.02

        while times < target_times:
            rs = ReservoirSample(sample_ratio * test_set_size)
            i = 0
            while i < test_set_size:
                i += 1
                rs.feed("obj-{}".format(i))
            result = rs.get_sample()
            sumbytime = 0
            for obj in result:
                # sumbytime += obj
                if obj not in result_set:
                    result_set[obj] = 1
                else:
                    result_set[obj] += 1

            # print sumbytime
            #     sum += sumbytime
            times += 1
        # avg_100 = sum /target_times

        result_arr = []
        # print avg_100
        for key in result_set:
            result_arr.append(result_set[key])
            print ("{}:{}".format(key, result_set[key]))
            # print ("{key}:{value}".format(key,value))
        arr_mean = np.mean(result_arr)
        arr_var = np.var(result_arr)
        arr_std = np.std(result_arr, ddof=1)
        arr_float = arr_std/arr_mean*100

        print ("平均值为：%f" % arr_mean)
        print ("方差为：%f" % arr_var)
        print ("标准差为:%f" % arr_std)
        print ('浮动率:%f' % arr_float)
        self.assertEqual(arr_mean, target_times * sample_ratio)


if __name__ == '__main__':
    unittest.main()
