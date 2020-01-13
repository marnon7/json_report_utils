# json_report_utils
# 常用的json报告处理脚本合集

把常用的小工具集成到一个git仓库方便维护和更新,没有特殊说明脚本均适用于 `python 3` 并且在 `OS X` 下编写并且测试通过。

### 按照分数统计结果

file: statistics_result.py  
author: [zeyu.yang@datavisor.com](mailto:zeyu.yang@datavisor.com)  
date: 2018/08/28

### Instructions
#### Setting up the environment
Execute the following command to setup your pandas environment
```
pip install numpy==1.14.5
pip install pandas
```

#### Extract files and merge

Execute the following command in the folder that needs to be processed.
You can use the `cd` command to enter the folder or *Drag and drop* the folder to the terminal

1. Extract all `.gz` files in the current folder, including those in subfolders
```
find ./ -type f -name "*.gz" |xargs gzip -d
```

2. Generate a file list and check if the file list is correct
```
find ./ -type f -name "part-*" > file_list
less file_list
```

3. Merge all files to `result_xxxx.json`. You can change it to any file name you want.
```
find ./ -type f -name "part-*" -exec cat {} \;>result_xxxx.json
```

#### Execution script
```
python statistics_result.py 'you file'
```

### 提取结果报告中的分数

file: getscore.py  
author: [zeyu.yang@datavisor.com](mailto:zeyu.yang@datavisor.com)  
date: 2020/01/06

用来提取检测结果中的uid和分数。输出文件名+ `_onlyscore` 若存在错误行和其他问题将会生成后缀名为`_errolines`的文件。
