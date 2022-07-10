# coding:utf-8
# Create your views here.
import random

from django.shortcuts import render, redirect,HttpResponse
from django.shortcuts import render
# Create your views here.
from folium.plugins import HeatMap

from KG import models
from django.conf import settings
import os
import json
import io
from django.http import JsonResponse
import sys
from django.shortcuts import render, HttpResponse, redirect
import sqlite3
from shapely import geometry
import folium
import math
import numpy as np
import pandas as pd
import KG.main as m
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


# 主界面
def home(request):
    if request.method == 'GET':
        # 处理绘制home界面的图谱所需数据，转成d3.js所需的格式
        # 设置绘制home页面的图谱时获取数据的文件路径，并在文件内写入相应内容
        dir1 = os.path.join(settings.MEDIA_ROOT + os.sep + 'json' + os.sep + 'pro_citys1.json')
        dir2 = os.path.join(settings.MEDIA_ROOT + os.sep + 'json' + os.sep + 'linkchina1.json')
        jsondata1 = Table1Json()
        f = open(dir1, 'w+', encoding='utf-8')
        f.write(jsondata1)
        f.close()

        jsondata2 = Table2Json()
        f = open(dir2, 'w+', encoding='utf-8')
        f.write(jsondata2)
        f.close()

        # 返回home界面
        return render(request, 'select.html')


# add_stu界面
def main(request):

    if request.method == 'GET':
        # json_reponse = setele2()
        con = sqlite3.connect('data.db')  # 连接桥

        cur = con.cursor()
        sql = 'drop table if exists DN05490062_RZB'
        cur.execute(sql)
        cur.close()
        con.commit()
        con.close()

        return render(request, 'add_stu.html')

    return HttpResponse("数据载入完毕")


# 处理各点的属性 转为json文件
def Table3Json():
    try:
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        doc = 'DN05490062'

        sql = "select * from classD"
        cur.execute(sql)
        result = cur.fetchall()
        con.commit()
        cur.close()
        con.close()
        jsonData = []
        interdata1 = {}
        data1 = {}
        interdata1['name'] = 'classD'
        temp = json.dumps(interdata1, ensure_ascii=False)

        data1['classD'] = temp

        temp2 = str(data1)
        jsonData.append(temp2)
        for row in result:
            interdata = dict()
            data = dict()
            # id,coding,name,typec,node,level,width,pwidth,blength,jklength,ton,kilo,
            # bigao,cmonth,wdeep,dizhi,minbj,maxzb,spec,zjzz,wgbzz "
            interdata['id'] = row[0]
            interdata['leixing'] = row[1]
            interdata['coding'] = row[2]
            interdata['name'] = row[3]
            interdata['typec'] = row[4]
            interdata['node'] = row[5]
            interdata['level'] = row[6]
            interdata['width'] = row[7]
            interdata['pwidth'] = row[8]
            interdata['blength'] = row[9]
            interdata['jklength'] = row[10]
            interdata['ton'] = row[11]
            interdata['kilo'] = row[12]
            interdata['bigao'] = row[13]
            interdata['cmonth'] = row[14]
            interdata['wdeep'] = row[15]
            interdata['dizhi'] = row[16]
            interdata['minbj'] = row[17]
            interdata['maxzb'] = row[18]
            interdata['spec'] = row[19]
            interdata['zjzz'] = row[20]
            interdata['wgbzz'] = row[21]
            temp = json.dumps(interdata, ensure_ascii=False)
            data[row[3]] = temp
            temp2 = str(data)
            jsonData.append(temp2)
            # print(temp2)
            # for i in range(0,len(temp2)):
            # if temp2[i] == "i":
            # jsonData.append(temp2[0:i+1] + temp2[i+3:len(temp2)-2])
            # break
            # print(jsonData)

        jsondatar = json.dumps(jsonData, ensure_ascii=False)
        jsondatar = jsondatar.replace('\\', '')
        jsondatar = jsondatar.replace('}"', '}')
        jsondatar = jsondatar.replace('"{', '{')
        jsondatar = jsondatar.replace("{'", "'")
        # jsondatar = jsondatar.replace()
        jsondatar = jsondatar[1:len(jsondatar) - 1]
        jsondatar = '{' + jsondatar + '}'
        jsondatar = jsondatar.replace("'", '"')
        jsondatar = jsondatar.replace('"{', '{')
        jsondatar = jsondatar.replace('}"}', '}')
        return jsondatar

    except Exception as e:
        print('db connect fail ', e)


# 处理circle节点的属性设置以及连线关系 json文件
def Table4Json():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    sql = 'select * from classD'
    cur.execute(sql)
    res = cur.fetchall()
    node = []
    link = []
    data = {}
    for i in res:
        inter = dict()
        links = dict()
        inter['name'] = str(i[0]) + i[3]
        inter['belong'] = 'D'
        inter['leixing'] = i[1]
        inter['group'] = 4
        inter['size'] = 8
        inter['distance'] = 50
        links['source'] = 'classD'
        links['target'] = str(i[0]) + i[3]
        links['value'] = 20
        temp = json.dumps(inter, ensure_ascii=False)
        temp1 = json.dumps(links, ensure_ascii=False)
        node.append(temp)
        link.append(temp1)

    leixing = dict()
    leixing['name'] = 'classD'
    leixing['belong'] = 'D'
    leixing['group'] = 4
    leixing['size'] = 10
    leixing = json.dumps(leixing, ensure_ascii=False)
    node.append(leixing)
    data['nodes'] = node
    data['links'] = link
    datar = json.dumps(data, ensure_ascii=False)
    datar = datar.replace('\\', '')
    datar = datar.replace('"{', '{')
    datar = datar.replace('}"', '}')
    # print(datar)
    return datar


# 根据add_stu界面的左侧下拉框动态改变图谱内容
# def classfiy(request):
#     if request.method == 'GET':
#         # 获取所选的类别
#         classe = request.GET.get("classes")
#         classe = classe.split(",")
#         print(classe)
#         classes = []
#         # 获取所选内容的所属类别
#         # print(classe)
#         # print(type(classe))
#         # 判断不为空
#         if classe[0] != '':
#             for i in classe:
#                 i = str(i)
#                 i = i[0]
#                 classes.append(i)
#         if len(classes) > 1:
#             classes.append('document')
#         # 找到指定class的json数据并重新拼接成新json文件
#         result = []
#         selectnode = []
#         result1 = []
#         dict = {}
#         p = os.path.join(settings.MEDIA_ROOT + os.sep + 'json' + os.sep + 'linkchina3.json')
#         p1 = os.path.join(settings.MEDIA_ROOT + os.sep + 'json' + os.sep + 'dataupdate.json')
#         if os.path.exists(p):
#             # python版本判断,不写也没啥，反正用的是3.6
#             if sys.version_info.major > 2:
#                 f = open(p, 'r', encoding='utf-8')
#             else:
#                 f = open(p, 'r')
#
#             dict_data = json.loads(f.read())
#             # print(dict_data)
#             # 数据根据所选类型重新拼接
#
#             for i in dict_data['nodes']:
#                 if i['belong'] in classes:
#                     result.append(i)
#                     selectnode.append(i['name'])
#             dict["nodes"] = result
#             # dict['links'] = dict_data['links']
#             # dict['links'] = [{"source": "中国", "target": "黑龙江", "value": 6}]
#
#             # 处理什么都不选的情况
#             if len(classes) < 1:
#                 dict['links'] = result1
#             else:
#                 for line in dict_data['links']:
#                     if line['source'] in selectnode:
#                         if line['target'] in selectnode:
#                             result1.append(line)
#                 dict['links'] = result1
#             print(dict)
#             dicts = json.dumps(dict, ensure_ascii=False)
#             f = open(p1, 'w+', encoding='utf-8')
#             f.write(dicts)
#             f.close()
#             # with open(p1, "w") as f:
#             # json.dump(dict, f ,ensure_ascii=False)
#             return HttpResponse(str(p1))

def classfiy(request):

    if request.method == 'GET':
        # 获取所选的类别
        classe = request.GET.get("classes")
        # classe = classe.split(",")
        parent = request.GET.get("parent")
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        aa = str(parent + '_' + classe[0] + 'SX')
        print(aa)
        s = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name = " + "'" + aa + "'"
        print(s)
        cur = con.cursor()
        cur.execute(s)
        a = cur.fetchall()
        print(a)
        if int(a[0][0]) == 1:
            # print(classe)
            # print(parent)
            p = os.path.join(settings.MEDIA_ROOT + os.sep + 'json' + os.sep + 'pro_citys3.json')
            p1 = os.path.join(settings.MEDIA_ROOT + os.sep + 'json' + os.sep + 'dataupdate.json')
            # classe = str(classe)
            jsondata = TableJsonUpdate1(parent, classe[0])
            f = open(p, 'w+', encoding='utf-8')
            f.write(jsondata)
            f.close()
            jsondata2 = TableJsonUpdate2(parent, classe[0])
            f = open(p1, 'w+', encoding='utf-8')
            f.write(jsondata2)
            f.close()
            return HttpResponse(str(p1))
        else:
            return HttpResponse(int(a[0][0]))


