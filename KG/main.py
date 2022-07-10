# coding:utf-8
# 目标检测主要业务逻辑
import os
import random
import sqlite3
import math
from decimal import Decimal
import json
import re
import folium
import requests
import math
import pandas as pd
import numpy as np
from folium.plugins import HeatMap

requests.packages.urllib3.disable_warnings()


# 点坐标
class Point:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def toString(self):
        return '('+'经度：'+str(self.x)+',纬度：'+str(self.y)+')'
# 线上的点的坐标


class Line:
    def __init__(self, id, x, y, z) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.z = z

    def showLine(self):
        print(self.id, ',', self.x, ',', self.y, ',', self.z)


# 找矩形凸壳（一个矩形将所有点都框住）
def getRectangleTuKe(pointList):

    xMin = float(pointList[0].x)
    xMax = float(pointList[0].x)
    yMin = float(pointList[0].y)
    yMax = float(pointList[0].y)

    for point in pointList:
        xMin = min(xMin, float(point.x))
        xMax = max(xMax, float(point.x))
        yMin = min(yMin, float(point.y))
        yMax = max(yMax, float(point.y))

    return [xMin, xMax, yMin, yMax]


# 点的矩形凸包 构造矩形凸包，划分网格
# xmin-最小x坐标值 xmax-最大x坐标值 ymin-最小y坐标值 ymax-最大y坐标值
# unitLen 单元正方形网格的边长
# maskLen 掩膜的边长
# xUnitSize x轴网格个数 yUnitSize y轴网格个数
# unitGirls 划分后的二维网格数组， unitGirl[i][j]={i,j网格对应的道路坐标索引（即道路条数）} 通过统计单元网格中道路id的个数来统计道路条数
# unitGirlsIsFuPo 二维网格中是否含有湖泊的标记数组
# maskGirls 掩膜的二维数组 maskGirls[j][i]=[{合并其中单元网格后的道路set}，该掩膜中维护的最低高程值，该掩膜中维护的最高高程值，是否包含湖泊的字段]
class Box:
    def __init__(self, pointList, maskLen) -> None:
        self.xMin, self.xMax, self.yMin, self.yMax = getRectangleTuKe(pointList)
        self.unitLen = 100.
        self.maskLen = 500.
        self.xUnitSize = math.ceil((self.xMax - self.xMin) / self.unitLen) + 5
        self.yUnitSize = math.ceil((self.yMax - self.yMin) / self.unitLen) + 5
        self.unitGirls = [[set() for i in range(self.xUnitSize)] for j in range(self.yUnitSize)]    # set自动去重
        self.unitGirlsFuPo = [[0 for i in range(self.xUnitSize + 100)] for j in range(self.yUnitSize + 100)]
        self.maskGirls = [[[set(), 50000.0, -20000.0, 0] for i in range(self.xUnitSize - (math.ceil(self.maskLen / self.unitLen)))] for j in range(self.yUnitSize- (math.ceil(self.maskLen / self.unitLen)))]
        
    # 初始化单位网格二维数组
    def initUnitGirls(self, LineList):
        for line in LineList:
            i = math.floor((line.x - self.xMin) / self.unitLen)
            j = math.floor((line.y - self.yMin) / self.unitLen)
            self.unitGirls[j][i].add(line.id)
 
    # 初始化掩膜的二维数组
    # #def initMaskGirls(self, pointWithZList, FuPoDict):
    def initMaskGirls(self, pointWithZList, pointMustInclude, pointNotInclude):
        for key in pointMustInclude.keys():
            # #for key in FuPoDict.keys():
            if len(pointMustInclude[key]) != 0:
                xMin, xMax, yMin, yMax = getRectangleTuKe(pointMustInclude[key])

                jMin = math.floor((xMin-self.xMin)/self.unitLen)
                iMin = math.floor((yMin-self.yMin)/self.unitLen)
                jMax = math.ceil((xMax-self.xMin)/self.unitLen)
                iMax = math.ceil((yMax-self.yMin)/self.unitLen)
                # (jMin," ",jMax," ",iMin," ",iMax)
                for j in range(jMin, jMax):
                    for i in range(iMin, iMax):
                        self.unitGirlsFuPo[j][i] = 1

        for key in pointNotInclude.keys():
            if len(pointNotInclude[key]) != 0:
                xTmpMin, xTmpMax, yTmpMin, yTmpMax = getRectangleTuKe(pointNotInclude[key])
                jTmpMin = math.floor((xTmpMin - self.xMin) / self.unitLen)
                iTmpMin = math.floor((yTmpMin - self.yMin) / self.unitLen)
                jTmpMax = math.ceil((xTmpMax - self.xMin) / self.unitLen)
                iTmpMax = math.ceil((yTmpMax - self.yMin) / self.unitLen)
                for j in range(jTmpMin, jTmpMax):
                    for i in range(iTmpMin, iTmpMax):
                        self.unitGirlsFuPo[j][i] = 0
        
        # print(self.unitGirlsFuPo)
        maskSize = math.floor(self.maskLen / self.unitLen)
        # 合并单元格中道路条数
        for i in range(self.xUnitSize - (math.ceil(self.maskLen / self.unitLen))):
            for j in range(self.yUnitSize - (math.ceil(self.maskLen / self.unitLen))):
                for i_increment in range(maskSize):
                    for j_increment in range(maskSize):
                        self.maskGirls[j][i][0] |= self.unitGirls[j+j_increment][i+i_increment]
                        self.maskGirls[j][i][3] = self.maskGirls[j][i][3] or self.unitGirlsFuPo[j+j_increment][i+i_increment]
                        # print("self.unitGirlsFuPo[j+j_increment][i+i_increment]=",self.unitGirlsFuPo[j+j_increment][i+i_increment])
        # 维护掩膜的高程值
        for p in pointWithZList:
            j = math.floor((p.x - self.xMin) / self.unitLen)
            i = math.floor((p.y - self.yMin) / self.unitLen)
            lenn = math.ceil(self.maskLen / self.unitLen)
            for a in range(lenn):
                for b in range(lenn):
                    if(j-a>0 and i-b>0 and j-a<len(self.maskGirls) and i-b<len(self.maskGirls)):
                        self.maskGirls[j-a][i-b][1] = min(self.maskGirls[j-a][i-b][1], p.z)
                        self.maskGirls[j-a][i-b][2] = max(self.maskGirls[j-a][i-b][2], p.z)

    # 得到符合要求的掩膜的左下和右上坐标
    # maxDensity：道路密度高的参数 minDensity：道路密度低的参数 hmin：最低高程值 hmax：最高高程值 isFuPo：是否是湖泊
    # maxDensityResult: 道路密度高的掩膜数组 剩下的以此类推
    def getZb(self, maxDensity, minDensity, h_min, h_max, isFuPo):
        maxDensityResult = []
        middleDensityResult = []
        minDensityResult = []
        for i in range(self.xUnitSize - (math.ceil(self.maskLen / self.unitLen))):
            for j in range(self.yUnitSize - (math.ceil(self.maskLen / self.unitLen))):
                workArray = []
                # if(self.maskGirls[j][i][1]<50000):
                #     print(self.maskGirls[j][i][1])
                
                if(self.maskGirls[j][i][1]>float(h_min) and self.maskGirls[j][i][2]<float(h_max) and self.maskGirls[j][i][1] < self.maskGirls[j][i][2]):
                    # print(self.maskGirls[j][i][1])
                    # print(self.maskGirls)
                    # print(self.unitGirlsFuPo)
                    if len(self.maskGirls[j][i][0]) > maxDensity:
                        # Decimal(i*self.unitLen+self.yMin+self.maskLen).quantize(Decimal('0.000'))
                        workArray.append(Point(Decimal(j*self.unitLen+self.xMin).quantize(Decimal('0.000')), Decimal(i*self.unitLen+self.yMin).quantize(Decimal('0.000')), 0).toString())
                        workArray.append(Point(Decimal(j*self.unitLen+self.xMin+self.maskLen).quantize(Decimal('0.000')), Decimal(i*self.unitLen+self.yMin+self.maskLen).quantize(Decimal('0.000')), 0).toString())
                        maxDensityResult.append(workArray)
                        maxDensityResult.append('<br>')
                    elif(len(self.maskGirls[j][i][0])<=maxDensity and len(self.maskGirls[j][i][0])>minDensity):
                        workArray.append(Point(Decimal(j*self.unitLen+self.xMin).quantize(Decimal('0.000')), Decimal(i*self.unitLen+self.yMin).quantize(Decimal('0.000')), 0).toString())
                        workArray.append(Point(Decimal(j*self.unitLen+self.xMin+self.maskLen).quantize(Decimal('0.000')), Decimal(i*self.unitLen+self.yMin+self.maskLen).quantize(Decimal('0.000')), 0).toString())
                        middleDensityResult.append(workArray)
                        middleDensityResult.append('<br>')
                    else:
                        workArray.append(Point(Decimal(j*self.unitLen+self.xMin).quantize(Decimal('0.000')), Decimal(i*self.unitLen+self.yMin).quantize(Decimal('0.000')), 0).toString())
                        workArray.append(Point(Decimal(j*self.unitLen+self.xMin+self.maskLen).quantize(Decimal('0.000')), Decimal(i*self.unitLen+self.yMin+self.maskLen).quantize(Decimal('0.000')), 0).toString())
                        minDensityResult.append(workArray)
                        minDensityResult.append('<br>')
        
        return [minDensityResult, middleDensityResult, maxDensityResult]

        
