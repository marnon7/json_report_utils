import sys
import os
import json

# reload(sys)
# sys.setdefaultencoding('utf8')

USER_ID = 'userID'
SCORE = 'score'
 
def read_file(filename):
    by_field = {}  # field -> values -> count
    error_lines = []
    lines_cnt = 0   # lines counter
    result_lines = []
    with open(filename, 'r') as f:
        # lines = f.readlines()         # zeyu: It will load all the lines into memory.
        for line in f:                  # zeyu: It is recommended to use "for line in f" so that only one row of data is loaded at a time.
            # line = line.replace('\\', '')
            lines_cnt += 1
            only_score = {}
            try:
                data = json.loads(line)
            except:
                error_lines.append(line.strip())
                continue

            if isinstance(data, dict) and USER_ID in data and SCORE in data: 
                only_score.setdefault(USER_ID,data[USER_ID])
                only_score.setdefault(SCORE,data[SCORE])
                result_lines.append(json.dumps(only_score))
            else:
                error_lines.append(line.strip())
    return result_lines, error_lines, lines_cnt

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ('USAGE: {0} [input json file]'.format(sys.argv[0]))
        sys.exit(0)

    inputfile = sys.argv[1] 
    if not os.path.isfile(inputfile):
       print ('Not valid file or file doesn\'t exist')
       sys.exit(0)
    
    (result_lines, error_lines, lines_cnt) = read_file(inputfile)    

    with open('{}_onlyscore'.format(inputfile), 'w', encoding='utf-8') as fout:
        fout.write('\n'.join(result_lines))
        print ('\n total {} lines, valid lines: {}'.format(lines_cnt, len(result_lines)))
    if error_lines:
        with open('{}_errorlines'.format(inputfile), 'w', encoding='utf-8') as fout:
            fout.write('\n'.join(error_lines))
            print ('\n got {} error lines. output file name:[{}_errorlines]'.format(len(error_lines),inputfile))