def connection():
    # 前端添加上传文件，后端用于生成表格
    # 建一个文件表，用于记录读过的表，下次读取时用于判断是否读过该文件，若重复可添加二次确认是否覆盖或者已读过的文件跳过不读
    # 文件表可同时用于动态生成表格页面中的第一个下拉框内容（已有文件）

    con = sqlite3.connect('data.db')      # 连接桥
    # s = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name = 'classD'"

    cur = con.cursor()
    # cur.execute(s)
    # sql = 'drop table if exists document'
    # cur.execute(sql)
    # 存放读过的文件名
    sql2 = "create table if not exists document(id INTEGER PRIMARY KEY,name varchar(50))"
    cur.execute(sql2)
    sql3 = 'select name from document'
    cur.execute(sql3)
    resu = cur.fetchall()
    # print(resu)
    sql4 = 'insert into document values (NULL ,"DN05490062")'
    if len(resu) == 0:
        cur.execute(sql4)
        cur.execute(sql3)
        re = cur.fetchall()
        # print(re)
    # if 'DN05490062' not in resu:
    else:
        count = 0
        for i, in resu:
            if i == 'DN05490062':
                break
            else:
                count += 1

        if count == len(resu):
            cur.execute(sql4)
            cur.execute(sql3)
            cur1 = cur.fetchall()
            # print(cur1)
    con.commit()
    cur.close()
    con.close()

    con = sqlite3.connect('data.db')
    cur = con.cursor()
    sql1 = "drop table if exists DN05490062_RSX"
    cur.execute(sql1)
    sql = "create table DN05490062_RSX( 要素编号 int(20),所属类别 varchar(20),编码 varchar(20) ,名称 varchar(20),类型 varchar(20),性质 varchar(20),编号 varchar(20),颜色 varchar(20),色彩方案 varchar(20),顶标颜色 varchar(20),发光状态 varchar(20),高度 varchar(20),灯光特性 varchar(20),信号组 varchar(20),信号周期 varchar(20),作用距离 varchar(20),灯光可视 varchar(20),方位 varchar(20),航行指向 varchar(20),光弧角度1 varchar(20),光弧角度2 varchar(20),雷达可视 varchar(20),水深值1 varchar(20),作用方式 varchar(20))"
    # sql = "create table DN05490062_NSX( 要素编号 int(20),所属类别 varchar(20),编码 varchar(20) ,名称 varchar(20),类型 varchar(20),高程 varchar(20),高度 varchar(20),胸径 varchar(20),宽度 varchar(20),图形特征 varchar(20),注记指针 varchar(20), 外挂表指针 varchar(20))"
    # if cur.fetchall()[0][0] == 0:
    cur.execute(sql)
    fil = open(r'C:\Users\Administrator.000\Desktop\DN05490062\DN05490062.RSX')  # 读文件
    re = fil.readline()  # 逐行读入
    re = fil.readline()
    re = fil.readline()
    re = fil.readline()
    re = fil.readline()
    re = fil.readline()
    ty = fil.read(6)
    # print("ty=", ty)
    Pleibie = 'P'
    Lleibie = 'L'
    Aleibie = "A"
    if ty.strip() == "P":
        PointNumber = fil.readline().strip()
        # print(int(PointNumber))
        if int(PointNumber) != 0:
         for id in range(int(PointNumber)):
            point = fil.readline().split()
            # print(int(len(point)))
            # print(point)

            pointId = point[0]
            coding = point[1]
            name = point[2]
            typec = point[3]
            node = point[4]
            level = point[5]
            width = point[6]
            pwidth = point[7]
            blength = point[8]
            jklength = point[9]
            ton = point[10]
    #        print(pointId, coding, name, typec, node, level, width, pwidth, blength, jklength, ton)
            kilo = point[11]
            bigao = point[12]
            cmonth = point[13]
            wdeep = point[14]
            dizhi = point[15]
            minbj = point[16]
            maxzb = point[17]
            spec = point[18]
            zjzz = point[19]
            wgbzz = point[20]
            add1 = point[21]
            add2 = point[22]
            #add3 = point[23]
            #print(pointId,coding,name,typec,node,level,width,pwidth,blength,jklength,ton,kilo,bigao,cmonth,wdeep,dizhi,minbj,maxzb,spec,zjzz,wgbzz)
         #   print(pointId, coding, name, typec, node, level, width, pwidth, blength, jklength)
            # cur.execute("insert into DN05490062_CSX(要素编号,所属类别,编码,名称,类型,编号,等级,宽度,铺宽,桥长,净空高,载重吨数,里程,比高,通行月份,水深,底质,最小曲率半径,最大纵坡,图形特征,注记指针,外挂表指针)values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(pointId,Pleibie,coding,name,typec,node,level,width,pwidth,blength,jklength,ton,kilo,bigao,cmonth,wdeep,dizhi,minbj,maxzb,spec,zjzz,wgbzz))
            cur.execute(
                "insert into DN05490062_RSX(要素编号,所属类别,编码,名称,类型,性质,编号,颜色,色彩方案,顶标颜色,发光状态,高度,灯光特性,信号组,信号周期,作用距离,灯光可视,方位,航行指向,光弧角度1,光弧角度2,雷达可视,水深值1,作用方式)values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (pointId, Pleibie, coding, name, typec, node, level, width, pwidth, blength, jklength, ton, kilo, bigao, cmonth, wdeep, dizhi, minbj, maxzb, spec, zjzz, wgbzz, add1, add2))
            ty = fil.read(6)
            # print(ty)
        else:
            ty = fil.read(6)

            # print(ty)
    if ty.strip() == 'L':
        # print(fil.readline())
        LineNumber = fil.readline().strip()
        # print(LineNumber)
        LineNumber = int(LineNumber)
        # print(type(LineNumber))
        for i in range(LineNumber):
            line = fil.readline().split()

            LineId = line[0]
            coding = line[1]
            name = line[2]
            typec = line[3]
            node = line[4]
            level = line[5]
            width = line[6]
            pwidth = line[7]
            blength = line[8]
            jklength = line[9]
            ton = line[10]
            kilo = line[11]
            bigao = line[12]
            cmonth = line[13]
            wdeep = line[14]
            dizhi = line[15]
            minbj = line[16]
            maxzb = line[17]
            spec = line[18]
            zjzz = line[19]
            wgbzz = line[20]
            add1 = line[21]
            add2 = line[22]
            # add3 = line[23]
            # for j in range(math.ceil(int(coding) / 5)):
            # lines = fil.readline().split()
            # print(LineId,coding,name,typec,node,level,width,pwidth,blength,jklength,ton,kilo,bigao,cmonth,wdeep,dizhi,minbj,maxzb,spec,zjzz,wgbzz)
            cur.execute(
                "insert into DN05490062_RSX(要素编号,所属类别,编码,名称,类型,性质,编号,颜色,色彩方案,顶标颜色,发光状态,高度,灯光特性,信号组,信号周期,作用距离,灯光可视,方位,航行指向,光弧角度1,光弧角度2,雷达可视,水深值1,作用方式)values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (LineId, Lleibie, coding, name, typec, node, level, width, pwidth, blength, jklength, ton, kilo, bigao,
                 cmonth, wdeep, dizhi, minbj, maxzb, spec, zjzz, wgbzz, add1, add2))
            ty = fil.read(6)
    if ty.strip() == 'A':
        AreaNumber = fil.readline().strip()

        for i in range(int(AreaNumber)):
            area = fil.readline().split()
            #area = fi1.readline().split()
            leibie = ty.strip()
            LineId = area[0]
            coding = area[1]
            name = area[2]
            typec = area[3]
            node = area[4]
            level = area[5]
            width = area[6]
            pwidth = area[7]
            blength = area[8]
            jklength = area[9]
            ton = area[10]
            kilo = area[11]
            bigao = area[12]
            cmonth = area[13]
            wdeep = area[14]
            dizhi = area[15]
            minbj = area[16]
            maxzb = area[17]
            spec = area[18]
            zjzz = area[19]
            wgbzz = area[20]
            add1 = area[21]
            add2 = area[22]
            # add3 = area[23]
            # for j in range(math.ceil(int(coding) / 5)):
            # lines = fil.readline().split()
            # print(leibie, LineId, coding, name, typec, node, level, width, pwidth, blength, jklength, ton)
            cur.execute(
                "insert into DN05490062_RSX(要素编号,所属类别,编码,名称,类型,性质,编号,颜色,色彩方案,顶标颜色,发光状态,高度,灯光特性,信号组,信号周期,作用距离,灯光可视,方位,航行指向,光弧角度1,光弧角度2,雷达可视,水深值1,作用方式)values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (LineId, Aleibie, coding, name, typec, node, level, width, pwidth, blength, jklength, ton, kilo, bigao,
                 cmonth, wdeep, dizhi, minbj, maxzb, spec, zjzz, wgbzz, add1, add2))
    cur.close()
    con.commit()
    con.close()


def connectDZB():

    con = sqlite3.connect('data.db')  # 连接桥

    cur = con.cursor()
    sql = 'drop table if exists DN05490062_NZB'
    cur.execute(sql)
    sql1 = "create table DN05490062_NZB(leibie varchar(20),AX varchar(20),AY varchar(20) ," \
           "ZX varchar(20),ZY varchar(20),LNUM varchar(20),LAX varchar(20),LAY varchar(20),ZNUM varchar(20)," \
           "ZAX varchar(20),ZAY varchar(20),ZZX varchar(20),ZZY varchar(20))"
    cur.execute(sql1)

    fil5 = open(r'C:\Users\Administrator.000\Desktop\2\DN05490062\DN05490062.NZB')  # 读文件
    re = fil5.readline()  # 逐行读入
    re = fil5.readline()
    re = fil5.readline()
    re = fil5.readline()
    re = fil5.readline()
    re = fil5.readline()
    ty5 = fil5.read(6)
    # print(ty5)
    if ty5.strip() == "P":
        PointNumber = fil5.readline().strip()
        # print(int(PointNumber))
        for id in range(int(PointNumber)):
            point5 = fil5.readline().split()
            # print(int(len(point)))
            # print(point3)
            leibie = ty5.strip()
            AX = point5[0]
            AY = point5[1]
            ZX = point5[2]
            ZY = point5[3]
            # print(leibie, AX, AY, ZX, ZY)
            cur.execute(
                "insert into DN05490062_NZB(leibie,AX,AY,ZX,ZY)"
                "values(?,?,?,?,?)",
                (ty5.strip(), AX, AY, ZX, ZY))
        ty5 = fil5.read(6)
    if ty5.strip() == 'L':
        listl = []
        LineNumber = fil5.readline().strip()
        leibie = ty5.strip()
    #    print(LineNumber)
        for i in range(int(LineNumber)):  # 从这里开始行位，点数
            line5 = fil5.readline().split()
            linenum = line5[0]  # 行位
            pointnum = line5[1]  # 点数，对数
    #        print(linenum, pointnum)
            if int(int(pointnum) * 2 % 10) == 0:
                n = int(int(pointnum) * 2 / 10)
            else:
                n = int(int(pointnum) * 2 / 10 + 1)
            # print(n)
            for i in range(n):
                fir = 0
                sec = 1
                re = fil5.readline()
                ll = re.split()
                # print(ll)
                ln = len(ll)
                # print(ln)
                for id in range(int(int(ln) / 2)):
                    # print(ty5.strip(), linenum, ll[fir], ll[sec])
                    LNUM = linenum
                    LAX = ll[fir]
                    LAY = ll[sec]
                    cur.execute("insert into DN05490062_NZB(leibie,LNUM,LAX,LAY)"
                                "values(?,?,?,?)",
                                (leibie, LNUM, LAX, LAY))
                    fir += 2
                    sec += 2
        ty5 = fil5.read(6)
    if ty5.strip() == 'A':
        listA = []
        AreaNumber = fil5.readline().strip()  # 第一行，A坐标有多少块
        leibie = ty5.strip()  # A标记
        # print(AreaNumber)
        for i in range(int(AreaNumber)):  # 从这里开始行位，点数
            area5 = fil5.readline().split()
            linenum = area5[0]  # 行位
            ZAX = area5[1]  # 界面横坐标
            ZAY = area5[2]  # 界面纵坐标
            JNUM = area5[3]  # 数量
            # print(linenum, ZAX, ZAY, JNUM)
            if JNUM == '0':
                continue
            else:
                if JNUM == '1':
                    pointnum = fil5.readline().split()
                    # print(pointnum)
                    if int(int(pointnum[0]) * 2 % 10) == 0:
                        n = int(int(pointnum[0]) * 2 / 10)
                    else:
                        n = int(int(pointnum[0]) * 2 / 10 + 1)
                    # print(n)
                    for i in range(n):
                        fir = 0
                        sec = 1
                        re = fil5.readline()
                        ll = re.split()
                        # print(ll)
                        ln = len(ll)
                        # print(ln)
                        for id in range(int(int(ln) / 2)):
                            # print(ty5.strip(), linenum, ll[fir], ll[sec])
                            ZNUM = linenum
                            ZZX = ll[fir]
                            ZZY = ll[sec]
                            cur.execute("insert into DN05490062_NZB(leibie,ZNUM,ZAX,ZAY, ZZX, ZZY)"
                                        "values(?,?,?,?,?,?)",
                                        (leibie, ZNUM, ZAX, ZAY, ZZX, ZZY))
                            fir += 2
                            sec += 2
                else:
                    Mnum = int(JNUM)
                    while (Mnum):
                        pointnum = fil5.readline().split()
                        # print(pointnum)
                        if int(int(pointnum[0]) * 2 % 10) == 0:
                            n = int(int(pointnum[0]) * 2 / 10)
                        else:
                            n = int(int(pointnum[0]) * 2 / 10 + 1)
                        # print(n)
                        for i in range(n):
                            fir = 0
                            sec = 1
                            re = fil5.readline()
                            ll = re.split()
                            # print(ll)
                            ln = len(ll)
                            # print(ln)
                            for id in range(int(int(ln) / 2)):
                                # print(ty5.strip(), linenum, ll[fir], ll[sec])
                                ZNUM = linenum
                                ZZX = ll[fir]
                                ZZY = ll[sec]
                                cur.execute("insert into DN05490062_NZB(leibie,ZNUM,ZAX,ZAY, ZZX, ZZY)"
                                            "values(?,?,?,?,?,?)",
                                            (leibie, ZNUM, ZAX, ZAY, ZZX, ZZY))
                                fir += 2
                                sec += 2
                        Mnum = Mnum - 1
    cur.close()
    con.commit()
    con.close()