# 从数据库文件中读取点返回
def readPoint(dbName):
    # print("进入"+dbName)
    con = sqlite3.connect(dbName)  # 连接桥
    # print("Open database successfully")  # 打开成功
    cur = con.cursor()
    sql1 = 'SELECT * FROM DN05490062_DZB WHERE leibie="P"'
    cur.execute(sql1)
    pointList = []
    for line in cur.fetchall():
        if line != None:
            pointList.append(Point(float(line[2]), float(line[3]), float(line[4])))
    cur.close()
    con.commit()
    con.close()
    return pointList


# 从数据库中读取线返回
def readLine(dbName):
    # print("进入"+dbName)
    con = sqlite3.connect(dbName)  # 连接桥
    # print("Open database successfully")  # 打开成功
    cur = con.cursor()
    sql1 = 'SELECT * FROM DN05490062_DZB WHERE leibie="L"'
    cur.execute(sql1)
    LineList = []
    for line in cur.fetchall():
        if line != None:
            LineList.append(Line(line[5], float(line[6]), float(line[7]), line[8]))
    cur.close()
    con.commit()
    con.close()
    return LineList


# 从数据库中读取高程值信息的点返回
def readPointWithZ(dbName):
    # print("进入"+dbName)
    con = sqlite3.connect(dbName)  # 连接桥
    # print("Open database successfully")  # 打开成功
    cur = con.cursor()
    sql1 = "SELECT jzb.LAX as x,jzb.LAY as y,jsx.高程 as z FROM DN05490062_JZB jzb LEFT JOIN DN05490062_JSX jsx ON jzb.LNUM = jsx.要素编号 WHERE jzb.leibie = 'L' AND jsx.所属类别 = 'L' AND jsx.高程 is NOT '-32767.00'"
    cur.execute(sql1)
    pointList = []
    for line in cur.fetchall():
        if line != None:
            pointList.append(Point(float(line[0]), float(line[1]), float(line[2])))
    cur.close()
    con.commit()
    con.close()
    return pointList


#  读取湖泊
#  返回列表，0：代表字典{湖泊序号，[湖泊序号对应的点]} 1：[湖泊列表点]
def readFuPo(dbName):
    # print("进入"+dbName)
    con = sqlite3.connect(dbName)  # 连接桥
    # print("Open database successfully")  # 打开成功
    cur = con.cursor()
    sql1 = "SELECT ZNUM As fuPoiD, ZZX aS x,ZZY aS y fROM DN05490062_FZB FZB wHere leibie='A'"
    cur.execute(sql1)
    FuPoDict = dict()
    FuPoList = []
    # print(FuPoDict.keys())

    for line in cur.fetchall():
        if line != None:
            if line[0] in FuPoDict.keys():
                # print(line)
                FuPoDict[line[0]].append(Point(float(line[1]), float(line[2]), 0))
            else:
                FuPoDict[line[0]] = []

        if line != None:
            FuPoList.append(Point(float(line[1]), float(line[2]), 0))
    cur.close()
    con.commit()
    con.close()
    print([FuPoDict, FuPoList])
    # print(FuPoList)
    return [FuPoDict, FuPoList]


