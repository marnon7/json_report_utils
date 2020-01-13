#!/usr/bin/python
# -*- coding:utf-8 -*-
# auth: zeyu.yang@datavisor.com 2019-07-04

import sys
import os
import json
from util.reservoir_sample import ReservoirSample

reload(sys)
sys.setdefaultencoding('utf8')

################################
RESULT_USER_ID = "userID"
RESULT_CAMPAIGN_NAME = "campaignName"
RESULT_SCORE = "score"
RESULT_REASON = "reason"

REASON_TEMPLATE_1 = "The user is strongly correlated with "
REASON_TEMPLATE_2 = " other fraudulent users. Their top correlated features and the percentages of the users sharing the same features are as follows: "

MODE_SIMPLE = '1'
MODE_STRATIFIED = '2'
MODE_SYSTEMATIC = '3'
MODE_CLUSTER = '4'
################################
# if a field's top value covers over SKEWED_THRESH of the data, then the field is considered skewed
SKEWED_THRESH = 0.25
# top N values will get printed out for each field
TOP_VALUE_N = 30

null_field_cnt = {'uid': 0, 'campaign': 0, 'score': 0, 'reason': 0}  # counter of null lines

'''
Prints out the top TOP_VALUE_N values for each field
'''


def print_fields():
    outputtext = []
    outputtext.append('Distribution of the top values in each field:\n')
    for k in sorted(by_field):
        outputtext.append('"{0}" has {1} unique values'.format(k, len(by_field[k])))
        i = 0
        for v in sorted(by_field[k], key=by_field[k].get, reverse=True):
            # ignore null values
            if v is None:
                continue

            if type(v) == int or type(v) == float or type(v) == bool or v is None:
                outputtext.append(
                    '\t{0}\t{1}\t{2}'.format(v, by_field[k][v], float(by_field[k][v]) / sum(by_field[k].values())))
            else:
                outputtext.append('\t%s\t%d\t%f' % (
                    v.encode('utf-8'), by_field[k][v], float(by_field[k][v]) / sum(by_field[k].values())))

            if i >= TOP_VALUE_N - 1:
                break
            i += 1
        outputtext.append('\n')
    return outputtext


def get_tier_byscore(f_str, n):
    f_str = str(f_str)
    a, b, c = f_str.partition('.')
    c = (c + "0" * n)[:n]
    min_str = ".".join([a, c])

    dis = 1
    i = 0
    while i < n:
        dis = dis / 10.0
        i += 1
    f_str = str(float(f_str) + dis)
    a, b, c = f_str.partition('.')
    c = (c + "0" * n)[:n]

    max_str = ".".join([a, c])

    # return ".".join([a, c])
    return ("[" + min_str + "," + max_str + ")")


# not good abandon
class dv_result:
    resCount = 0
    error_lines = []
    null_field_cnt = {'uid': 0, 'campaign': 0, 'score': 0, 'reason': 0}  # counter of null lines

    def __init__(self, line):
        try:
            data = json.loads(line)
        except:
            self.error_lines.append(data)
        else:
            if data.has_key(RESULT_USER_ID):
                self.uid = data.get(RESULT_USER_ID)
                if not self.uid:
                    self.null_field_cnt['uid'] += 1
            if data.has_key(RESULT_CAMPAIGN_NAME):
                campaign_name_str = data.get(RESULT_CAMPAIGN_NAME)
                if not campaign_name_str:
                    self.null_field_cnt['campaign'] += 1

            if data.has_key(RESULT_REASON):
                self.reason = data.get(RESULT_REASON)
                if not self.reason:
                    null_field_cnt['reason'] += 1
                else:
                    simple_reason = self.reason.strip(REASON_TEMPLATE_1).split(REASON_TEMPLATE_2)
                    group_size = simple_reason[0]
                    self.simple_reason = group_size + " " + simple_reason[len(simple_reason) - 1]
                    data[RESULT_REASON] = simple_reason

            if data.has_key(RESULT_SCORE):
                self.score = data.get(RESULT_SCORE)
                if not self.score:
                    null_field_cnt['score'] += 1

        dv_result.resCount += 1

    def displayCount(self):
        print "Total lines %d" % dv_result.resCount

    def displayResult(self):
        print "some thing"