# 表格数据填充
def data(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": 201,
                "message": "method error"
            }
        )

    tdata = {}
    data = []
    # 接收所选表格的所属文件以及想要查看的图层属性
    doc = request.POST.get("doc", None)
    sx = request.POST.get("sx", None)
    # entity = request.POST.get("entity", None)
    # entity = str(entity)
    doc = str(doc)
    sx = str(sx)

    # 读取数据库对应表格数据
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    # 计算数据总数 用于分页（若不分页 对于较多数据的表格会导致页面严重卡顿
    count = 'select count(*) from ' + doc + '_' + sx
    cur.execute(count)
    count = cur.fetchall()[0][0]
    # sql = 'select count(*) from ' + entity
    sql = 'select * from ' + doc + '_' + sx
    cur.execute(sql)
    col_name_list = [tuple[0] for tuple in cur.description]
    result = cur.fetchall()
    for i in range(len(result)):
        temp = {}
        for j in range(len(col_name_list)):
            temp[col_name_list[j]] = result[i][j]
        data.append(temp)

    # for i in result:

    #    temp = {}
    #    # 读取到列名及数据后用循环代替
    #    # id, coding, name, typec, node, level, width, pwidth, blength,
    #    jklength, ton, kilo, bigao, cmonth, wdeep, dizhi, minbj, maxzb, spec, zjzz, wgbzz
    #    temp["id"] = i[0]
    #    temp["coding"] = i[1]
    #    temp["name"] = i[2]
    #    temp["typec"] = i[3]
    #    temp["node"] = i[4]
    #    temp["level"] = i[5]
    #    temp["width"] = i[6]
    #    temp["pwidth"] = i[7]
    #    temp["blength"] = i[8]
    #    temp["jklength"] = i[9]
    #    temp["ton"] = i[10]
    #    temp["kilo"] = i[11]
    #    temp["bigao"] = i[12]
    #    temp["cmoth"] = i[13]
    #    temp["wdeep"] = i[14]
    #    temp["dizhi"] = i[15]
    #    temp["minbj"] = i[16]
    #    temp["maxzb"] = i[17]
    #    temp["spec"] = i[18]
    #    temp["zjzz"] = i[19]
    #    temp["wgbzz"] = i[20]
    #   data.append(temp)

    # 制作符合格式的数据
    tdata["code"] =0
    tdata["msg"] = ""
    tdata["count"] = count
    tdata["data"] = data
    tdata = json.dumps(tdata, ensure_ascii=False)
    p1 = os.path.join(settings.MEDIA_ROOT + os.sep + 'getdata' + os.sep + 't')
    f = open(p1, 'w+', encoding='utf-8')
    f.write(tdata)
    f.close()
    # return render(request, "database.html")
    return HttpResponse("success")


# 返回表格页面
def datapage(request):
    if request.method == 'GET':
        return render(request, "database.html")
        # return render(request, 'tablea.html')


def tablecol(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": 201,
                "message": "method error"
            }
        )
    data = []
    doc = request.POST.get('doc', None)
    sx = request.POST.get('sx', None)
    doc = str(doc)
    sx = str(sx)

    # entity = request.POST.get('entity', None)
    # entity = str(entity)
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    # 判断是否存在想要获取的表，不存在则返回提示
    # 其他可供选择：不存在的表也进行创建，查找时返回空表，在该表有第一个数据时可供手动添加
    cur.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='" + doc + "_" + sx + "'")
    res = cur.fetchall()
    if res[0][0] == 1:
        sql = 'select * from ' + doc + '_' + sx
        cur.execute(sql)
        col_name_list = [tuple[0] for tuple in cur.description]
        for i in range(len(col_name_list)):
            a = dict()
            a["field"] = col_name_list[i]
            a["title"] = col_name_list[i]
            a["width"] = 80
            data.append(a)
        b = dict()
        b['fixed'] = 'right'
        b['width'] = 178
        b['align'] = 'center'
        b['toolbar'] = '#barDemo'
        data.append(b)
        data[0]["fixed"] = 'left'
        b = json.dumps(data, ensure_ascii=False)
        # b = b.replace('"field":', "field:")
        # b = b.replace('"title":', "title:")
        # b = b.replace('"width":', "width:")
        # b = b.replace('"fixed":', "fixed:")
        return HttpResponse(b)
    else:
        a = dict()
        a["警告"] = "该表格无数据"
        a = json.dumps(a, ensure_ascii=False)
        return HttpResponse(a)


# 动态获取表格页面下拉框内值
def getdocumentname(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": 201,
                "message": "method error"
            }

         )
    data = []
    # entity = request.POST.get("entity", None)
    # entity = str(entity)
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    sql = 'select name from document'
    cur.execute(sql)
    result = cur.fetchall()
    # col_name_list = [tuple[0] for tuple in cur.description]
    j = 0
    for i in result:
        doc = dict()

        doc['ID'] = j
        doc['TAGNAME'] = i
        j += 1
        data.append(doc)
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


# 文件夹上传   暂未写
def upload(request):
    if request.method == 'POST':  # 获取对象
        obj = request.FILES.get('fafafa')
        # 上传文件的文件名
        # print(obj.name)

        return HttpResponse('OK')
    return render(request, 'select.html')


# 动态获取图谱界面左侧下拉框内值
# def setele(request):
#     if request.method != "POST":
#         return JsonResponse(
#          {
#             "status": 201,
#             "message": "method error"
#          }
#      )
#     data = []
#     con = sqlite3.connect('data.db')
#     cur = con.cursor()
#     sql = "select name from document"
#     cur.execute(sql)
#     result = cur.fetchall()
#     sql1 = 'select name from tuceng'
#     cur.execute(sql1)
#     classes = cur.fetchall()
#     classes1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
#     # [{title: '数据',id: 1,children: [{title: 'country',id: 5},{title: 'province',id: 6},{title: 'city',id: 7}]}]
#     for i in range(len(result)):
#         a = dict()
#         a['title'] = result[i]
#         a['id'] = i
#         a['spread'] = True  # 使左侧下拉树形组件默认为展开状态
#         children = []
#         for j in range(0, 18):
#             temp = dict()
#             temp['title'] = str(classes1[j]) + str(classes[j][0])
#             temp['id'] = (i + 10) * 18 + j
#             temp['spread'] = True
#             # temp['spread'] = 'true'
#             children.append(temp)
#         a['children'] = children
#         data.append(a)
#     datas = json.dumps(data, ensure_ascii=False)
#     return HttpResponse(datas)
# 动态获取图谱界面左侧下拉框内值


# 动态获取图谱界面左侧下拉框内值
def setele2():

    data = []
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    sql = "select name from document"
    cur.execute(sql)
    result = cur.fetchall()
    sql1 = 'select name from tuceng'
    cur.execute(sql1)
    classes = cur.fetchall()
    classes1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
    # [{title: '数据',id: 1,children: [{title: 'country',id: 5},{title: 'province',id: 6},{title: 'city',id: 7}]}]
    for i in range(len(result)):
        a = dict()
        a['title'] = result[i][0]
        # a['id'] = i
        # a['spread'] = True  # 使左侧下拉树形组件默认为展开状态

        children = []
        for j in range(0, 18):
            temp = dict()
            temp['title'] = str(classes1[j]) + str(classes[j][0])
            temp['id'] = (i + 10) * 18 + j
            # temp['spread'] = True
            # temp['parent'] = result[i]  # 添加父节点名称，方便传回查找
            # temp['spread'] = 'true'
            children.append(temp)
            a['children'].update(temp)
        # data.append(a)
    # datas = json.dumps(data, ensure_ascii=False)
    return a

def setele(request):
    if request.method != "POST":
        return JsonResponse(
         {
            "status": 201,
            "message": "method error"
         }
     )
    data = []
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    sql = "select name from document"
    cur.execute(sql)
    result = cur.fetchall()
    sql1 = 'select name from tuceng'
    cur.execute(sql1)
    classes = cur.fetchall()
    classes1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
    # [{title: '数据',id: 1,children: [{title: 'country',id: 5},{title: 'province',id: 6},{title: 'city',id: 7}]}]
    for i in range(len(result)):
        a = dict()
        a['title'] = result[i]
        a['id'] = i
        a['spread'] = True  # 使左侧下拉树形组件默认为展开状态

        children = []
        for j in range(0, 18):
            temp = dict()
            temp['title'] = str(classes1[j]) + str(classes[j][0])
            temp['id'] = (i + 10) * 18 + j
            temp['spread'] = True
            temp['parent'] = result[i]  # 添加父节点名称，方便传回查找
            # temp['spread'] = 'true'
            children.append(temp)
        a['children'] = children
        data.append(a)
    datas = json.dumps(data, ensure_ascii=False)
    return HttpResponse(datas)


# 判断某点是否在矩形内部
def if_inPoly(polygon, Points):
    line = geometry.LineString(polygon)
    point = geometry.Point(Points)
    polygon = geometry.Polygon(line)
    return polygon.contains(point)
    # square = [(1, 5), (3, 3), (9, 9), (7, 11)]  # 多边形坐标
    # pt1 = (3, 3)  # 点坐标
    # pt2 = (3, 6.9)
    # print(if_inPoly(square, pt1))
    # print(if_inPoly(square, pt2))


def path_point(array, x_min, x_max, y_min, y_max, ver):
    pinnerpoint = []
    linnerpoint = []
    ainnerpoint = []
    for i in array:
        if i[0] == 'P':
            x, y = float(i[2]), float(i[3])
            if x > x_min and x < x_max and y > y_min and y < y_max:
                p = (x, y)
                if if_inPoly(ver, p):
                    pinnerpoint.append(i[1])
        elif i[0] == 'L':
            if i[5] not in linnerpoint:
                x, y = float(i[6]), float(i[7])
                if x > x_min and x < x_max and y > y_min and y < y_max:
                    p = (x, y)
                    if if_inPoly(ver, p):
                        linnerpoint.append(i[5])
        elif i[0] == 'A':
            if i[8] not in ainnerpoint:
                x, y = float(i[9]), float(i[10])
                if x > x_min and x < x_max and y > y_min and y < y_max:
                    p = (x, y)
                    if if_inPoly(ver, p):
                        ainnerpoint.append(i[8])
            elif i[8] not in ainnerpoint:
                x, y = float(i[11]), float(i(12))
                if x > x_min and x < x_max and y > y_min and y < y_max:
                    p = (x, y)
                    if if_inPoly(ver, p):
                        ainnerpoint.append(i[8])
    return pinnerpoint, linnerpoint, ainnerpoint