# 后加
# 读取工农业社会文化设施
def readGongNongYe(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = "sELECT * fROM DN05490062_BZB WHERE leibie='P'"
    cur.execute(sql1)
    GongNongYeDict = {'P': [], 'A': [], 'L': []}
    GongNongYeList = []
    for line in cur.fetchall():
        if line != None:
            # print(line)
            GongNongYeList.append(Point(float(line[2]), float(line[3]), 0))
            if line[0] in GongNongYeDict.keys():
                # print(line)
                GongNongYeDict[line[0]].append(Point(float(line[2]), float(line[3]), 0))
            else:
                GongNongYeDict[line[0]] = []
    cur.close()
    con.commit()
    con.close()
    # print('工农业设施！！！！！！！！！！！！！！！！！！！！！！！！！！！！')
    print(GongNongYeList)
    return [GongNongYeDict, GongNongYeList]


# 读取测量控制点
def readControlPoint(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = "sELECT * fROM DN05490062_AZB WHERE leibie='P'"
    cur.execute(sql1)
    ControlPointDict = {'P': [], 'A': [], 'L': []}
    ControlPointList = []
    for line in cur.fetchall():
        if line != None:
            # print(line)
            ControlPointList.append(Point(float(line[2]), float(line[3]), 0))
            ControlPointDict[line[0]].append(Point(float(line[2]), float(line[3]), 0))
    cur.close()
    con.commit()
    con.close()
    return [ControlPointDict, ControlPointList]


# 读取植被
def readVegetationPoint(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = "sELECT * fROM DN05490062_LZB WHERE leibie='P'"
    cur.execute(sql1)
    VegetationPointDict = {'P': [], 'A': [], 'L': []}
    VegetationPointList = []
    for line in cur.fetchall():
        if line != None:
            # print(line)
            VegetationPointList.append(Point(float(line[2]), float(line[3]), 0))
            VegetationPointDict[line[0]].append(Point(float(line[2]), float(line[3]), 0))
    cur.close()
    con.commit()
    con.close()
    return [VegetationPointDict, VegetationPointList]


# 读取居民地以及附属设施3种
def readResidentAndFacilitiesPoint1(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = '''SELECT A.leibie,A.AY,A.ZX,B."编码" FROM DN05490062_CZB AS A JOIN DN05490062_CSX AS B ON A.AX=B."要素编号" WHERE B."编码"LIKE"1301%" '''
    cur.execute(sql1)
    readResidentAndFacilitiesPoint1Dict = {'P': [], 'A': [], 'L': []}
    readResidentAndFacilitiesPoint1List = []
    for line in cur.fetchall():
        if line != None:
            # print(line)
            readResidentAndFacilitiesPoint1List.append(Point(float(line[1]), float(line[2]), 0))
            readResidentAndFacilitiesPoint1Dict[line[0]].append(Point(float(line[1]), float(line[2]), 0))
    print("END")
    cur.close()
    con.commit()
    con.close()
    return [readResidentAndFacilitiesPoint1Dict, readResidentAndFacilitiesPoint1List]


def readResidentAndFacilitiesPoint0(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = '''SELECT A.leibie,A.AY,A.ZX,B."编码" FROM DN05490062_CZB AS A JOIN DN05490062_CSX AS B ON A.AX=B."要素编号" WHERE B."编码"LIKE"1302%" '''
    cur.execute(sql1)
    readResidentAndFacilitiesPoint0Dict = {'P': [], 'A': [], 'L': []}
    readResidentAndFacilitiesPoint0List = []
    for line in cur.fetchall():
        if line != None:
            print(line)
            readResidentAndFacilitiesPoint0List.append(Point(float(line[1]), float(line[2]), 0))
            readResidentAndFacilitiesPoint0Dict[line[0]].append(Point(float(line[1]), float(line[2]), 0))
    print("END")
    cur.close()
    con.commit()
    con.close()
    return [readResidentAndFacilitiesPoint0Dict, readResidentAndFacilitiesPoint0List]


def readResidentAndFacilitiesPoint2(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = '''SELECT A.leibie,A.AY,A.ZX,B."编码" FROM DN05490062_CZB AS A JOIN DN05490062_CSX AS B ON A.AX=B."要素编号" WHERE B."编码"LIKE"1303%" '''
    cur.execute(sql1)
    readResidentAndFacilitiesPoint2Dict = {'P': [], 'A': [], 'L': []}
    readResidentAndFacilitiesPoint2List = []
    for line in cur.fetchall():
        if line != None:
            print(line)
            readResidentAndFacilitiesPoint2List.append(Point(float(line[1]), float(line[2]), 0))
            readResidentAndFacilitiesPoint2Dict[line[0]].append(Point(float(line[1]), float(line[2]), 0))
    print("END")
    cur.close()
    con.commit()
    con.close()
    return [readResidentAndFacilitiesPoint2Dict, readResidentAndFacilitiesPoint2List]


# 读取管线
def readPipelinePoint0(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = '''SELECT A.leibie,A.LAX,A.LAY,B."编码" FROM DN05490062_EZB AS A JOIN DN05490062_ESX AS B ON A.LNUM=B."要素编号" WHERE B."编码"LIKE"1501%" '''
    cur.execute(sql1)
    PipelinePoint0Dict = {'P': [], 'A': [], 'L': []}
    PipelinePoint0List = []
    for line in cur.fetchall():
        if line != None:
            # print(line)
            PipelinePoint0List.append(Point(float(line[1]), float(line[2]), 0))
            PipelinePoint0Dict[line[0]].append(Point(float(line[1]), float(line[2]), 0))
    print("END")
    cur.close()
    con.commit()
    con.close()
    return [PipelinePoint0Dict, PipelinePoint0List]


def readPipelinePoint1(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = '''SELECT A.leibie,A.LAX,A.LAY,B."编码" FROM DN05490062_EZB AS A JOIN DN05490062_ESX AS B ON A.LNUM=B."要素编号" WHERE B."编码"LIKE"1502%" '''
    cur.execute(sql1)
    PipelinePoint1Dict = {'P': [], 'A': [], 'L': []}
    PipelinePoint1List = []
    for line in cur.fetchall():
        if line != None:
            # print(line)
            PipelinePoint1List.append(Point(float(line[1]), float(line[2]), 0))
            PipelinePoint1Dict[line[0]].append(Point(float(line[1]), float(line[2]), 0))
    print("END")
    cur.close()
    con.commit()
    con.close()
    return [PipelinePoint1Dict, PipelinePoint1List]


def readPipelinePoint2(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = '''SELECT A.leibie,A.LAX,A.LAY,B."编码" FROM DN05490062_EZB AS A JOIN DN05490062_ESX AS B ON A.LNUM=B."要素编号" WHERE B."编码"LIKE"1503%" '''
    cur.execute(sql1)
    PipelinePoint2Dict = {'P': [], 'A': [], 'L': []}
    PipelinePoint2List = []
    for line in cur.fetchall():
        if line != None:
            # print(line)
            PipelinePoint2List.append(Point(float(line[1]), float(line[2]), 0))
            PipelinePoint2Dict[line[0]].append(Point(float(line[1]), float(line[2]), 0))
    # print("END")
    cur.close()
    con.commit()
    con.close()
    return [PipelinePoint2Dict, PipelinePoint2List]

# 读取地貌
def readLandformPoint0(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = '''SELECT A.leibie,A.AY,A.ZX,B."编码" FROM DN05490062_JZB AS A JOIN DN05490062_JSX AS B ON A.AX=B."要素编号" WHERE B."编码" LIKE"2003%"'''
    cur.execute(sql1)
    Landform0Dict = {'P': [], 'A': [], 'L': []}
    Landform0List = []
    for line in cur.fetchall():
        if line != None:
            # print(line)
            Landform0List.append(Point(float(line[1]), float(line[2]), 0))
            Landform0Dict[line[0]].append(Point(float(line[1]), float(line[2]), 0))
    # print("END")
    cur.close()
    con.commit()
    con.close()
    return [Landform0Dict, Landform0List]

def readLandformPoint1(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = '''SELECT A.leibie,A.AY,A.ZX,B."编码" FROM DN05490062_JZB AS A JOIN DN05490062_JSX AS B ON A.AX=B."要素编号" WHERE B."编码" LIKE"2004%"'''
    cur.execute(sql1)
    Landform1Dict = {'P': [], 'A': [], 'L': []}
    Landform1List = []
    for line in cur.fetchall():
        if line != None:
            # print(line)
            Landform1List.append(Point(float(line[1]), float(line[2]), 0))
            Landform1Dict[line[0]].append(Point(float(line[1]), float(line[2]), 0))
    # print("END")
    cur.close()
    con.commit()
    con.close()
    return [Landform1Dict, Landform1List]

def readLandformPoint2(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = '''SELECT A.leibie,A.AY,A.ZX,B."编码" FROM DN05490062_JZB AS A JOIN DN05490062_JSX AS B ON A.AX=B."要素编号" WHERE B."编码" LIKE"2005%"'''
    cur.execute(sql1)
    Landform2Dict = {'P': [], 'A': [], 'L': []}
    Landform2List = []
    for line in cur.fetchall():
        if line != None:
            # print(line)
            Landform2List.append(Point(float(line[1]), float(line[2]), 0))
            Landform2Dict[line[0]].append(Point(float(line[1]), float(line[2]), 0))
    # print("END")
    cur.close()
    con.commit()
    con.close()
    return [Landform2Dict, Landform2List]

def readLandformPoint3(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = '''SELECT A.leibie,A.AY,A.ZX,B."编码" FROM DN05490062_JZB AS A JOIN DN05490062_JSX AS B ON A.AX=B."要素编号" WHERE B."编码" LIKE"2006%"'''
    cur.execute(sql1)
    Landform3Dict = {'P': [], 'A': [], 'L': []}
    Landform3List = []
    for line in cur.fetchall():
        if line != None:
            # print(line)
            Landform3List.append(Point(float(line[1]), float(line[2]), 0))
            Landform3Dict[line[0]].append(Point(float(line[1]), float(line[2]), 0))
    # print("END")
    cur.close()
    con.commit()
    con.close()
    return [Landform3Dict, Landform3List]

def readLandformPoint4(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = '''SELECT A.leibie,A.AY,A.ZX,B."编码" FROM DN05490062_JZB AS A JOIN DN05490062_JSX AS B ON A.AX=B."要素编号" WHERE B."编码" LIKE"2007%"'''
    cur.execute(sql1)
    Landform4Dict = {'P': [], 'A': [], 'L': []}
    Landform4List = []
    for line in cur.fetchall():
        if line != None:
            # print(line)
            Landform4List.append(Point(float(line[1]), float(line[2]), 0))
            Landform4Dict[line[0]].append(Point(float(line[1]), float(line[2]), 0))
    # print("END")
    cur.close()
    con.commit()
    con.close()
    return [Landform4Dict, Landform4List]

def readLandformPoint5(dbName):
    con = sqlite3.connect(dbName)
    cur = con.cursor()
    sql1 = '''SELECT A.leibie,A.AY,A.ZX,B."编码" FROM DN05490062_JZB AS A JOIN DN05490062_JSX AS B ON A.AX=B."要素编号" WHERE B."编码" LIKE"2008%"'''
    cur.execute(sql1)
    Landform5Dict = {'P': [], 'A': [], 'L': []}
    Landform5List = []
    for line in cur.fetchall():
        if line != None:
            # print(line)
            Landform5List.append(Point(float(line[1]), float(line[2]), 0))
            Landform5Dict[line[0]].append(Point(float(line[1]), float(line[2]), 0))
    # print("END")
    cur.close()
    con.commit()
    con.close()
    return [Landform5Dict, Landform5List]


# 以下是路径规划功能的代码
'''
# 路径规划功能使用实例
# origin是起点坐标，destination是目的地坐标，注意不要坐标的x和y不要搞反
# routes是返回路径的列表，routes列表中每个元素也是列表，每个用来表示整条路中其中一段路
origin = [3383.189209, 12753.866229]
destination = [6898.159668, 13558.871111]
routes = findWay(origin, destination)

# 取出起始点坐标和终点坐标
start_x = routes[0][0][0]
start_y = routes[0][0][1]
end_x = routes[-1][-1][0]
end_y = routes[-1][-1][1]

# 地图中心以起点坐标为准
folium_map = drawMapCenter([start_x, start_y])
# 绘制起始点和终点标记
folium.Marker([start_x, start_y], tooltip="起点", popup="<b>起\t点</b>").add_to(folium_map)
folium.Marker([end_x, end_y], tooltip="终点", popup="<b>终\t点</b>").add_to(folium_map)

# 绘制路径
for route in routes:
    folium_map = drawMapLines(route, folium_map)

# 生成最终的地图
folium_map.save('tmp.html')
'''

def drawMapCenter0():
    folium_map = folium.Map()
    return folium_map
#
#
# def drawMapCenter(start_coords):
#     response = requests.get(
#         'https://api.map.baidu.com/geoconv/v1/?coords=' + str(start_coords[0]) + ',' + str(
#             start_coords[1]) + '&from=1&to=3&ak=V9pGzEIigoQqQyGMG4v4C1qqbTl7vccz&output=json')
#     print(response.text)
#     x = json.loads(response.text)["result"][0]['x']
#     y = json.loads(response.text)["result"][0]['y']
#     folium_map = folium.Map(
#         location=[x, y],
#         zoom_start=12,
#         tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
#         # tiles='https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
#         attr='default'
#     )
#     return folium_map


def retry_func(X, Y):
    try:
        response = requests.get(
            'https://api.map.baidu.com/geoconv/v1/?coords=' + str(X) + ',' + str(
                Y) + '&from=1&to=3&ak=V9pGzEIigoQqQyGMG4v4C1qqbTl7vccz&output=json')
    except Exception:
        response = retry_func(X, Y)
    return response


def bd_decrypt(bd_lat, bd_lon):

    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * math.pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * math.pi)
    gg_lon = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return gg_lat, gg_lon


def add_map_point(point, folium_map):
    x = point[0] / 1000 + 2192935.10
    y = point[1] / 1000 + 19472810.74
    tmp_x, tmp_y = CGCS2WSG(x, y)
    X = tmp_x[1] + tmp_x[2] / 60 + tmp_x[3] / 3600
    Y = tmp_y[1] + tmp_y[2] / 60 + tmp_y[3] / 3600
    xx, yy = bd_decrypt(X, Y)
    folium.Marker([xx, yy]).add_to(folium_map)


def drawMapPoints(points, folium_map):
    cnt = 0
    for point in points:
        print(point)
        for p in point:
            pattern = re.compile(r'\d+')  # 查找数字
            result = pattern.findall(p)
            print(result)
            if len(result) != 0:
                x = int(result[0]) + int(result[1]) / 1000 + 2192935.10
                y = int(result[2]) + int(result[3]) / 1000 + 19472810.74
                tmp_x, tmp_y = CGCS2WSG(x, y)
                X = tmp_x[1] + tmp_x[2] / 60 + tmp_x[3] / 3600
                Y = tmp_y[1] + tmp_y[2] / 60 + tmp_y[3] / 3600
                if cnt < 100:
                    xx, yy = bd_decrypt(X, Y)
                    # try:
                    #     response = requests.get(
                    #         'https://api.map.baidu.com/geoconv/v1/?coords=' + str(X) + ',' + str(
                    #             Y) + '&from=1&to=3&ak=V9pGzEIigoQqQyGMG4v4C1qqbTl7vccz&output=json')
                    # except Exception:
                    #     response = retry_func(X, Y)
                    # xx = json.loads(response.text)["result"][0]['x']
                    # yy = json.loads(response.text)["result"][0]['y']
                    # print(response.text)
                    print(xx)
                    print(yy)
                    folium.Marker([xx, yy]).add_to(folium_map)
                cnt += 1
                # response = requests.get(
                #     'https://api.map.baidu.com/geoconv/v1/?coords=' + str(tmp_x[3]) + ',' + str(
                #         tmp_y[3]) + '&from=1&to=3&ak=V9pGzEIigoQqQyGMG4v4C1qqbTl7vccz&output=json')
                # # print(response.text)
                # xx = json.loads(response.text)["result"][0]['x']
                # yy = json.loads(response.text)["result"][0]['y']
                # print(xx)
                # print(yy)
                #
                # folium.Marker([xx, yy]).add_to(folium_map)
    return folium_map

#
# def drawMapLines(points, folium_map):
#     pointsList = []
#     for point in points:
#         print(point)
#         for p in point:
#             pattern = re.compile(r'\d+')  # 查找数字
#             result = pattern.findall(p)
#             print(result)
#             if len(result) != 0:
#                 x = int(result[0]) + int(result[1]) / 1000
#                 y = int(result[2]) + int(result[3]) / 1000
#                 tmp_x, tmp_y = CGCS2WSG(x, y)
#                 response = requests.get(
#                     'https://api.map.baidu.com/geoconv/v1/?coords=' + str(tmp_x[3]) + ',' + str(
#                         tmp_y[3]) + '&from=1&to=3&ak=V9pGzEIigoQqQyGMG4v4C1qqbTl7vccz&output=json')
#                 # print(response.text)
#                 xx = json.loads(response.text)["result"][0]['x']
#                 yy = json.loads(response.text)["result"][0]['y']
#                 # print(xx)
#                 # print(yy)
#                 folium.Marker([xx, yy]).add_to(folium_map)
#                 pointsList.append([xx, yy])
#     folium.PolyLine(pointsList, color='blue').add_to(folium_map)
#     return folium_map
#
#
# def CGCS2WSG(X, Y):
#     PI = math.pi
#     rad_dgr = 180 / PI
#     rad_min = rad_dgr * 60
#     rad_sec = rad_min * 60
#     Maxcnt = 5
#
#     a = 6378137.0
#     b = 6356752.3142
#
#     e2 = (a * a - b * b) / a / a
#     _e2 = (a * a - b * b) / b / b
#     c = a * a / b
#
#     bata0 = 1 - 3.0 / 4 * _e2 + 45. / 64 * _e2 * _e2 - 175.0 / 256 * pow(_e2, 3) + 11025. / 16384 * pow(_e2, 4)
#     C0 = bata0 * c
#
#     m0 = a * (1 - e2)
#     m2 = 3.0 / 2 * e2 * m0
#     m4 = 5.0 / 4 * e2 * m2
#     m6 = 7.0 / 6 * e2 * m4
#     m8 = 9.0 / 8 * e2 * m6
#
#     a2 = m2 / 2 + m4 / 2 + 15.0 / 32 * m6 + 7.0 / 16 * m8
#     a4 = m4 / 8 + 3.0 / 16 * m6 + 7.0 / 32 * m8
#     a6 = m6 / 32 + m8 / 16
#     a8 = m8 / 128
#
#     x = X
#     Daihao = int(Y / 1000000)
#     y = Y - Daihao * 1000000 - 500000
#     Bf = X / C0
#     cnt = 0
#
#     Bf1 = Bf
#     FBf1 = -a2 / 2 * math.sin(2 * Bf1) + a4 / 4 * math.sin(4 * Bf1) - a6 / 6 * math.sin(6 * Bf1)
#     Bf = (X - FBf1) / C0
#     cnt += 1
#     while abs(Bf - Bf1) >= 0.0000001 and cnt < Maxcnt:
#         Bf1 = Bf
#         FBf1 = -a2 / 2 * math.sin(2 * Bf1) + a4 / 4 * math.sin(4 * Bf1) - a6 / 6 * math.sin(6 * Bf1)
#         Bf = (X - FBf1) / C0
#         cnt += 1
#
#     if cnt == Maxcnt and abs(Bf - Bf1) >= 0.0000001:
#
#         print("Error in counting Bf!")
#         return
#     else:
#         Vf = math.sqrt(1 + _e2 * math.cos(Bf) * math.cos(Bf))
#         Nf = c / Vf
#         Nf2 = Nf * Nf
#         Mf = c / (Vf * Vf * Vf)
#         tf2 = math.tan(Bf) * math.tan(Bf)
#         etarf2 = _e2 * math.cos(Bf) * math.cos(Bf)
#
#         y2 = y * y
#         tb = math.tan(Bf) / (Mf * Nf) * y2
#         B = []
#         B.append(Bf - tb / 2 + tb / (24 * Nf2) * y2 * (5 + 3 * tf2 + etarf2 - 9 * etarf2 * tf2) - tb / (
#                     720 * Nf2 * Nf2) * y2 * y2 * (61 + 90 * tf2 + 45 * tf2 * tf2))
#         B.append(int(B[0] * rad_dgr))
#         B.append(int(B[0] * rad_min - B[1] * 60))
#         B.append(B[0] * rad_sec - B[1] * 3600 - B[2] * 60)
#
#         L = []
#         tl = y / Nf / math.cos(Bf)
#         L.append(tl - tl / (6 * Nf2) * y2 * (1 + 2 * tf2 + etarf2) + tl / (120 * Nf2 * Nf2) * y2 * y2 * (
#                     5 + 28 * tf2 + 24 * tf2 * tf2 + 6 * etarf2 + 8 * etarf2 * tf2))
#         t = ((6 * Daihao - 3) / rad_dgr + L[0]) * rad_dgr
#         L.append(int(t))
#         t = (t - L[1]) * 60
#         L.append(int(t))
#         t = (t - L[2]) * 60
#         L.append(t)
#
#         print(B)
#         print(L)
#         return B, L


# 绘制地图，确定地图的中心位置，地图大小，地图背景。
def drawMapCenter(start_coords):
    response = requests.get(
        'https://api.map.baidu.com/geoconv/v1/?coords=' + str(start_coords[0]) + ',' + str(
            start_coords[1]) + '&from=1&to=3&ak=V9pGzEIigoQqQyGMG4v4C1qqbTl7vccz&output=json', verify=False)
    # print(response.text)
    x = json.loads(response.text)["result"][0]['x']
    y = json.loads(response.text)["result"][0]['y']
    folium_map = folium.Map(
        location=[x, y],
        zoom_start=10,
        tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
        # tiles='https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='default'
    )
    return folium_map


def drawHeatMapCenter(start_coords):
    response = requests.get(
        'https://api.map.baidu.com/geoconv/v1/?coords=' + str(start_coords[0]) + ',' + str(
            start_coords[1]) + '&from=1&to=3&ak=V9pGzEIigoQqQyGMG4v4C1qqbTl7vccz&output=json', verify=False)
    # print(response.text)
    x = json.loads(response.text)["result"][0]['x']
    y = json.loads(response.text)["result"][0]['y']
    folium_map = folium.Map(
        location=[x, y],
        zoom_start=12,
        tiles='Stamen Toner',
        # tiles='https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='default'
    )
    return folium_map

# 画线
def drawMapLines(points, color, folium_map):
    folium.PolyLine(points, color=color).add_to(folium_map)
    return folium_map


# 坐标转化函数
def CGCS2WSG(X, Y):
    PI = math.pi
    rad_dgr = 180 / PI
    rad_min = rad_dgr * 60
    rad_sec = rad_min * 60
    Maxcnt = 5

    a = 6378137.0
    b = 6356752.3142

    e2 = (a * a - b * b) / a / a
    _e2 = (a * a - b * b) / b / b
    c = a * a / b

    bata0 = 1 - 3.0 / 4 * _e2 + 45. / 64 * _e2 * _e2 - 175.0 / 256 * pow(_e2, 3) + 11025. / 16384 * pow(_e2, 4)
    C0 = bata0 * c

    m0 = a * (1 - e2)
    m2 = 3.0 / 2 * e2 * m0
    m4 = 5.0 / 4 * e2 * m2
    m6 = 7.0 / 6 * e2 * m4
    m8 = 9.0 / 8 * e2 * m6

    a2 = m2 / 2 + m4 / 2 + 15.0 / 32 * m6 + 7.0 / 16 * m8
    a4 = m4 / 8 + 3.0 / 16 * m6 + 7.0 / 32 * m8
    a6 = m6 / 32 + m8 / 16
    a8 = m8 / 128

    x = X
    Daihao = int(Y / 1000000)
    y = Y - Daihao * 1000000 - 500000
    Bf = X / C0
    cnt = 0

    Bf1 = Bf
    FBf1 = -a2 / 2 * math.sin(2 * Bf1) + a4 / 4 * math.sin(4 * Bf1) - a6 / 6 * math.sin(6 * Bf1)
    Bf = (X - FBf1) / C0
    cnt += 1
    while abs(Bf - Bf1) >= 0.0000001 and cnt < Maxcnt:
        Bf1 = Bf
        FBf1 = -a2 / 2 * math.sin(2 * Bf1) + a4 / 4 * math.sin(4 * Bf1) - a6 / 6 * math.sin(6 * Bf1)
        Bf = (X - FBf1) / C0
        cnt += 1

    if cnt == Maxcnt and abs(Bf - Bf1) >= 0.0000001:

        print("Error in counting Bf!")
        return
    else:
        Vf = math.sqrt(1 + _e2 * math.cos(Bf) * math.cos(Bf))
        Nf = c / Vf
        Nf2 = Nf * Nf
        Mf = c / (Vf * Vf * Vf)
        tf2 = math.tan(Bf) * math.tan(Bf)
        etarf2 = _e2 * math.cos(Bf) * math.cos(Bf)

        y2 = y * y
        tb = math.tan(Bf) / (Mf * Nf) * y2
        B = []
        B.append(Bf - tb / 2 + tb / (24 * Nf2) * y2 * (5 + 3 * tf2 + etarf2 - 9 * etarf2 * tf2) - tb / (
                    720 * Nf2 * Nf2) * y2 * y2 * (61 + 90 * tf2 + 45 * tf2 * tf2))
        B.append(int(B[0] * rad_dgr))
        B.append(int(B[0] * rad_min - B[1] * 60))
        B.append(B[0] * rad_sec - B[1] * 3600 - B[2] * 60)

        L = []
        tl = y / Nf / math.cos(Bf)
        L.append(tl - tl / (6 * Nf2) * y2 * (1 + 2 * tf2 + etarf2) + tl / (120 * Nf2 * Nf2) * y2 * y2 * (
                    5 + 28 * tf2 + 24 * tf2 * tf2 + 6 * etarf2 + 8 * etarf2 * tf2))
        t = ((6 * Daihao - 3) / rad_dgr + L[0]) * rad_dgr
        L.append(int(t))
        t = (t - L[1]) * 60
        L.append(int(t))
        t = (t - L[2]) * 60
        L.append(t)
        #
        # print(B)
        # print(L)
        return B, L


def WSG2GSJ(x, y):
    response = requests.get(
        'https://api.map.baidu.com/geoconv/v1/?coords=' + str(x) + ',' + str(
            y) + '&from=1&to=3&ak=V9pGzEIigoQqQyGMG4v4C1qqbTl7vccz&output=json')
    xx = json.loads(response.text)["result"][0]['x']
    yy = json.loads(response.text)["result"][0]['y']
    return xx, yy


# 坐标转化 CGCS2000转GCJ火星坐标系
def CGCS2GSJ(x, y):
    tmp_x, tmp_y = CGCS2WSG(x, y)
    X = tmp_x[1] + tmp_x[2] / 60 + tmp_x[3] / 3600
    Y = tmp_y[1] + tmp_y[2] / 60 + tmp_y[3] / 3600

    response = requests.get(
        'https://api.map.baidu.com/geoconv/v1/?coords=' + str(X) + ',' + str(
            Y) + '&from=1&to=3&ak=V9pGzEIigoQqQyGMG4v4C1qqbTl7vccz&output=json')
    # print(response.text)
    xx = json.loads(response.text)["result"][0]['x']
    yy = json.loads(response.text)["result"][0]['y']
    return xx, yy


# 将元素类型为string的列表转化为元素类型为float的列表
def castStringListToFloatList(point):
    result = []
    for tmp in point:
        result.append(float(tmp))
    return result


# findWay函数返回值是列表，包含经过的每条路的坐标，第一维度表示单独的一条路，第二维度表示该条路经过的所有坐标，用于画线
def findWay(origin, destination):
    origin_x, origin_y = CGCS2GSJ(origin[0] + 2192935.10, origin[1] + 19472810.74)
    destination_x, destination_y = CGCS2GSJ(destination[0] + 2192935.10, destination[1] + 19472810.74)
    origin_x = round(origin_x, 6)  # 保留六位
    origin_y = round(origin_y, 6)
    destination_x = round(destination_x, 6)
    destination_y = round(destination_y, 6)

    response = requests.get(
        'https://restapi.amap.com/v3/direction/walking?origin=' + str(origin_y) + ',' + str(origin_x) + '&destination=' + str(destination_y) + ',' + str(destination_x) + '&key=95cf688505e14a1d92a0c76a730c1b9d'
    )
    List = json.loads(response.text)["route"]["paths"][0]["steps"]
    # result是最终返回结果
    result = []
    for line in List:
        # one_of_routes是一个列表，每一项都是一条完整的路
        print("------------------------------------------------------------")
        print(line)
        one_of_routes = line["polyline"].split(';')
        print(one_of_routes)
        route = []
        for point_of_one_route in one_of_routes:
            point = point_of_one_route.split(',')[::-1]
            print(point) # ###############
            route.append(castStringListToFloatList(point))
        result.append(route)
        print(route)
        print("----------------------------------------------------------")
        # print('')

    return result


# 传入的是2000坐标
def findWay2(origin, destination):
    origin_x, origin_y = CGCS2GSJ(origin[0] + 2192935.10, origin[1] + 19472810.74)
    destination_x, destination_y = CGCS2GSJ(destination[0] + 2192935.10, destination[1] + 19472810.74)
    origin_x = round(origin_x, 6)  # 保留六位
    origin_y = round(origin_y, 6)
    destination_x = round(destination_x, 6)
    destination_y = round(destination_y, 6)

    # response = requests.get(
    #     'https://restapi.amap.com/v3/direction/walking?origin=' + str(origin_y) + ',' + str(origin_x) + '&destination=' + str(destination_y) + ',' + str(destination_x) + '&key=95cf688505e14a1d92a0c76a730c1b9d'
    # )

    # 步行
    response1 = requests.get(
        'https://restapi.amap.com/v3/direction/walking?origin=' + str(origin_y) + ',' + str(
            origin_x) + '&destination=' + str(destination_y) + ',' + str(
            destination_x) + '&key=95cf688505e14a1d92a0c76a730c1b9d'
    )


    # 驾车策略  (速度优先，不一定是距离最短)
    # https://restapi.amap.com/v3/direction/driving?origin=116.481028,39.989643&destination=116.465302,40.004717&extensions=all&output=json&key=95cf688505e14a1d92a0c76a730c1b9d&strategy=0
    response2 = requests.get(
        'https://restapi.amap.com/v3/direction/driving?origin=' + str(origin_y) + ',' + str(origin_x) + '&destination='+ str(destination_y) + ',' + str(destination_x) +'&extensions=all&output=json&key=95cf688505e14a1d92a0c76a730c1b9d&strategy=0'
    )

    # 驾车策略  (距离最短路线，其中穿插小路，可能存在埋伏)
    response3 = requests.get(
        'https://restapi.amap.com/v3/direction/driving?origin=' + str(origin_y) + ',' + str(
            origin_x) + '&destination=' + str(destination_y) + ',' + str(
            destination_x) + '&extensions=all&output=json&key=95cf688505e14a1d92a0c76a730c1b9d&strategy=2'
    )

    # 驾车策略  (不走高速国道，避免较大的路段)
    response4 = requests.get(
        'https://restapi.amap.com/v3/direction/driving?origin=' + str(origin_y) + ',' + str(origin_x) + '&destination='+ str(destination_y) + ',' + str(destination_x) +'&extensions=all&output=json&key=95cf688505e14a1d92a0c76a730c1b9d&strategy=7'
    )

    # 处理第一条路经
    List = json.loads(response1.text)["route"]["paths"][0]["steps"]
    # result是最终返回结果
    result = []
    for line in List:
        # one_of_routes是一个列表，每一项都是一条完整的路
        print("------------------------------------------------------------")
        print(line)
        one_of_routes = line["polyline"].split(';')
        print(one_of_routes)
        route = []
        for point_of_one_route in one_of_routes:
            point = point_of_one_route.split(',')[::-1]
            print(point)
            route.append(castStringListToFloatList(point))
        result.append(route)
        print(route)
        print("----------------------------------------------------------")
        # print('')

    # 处理第二条路径
    List2 = json.loads(response2.text)["route"]["paths"][0]["steps"]
    result2 = []
    for line in List2:
        # one_of_routes是一个列表，每一项都是一条完整的路
        print("------------------------------------------------------------")
        print(line)
        one_of_routes = line["polyline"].split(';')
        print(one_of_routes)
        route = []
        for point_of_one_route in one_of_routes:
            point = point_of_one_route.split(',')[::-1]
            print(point)
            route.append(castStringListToFloatList(point))
        result2.append(route)
        print(route)
        print("----------------------------------------------------------")
        # print('')

    List3 = json.loads(response3.text)["route"]["paths"][0]["steps"]
    result3 = []
    for line in List3:
        # one_of_routes是一个列表，每一项都是一条完整的路
        print("------------------------------------------------------------")
        print(line)
        one_of_routes = line["polyline"].split(';')
        print(one_of_routes)
        route = []
        for point_of_one_route in one_of_routes:
            point = point_of_one_route.split(',')[::-1]
            print(point)
            route.append(castStringListToFloatList(point))
        result3.append(route)
        print(route)
        print("----------------------------------------------------------")
        # print('')

    List4 = json.loads(response4.text)["route"]["paths"][0]["steps"]
    result4 = []
    for line in List4:
        # one_of_routes是一个列表，每一项都是一条完整的路
        print("------------------------------------------------------------")
        print(line)
        one_of_routes = line["polyline"].split(';')
        print(one_of_routes)
        route = []
        for point_of_one_route in one_of_routes:
            point = point_of_one_route.split(',')[::-1]
            print(point)
            route.append(castStringListToFloatList(point))
        result4.append(route)
        print(route)
        print("----------------------------------------------------------")
        # print('')
    return result, result2, result3, result4


# 传入的是大地坐标
def findWay3(origin, destination, choice):
    origin_y, origin_x = WSG2GSJ(origin[0], origin[1])
    destination_y, destination_x = WSG2GSJ(destination[0], destination[1])
    origin_x = round(origin_x, 6)  # 保留六位
    origin_y = round(origin_y, 6)
    destination_x = round(destination_x, 6)
    destination_y = round(destination_y, 6)


    if choice == '1':
        # 处理第一条路经:步行
        response = requests.get(
            'https://restapi.amap.com/v3/direction/walking?origin=' + str(origin_y) + ',' + str(
                origin_x) + '&destination=' + str(destination_y) + ',' + str(
                destination_x) + '&key=95cf688505e14a1d92a0c76a730c1b9d'
        )

        try:
            List = json.loads(response.text)["route"]["paths"][0]["steps"]
        except KeyError:
            return False

        # result是最终返回结果
        result = []
        for line in List:
            # one_of_routes是一个列表，每一项都是一条完整的路
            one_of_routes = line["polyline"].split(';')
            route = []
            for point_of_one_route in one_of_routes:
                point = point_of_one_route.split(',')[::-1]
                route.append(castStringListToFloatList(point))
            result.append(route)
        return result

    elif choice == '2':
        # 处理第二条路经:驾车策略  (速度优先，不一定是距离最短)
        response = requests.get(
            'https://restapi.amap.com/v3/direction/driving?origin=' + str(origin_y) + ',' + str(
                origin_x) + '&destination=' + str(destination_y) + ',' + str(
                destination_x) + '&extensions=all&output=json&key=95cf688505e14a1d92a0c76a730c1b9d&strategy=0'
        )

        List = json.loads(response.text)["route"]["paths"][0]["steps"]

        # result是最终返回结果
        result = []
        for line in List:
            # one_of_routes是一个列表，每一项都是一条完整的路
            one_of_routes = line["polyline"].split(';')
            route = []
            for point_of_one_route in one_of_routes:
                point = point_of_one_route.split(',')[::-1]
                route.append(castStringListToFloatList(point))
            result.append(route)
        return result

    elif choice == '3':
        # 处理第三条路经:驾车策略  (距离最短路线，其中穿插小路，可能存在埋伏)
        response = requests.get(
            'https://restapi.amap.com/v3/direction/driving?origin=' + str(origin_y) + ',' + str(
                origin_x) + '&destination=' + str(destination_y) + ',' + str(
                destination_x) + '&extensions=all&output=json&key=95cf688505e14a1d92a0c76a730c1b9d&strategy=2'
        )

        List = json.loads(response.text)["route"]["paths"][0]["steps"]

        # result是最终返回结果
        result = []
        for line in List:
            # one_of_routes是一个列表，每一项都是一条完整的路
            one_of_routes = line["polyline"].split(';')
            route = []
            for point_of_one_route in one_of_routes:
                point = point_of_one_route.split(',')[::-1]
                route.append(castStringListToFloatList(point))
            result.append(route)
        return result

    elif choice == '4':
        # 处理第四条路经:驾车策略  (不走高速国道，避免较大的路段)
        response = requests.get(
            'https://restapi.amap.com/v3/direction/driving?origin=' + str(origin_y) + ',' + str(origin_x) + '&destination='+ str(destination_y) + ',' + str(destination_x) +'&extensions=all&output=json&key=95cf688505e14a1d92a0c76a730c1b9d&strategy=7'
        )

        List = json.loads(response.text)["route"]["paths"][0]["steps"]

        # result是最终返回结果
        result = []
        for line in List:
            # one_of_routes是一个列表，每一项都是一条完整的路
            one_of_routes = line["polyline"].split(';')
            route = []
            for point_of_one_route in one_of_routes:
                point = point_of_one_route.split(',')[::-1]
                route.append(castStringListToFloatList(point))
            result.append(route)
        return result





# K-Means
def findDistance(x, y):
    return np.sqrt(np.sum(np.power(x - y, 2)))


def findPoints(data, k):
    m, n = np.shape(data)
    points = np.mat(np.zeros((k, n)))
    for i in range(n):
        min = np.min(data[:, i])
        I = float(np.max(data[:, i]) - min)
        points[:, i] = min + I * np.random.rand(k, 1)
    return points


def kMeans(data, k):
    m, n = np.shape(data)
    cluster = np.mat(np.zeros((m, 2)))
    points = findPoints(data, k)
    flag = True
    while flag:
        flag = False
        for i in range(m):
            minDistance = np.inf
            minIndex = -1
            for j in range(k):
                distance = findDistance(points[j, :], data[i, :])
                if distance < minDistance:
                    minDistance = distance
                    minIndex = j
            if cluster[i, 0] != minIndex:
                flag = True
            cluster[i, :] = minIndex, minDistance ** 2
        for p in range(k):
            pts = data[np.nonzero(cluster[:, 0].A == p)[0]]
            points[p, :] = np.mean(pts, axis=0)
    return points, cluster


def dichotomyKMeans(data, k):
    m, n = np.shape(data)
    cluster = np.mat(np.zeros((m, 2)))
    points = np.mean(data, axis=0).tolist()[0]
    pointsList = [points]
    for i in range(m):
        cluster[i, 1] = findDistance(points, data[i, :]) ** 2

    while len(pointsList) < k:
        SSE = np.inf

        for j in range(len(pointsList)):
            pts = data[np.nonzero(cluster[:, 0].A == j)[0], :]
            pointsMatrix, informationOfData = kMeans(pts, 2)
            SSESplit = np.sum(informationOfData[:, 1])
            SSENoSplit = np.sum(cluster[np.nonzero(cluster[:, 0].A != j)[0], 1])

            tempLowestSEE = SSESplit + SSENoSplit
            if tempLowestSEE < SSE:
                splitPoints = j
                newPoints = pointsMatrix
                newInformationOfData = informationOfData
                SSE = tempLowestSEE

        newInformationOfData[np.nonzero(newInformationOfData[:, 0].A == 1)[0], 0] = len(pointsList)
        newInformationOfData[np.nonzero(newInformationOfData[:, 0].A == 0)[0], 0] = splitPoints
        pointsList[splitPoints] = newPoints[0, :]
        pointsList.append(newPoints[1, :])
        cluster[np.nonzero(cluster[:, 0].A == splitPoints)[0], :] = newInformationOfData

    try:
        return np.mat(pointsList), cluster
    except ValueError:
        return np.mat(np.array(list(map(lambda x: [int(x[0]), x[1]],
                                        [np.matrix.tolist(i)[0] for i in pointsList])))), cluster


def real_k_means(choice, k, folium_map):
    pointList = []

    if choice == '0':
        pass
    elif choice == '1':
        con = sqlite3.connect("DN05490062.db")  # 连接桥
        # print("Open database successfully")  # 打开成功
        cur = con.cursor()
        sql1 = "SELECT fzb.AY as x,fzb.ZX as y FROM DN05490062_FZB fzb LEFT JOIN DN05490062_FSX fsx ON fzb.AX = fsx.要素编号"
        cur.execute(sql1)

        for line in cur.fetchall():
            if line[0] != None and line[1] != None:
                pointList.append([float(line[0]), float(line[1])])
        cur.close()
        con.commit()
        con.close()
    elif choice == '2':
        con = sqlite3.connect("DN05490062.db")  # 连接桥
        # print("Open database successfully")  # 打开成功
        cur = con.cursor()
        sql1 = "SELECT azb.AY as x,azb.ZX as y FROM DN05490062_AZB azb LEFT JOIN DN05490062_ASX asx ON azb.AX = asx.要素编号"
        cur.execute(sql1)

        for line in cur.fetchall():
            if line[0] != None and line[1] != None:
                pointList.append([float(line[0]), float(line[1])])
        cur.close()
        con.commit()
        con.close()
    elif choice == '3':
        con = sqlite3.connect("DN05490062.db")  # 连接桥
        # print("Open database successfully")  # 打开成功
        cur = con.cursor()
        sql1 = "SELECT bzb.AY as x,bzb.ZX as y FROM DN05490062_BZB bzb LEFT JOIN DN05490062_BSX bsx ON bzb.AX = bsx.要素编号"
        cur.execute(sql1)

        for line in cur.fetchall():
            if line[0] != None and line[1] != None:
                pointList.append([float(line[0]), float(line[1])])
        cur.close()
        con.commit()
        con.close()
    elif choice == '4':
        con = sqlite3.connect("DN05490062.db")  # 连接桥
        # print("Open database successfully")  # 打开成功
        cur = con.cursor()
        sql1 = "SELECT lzb.AY as x,lzb.ZX as y FROM DN05490062_LZB lzb LEFT JOIN DN05490062_LSX lsx ON lzb.AX = lsx.要素编号"
        cur.execute(sql1)

        for line in cur.fetchall():
            if line[0] != None and line[1] != None:
                pointList.append([float(line[0]), float(line[1])])
        cur.close()
        con.commit()
        con.close()
    elif choice == '5':
        con = sqlite3.connect("DN05490062.db")  # 连接桥
        # print("Open database successfully")  # 打开成功
        cur = con.cursor()
        sql1 = "SELECT pzb.AY as x,pzb.ZX as y FROM DN05490062_PZB pzb LEFT JOIN DN05490062_PSX psx ON pzb.AX = psx.要素编号"
        cur.execute(sql1)

        for line in cur.fetchall():
            if line[0] != None and line[1] != None:
                pointList.append([float(line[0]), float(line[1])])
        cur.close()
        con.commit()
        con.close()



    data = np.array(pointList)
    a, b = dichotomyKMeans(data, k)

    for i in range(len(a[:, 0])):
        pts = data[np.nonzero(b[:, 0] == i)[0], :]

        colors = ['#6495ED', '#6495ED', '#FFEC8B', '#EE6363', '#FFA500']
        Color = colors[i % len(colors)]
        x = a[i, 0] / 1000 + 2192935.10
        y = a[i, 1] / 1000 + 19472810.74
        tmp_x, tmp_y = CGCS2WSG(x, y)
        X = tmp_x[1] + tmp_x[2] / 60 + tmp_x[3] / 3600
        Y = tmp_y[1] + tmp_y[2] / 60 + tmp_y[3] / 3600
        xx, yy = bd_decrypt(X, Y)

        folium.Marker(
            location=[xx, yy],
        ).add_to(folium_map)

        folium.Circle(
            location=[xx, yy],
            radius=len(pts) * 10,
            color=Color,
            fill=True,
            fill_color=Color
        ).add_to(folium_map)
        print(a[i, 0], a[i, 1])

    folium_map.save("templates/kmeans.html")
    replaceJsRef("templates/kmeans.html")


def get_road_or_tree_data(place_name, folium_map):
    if place_name == "DN05490062-road":
        con = sqlite3.connect("DN05490062.db")  # 连接桥
        # print("Open database successfully")  # 打开成功
        cur = con.cursor()
        sql1 = "SELECT dzb.AY as x,dzb.ZX as y,dzb.ZY as width FROM DN05490062_DZB dzb LEFT JOIN DN05490062_DSX dsx ON dzb.AX = dsx.'要素编号'"
        sql2 = "SELECT dzb.LAX as x,dzb.LAY as y,dsx.宽度 as width FROM DN05490062_DZB dzb LEFT JOIN DN05490062_DSX dsx ON dzb.LNUM = dsx.要素编号"
        pointList = []

        cur.execute(sql1)
        for line in cur.fetchall():
            if line[0] != None and line[1] != None and line[2] != None:
                pointList.append([float(line[0]), float(line[1]), float(line[2])])

        cur.execute(sql2)
        for line in cur.fetchall():
            if line[0] != None and line[1] != None and line[2] != None:
                pointList.append([float(line[0]), float(line[1]), float(line[2])])

        cur.close()
        con.commit()
        con.close()
        # print(pointList)
        cnt = 0
        for point in pointList:
            x = point[0] / 1000 + 2192935.10
            y = point[1] / 1000 + 19472810.74
            tmp_x, tmp_y = CGCS2WSG(x, y)
            X = tmp_x[1] + tmp_x[2] / 60 + tmp_x[3] / 3600
            Y = tmp_y[1] + tmp_y[2] / 60 + tmp_y[3] / 3600
            point[0], point[1] = bd_decrypt(X, Y)
            point[2] *= 100
            # cnt += 1
            # if cnt <= 30:
            #     folium.Marker(
            #         location=[point[0], point[1]],
            #     ).add_to(folium_map)
        print(pointList)
        HeatMap(pointList, radius=5).add_to(folium_map)  # 将热力图添加到前面建立的map里
        return folium_map
    elif place_name == "DN05490062-tree":
        con = sqlite3.connect("DN05490062.db")  # 连接桥
        # print("Open database successfully")  # 打开成功
        cur = con.cursor()
        sql1 = "SELECT lzb.AY as x,lzb.ZX as y FROM DN05490062_LZB lzb"
        pointList = []

        cur.execute(sql1)
        for line in cur.fetchall():
            if line[0] != None and line[1] != None:
                pointList.append([float(line[0]), float(line[1]), 50000])

        cur.close()
        con.commit()
        con.close()
        # print(pointList)
        cnt = 0
        for point in pointList:
            x = point[0] / 1000 + 2192935.10
            y = point[1] / 1000 + 19472810.74
            tmp_x, tmp_y = CGCS2WSG(x, y)
            X = tmp_x[1] + tmp_x[2] / 60 + tmp_x[3] / 3600
            Y = tmp_y[1] + tmp_y[2] / 60 + tmp_y[3] / 3600
            point[0], point[1] = bd_decrypt(X, Y)
        print(pointList)
        HeatMap(pointList, radius=5).add_to(folium_map)  # 将热力图添加到前面建立的map里
        return folium_map


def get_data_zhifangtu():
    con = sqlite3.connect("DN05490062.db")  # 连接桥
    # print("Open database successfully")  # 打开成功
    cur = con.cursor()
    A_L = 0
    A_P = 0
    B_L = 0
    B_P = 0
    C_L = 0
    C_P = 0
    D_L = 0
    D_P = 0
    L_L = 0
    L_P = 0

    sql1 = "SELECT 所属类别, COUNT(所属类别) FROM DN05490062_ASX GROUP BY 所属类别 "
    cur.execute(sql1)
    for line in cur.fetchall():
        if line[0] == 'P':
            A_P = line[1]
        elif line[0] == 'L':
            A_L = line[1]

    sql2 = "SELECT 所属类别, COUNT(所属类别) FROM DN05490062_BSX GROUP BY 所属类别 "
    cur.execute(sql2)
    for line in cur.fetchall():
        if line[0] == 'P':
            B_P = line[1]
        elif line[0] == 'L':
            B_L = line[1]

    sql3 = "SELECT 所属类别, COUNT(所属类别) FROM DN05490062_CSX GROUP BY 所属类别 "
    cur.execute(sql3)
    for line in cur.fetchall():
        if line[0] == 'P':
            C_P = line[1]
        elif line[0] == 'L':
            C_L = line[1]

    sql4 = "SELECT 所属类别, COUNT(所属类别) FROM DN05490062_DSX GROUP BY 所属类别 "
    cur.execute(sql4)
    for line in cur.fetchall():
        if line[0] == 'P':
            D_P = line[1]
        elif line[0] == 'L':
            D_L = line[1]

    sql4 = "SELECT 所属类别, COUNT(所属类别) FROM DN05490062_LSX GROUP BY 所属类别 "
    cur.execute(sql4)
    for line in cur.fetchall():
        if line[0] == 'P':
            L_P = line[1]
        elif line[0] == 'L':
            L_L = line[1]

    return A_P, A_L, B_P, B_L, C_P, C_L, D_P, D_L, L_P, L_L


def get_data_pie():
    con = sqlite3.connect("DN05490062.db")  # 连接桥
    # print("Open database successfully")  # 打开成功
    cur = con.cursor()
    P = 0
    L = 0

    sql1 = "SELECT 所属类别, COUNT(所属类别) FROM DN05490062_ASX GROUP BY 所属类别 "
    cur.execute(sql1)
    for line in cur.fetchall():
        if line[0] == 'P':
            P += line[1]
        elif line[0] == 'L':
            L += line[1]

    sql2 = "SELECT 所属类别, COUNT(所属类别) FROM DN05490062_BSX GROUP BY 所属类别 "
    cur.execute(sql2)
    for line in cur.fetchall():
        if line[0] == 'P':
            P += line[1]
        elif line[0] == 'L':
            L += line[1]

    sql3 = "SELECT 所属类别, COUNT(所属类别) FROM DN05490062_CSX GROUP BY 所属类别 "
    cur.execute(sql3)
    for line in cur.fetchall():
        if line[0] == 'P':
            P += line[1]
        elif line[0] == 'L':
            L += line[1]

    sql4 = "SELECT 所属类别, COUNT(所属类别) FROM DN05490062_DSX GROUP BY 所属类别 "
    cur.execute(sql4)
    for line in cur.fetchall():
        if line[0] == 'P':
            P += line[1]
        elif line[0] == 'L':
            L += line[1]

    sql4 = "SELECT 所属类别, COUNT(所属类别) FROM DN05490062_LSX GROUP BY 所属类别 "
    cur.execute(sql4)
    for line in cur.fetchall():
        if line[0] == 'P':
            P += line[1]
        elif line[0] == 'L':
            L += line[1]

    return L, P


def get_data_sheet(sheet):
    con = sqlite3.connect("DN05490062.db")  # 连接桥
    # print("Open database successfully")  # 打开成功
    cur = con.cursor()
    pointList = []

    sql = f"SELECT a.AY, a.ZX, a.ZY, b.名称 FROM DN05490062_DZB a LEFT JOIN DN05490062_DSX b ON a.leibie = b.'所属类别' WHERE a.leibie = 'P'"
    cur.execute(sql)
    for line in cur.fetchall():
        if line[0] != None and line[1] != None and line[2] != None and line[3] != None:
            pointList.append({"x": line[0], "y": line[1], "z": line[2], "label": line[3]})
    result = random.sample(pointList, 50)
    return result


def predict(R0, B0, b, a, mode):
    print("——————————————————————————————————————————————")
    print("战斗过程预测结果为：")
    if mode == "SquareLaw":
        R0_square = R0 ** 2                     # 红方兵力的平方
        B0_square = B0 ** 2                     # 蓝方兵力的平方
        if R0_square * b > B0_square * a:       # 根据平方律的胜负条件做比较
            print("红方将【取得胜利】！")
            return "红方将【取得胜利】！"
        else:
            print("蓝方将【取得胜利】！")
            return "蓝方将【取得胜利】！"
    elif mode == "LinearLaw":
        if R0 * b > B0 * a:
            print("红方将【取得胜利】！")
            return "红方将【取得胜利】！"
        else:
            print("蓝方将【取得胜利】！")
            return "蓝方将【取得胜利】！"


def finalTroops(r, b):
    print("红方剩余兵力为【", r, "】")
    print("蓝方剩余兵力为【", b, "】")
    return r, b


def SquareLaw(R, B, b_s, a_s, t):
    R.append(R[t] - a_s * B[t])
    B.append(B[t] - b_s * R[t])
    return R, B


def LinearLaw(R, B, b_l, a_l, t):
    R.append(R[t] - a_l * B[t] * R[t])
    B.append(B[t] - b_l * B[t] * R[t])
    return R, B


def MoLanMdl(R, B, b_s, a_s, b_l, a_l, f_r, s_r, f_b, s_b, e_r, e_b, t):
    rValue = R[t] - (1-f_r)*s_b*b_s*B[t]*e_b - (1-(1-f_r)*s_b)*b_l*B[t]*R[t]*e_b
    bValue = B[t] - (1-f_b)*s_r*a_s*R[t]*e_r - (1-(1-f_b)*s_r)*a_l*B[t]*R[t]*e_r
    R.append(rValue)
    B.append(bValue)
    return R, B


def do_predict(R0, B0, b_s, a_s, b_l, a_l, f_r, f_b, s_r, s_b, epsilon_r, epsilon_b, mode):
    result = ""
    R = [R0, ]  # 用于记录红方兵力变化的列表
    B = [B0, ]  # 用于记录蓝方病理变化的列表

    T = 100  # 仿真总步长
    dt = 1  # 时间间隔
    if mode == "SquareLaw":  # 采用平方律的战斗过程
        # 预测战斗进程
        result = predict(R0, B0, b_s, a_s, mode)
        for t in np.arange(0, T, dt):
            SquareLaw(R, B, b_s, a_s, t)
            if R[-1] < 1e-6 or B[-1] < 1e-6:
                break
    elif mode == "LinearLaw":  # 采用线性律的战斗过程
        result = predict(R0, B0, b_l, a_l, mode)
        for t in np.arange(0, T, dt):
            LinearLaw(R, B, b_l, a_l, t)
            if R[-1] < 1e-6 or B[-1] < 1e-6:
                break
    elif mode == "ModernizedLanchesterModel":
        # 初始化参数
        for t in np.arange(0, T, dt):
            MoLanMdl(R, B, b_s, a_s, b_l, a_l, f_r, s_r, f_b, s_b, epsilon_r, epsilon_b, t)
            if R[-1] < 1e-6 or B[-1] < 1e-6:
                break
        print("——————————————————————————————————————————————")
        print("战斗过程预测结果为：")
        if R[-1] > B[-1]:
            print("红方将【取得胜利】！")
            result = "红方将【取得胜利】！"
        else:
            print("蓝方将【取得胜利】！")
            result = "蓝方将【取得胜利】！"
    print("——————————————————————————————————————————————")
    r, b = finalTroops(R[-1], B[-1])  # 打印红、蓝双方最终剩余兵力
    print("——————————————————————————————————————————————")
    return {
        # 红方剩余兵力
        "r": r,
        # 蓝方剩余兵力
        "b": b,
        # 预测结果
        "result": result,
    }

def draw_bingli_map():
    pointList = []


    con = sqlite3.connect("DN05490062.db")  # 连接桥
    # print("Open database successfully")  # 打开成功
    cur = con.cursor()
    sql1 = "SELECT fzb.AY as x,fzb.ZX as y FROM DN05490062_FZB fzb LEFT JOIN DN05490062_FSX fsx ON fzb.AX = fsx.要素编号"
    cur.execute(sql1)

    for line in cur.fetchall():
        if line[0] != None and line[1] != None:
            pointList.append([float(line[0]), float(line[1])])
    cur.close()
    con.commit()
    con.close()

    pointList = random.sample(pointList, 25)
    print(pointList)

    data = np.array(pointList)
    # data = dict(np.random.choice(data, 50))
    a, b = dichotomyKMeans(data, 2)

    start_coords = (2192935.10, 19472810.74)
    tmp_x, tmp_y = CGCS2WSG(start_coords[0], start_coords[1])
    X = tmp_x[1] + tmp_x[2] / 60 + tmp_x[3] / 3600
    Y = tmp_y[1] + tmp_y[2] / 60 + tmp_x[3] / 3600
    folium_map = drawMapCenter([X, Y])

    for i in range(2):
        pts = data[np.nonzero(b[:, 0].A == i)[0], :]
        colors = ['blue', 'red']
        Color = colors[i % len(colors)]

        for j in range(len(np.matrix(pts[:, 0]).A[0])):

            x = np.matrix(pts[j, 0]).A[0] / 1000 + 2192935.10
            y = np.matrix(pts[j, 1]).A[0] / 1000 + 19472810.74
            tmp_x, tmp_y = CGCS2WSG(x, y)
            X = tmp_x[1] + tmp_x[2] / 60 + tmp_x[3] / 3600
            Y = tmp_y[1] + tmp_y[2] / 60 + tmp_y[3] / 3600
            xx, yy = bd_decrypt(X, Y)

            folium.Marker(
                [xx, yy],
                icon=folium.Icon(color=Color)
                        ).add_to(folium_map)
        # ax.scatter(np.matrix(pts[:, 0]).A[0], np.matrix(pts[:, 1]).A[0], marker=Marker, s=90, color=Color, alpha=0.2)

    folium_map.save("templates/fzjc.html")
    replaceJsRef("templates/fzjc.html")



# 本函数的根本作用，是将folium所生成的html文件中的相关js/css引用链接，替换为本地的js/css路径。所使用的路径为相对路径，所以在打开html文件的时候，需要将html文件与src文件夹放置在同一个路径下
def replaceJsRef(fileFullName):
    replaceContents = [['''<script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>''',
                        '''<script src="{% static 'src/jQuery/jquery-2.0.0.js' %}"></script> '''],
                       ['''<script src="https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.js"></script>''',
                        '''<script src="{% static 'src/leaflet/leaflet.js' %}"></script>'''],
                       ['''<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>''',
                        '''<script src="{% static 'src/bootstrap-3.3.7/js/bootstrap.min.js' %}"></script>'''],
                       ['''<script src="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js"></script>''',
                        '''<script src="{% static 'src/Leaflet.awesome-markers-2.0/dist/leaflet.awesome-markers.js' %}"></script>'''],
                       ['''<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="{% static 'src/leaflet/leaflet.css' %}"/>'''],
                       ['''<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="{% static 'src/bootstrap-3.3.7/css/bootstrap.min.css' %}"/>'''],
                       ['''<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="{% static 'src/bootstrap-3.3.7/css/bootstrap-theme.min.css' %}"/>'''],
                       ['''<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="{% static 'src/font-awesome-4.7.0/css/font-awesome.min.css' %}"/>'''],
                       ['''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="{% static 'src/Leaflet.awesome-markers-2.0/dist/leaflet.awesome-markers.css' %}"/>'''],
                       ['''<link rel="stylesheet" href="https://rawcdn.githack.com/python-visualization/folium/master/folium/templates/leaflet.awesome.rotate.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="{% static 'src/leaflet.awesome.rotate/leaflet.awesome.rotate.css' %}"/>'''],
                       ['''<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/leaflet.markercluster.js"></script>''',
                        '''<script src="{% static 'src/leaflet.markercluster/dist/leaflet.markercluster.js' %}"></script>'''],
                       ['''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="{% static 'src/leaflet.markercluster/dist/MarkerCluster.css' %}"/>'''],
                       ['''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.1.0/MarkerCluster.Default.css"/>''',
                        '''<link rel="stylesheet" type="text/css" href="{% static 'src/leaflet.markercluster/dist/MarkerCluster.Default.css' %}"/>'''],
                       ['''<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-dvf/0.3.0/leaflet-dvf.markers.min.js"></script>''',
                        '''<script src="{% static 'src/leaflet-dvf/leaflet-dvf.markers.min.js' %}"></script>''']
                       ]

    with open(fileFullName, "r", encoding="utf-8") as f1, open("%s.bak" % fileFullName, "w", encoding="utf-8") as f2:
        for line in f1:
            for itm in replaceContents:
                if "<head>" in line:
                    line = line.replace("<head>", "<head>\n{% load static %}")

                if itm[0] in line:
                    line = line.replace(itm[0], itm[1])
                    replaceContents.remove(itm)
            f2.write(line)
    os.remove(fileFullName)
    os.rename("%s.bak" % fileFullName, fileFullName)




