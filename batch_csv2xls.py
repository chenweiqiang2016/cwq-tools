import os
from csv2xls import convert

subStrs = ['.csv']

def main():
    for file in find_files('./datas'):
        convert(file)

def find_files(path='.'):
    result = []
    fileList = os.listdir(path)
    print fileList
    for filename in fileList:
        flag = True
        for subStr in subStrs:
            if subStr not in filename:
                flag = False
        if flag:
            result.append(os.path.join(path, filename))
    return result
                

if __name__ == '__main__':
    main()