def path_final(array, p, l, a):
    final_result = list()
    num = 0
    for i in array:
        if i[1] == 'P':
            if str(i[0]) in p:
                temp = list()
                temp.append((i[0], i[1], i[2], i[3]))
                final_result.append(temp)
                num += 1
        elif str(i[1]) == 'L':
            if str(i[0]) in l:
                temp = list()
                temp.append((i[0], i[1], i[2], i[3]))
                final_result.append(temp)
                num += 1
        elif str(i[1]) == 'A':
            if str(i[0]) in a:
                temp = list()
                temp.append((i[0], i[1], i[2], i[3]))
                final_result.append(temp)
                num += 1
    return final_result, num


# 路径规划
# # # # # #
# 居民地、水体/陆地、植被、地貌、国界。
def path(request):
    if request.method != "POST":
        return JsonResponse(
         {
            "status": 201,
            "message": "method error"
         })

    name = request.POST.get('name', None)   # 接受前端传递数据‘name’
    leixing = request.POST.get('leixing', None)     # ‘类型’
    cla = request.POST.get('class', None)       # 图层
    parent = request.POST.get('parent', None)      # 所属文件
    name = name.split(',')  # 转为数组
    leixing = leixing.split(',')
    # cla = cla.split(',') + for循环 处理不同类型的两个点
    cla = str(cla)  # 数据库查找需转为str
    # cla  = cla/split(',')
    parent = str(parent)

    con = sqlite3.connect('data.db')
    cur = con.cursor()
    # 存入对应的id值
    id = []

    # re用来存储所选取的两个点对应的坐标数组
    re = []

    # 存入前端所选择点的id
    # 还需所选点的类型（P、L、A），未存入表中
    sql = 'select 要素编号,名称 from ' + parent + '_' + cla + 'SX'
    # sql = 'select id,name from class' + cla     # 从属性 表 中查找
    cur.execute(sql)
    r = cur.fetchall()      # 转成数组格式
    for i in name:
        for j in r:
            if str(j[0])+j[1] == i:
                id.append(j[0])     # 传来 ID
    # 寻找对应坐标点  table
    for i in range(0, 2):
        # 分别判断是  点线面
        if leixing[i] == 'P':
            sql = 'select AY,ZX from ' + parent + '_' + cla + 'ZB where leibie="P" and AX=' + str(id[i])
            # sql = 'select AY,ZX from DN05490062_DZB where leibie="P" and AX=' + str(id[i])
            cur.execute(sql)
            result = cur.fetchall()
            re.append(result)
            # print(result)
        elif leixing[i] == 'L':
            sql = 'select LAX,LAY from ' + parent + '_' + cla + 'ZB where leibie="L" and LNUM=' + str(id[i])
            # sql = 'select LAX,LAY from DN05490062_DZB where leibie="L" and LNUM=' + str(id[i])
            cur.execute(sql)
            result = cur.fetchall()
            re.append(result)
            # print(result)
        elif leixing[i] == 'A':
            sql = 'select ZZX,ZZY from ' + parent + '_' + cla + 'ZB where leibie="A" and ZNUM=' + str(id[i])
            # sql = 'select ZZX,ZZY from DN05490062_DZB where leibie="A" and ZNUM=' + str(id[i])
            cur.execute(sql)
            result = cur.fetchall()
            re.append(result)   # re是点线面中坐标
            # re存得两点分别对应的坐标数组
    xsum = 0.0
    ysum = 0.0
    coor = []
    # 设定代表点  sum/len
    for i in re:
        # print(i)
        for j in range(0, len(i)):
            # print(float(i[j][0]))

            xsum += float(i[j][0])
            ysum += float(i[j][1])
        # print(len(i))
        x = xsum / len(i)
        y = ysum / len(i)
        # coor.append((x, y))
        coor.append([x, y])
        # coor内包含分别代表两地的坐标点
        # 以两点之间的直线距离为长，长度的1/3为宽做矩形，两点分别位于两条宽的中点处
        # 根据两点计算所做矩形框的四个顶点坐标
    origin = coor[0]
    destination = coor[1]
    routes, routes2, routes3, routes4 = m.findWay2(origin, destination)

    start_x = routes[0][0][0]
    start_y = routes[0][0][1]
    end_x = routes[-1][-1][0]
    end_y = routes[-1][-1][1]
    folium_map = m.drawMapCenter([start_x, start_y])
    folium.Marker([start_x, start_y], tooltip="起点", popup="<b>起\t点</b>").add_to(folium_map)
    folium.Marker([end_x, end_y], tooltip="终点", popup="<b>终\t点</b>").add_to(folium_map)
    for route in routes:
        folium_map = m.drawMapLines(route, 'blue', folium_map)
        # folium_map = m.drawMapLines(route, folium_map)

    for route in routes2:
        folium_map = m.drawMapLines(route, 'red', folium_map)
        # folium_map = m.drawMapLines(route, folium_map)

    for route in routes3:
        folium_map = m.drawMapLines(route, 'yellow', folium_map)
        # folium_map = m.drawMapLines(route, folium_map)

    for route in routes4:
        folium_map = m.drawMapLines(route, 'green', folium_map)
        # folium_map = m.drawMapLines(route, folium_map)

    folium_map.save("templates/tmp.html")
    m.replaceJsRef("templates/tmp.html")
    return HttpResponse(routes)


def find_road_2(request):
    if request.method == "GET":
        return render(request, "path_begin_end.html")
    elif request.method == "POST":
        typeOfWay = request.POST.get('choice')

        start_du_j = request.POST.get('start_du_j')
        start_fen_j = request.POST.get('start_fen_j')
        start_miao_j = request.POST.get('start_miao_j')
        start_point_j = int(start_du_j) + int(start_fen_j) / 60 + int(start_miao_j) / 3600

        start_du_w = request.POST.get('start_du_w')
        start_fen_w = request.POST.get('start_fen_w')
        start_miao_w = request.POST.get('start_miao_w')
        start_point_w = int(start_du_w) + int(start_fen_w) / 60 + int(start_miao_w) / 3600

        end_du_j = request.POST.get('end_du_j')
        end_fen_j = request.POST.get('end_fen_j')
        end_miao_j = request.POST.get('end_miao_j')
        end_point_j = int(end_du_j) + int(end_fen_j) / 60 + int(end_miao_j) / 3600

        end_du_w = request.POST.get('end_du_w')
        end_fen_w = request.POST.get('end_fen_w')
        end_miao_w = request.POST.get('end_miao_w')
        end_point_w = int(end_du_w) + int(end_fen_w) / 60 + int(end_miao_w) / 3600

        routes = m.findWay3([start_point_j, start_point_w], [end_point_j, end_point_w], typeOfWay)
        if routes == False:
            return render(request, 'path_begin_end_error.html')
        start_x = routes[0][0][0]
        start_y = routes[0][0][1]
        end_x = routes[-1][-1][0]
        end_y = routes[-1][-1][1]
        folium_map = m.drawMapCenter([start_x, start_y])
        folium.Marker([start_x, start_y], tooltip="起点", popup="<b>起\t点</b>").add_to(folium_map)
        folium.Marker([end_x, end_y], tooltip="终点", popup="<b>终\t点</b>").add_to(folium_map)
        for route in routes:
            folium_map = m.drawMapLines(route, 'blue', folium_map)
            # folium_map = m.drawMapLines(route, folium_map)
        folium_map.save("templates/tmp3.html")
        m.replaceJsRef("templates/tmp3.html")
        return render(request, 'tmp3.html')