def read_file():
    i = 0

    with open(inputfile, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
            except:
                # print "Erro->"+data
                error_lines.append(data)
            else:
                if data.has_key(RESULT_USER_ID):
                    uid = data.get(RESULT_USER_ID)
                    if not uid:
                        null_field_cnt['uid'] += 1
                if data.has_key(RESULT_CAMPAIGN_NAME):
                    campaign_name_str = data.get(RESULT_CAMPAIGN_NAME)
                    if not campaign_name_str:
                        null_field_cnt['campaign'] += 1

                if data.has_key(RESULT_REASON):
                    reason = data.get(RESULT_REASON)
                    if not reason:
                        null_field_cnt['reason'] += 1
                    else:
                        simple_reason = reason.strip(REASON_TEMPLATE_1).split(REASON_TEMPLATE_2)
                        group_size = simple_reason[0]
                        simple_reason = group_size + " " + simple_reason[len(simple_reason) - 1]
                        data[RESULT_REASON] = simple_reason

                if data.has_key(RESULT_SCORE):
                    score = data.get(RESULT_SCORE)
                    if not score:
                        null_field_cnt['score'] += 1
                    elif data.has_key('user_sex'):
                        sex = data.get('user_sex')
                        sex_value = str('user_sex_' + sex)

                        if sex_value not in by_field:
                            by_field[sex_value] = {}
                        tier_byscore = get_tier_byscore(score, 1)
                        if tier_byscore not in by_field[sex_value]:
                            by_field[sex_value][tier_byscore] = 0
                        by_field[sex_value][tier_byscore] += 1

                        if float(score) >= 0.9 and sex == '0':
                            high_score_sex_0.append(json.dumps(data))

                for k in data:
                    if k not in by_field:
                        by_field[k] = {}

                    value = data[k]
                    if value not in by_field[k]:
                        by_field[k][value] = 0
                    by_field[k][value] += 1

                all_lines.append(json.dumps(data))
                simple_samples.feed(line)
                i += 1
            # print(i)
    return i  # return the count of all lines


def menu():
    print ("1. Simple Sampling;")
    print ("2. Stratified Random Sampling;")
    print ("3. Systematic Sampling;")
    print ("4. Cluster Sampling;")
    item = raw_input("Enter:")
    return item

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'USAGE: {0} [input json file]'.format(sys.argv[0])
        sys.exit(0)

    inputfile = sys.argv[1]
    if not os.path.isfile(inputfile):
        print 'Not valid file or file doesn\'t exist'
        sys.exit(0)

    outputtext = []
    error_lines = []
    all_lines = []
    high_score_sex_0 = []

    by_field = {}  # field -> values -> count

    mode = menu()
    if mode == MODE_SIMPLE:
        sample_size = int(raw_input('Enter the sample size ：'))
        simple_samples = ReservoirSample(sample_size)
        unique_id_cnt = read_file()  # Simple Sampling needs run after read_file
        simple_samples.white_to_file("simple_sample_result.json")

    elif mode == MODE_STRATIFIED:
        print "MODE_STRATIFIED"
        sys.exit(0)

    elif mode == MODE_STRATIFIED:
        print "MODE_STRATIFIED"
        sys.exit(0)
    else:
        sys.exit(0)




    outputtext_all_fields = print_fields()
    outputtext.append('\n')
    outputtext.extend(outputtext_all_fields)
    # print ("all_lines cnt %d" %all_lines.count())
    print("\terror lines->")
    print(error_lines)

    for key, value in null_field_cnt.iteritems():
        print ("\tempty %s:\t%d" % (key, value))

    try:
        mfout = open('result_simple_result.txt', 'w')
        mfout.write('\n'.join(all_lines))
        mfout.close()

        mfout = open('result_high_score_sex_0.txt', 'w')
        mfout.write('\n'.join(high_score_sex_0))
        mfout.close()

        mfout = open('check_output.txt', 'w')
        mfout.write('\n'.join(outputtext))
        mfout.close()
    except:
        print ("write to files fail")
    else:
        print ("write to files success")
print ("end")
