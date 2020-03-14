# -*- coding: utf-8 -*-
import time

DAYSET = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]       # 平年的每月的天数

# 得到某月的天数
def daysOFmon(year, mon):
    # 如果是2月，且为闰年
    if (mon == 2) and ((year%4 == 0 and year%100 != 0) or (year%400 == 0)):
        days = 29
    else:
        days = DAYSET[mon-1]
    return days

# 得到当年的总天数
def daysOFyear(year):
    if (year%4 == 0 and year%100 != 0) or (year%400 == 0):
        return 366
    return 365


# 通过输入今年第几天,获取当前月份
def getMon(year, days):
    mon = 1
    while mon <= 12:
        tmp = days - daysOFmon(year, mon)
        if tmp <= 0:
            break
        
        days = tmp
        mon += 1
        
    return mon, days

# 得到year-month-day格式
# 输入距离今天的天数，如days=1，即今天，days=2,是昨天

def getDate(dayDist):
    TODAY = time.localtime()
    year = TODAY[0]
    month = TODAY[1]
    day = TODAY[2]
    
    # 首先计算今年过去几天 月=i+1
    curSum = 0
    for i in range(month-1):
        curSum += daysOFmon(year, i+1)
    # 如果dayDist的天数大于今年的数量，则为上年或上上。。年的天数
    curSum += day
    
    #print('今年过去了:', curSum)
    if dayDist <= curSum:
        #print('还在今年')
        days = curSum - dayDist+1
        #print('今年的第', days)
        mon,days = getMon(year, days)
    else:
        #print('其他年份')
        days = dayDist - curSum
        year -= 1
        while year >= 0:
            if days > daysOFyear(year):
                days = days - daysOFyear(year)
                year -= 1
            else:
                break
        days = daysOFyear(year) - days + 1
        mon, days = getMon(year, days)
        
    date = '%d-%02d-%02d'%(year, mon, days)
    print(date)
    return date

# 得到一个时间格式，用于到GUI展示，即获取监控的时间
# days为监控的天数
# 内容为: 今天的时间: (搜素的时间范围)
# 格式：year/month/day h:m:s:(month/day - month/day)
def getTimeType(days):
    TODAY = time.localtime()
    year = TODAY[0]
    month = TODAY[1]
    today = TODAY[2]
    hour = TODAY[3]
    mins = TODAY[4]
    sec = TODAY[5]
    
    todayType = "%d/%02d/%02d %02d:%02d:%02d"%(year, month, today, hour, mins, sec)
    
    toType = "%02d/%02d"%(month, today)
    
    if days > today:
        month -= 1
        day = daysOFmon(year, month) - (days - today-1)
    else:
        day = today - days + 1
    
    fromType = "%02d/%02d"%(month, day)
    
    ans = todayType + ": (" + fromType + "-" + toType + ") "
    
    return ans

if __name__ == '__main__':
    for i in range(1000):
        print(getDate(i))