''' 
    # 直接绘图尝试
    # 计算两点间的直线距离作为长,1/3为宽
    dx = 0.0
    dy = 0.0
    for point in coor:
        dx = point[0] - dx
        dy = point[1] - dy
    length = math.sqrt(pow(dx, 2) + pow(dy, 2))
    width = length / 3

    # 计算顶点
    # 可直接确定四个点的情况
    vertex = []
    # 所选两点横坐标相同
    if coor[0][0] == coor[1][0]:
        vertex.append((float(coor[0][0]) - width / 2, coor[0][1]))
        vertex.append((float(coor[0][0]) + width / 2, coor[0][1]))
        vertex.append((float(coor[1][0]) + width / 2, coor[1][1]))
        vertex.append((float(coor[1][0]) - width / 2, coor[1][1]))

    # 所选两点纵坐标相同
    elif coor[0][1] == coor[1][1]:
        vertex.append((coor[0][0], float(coor[0][1]) + width / 2))
        vertex.append((coor[0][0], float(coor[0][1]) - width / 2))
        vertex.append((coor[1][0], float(coor[1][1]) - width / 2))
        vertex.append((coor[1][0], float(coor[1][1]) + width / 2))
    else:
        # 斜边的情况
        # 两点间无特殊位置关系，需要根据两点斜率及三角运算计算四个顶点的坐标
        k = dy / dx
        if k > 0:
            angle = math.atan(k)
            temp = width / 2
            ddx = temp * math.sin(angle)
            ddy = temp * math.cos(angle)
            vertex.append((float(coor[0][0]) + ddx, float(coor[0][1]) - ddy))
            vertex.append((float(coor[0][0]) - ddx, float(coor[0][1]) + ddy))
            vertex.append((float(coor[1][0]) - ddx, float(coor[1][1]) + ddy))
            vertex.append((float(coor[1][0]) + ddx, float(coor[1][1]) - ddy))
        elif k < 0:
            k = abs(k)
            angle = math.atan(k)
            temp = width / 2
            ddx = temp * math.sin(angle)
            ddy = temp * math.cos(angle)
            vertex.append((float(coor[0][0]) - ddx, float(coor[0][1]) - ddy))
            vertex.append((float(coor[0][0]) + ddx, float(coor[0][1]) + ddy))
            vertex.append((float(coor[1][0]) + ddx, float(coor[1][1]) + ddy))
            vertex.append((float(coor[1][0]) - ddx, float(coor[1][1]) - ddy))

    # 找出该矩形框的x_min,x_max,y_min,y_max，在做点在面内的判断时进行初步筛选
    x_min, x_max = vertex[0][0], vertex[0][0]
    y_min, y_max = vertex[0][1], vertex[0][1]
    for i in range(1, len(vertex)):
        if vertex[i][0] < x_min:
            x_min = vertex[i][0]
        if vertex[i][0] > x_max:
            x_max = vertex[i][0]
        if vertex[i][1] < y_min:
            y_min = vertex[i][1]
        if vertex[i][1] > y_max:
            y_max = vertex[i][1]

    # 判断点是否在以vertex内四个点为顶点的矩形框内
    # if_inPoly(vertex,p): 为true则在内，false在外

    # 新增其他类型点的判断

    # 道路
    cur.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='DN05490062_DZB'")
    Dre = cur.fetchall()
    if Dre[0][0] == 1:
        sql = 'select * from DN05490062_DZB'
        cur.execute(sql)
        # 遍历坐标，判断是否满足条件
        result = cur.fetchall()
        dp, dl, da = path_point(result, x_min, x_max, y_min, y_max, vertex)
        # pinnerpoint = []
    # linnerpoint = []
    # ainnerpoint = []
    # for i in result:
    #     # 分PLA三种情况分别把对应id存入对应数组，以便回属性表查找对应点
    #     if i[0] == 'P':
    #         p = (float(i[2]), float(i[3]))
    #         if float(i[2]) > x_min and float(i[2]) < x_max and float(i[3]) > y_min and float(i[3]) < y_max:
    #             if if_inPoly(vertex, p):
    #                 pinnerpoint.append(i[1])
    #     elif i[0] == 'L':
    #         if i[5] not in linnerpoint:
    #             p = (float(i[6]), float(i[7]))
    #             if float(i[6]) > x_min and float(i[6]) < x_max and float(i[7]) > y_min and float(i[7]) < y_max:
    #                 if if_inPoly(vertex, p):
    #                     linnerpoint.append(i[5])
    #     elif i[0] == 'A':
    #         if i[8] not in ainnerpoint:
    #             p = (float(i[9]), float(i[10]))
    #             if float(i[9]) > x_min and float(i[9]) < x_max and float(i[10]) > y_min and float(i[10]) < y_max:
    #                 if if_inPoly(vertex, p):
    #                     ainnerpoint.append(i[8])
    #         if i[8] not in ainnerpoint:
    #             p = (float(i[11]), float(i[12]))
    #             if float(i[11]) > x_min and float(i[11]) < x_max and float(i[12]) > y_min and float(i[12]) < y_max:
    #                 if if_inPoly(vertex, p):
    #                     ainnerpoint.append(i[8])

    # 符合条件的三类点的id值
    # print(pinnerpoint)
    # print(linnerpoint)
    # print(ainnerpoint)
    # 在属性表寻找对应点的属性（可存id，name，级别，编码对应的类型）
        sql3 = 'select * from DN05490062_DSX'
        cur.execute(sql3)
        result_sx = cur.fetchall()
        Dfinal, dnum = path_final(result_sx, dp, dl, da)
    else:
        Dfinal = []
        dnum = 0

    # 植被
    cur.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='DN05490062_LZB'")
    Lre = cur.fetchall()
    if Lre[0][0] == 1:
        sql = 'select * from DN05490062_LZB'
        cur.execute(sql)
        result_L = cur.fetchall()
        lp, ll, la = path_point(result_L, x_min, x_max, y_min, y_max, vertex)
        cur.execute('select * from DN05490062_LSX')
        result_Lsx = cur.fetchall()
        Lfinal, lnum = path_final(result_Lsx, lp, ll, la)
    else:
        Lfinal = []
        lnum = 0

    # 居民地
    cur.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='DN05490062_CZB'")
    Cre = cur.fetchall()
    if Cre[0][0] == 1:
        sql = 'select * from DN05490062_CZB'
        cur.execute(sql)
        result_C = cur.fetchall()
        cp, cl, ca = path_point(result_C, x_min, x_max, y_min, y_max, vertex)
        cur.execute('select * from DN05490062_CSX')
        result_Csx = cur.fetchall()
        Cfinal, cnum = path_final(result_Csx, cp, cl, ca)
    else:
        Cfinal = []
        cnum = 0

    # 水域/陆地
    cur.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='DN05490062_FZB'")
    Fre = cur.fetchall()
    if Fre[0][0] == 1:
        sql = 'select * from DN05490062_FZB'
        cur.execute(sql)
        result_F = cur.fetchall()
        fp, fl, fa = path_point(result_F, x_min, x_max, y_min, y_max, vertex)
        cur.execute('select * from DN05490062_FSX')
        result_Fsx = cur.fetchall()
        Ffinal, fnum = path_final(result_Fsx, fp, fl, fa)
    else:
        Ffinal = []
        fnum = 0

    # 陆地地貌及土质
    cur.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='DN05490062_JZB'")
    Jre = cur.fetchall()
    if Jre[0][0] == 1:
        sql = 'select * from DN05490062_JZB'
        cur.execute(sql)
        result_J = cur.fetchall()
        jp, jl, ja = path_point(result_J, x_min, x_max, y_min, y_max, vertex)
        cur.execute('select * from DN05490062_JSX')
        result_Jsx = cur.fetchall()
        Jfinal, jnum = path_final(result_Jsx, jp, jl, ja)
    else:
        Jfinal = []
        jnum = 0

    # 境界及政区
    cur.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='DN05490062_KZB'")
    Kre = cur.fetchall()
    if Kre[0][0] == 1:
        sql = 'select * from DN05490062_KZB'
        cur.execute(sql)
        result_K = cur.fetchall()
        kp, kl, ka = path_point(result_K, x_min, x_max, y_min, y_max, vertex)
        cur.execute('select * from DN05490062_KSX')
        result_Ksx = cur.fetchall()
        Kfinal, knum = path_final(result_Ksx, kp, kl, ka)
    else:
        Kfinal = []
        knum = 0

    final = dict()
    data = list()
    # final["道路"] = Dfinal
    if len(Dfinal) > 0:
        for i in Dfinal:
            # print(i)
            Ddata = dict()
            Ddata["type"] = "陆地交通"
            # Ddata["de"] = i[0][1]
            if i[0][1] == 'P':
                Ddata["cnm"] = "点类"
            elif i[0][1] == 'L':
                Ddata["cnm"] = "线类"
            elif i[0][1] == "A":
                Ddata["cnm"] = "面类"
            Ddata["name"] = i[0][3]
            data.append(Ddata)
    # final["居民地"] = Cfinal
    if len(Cfinal) > 0:
        for i in Cfinal:
            Cdata = dict()
            Cdata["type"] = "居民地及附属设施"
            if i[0][1] == 'P':
                Cdata["cnm"] = "点类"
            elif i[0][1] == 'L':
                Cdata["cnm"] = "线类"
            elif i[0][1] == 'A':
                Cdata["cnm"] = "面类"
            Cdata["name"] = i[0][3]
            data.append(Cdata)
    # final["植被"] = Lfinal
    if len(Lfinal) > 0:
        for i in Lfinal:
            Ldata = dict()
            Ldata["type"] = "植被"
            if i[0][1] == "P":
                Ldata["cnm"] = "点类"
            elif i[0][1] == 'L':
                Ldata["cnm"] = "线类"
            elif i[0][1] == 'A':
                Ldata["cnm"] = "面类"
            Ldata["name"] = i[0][3]
            data.append(Ldata)
    # final["水域/陆地"] = Ffinal
    if len(Ffinal) > 0:
        for i in Ffinal:
            Fdata = dict()
            Fdata["type"] = "水域/陆地"
            if i[0][1] == 'P':
                Fdata["cnm"] = "点类"
            elif i[0][1] == 'L':
                Fdata["cnm"] = "线类"
            elif i[0][1] == 'A':
                Fdata["cnm"] = "面类"
            Fdata["name"] = i[0][3]
            data.append(Fdata)
    # final["境界与政区"] = Kfinal
    if len(Kfinal) > 0:
        for i in Kfinal:
            Kdata = dict()
            Kdata["type"] = "境界与政区"
            if i[0][1] == "P":
                Kdata["cnm"] = "点类"
            elif i[0][1] == "L":
                Kdata["cnm"] = "线类"
            elif i[0][1] == "A":
                Kdata["cnm"] = "面类"
            Kdata["name"] = i[0][3]
            data.append(Kdata)
    # final["陆地地貌及土质"] = Jfinal
    if len(Jfinal) > 0:
        for i in Jfinal:
            Jdata = dict()
            Jdata["type"] = "陆地地貌及土质"
            if i[0][1] == 'P':
                Jdata["cnm"] = "点类"
            elif i[0][1] == 'L':
                Jdata["cnm"] = "线类"
            elif i[0][1] == 'A':
                Jdata["cnm"] = "面类"
            Jdata["name"] = i[0][3]
            data.append(Jdata)
    final["code"] =0
    final["msg"] = ""
    final["count"] = cnum + dnum + fnum + jnum + lnum + knum
    final["data"] = data
    final = json.dumps(final, ensure_ascii=False)
    dir = os.path.join(settings.MEDIA_ROOT + os.sep + 'getdata' + os.sep + 'Result')
    f = open(dir, 'w+', encoding='utf-8')
    f.write(final)
    f.close()
    # 新建数组用于保存最终符合要求的点及属性
    # realinner = list()
    # # 点 线 面的ID 有重合，同时用 ID 和 类型 代表一个数据
    # for i in result_sx:
    #     # print(i)
    #     if i[1] == 'P':
    #         if str(i[0]) in pinnerpoint:
    #             temp = list()
    #             temp.append((i[0], i[2], i[3], i[6]))
    #             realinner.append(temp)
    #     elif i[1] == 'L':
    #         if str(i[1]) in linnerpoint:
    #             temp = list()
    #             temp.append((i[0], i[2], i[3], i[6]))
    #             realinner.append(temp)
    #     elif i[1] == 'A':
    #         if str(i[1]) in ainnerpoint:
    #             temp = list()
    #             temp.append((i[0], i[2], i[3], i[6]))
    #             realinner.append(temp)
    # # print(realinner)
    return HttpResponse(final)
'''


def adata(request):
    if request.method == 'GET':
        return render(request, "adata.html")


def aim(request):
    return render(request, 'aim.html')


def draw_geo(request):
    return render(request, 'draw_geo.html')


def login(request):
    return render(request, 'login.html')


