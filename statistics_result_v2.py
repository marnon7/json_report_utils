#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth:myoungs  2018-08-28
#
import sys
import os
import time
import json
import pandas as pd

reload(sys)
sys.setdefaultencoding('utf-8')
#
# ## Instructions
# > file: statistics_result.py
# > author: [zeyu.yang@datavisor.com](mailto:zeyu.yang@datavisor.com)
# > date: 2018/08/28
#
# #### Setting up the environment
# Execute the following command to setup your pandas environment
# ```
# pip install numpy==1.14.5
# pip install pandas
# ```
#
# #### Extract files and merge
#
# Execute the following command in the folder that needs to be processed.
# You can use the `cd` command to enter the folder or *Drag and drop* the folder to the terminal
#
# 1. Extract all `.gz` files in the current folder, including those in subfolders
# ```
# find ./ -type f -name "*.gz" |xargs gzip -d
# ```
#
# 2. Generate a file list and check if the file list is correct
# ```
# find ./ -type f -name "part-*" > file_list
# less file_list
# ```
#
# 3. Merge all files to `result_xxxx.json`. You can change it to any file name you want.
# ```
# find ./ -type f -name "part-*" -exec cat {} \;>result_xxxx.json
# ```
#
# #### Execution script
# ```
# python statistics_result.py 'you file'
# ```

# ######## ######## ######## ######## ######## ######## ######## ######## #
# You can edit the vars here

# 用于排重的主键
uid_key = "userID"
# 用于筛选字段的键值
score_key = "score"
# 目标分数最大值
score_max = 1.0
# 目标分数最低值
score_min = 0.9
# 输出文件名
output_file = "result_180801_180827"
# 输出目录
output_path = os.getcwd()

# ######## ######## ######## ######## ######## ######## ######## ######## #

if len(sys.argv) != 2:
    print 'USAGE: {0} [input json file]'.format(sys.argv[0])
    sys.exit(0)

json_file = sys.argv[1]
if not os.path.isfile(json_file):
    print 'Not valid file or file doesn\'t exist'
    sys.exit(0)

start_time = time.time()

# 读入数据
result = []

with open(json_file, 'rb') as inputFile:
    counter = 0
    #  测试read_json
    for rawline in inputFile:
        line = json.loads(rawline.rstrip(), strict=False)
        result.append(line)
        if counter % 10000 == 0:
            print "lines counter: " + str(counter)
        counter += 1

print ("\033[1;33mLoad data used: {0:0.2f}s \033[0m".format((time.time() - start_time)))

df_result = pd.DataFrame(result)

filter_result = df_result[(df_result[score_key] >= score_min) & (df_result[score_key] <= score_max)].copy()    # 筛选条件
print ("\033[1;32m{0} rows the value of '{1}' between {2} and {3} \033[0m"
       .format(filter_result[uid_key].count(), score_key, score_min, score_max))

# drop duplicates
df_result.drop_duplicates(uid_key, keep="first", inplace=True)
filter_result.drop_duplicates(uid_key, keep="first", inplace=True)

print ("\033[1;32m{0} rows with no duplicate `{1}`\033[0m"
       .format( df_result[uid_key].count(), uid_key))

print ("\033[1;32m{0} rows the value of '{1}' between {2} and {3} with no duplicate '{4}'\033[0m"
       .format(filter_result[uid_key].count(), score_key, score_min, score_max, uid_key))

print "Start writing data..."
df_result.to_csv(os.path.join(output_path, (output_file + ".csv")), index=False, encoding='utf_8_sig')
df_result.to_json(os.path.join(output_path, (output_file + ".json")))

filter_result.to_csv(os.path.join(output_path, (output_file + "_selected.csv")), index=False, encoding='utf_8_sig')
filter_result.to_json(os.path.join(output_path, (output_file + "_selected.json")))
print "Successfully written data"

print ("\033[1;33mTime used：{0:0.2f}s \033[0m".format((time.time() - start_time)))