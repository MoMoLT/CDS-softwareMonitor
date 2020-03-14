# -*- coding: utf-8 -*-
import csv

# 将数据保存到csv文件中
def saveAppToCsv(filePath, appSet,encode='utf-8-sig'):
    header = ['Apple ID', 'APP', '发行商', '类型', '发行时间', '下架时间', '价格', '描述链接']
    '''
    try:
        with open(filePath, 'w', newline='',encoding=encode) as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for app in appSet:
                writer.writerow([app['ID'], app['App'], app['发行商'], app['类别'], app['发布时间'], app['下架时间'], app['价格'], app['链接']])
            return True
    except:
        return False
    '''
    with open(filePath, 'w', newline='',encoding=encode) as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for app in appSet:
            writer.writerow([app['ID'], app['APP'], app['发行商'], app['类别'], app['发布时间'], app['下架时间'], app['价格'], app['链接']])
        return True
    return False
def saveListToTxt(filePath, dataSet):
    '''
        将列表数据保存到txt文件中
        参数：生成器，文件路径
    '''
    try:
        with open(filePath, 'w') as f:
            for line in dataSet:
                f.write(line+'\n')
            return True
    except:
        return False
    
def saveHostAndPass(filePath):
    '''
    '''
    pass

def getTxt(filePath):
    '''
        将txt文件中的数据提取
        参数：文件路径
        返回值：生成器？[列表？]
    '''
    with open(filePath, 'r') as f:
        dataSet = f.readlines()
        for data in dataSet:
            yield data.strip()
        #for i in range(len(dataSet)):
        #    dataSet[i] = dataSet[i].strip()
        #return dataSet
if __name__ == '__main__':
    #saveAppToCsv('test.csv',, [])
    #print(getTxt('test.txt'))
    getTxt('test.txt')
    