# 目标定位
def aim1(request):
    # 下面是表单提交后的内容的格式
    # ddata={"dbName":"DN05490062","maskLen":"500.0","road-density":"0","h_min":"-20000","h_max":"50000","landform[0]":"0","lake":"0","surveyControlPoint":"1","industrial_and_agricultural_social_and_cultural_facilities":"1","residential_land_and_ancillary_facilities[0]":"0","residential_land_and_ancillary_facilities[1]":"1","residential_land_and_ancillary_facilities[2]":"2","pipeline[0]":"0","pipeline[1]":"1","pipeline[2]":"2","plant":"-1","airport":"-1","military_area":"-1"}
    if request.method == 'GET':     # 数据发送方式;get post
        road_density = int(request.GET.get("road-density", None))   # ajax传递字符串
        h_min = request.GET.get("h_min", None)
        h_max = request.GET.get("h_max", None)
        isFuPo = request.GET.get("lake", None)
        dbName = request.GET.get("dbName", None) + '.db'
        dbName = 'data.db'
        maskLen = request.GET.get("maskLen", None)
        isGongNongYe = request.GET.get("industrial_and_agricultural_social_and_cultural_facilities", None)
        isControlPoint = request.GET.get("surveyControlPoint", None)
        isVegetation = request.GET.get("plant", None)
        residentAndFacilities1 = request.GET.get("residential_land_and_ancillary_facilities[1]", None)
        residentAndFacilities0 = request.GET.get("residential_land_and_ancillary_facilities[0]", None)
        residentAndFacilities2 = request.GET.get("residential_land_and_ancillary_facilities[2]", None)
        pipeline0 = request.GET.get("pipeline[0]", None)
        pipeline1 = request.GET.get("pipeline[1]", None)
        pipeline2 = request.GET.get("pipeline[2]", None)
        landform0 = request.GET.get("landform[0]", None)
        landform1 = request.GET.get("landform[1]", None)
        landform2 = request.GET.get("landform[2]", None)
        landform3 = request.GET.get("landform[3]", None)
        landform4 = request.GET.get("landform[4]", None)
        landform5 = request.GET.get("landform[5]", None)

        # 点或者线的List
        daoLuPointList = m.readPoint(dbName)
        LineList = m.readLine(dbName)
        PointWithZList = m.readPointWithZ(dbName)
        AllList = daoLuPointList

        pointNotIncludeDict = {}
        AllDict = {'A': [], 'P': [], 'L': []}

        # 居民地及附属设施
        # 0为居民地，代码1302
        # 1为独立建筑物，代码1301
        # 2为其他建筑物，代码1303
        if residentAndFacilities0 is not None:
            ResidentAndFacilitiesPoint0Dict, ResidentAndFacilitiesPoint0List = m.readResidentAndFacilitiesPoint0(dbName)
            AllList += ResidentAndFacilitiesPoint0List
            AllDict.update(ResidentAndFacilitiesPoint0Dict)
        if residentAndFacilities1 is not None:
            ResidentAndFacilitiesPoint1Dict, ResidentAndFacilitiesPoint1List = m.readResidentAndFacilitiesPoint1(dbName)
            AllList += ResidentAndFacilitiesPoint1List
            AllDict.update(ResidentAndFacilitiesPoint1Dict)
        if residentAndFacilities2 is not None:
            ResidentAndFacilitiesPoint2Dict, ResidentAndFacilitiesPoint2List = m.readResidentAndFacilitiesPoint1(dbName)
            AllList += ResidentAndFacilitiesPoint2List
            AllDict.update(ResidentAndFacilitiesPoint2Dict)

        # 管线
        # 0为电力线，代码1501
        # 1为通信线，代码1502
        # 2为管道，代码1503
        if pipeline0 is not None:
            pipelinePoint0Dict, pipelinePoint0List = m.readPipelinePoint0(dbName)
            AllList += pipelinePoint0List
            AllDict.update(pipelinePoint0Dict)
        if pipeline1 is not None:
            pipelinePoint1Dict, pipelinePoint1List = m.readPipelinePoint1(dbName)
            AllList += pipelinePoint1List
            AllDict.update(pipelinePoint1Dict)
        if pipeline2 is not None:
            pipelinePoint2Dict, pipelinePoint2List = m.readPipelinePoint2(dbName)
            AllList += pipelinePoint2List
            AllDict.update(pipelinePoint2Dict)

        # 地貌
        # 0为雪山地貌，代码2003
        # 1为黄土地貌，代码2004
        # 2为岩溶地貌，代码2005
        # 3为风成地貌，代码2006
        # 4为火山地貌，代码2007
        # 5为其他地貌，代码2008
        if landform0 is not None:
            landform0Dict, landform0List = m.readLandformPoint0(dbName)
            AllList += landform0List
            AllDict.update(landform0Dict)
        if landform1 is not None:
            landform1Dict, landform1List = m.readLandformPoint1(dbName)
            AllList += landform1List
            AllDict.update(landform1Dict)
        if landform2 is not None:
            landform2Dict, landform2List = m.readLandformPoint2(dbName)
            AllList += landform2List
            AllDict.update(landform2Dict)
        if landform3 is not None:
            landform3Dict, landform3List = m.readLandformPoint3(dbName)
            AllList += landform3List
            AllDict.update(landform3Dict)
        if landform4 is not None:
            # landform4Dict, landform4List = m.readLandformPoint0(dbName)
            landform4Dict, landform4List = m.readLandformPoint4(dbName)
            AllList += landform4List
            AllDict.update(landform4Dict)
        if landform5 is not None:
            landform5Dict, landform5List = m.readLandformPoint5(dbName)
            AllList += landform5List
            AllDict.update(landform5Dict)

        # 判断“水域”一项的选择
        if isFuPo == '-1':
            pass
        elif isFuPo == '1':
            FuPoDict, FuPoList = m.readFuPo(dbName)
            # 直接取交集
            AllList += FuPoList
            AllDict.update(FuPoDict)
        else:
            FuPoDict, FuPoList = m.readFuPo(dbName)
            # 直接取差集
            pointNotIncludeDict.update(FuPoDict)

        # 判断“工农业社会文化设施”一项的选择
        if isGongNongYe == '-1':
            pass
        elif isGongNongYe == '1':
            GongNongYeDict, GongNongYeList = m.readGongNongYe(dbName)
            # 直接取交集
            AllList += GongNongYeList
            AllDict.update(GongNongYeDict)
        else:
            GongNongYeDict, GongNongYeList = m.readGongNongYe(dbName)
            # 直接取差集
            pointNotIncludeDict.update(GongNongYeDict)

        # 判断“测量控制点”一项的选择
        if isControlPoint == '-1':
            pass
        elif isControlPoint == '1':
            ControlPointDict, ControlPointList = m.readControlPoint(dbName)
            # 直接取交集
            AllList += ControlPointList
            AllDict.update(ControlPointDict)
        else:
            ControlPointDict, ControlPointList = m.readControlPoint(dbName)
            # 直接取差集
            pointNotIncludeDict.update(ControlPointDict)

        # 判断“植被”一项的选择
        if isVegetation == '-1':
            pass
        elif isVegetation == '1':
            VegetationPointDict, VegetationPointList = m.readVegetationPoint(dbName)
            # 直接取交集
            AllList += VegetationPointList
            AllDict.update(VegetationPointDict)
        else:
            VegetationPointDict, VegetationPointList = m.readControlPoint(dbName)
            # 直接取差集
            pointNotIncludeDict.update(VegetationPointDict)

        # 初始化Box数据结构
        b = m.Box(AllList, maskLen)

        # 遍历湖泊字典，维护单元格中是否含有湖泊
        # for key in FuPoDict.keys():
        #     xMin,xMax,yMin,yMax=m.getRectangleTuKe(FuPoDict[key])
        #     jMin=math.floor((xMin-b.xMin)/b.unitLen)
        #     iMin=math.floor((yMin-b.yMin)/b.unitLen)
        #     jMax=math.ceil((xMax-b.xMax)/b.unitLen)
        #     iMax=math.ceil((yMax-b.xMax)/b.unitLen)

        #     for j in range(jMin,jMax+1):
        #         for i in range(iMin,iMax+1):
        #             b.unitGirlsFuPo[j][i]=1

        # 初始化单元网格 、 掩膜的二维数组
        b.initUnitGirls(LineList)
        b.initMaskGirls(PointWithZList, AllDict, pointNotIncludeDict)

        # 获取道路密度返回数组结果
        densityResult = b.getZb(5, 0, h_min, h_max, isFuPo)
        # FuPoDict = m.readFuPo(dbName)

        # if road_density == '-1':
        #     result = densityResult[0] + densityResult[1] + densityResult[2]
        #     return result

        start_coords = (2192935.10, 19472810.74)
        tmp_x, tmp_y = m.CGCS2WSG(start_coords[0], start_coords[1])
        X = tmp_x[1] + tmp_x[2] / 60 + tmp_x[3] / 3600
        Y = tmp_y[1] + tmp_y[2] / 60 + tmp_x[3] / 3600
        folium_map = m.drawMapCenter([X, Y])
        folium_map = m.drawMapPoints(densityResult[road_density], folium_map)
        # print(AllList)
        # if len(AllList) >= 100:
        #     AllList = random.sample(AllList, 100)
        # folium_map = m.drawMapPoints(AllList, folium_map)
        # for point in densityResult[road_density]:
        #    print(point)
        # folium_map.save("templates/tmp.html")
        folium_map.save("templates/draw_geo.html")
        m.replaceJsRef("templates/draw_geo.html")

        # 服务器返回结果
        return render(request, 'result_road.html', context={'context': densityResult[road_density]})
        # return HttpResponse(densityResult[road_density])
    '''
def aim1(request):
    # 下面是表单提交后的内容的格式
    # ddata={"dbName":"DN05490062","road-density":"-1","h_min":"-20000","h_max":"50000","lake":"0","the-residential-areas-are-close-to-each-other":"0"}
    if request.method == 'GET':     # 数据发送方式;get post
        road_density = int(request.GET.get("road-density", None))   # ajax传递字符串
        h_min = request.GET.get("h_min", None)
        h_max = request.GET.get("h_max", None)
        isFuPo = request.GET.get("lake", None)
        dbName = request.GET.get("dbName", None) + '.db'
        maskLen = request.GET.get("maskLen", None)

        # 点或者线的List
        daoLuPointList = m.readPoint(dbName)
        LineList = m.readLine(dbName)
        PointWithZList = m.readPointWithZ(dbName)
        FuPoDict, FuPoList = m.readFuPo(dbName)

        # 初始化Box数据结构
        b = m.Box(daoLuPointList + FuPoList, maskLen)

        # 遍历湖泊字典，维护单元格中是否含有湖泊
        # for key in FuPoDict.keys():
        #     xMin,xMax,yMin,yMax=m.getRectangleTuKe(FuPoDict[key])
        #     jMin=math.floor((xMin-b.xMin)/b.unitLen)
        #     iMin=math.floor((yMin-b.yMin)/b.unitLen)
        #     jMax=math.ceil((xMax-b.xMax)/b.unitLen)
        #     iMax=math.ceil((yMax-b.xMax)/b.unitLen)

        #     for j in range(jMin,jMax+1):
        #         for i in range(iMin,iMax+1):
        #             b.unitGirlsFuPo[j][i]=1

        # 初始化单元网格 、 掩膜的二维数组
        b.initUnitGirls(LineList)
        b.initMaskGirls(PointWithZList, FuPoDict)

        # 获取道路密度返回数组结果
        densityResult = b.getZb(5, 0, h_min, h_max, isFuPo)
        # FuPoDict = m.readFuPo(dbName)

        if road_density == '-1':
            result = densityResult[0] + densityResult[1] + densityResult[2]
            return result

        # 服务器返回结果
        return HttpResponse(densityResult[road_density])
'''


def add(request):
    if request.method != "POST":
        return JsonResponse(
         {
            "status": 201,
            "message": "method error"
         })
    doc = request.POST.get("doc", None)
    sx = request.POST.get("sx", None)
    data = request.POST.get("data", None)
    # print(data)
    # print(type(data))
    # data = json.dumps(data, ensure_ascii=False)
    data = json.loads(data)
    # data = data.replace('\"', '"')
    # print(data)
    value = []
    # print(type(data))
    a = ''
    for key in data:
        if data[key]:
            a = a + str(data[key])
            a = a + ','
        else:
            a = a + 'NULL'
            a = a + ','
    # print(type(a))
    a = a[:len(a)-1]
    b = a.split(',')
    b[0] = b[0] + ','
    for i in range(1, len(b)):
        b[i] = '"' + b[i] + '",'

    c = ''.join(b)
    c = c[:len(c)-1]
    # print(c)
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    # sql = "insert into classD(id,leixing,coding,name,typec,node,level,width,pwidth,blength,
    # jklength,ton,kilo,bigao,cmonth,wdeep,dizhi,minbj,maxzb,spec,zjzz,wgbzz)
    # values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(
    # int(data["id"]), data["leixing"], data["coding"], data["name"], data["typec"], data["node"],
    # data["level"], data["width"], data["pwidth"], data["blength"], data["jklength"], data["ton"],
    # data["kilo"], data["bigao"], int(data["cmonth"]), data["wdeep"], data["dizhi"], data["minbj"],
    # data["maxzb"], data["spec"], data["zjzz"], data["wgbzz"])
    # b = 'insert into classD values (' + c + ')'
    # print(b)
    # sql = 'insert into classD values (' + c + ')'
    sql = 'insert into ' + doc + '_' + sx + ' values (' + c + ')'
    cur.execute(sql)

    # cur.execute("insert into classD(id,leixing,coding,name,typec,node,level,width,pwidth,blength,jklength,ton,kilo,
    # bigao,cmonth,wdeep,dizhi,minbj,maxzb,spec,zjzz,wgbzz)values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(
    # data["id"], data["leixing"], data["coding"], data["name"], data["typec"], data["node"], data["level"], data["wid
    # th"], data["pwidth"], data["blength"], data["jklength"], data["ton"], data["kilo"], data["bigao"], data["cmont
    # h"], data["wdeep"], data["dizhi"], data["minbj"], data["maxzb"], data["spec"], data["zjzz"], data["wgbzz"]))

    cur.close()
    con.commit()
    con.close()
    return HttpResponse("数据添加成功")
    # return render(request, 'database.html')


def delete(request):
    if request.method != "POST":
        return JsonResponse(
         {
            "status": 201,
            "message": "method error"
         })
    doc = request.POST.get('doc', None)
    doc = str(doc)
    sx = request.POST.get('sx', None)
    sx = str(sx)
    id = request.POST.get('id', None)
    type = request.POST.get('leixing', None)

    id = str(id)
    type = str(type)
    # print(data)
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    # name = j

    cur.execute('delete from ' + doc + '_' + sx + ' where 要素编号=' + id + ' and 所属类别="' + type + '"')
    cur.close()
    con.commit()
    con.close()
    return HttpResponse("delete")


def edit(request):
    if request.method == 'GET':
        return render(request, 'edit.html')


def updata(request):
    if request.method != "POST":
        return JsonResponse(
         {
            "status": 201,
            "message": "method error"
         })
    doc = request.POST.get("doc", None)
    doc = str(doc)
    sx = request.POST.get("sx", None)
    sx = str(sx)
    currentid = request.POST.get("currentid", None)
    currentleixing = request.POST.get("currentleixing", None)
    newdatas = request.POST.get("newdatas", None)
    newdata = newdatas.split(",")

    # newdata = list()
    # currentid = request.POST.get("currentid", None)
    # newdata.append(currentid)
    # currentleixing = request.POST.get("currentleixing", None)
    # newdata.append(currentleixing)
    # id = request.POST.get('id', None)
    # newdata.append(id)
    # leixing = request.POST.get("leixing", None)
    # newdata.append(leixing)
    # coding = request.POST.get("coding", None)
    # newdata.append(coding)
    # name = request.POST.get("name", None)
    # newdata.append(name)
    # typec = request.POST.get("typec", None)
    # newdata.append(typec)
    # node = request.POST.get("node", None)
    # newdata.append(node)
    # level = request.POST.get("level", None)
    # newdata.append(level)
    # width = request.POST.get("width", None)
    # newdata.append(width)
    # pwidth = request.POST.get("pwidth", None)
    # newdata.append(pwidth)
    # blength = request.POST.get("blength", None)
    # newdata.append(blength)
    # jklength = request.POST.get("jklength", None)
    # newdata.append(jklength)
    # ton = request.POST.get("ton", None)
    # newdata.append(ton)
    # kilo = request.POST.get("kilo", None)
    # newdata.append(kilo)
    # bigao = request.POST.get("bigao", None)
    # newdata.append(bigao)
    # cmonth = request.POST.get("cmonth", None)
    # newdata.append(cmonth)
    # wdeep = request.POST.get("wdeep", None)
    # newdata.append(wdeep)
    # dizhi = request.POST.get("dizhi", None)
    # newdata.append(dizhi)
    # minbj = request.POST.get("minbj", None)
    # newdata.append(minbj)
    # maxzb = request.POST.get("maxzb", None)
    # newdata.append(maxzb)
    # spec = request.POST.get("spec", None)
    # newdata.append(spec)
    # zjzz = request.POST.get("zjzz", None)
    # newdata.append(zjzz)
    # wgbzz = request.POST.get("wgbzz", None)
    # newdata.append(wgbzz)
    # print(newdata)

    con = sqlite3.connect("data.db")
    cur = con.cursor()
    sql = 'select * from ' + doc + '_' + sx
    cur.execute(sql)
    col_list = [tuple[0] for tuple in cur.description]
    # print(col_list)
    # print(newdata)
    for i in range(len(col_list)):
        # sql = 'update classD set ' + col_list[i] + '=' + newdata[i+2] + ' where ' + col_list[0] + '=' + newdata[0]
        # + ' and ' + col_list[1] + '=' + newdata[1]
        # updata classD set id=id where id=1 and leixing=leixing
        cur.execute('update ' + doc + '_' + sx + ' set ' + col_list[i] + '="' + newdata[i] + '" where ' + col_list[0] + '=' + currentid + ' and ' + str(col_list[1]) + '="' + currentleixing + '"')
    cur.close()
    con.commit()
    con.close()

    return HttpResponse(newdata)


def Table1Json():
    # 数据本身属性
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    sql1 = 'select * from document'
    cur.execute(sql1)
    document = cur.fetchall()

    sql2 = 'select * from tuceng'
    cur.execute(sql2)
    tuceng = cur.fetchall()

    sql3 = 'select * from home'
    cur.execute(sql3)
    home = cur.fetchall()
    con.commit()
    cur.close()
    con.close()

    jsonData = list()
    for row0 in document:
        interdata0 = {}
        data0 = {}
        interdata0['name'] = str(row0[1])
        temp = json.dumps(interdata0, ensure_ascii=False)
        data0[row0[1]] = temp
        temp0 = str(data0)
        for i in range(0, len(temp0)):
            if temp0[i] == ":":
                jsonData.append(temp0[0:i + 1] + temp0[i + 3:len(temp0) - 2])
                break

    for row in tuceng:
        data = dict()
        interdata = dict()
        xiao = ' '
        interdata['name'] = str(row[1])
        for row1 in home:

            if str(row1[3]) == str(row[2]):
                xiao = xiao + row1[1] + " "
                # xiao.append(row1[1])
                interdata['小类别'] = xiao
        # print(interdata)

        temp = json.dumps(interdata, ensure_ascii=False)
        data[row[1]] = temp
        temp2 = str(data)

        for i in range(0, len(temp2)):
            if temp2[i] == ":":

                jsonData.append(temp2[0:i + 1] + temp2[i + 3:len(temp2) - 2])

                break
    for row2 in home:
        interdata2 = {}
        data2 = {}
        interdata2['name'] = row2[1]
        interdata2['要素编码'] = str(row2[2])
        # interdata2['ZBY'] = str(row2[3])
        # interdata2['ZBA'] = str(row2[4])
        # interdata2['ZBL'] = str(row2[5])
        temp = json.dumps(interdata2, ensure_ascii=False)
        data2[row2[1]] = temp
        temp2 = str(data2)

        for i in range(0, len(temp2)):

            if temp2[i] == ":":
                jsonData.append(temp2[0:i + 1] + temp2[i + 3:len(temp2) - 2])
                break

    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    jsondatar = jsondatar.replace('\\', '')
    jsondatar = jsondatar.replace('}"', '}')
    jsondatar = jsondatar.replace('"{', '{')
    jsondatar = jsondatar.replace("{'", "'")
    #   jsondatar = jsondatar.replace()
    jsondatar = jsondatar[1:len(jsondatar) - 1]
    jsondatar = '{' + jsondatar + '}'
    jsondatar = jsondatar.replace("'", '"')
    return jsondatar


def Table2Json():
    # 显示第三类的属性
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    sql2 = 'select * from tuceng'
    cur.execute(sql2)
    tuceng = cur.fetchall()

    sql3 = 'select * from home'
    cur.execute(sql3)
    home = cur.fetchall()

    sql1 = 'select * from document'
    cur.execute(sql1)
    document = cur.fetchall()

    con.commit()
    cur.close()
    con.close()

    node = []
    link = []
    data = {}

    # 一类节点的属性
    for row0 in document:
        interdata0 = {}
        interdata0['name'] = row0[1]
        interdata0['class'] = "document"
        interdata0['group'] = 2
        interdata0['size'] = 40
        temp = json.dumps(interdata0, ensure_ascii=False)
        node.append(temp)

    # 二类节点属性
    for row in tuceng:
        # data = {}
        interdata = {}
        interdata['name'] = row[1]
        interdata['class'] = "tuceng"
        interdata['group'] = 0  # 同一组 同一色
        interdata['size'] = 20  # 节点大小

        temp = json.dumps(interdata, ensure_ascii=False)
        #   temp = temp.replace("'"," ")
        node.append(temp)

    # 第三类节点属性
    for row in home:
        interdata1 = {}
        interdata1['name'] = row[1]
        interdata1['class'] = "小类别"
        interdata1['group'] = 1
        interdata1['size'] = 10
        temp1 = json.dumps(interdata1, ensure_ascii=False)
        node.append(temp1)

    # 连线关系
    for row0 in document:
        # 第一类到第二类连接
        links = {}
        for row1 in tuceng:
            links['source'] = row0[1]
            links['target'] = row1[1]
            # links['value'] = 6
            temp = json.dumps(links, ensure_ascii=False)
            link.append(temp)

    for row3 in tuceng:
        links = {}
        # 第二类到第三类连接
        for row4 in home:
            if str(row4[3]) == str(row3[2]):
                links['source'] = row3[1]
                links['target'] = row4[1]
                # links['value'] = 3
                temp = json.dumps(links, ensure_ascii=False)
                link.append(temp)

    data['nodes'] = node
    data['links'] = link

    datar = json.dumps(data, ensure_ascii=False)
    datar = datar.replace('\\', '')
    datar = datar.replace('"{', '{')
    datar = datar.replace('}"', '}')
    return datar


# 表格的增加和编辑界面 动态生成
def addpagecol(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": 201,
                "message": "method error"
            }
        )
    doc = request.POST.get("doc", None)
    sx = request.POST.get("sx", None)
    doc = str(doc)
    sx = str(sx)
    data = dict()
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    sql = 'select * from ' + doc + '_' + sx
    cur.execute(sql)
    col_list = [tuple[0] for tuple in cur.description]
    data["data"] = col_list
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data)


def PathResult(request):
    if request.method == 'GET':
        return render(request, 'PathResult.html')


def draw_map(request):
    return render(request, 'tmp.html')


def login2(request):
    if request.method == 'POST':
        # resp = HttpResponse()
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj_user = models.WangUser.objects.filter(username=username, password=password)
        if obj_user:
            request.session["username"] = username
            return redirect('select')
        else:
            return render(request, 'login_error.html')
    elif request.method == 'GET':
        return render(request, 'login.html')


def index(request):
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_list = models.WangUser.objects.filter(username=username)
        error_name = []
        if user_list:
            error_name = '用户名已经存在'
            return render(request, 'register.html', {'error_name': error_name})
        else:
            username = models.WangUser.objects.create(username=username, password=password)
            username.save()
            return redirect('login')
    return render(request, 'register.html')


def get_cookie(request):
    username = request.COOKIES.get_cookie('username', None)
    return username


def test(request):
    if request.method == 'GET':
        # 处理绘制home界面的图谱所需数据，转成d3.js所需的格式
        # 设置绘制home页面的图谱时获取数据的文件路径，并在文件内写入相应内容
        dir1 = os.path.join(settings.MEDIA_ROOT + os.sep + 'json' + os.sep + 'pro_citys1.json')
        dir2 = os.path.join(settings.MEDIA_ROOT + os.sep + 'json' + os.sep + 'linkchina1.json')
        jsondata1 = Table1Json()
        f = open(dir1, 'w+', encoding='utf-8')
        f.write(jsondata1)
        f.close()

        jsondata2 = Table2Json()
        f = open(dir2, 'w+', encoding='utf-8')
        f.write(jsondata2)
        f.close()

        # 返回home界面
        return render(request, 'select2.html')


def logout1(request):
    request.session.flush()
    return render(request, 'select.html')


def logout2(request):
    request.session.flush()
    return render(request, 'add_stu_tmp2.html')


def render_database(request):
    return render(request, 'database.html')


def geo(request):
    return render(request, 'draw_geo.html')


def temp(request):
    return render(request, 'tmp.html')

def temp2(request):
    return render(request, 'tmp2.html')


def find_road(request):
    username = request.session.get('username')
    if username is None:
        return render(request, 'pleaselogin.html')
    else:
        return render(request, 'findroad.html')


def web_k_means(request):
    username = request.session.get('username')
    if username is None:
        return render(request, 'pleaselogin.html')
    else:

        if request.method == 'GET':
            # 绘制地图中心
            start_coords = (2192935.10, 19472810.74)
            tmp_x, tmp_y = m.CGCS2WSG(start_coords[0], start_coords[1])
            X = tmp_x[1] + tmp_x[2] / 60 + tmp_x[3] / 3600
            Y = tmp_y[1] + tmp_y[2] / 60 + tmp_x[3] / 3600
            folium_map = m.drawMapCenter([X, Y])
            folium_map.save("templates/kmeans.html")
            m.replaceJsRef("templates/kmeans.html")
            return render(request, 'full_kmeans.html')

        elif request.method == 'POST':
            start_coords = (2192935.10, 19472810.74)
            tmp_x, tmp_y = m.CGCS2WSG(start_coords[0], start_coords[1])
            X = tmp_x[1] + tmp_x[2] / 60 + tmp_x[3] / 3600
            Y = tmp_y[1] + tmp_y[2] / 60 + tmp_x[3] / 3600
            folium_map = m.drawMapCenter([X, Y])

            k = int(request.POST.get('k'))
            choice = request.POST.get('choice')
            m.real_k_means(choice, k, folium_map)
            return render(request, 'full_kmeans.html')


def web_inside_k_means(request):
    return render(request, 'kmeans.html')


def please_login(request):
    return render(request, 'pleaselogin.html')


def TableJsonUpdate1(document, classes):
    con = sqlite3.connect('data.db')
    cur = con.cursor()

    sql1 = 'select * from ' + document + '_' + classes + 'SX'
    # print(document, classes)
    cur.execute(sql1)
    dataa = cur.fetchall()

    sql2 = 'select * from tuceng'
    cur.execute(sql2)
    tuceng = cur.fetchall()

    sql3 = 'select * from home'
    cur.execute(sql3)
    home = cur.fetchall()

    con.commit()
    cur.close()
    jsonData = list()
    # print(tuceng)
    for row0 in tuceng:
        if row0[2] == classes:
            interdata = {}
            data = {}
            interdata['name'] = str(row0[1])
            temp = json.dumps(interdata, ensure_ascii=False)
            data[row0[1]] = temp
            temp0 = str(data)
            for i in range(0, len(temp0)):
                if temp0[i] == ":":
                    jsonData.append(temp0[0:i + 1] + temp0[i + 3:len(temp0) - 2])
                    break
    for row in home:
        if row[3] == classes:
            interdata = {}
            data = {}
            interdata['name'] = str(row[1])
            temp = json.dumps(interdata, ensure_ascii=False)
            data[row[1]] = temp
            temp0 = str(data)
            for i in range(0, len(temp0)):
                if temp0[i] == ":":
                    jsonData.append(temp0[0:i + 1] + temp0[i + 3:len(temp0) - 2])
                    break

    for row2 in dataa:
        # if classes == 'F':
            # print(int(str(row2[0])[-1]))
            if int(str(row2[0])[-1]) == 1:
            # if int(str(row2[0])[-1]) != 2 and int(str(row2[0])[-1]) != 3 and int(str(row2[0])[-1]) != 4 and int(str(row2[0])[-1]) != 5 and int(str(row2[0])[-1]) != 9:
                # print(int(str(row2[0])[-1]))
                interdata = dict()
                datas = dict()
                interdata['id'] = row2[0]
                interdata['类型'] = row2[1]
                interdata['编码'] = row2[2]
                interdata['名称'] = row2[3]
                temp = json.dumps(interdata, ensure_ascii=False)
                datas[row2[3]] = temp
                temp2 = str(datas)
                jsonData.append(temp2)
            else:
                continue
    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    jsondatar = jsondatar.replace('\\', '')
    jsondatar = jsondatar.replace('}"', '}')
    jsondatar = jsondatar.replace('"{', '{')
    jsondatar = jsondatar.replace("{'", "'")
    # jsondatar = jsondatar.replace()
    jsondatar = jsondatar[1:len(jsondatar) - 1]
    jsondatar = '{' + jsondatar + '}'
    jsondatar = jsondatar.replace("'", '"')
    jsondatar = jsondatar.replace('"{', '{')
    jsondatar = jsondatar.replace('}"}', '}')
    # print(jsondatar)
    return jsondatar


def TableJsonUpdate2(document, classes):  # document = tuceng,tuceng = home,home = calssD
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    sql = 'select * from tuceng'
    cur.execute(sql)
    tuceng = cur.fetchall()

    sql2 = 'select * from home'
    cur.execute(sql2)
    home = cur.fetchall()

    sql3 = 'select * from ' + document + '_' + classes + 'SX'
    cur.execute(sql3)
    datas = cur.fetchall()

    con.commit()
    cur.close()
    con.close()

    node = []
    link = []
    data = {}

    for row in tuceng:
        if row[2] == classes:
            interdata = {}
            interdata['name'] = row[1]
            interdata['class'] = "图层"
            interdata['group'] = 2
            interdata['size'] = 30
            temp = json.dumps(interdata, ensure_ascii=False)
            node.append(temp)
            links = {}
            for row1 in home:
                if row1[3] == classes:
                    interdata1 = {}
                    interdata1['name'] = row1[1]
                    interdata1['class'] = "类别"
                    interdata1['group'] = 0
                    interdata1['size'] = 15
                    temp = json.dumps(interdata1, ensure_ascii=False)
                    node.append(temp)
                    links['source'] = row[1]
                    links['target'] = row1[1]
                    links['value'] = 20
                    temp = json.dumps(links, ensure_ascii=False)
                    link.append(temp)

    for row2 in datas:
        # if classes == 'F':
            print(int(str(row2[0])))
            # if int(str(row2[0])[-1]) != 2 and int(str(row2[0])[-1]) != 3 and int(str(row2[0])[-1]) != 4 and int(str(row2[0])[-1]) != 5 and int(str(row2[0])[-1]) != 9:
            if int(str(row2[0])[-1]) == 1:
                print(int(str(row2[0])[-1]))
                interdata2 = {}
                interdata2['name'] = str(row2[0]) + row2[3]
                interdata2['group'] = 1
                interdata2['belong'] = classes
                interdata2['leixing'] = row2[1]
                interdata2['parent'] = document
                # interdata2['distance'] = 20
                interdata2['size'] = 10
                temp0 = json.dumps(interdata2, ensure_ascii=False)
                node.append(temp0)
            else:
                continue
    for row3 in home:
        links = {}
        if row3[3] == classes:
            for row4 in datas:
                # if classes == 'F':
                    # print(int(str(row4[0])[-1]))
                    if int(str(row4[0])[-1]) == 1:
                    # if int(str(row4[0])[-1]) != 2 and int(str(row4[0])[-1]) != 3 and int(str(row4[0])[-1]) != 4 and int(str(row4[0])[-1]) != 5 and int(str(row4[0])[-1]) != 9:
                        if len(str(row4[2])) >= 4:
                            code = str(row4[2])[0:4]
                            # print(code)
                            if code == str(row3[2]):
                                links['source'] = row3[1]
                                links['target'] = str(row4[0]) + row4[3]
                                links['value'] = 20
                                temp = json.dumps(links, ensure_ascii=False)
                                link.append(temp)
                        else:
                            continue
    # print(link)
    data['nodes'] = node
    data['links'] = link
    datar = json.dumps(data, ensure_ascii=False)
    datar = datar.replace('\\', '')
    datar = datar.replace('"{', '{')
    datar = datar.replace('}"', '}')
    # print(datar)
    return datar


def heat_map(request):
    username = request.session.get('username')
    if username is None:
        return render(request, 'pleaselogin.html')
    else:
        if request.method == 'GET':
            # 绘制地图中心
            start_coords = (2192935.10, 19472810.74)
            tmp_x, tmp_y = m.CGCS2WSG(start_coords[0], start_coords[1])
            X = tmp_x[1] + tmp_x[2] / 60 + tmp_x[3] / 3600
            Y = tmp_y[1] + tmp_y[2] / 60 + tmp_x[3] / 3600
            folium_map = m.drawHeatMapCenter([X, Y])
            folium_map.save("templates/inside_heat_map.html")
            m.replaceJsRef("templates/inside_heat_map.html")
            return render(request, 'heatmap.html')

        elif request.method == 'POST':

            # 绘制地图中心
            start_coords = (2192935.10, 19472810.74)
            tmp_x, tmp_y = m.CGCS2WSG(start_coords[0], start_coords[1])
            X = tmp_x[1] + tmp_x[2] / 60 + tmp_x[3] / 3600
            Y = tmp_y[1] + tmp_y[2] / 60 + tmp_x[3] / 3600
            # tiles='Stamen Toner'
            folium_map = m.drawHeatMapCenter([X, Y])

            # 绘制热力图
            place_name = request.POST.get('choice')
            folium_map = m.get_road_or_tree_data(place_name, folium_map)
            folium_map.save('templates/inside_heat_map.html')# 将绘制好的地图保存为html文件
            m.replaceJsRef("templates/inside_heat_map.html")
            return render(request, 'heatmap.html')


def inside_heat_map(request):
    return render(request, "inside_heat_map.html")


def summarize(request):
    L, P = m.get_data_pie()
    A_P, A_L, B_P, B_L, C_P, C_L, D_P, D_L, L_P, L_L = m.get_data_zhifangtu()
    d_data = m.get_data_sheet('D')
    f_data = m.get_data_sheet('F')
    context = {
        'data_pie_L': L,
        'data_pie_P': P,
        'A_P': A_P,
        'A_L': A_L,
        'B_P': B_P,
        'B_L': B_L,
        'C_P': C_P,
        'C_L': C_L,
        'D_P': D_P,
        'D_L': D_L,
        'L_P': L_P,
        'L_L': L_L,
        'd_data': d_data,
        'f_data': f_data,
    }
    # print(context)
    return render(request, "summarize.html", context=context)


def fuzhujuece(request):
    if request.method == "GET":
        return render(request, 'juece.html', context={
            'r': 0,
            "b": 0,
            'result': "该模块使用兰彻斯特战争模型，请按下左侧按提交钮进行预测！！！"},)
    elif request.method == "POST":
        # 初始化双方作战效能
        r_0 = float(request.POST.get('r0'))
        b_0 = float(request.POST.get('b0'))
        # 初始化双方战斗单位在单位时间平均毁伤对方战斗成员的数量
        r_l = float(request.POST.get('rl'))
        b_l = float(request.POST.get('bl'))
        # 初始化双方战斗单位平均毁伤对方的数量
        r_s = float(request.POST.get('rs'))
        b_s = float(request.POST.get('bs'))
        # 初始化双方的伪装能力系数
        r_f = float(request.POST.get('rf'))
        b_f = float(request.POST.get('bf'))
        # 初始化双方的侦察能力
        r_sf = float(request.POST.get('rsf'))
        b_sf = float(request.POST.get('bsf'))
        # 初始化双方信息作战能力系数
        epsilon_r = float(request.POST.get('epsilon_r'))
        epsilon_b = float(request.POST.get('epsilon_b'))
        # 攻击模式
        mode = request.POST.get('mode')

        result = m.do_predict(r_0, b_0, b_s, r_s, b_l, r_l, r_f, b_f, r_sf, b_sf, epsilon_r, epsilon_b, mode)
        m.draw_bingli_map()
        return render(request, 'juece.html', context=result)


def fzjc(requests):
    return render(requests, "fzjc.html")