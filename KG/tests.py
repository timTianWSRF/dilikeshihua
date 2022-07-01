# coding:utf-8
import sys
import os
import json
import sqlite3
import math
from shapely import geometry
'''
classes = ['city', 'country']
result = []
result1 = []
coun = []
dict = {}
p = "../media/json/linkchina2.json"
if os.path.exists(p):
    if sys.version_info.major > 2:
        f = open(p, 'r', encoding='utf-8')
    else:
        f = open(p, 'r')

    dict_data = json.loads(f.read())
   # print(dict_data)
    for i in dict_data['nodes']:
         if i['class'] in classes:
             coun.append(i['name'])
             result.append(i)
    dict["nodes"] = result

    print(dict_data['links'])
    for line in dict_data['links']:
        if line['source'] and line['target'] in coun:
            result1.append(line)
    dict['links'] = result1
    '''

'''
def Table1Json():  # 点及属性json生成  procitys
    try:

        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        sqlpro = "select * from pro"
        cur.execute(sqlpro)
        result_pro = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        conn = get_connect()
        cur2 = conn.cursor()
        sqlcity = "select * from city"
        cur2.execute(sqlcity)
        result_city = cur2.fetchall()
        conn.commit()
        cur2.close()
        conn.close()

        conn = get_connect()
        cur3 = conn.cursor()
        sqlcoun = "select * from country"
        cur3.execute(sqlcoun)
        result_coun = cur3.fetchall()
        conn.commit()
        cur3.close()
        conn.close()

        jsonData = []

        for row0 in result_coun:
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

        for row in result_pro:
            data = {}
            interdata = {}
            citys = ' '
            interdata['name'] = str(row[1])
            for row1 in result_city:

                if str(row1[6]) == str(row[0]):
                    citys = citys + row1[1] + " "
                    #  citys.append(row1[1])
                    interdata['city'] = citys
            #    print(interdata)
            temp = json.dumps(interdata, ensure_ascii=False)
            data[row[1]] = temp
            temp2 = str(data)

            for i in range(0, len(temp2)):
                if temp2[i] == ":":
                    #  print(jsonData)
                    jsonData.append(temp2[0:i + 1] + temp2[i + 3:len(temp2) - 2])
                    #  print(jsonData)
                    break

        for row2 in result_city:
            interdata2 = {}
            data2 = {}
            interdata2['name'] = row2[1]
            interdata2['ZBX'] = str(row2[2])
            interdata2['ZBY'] = str(row2[3])
            interdata2['ZBA'] = str(row2[4])
            interdata2['ZBL'] = str(row2[5])
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

    #    print("连接成功")
    # print(jsonData[1:len(jsonData)-1])
    except Exception as e:
        print('MySQL connect fail ', e)


a = {}
data = []
c = []
entity = "classD"
con = sqlite3.connect('data.db')
cur = con.cursor()
#sql = "select count(*) from classD"
sql = 'select * from ' + entity
cur.execute(sql)
#获取列名
col_name_list = [tuple[0] for tuple in cur.description]
for i in range(len(col_name_list)):
    a = {}
    a["field"] = col_name_list[i]
    a["title"] = col_name_list[i]
    a["width"] = 80
    data.append(a)
data[0]["fixed"] = 'left'
b = json.dumps(data, ensure_ascii=False)
b = b.replace('"field":', "field:")
b = b.replace('"title":', "title:")
b = b.replace('"width":', "width:")
b = b.replace('"fixed":', "fixed:")
b = b[1:-1]
# c.append(b)
print(b)


# result = cur.fetchall()
# for i in result:
#     temp = {}
#     #读取到列名及数据后用循环代替
# #id, coding, name, typec, node, level, width, pwidth, blength, jklength, ton, kilo, bigao, cmonth, wdeep, dizhi, minbj, maxzb, spec, zjzz, wgbzz
#     temp["id"] = i[0]
#     temp["coding"] = i[1]
#     temp["name"] = i[2]
#     temp["typec"] = i[3]
#     temp["node"] = i[4]
#     temp["level"] = i[5]
#     temp["width"] = i[6]
#     temp["pwidth"] = i[7]
#     temp["blength"] = i[8]
#     temp["jklength"] = i[9]
#     temp["ton"] = i[10]
#     temp["kilo"] = i[11]
#     temp["bigao"] = i[12]
#     temp["cmoth"] = i[13]
#     temp["wdeep"] = i[14]
#     temp["dizhi"] = i[15]
#     temp["minbj"] = i[16]
#     temp["maxzb"] = i[17]
#     temp["spec"] = i[18]
#     temp["zjzz"] = i[19]
#     temp["wgbzz"] = i[20]
#     data.append(temp)
# a["Data"] = data
# tdata = json.dumps(a, ensure_ascii=False)
# print(a)
'''
# data = []
# con = sqlite3.connect('data.db')
# cur = con.cursor()
# sql = 'select * from classD'
# cur.execute(sql)
# col_name_list = [tuple[0] for tuple in cur.description]
# j = 0
# for i in col_name_list:
#         doc = {}
#
#         doc['ID'] = j
#         doc['TAGNAME'] = i
#         j += 1
#         data.append(doc)
# print(data)
# for i in data:
#     print(i)
# for i in range(len(col_name_list)):
#         temp = {}
#         j = 0
#         temp[col_name_list[j]] = result[j]
#         data.append(temp)


# import sqlite3
#
# def connectRSX():   #RSX
#     print("进入")
#     con = sqlite3.connect('tDN05490062.db')  # 连接桥
#     print("Open database successfully")  # 打开成功
#     cur = con.cursor()
#     sql1 = "create table DN05490061_RSX007 (leibie varchar(20),id int primary key," \
#            "coding varchar(20) ,name varchar(20),typec varchar(20),node varchar(20)," \
#            "level varchar(20),width varchar(20),pwidth varchar(20))"
#     cur.execute(sql1)
#     # res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     # for name in res:
#     # print(name[0])
#     with open(r'C:\Users\16855\Desktop\RSX.RSX', 'r' ,encoding='utf-8') as fil1:  # 读文件
#       print(fil1)
#       re = fil1.readline()  # 逐行读入
#       re = fil1.readline()
#       re = fil1.readline()
#       re = fil1.readline()
#       re = fil1.readline()
#       re = fil1.readline()
#       ty = fil1.read(1)
#       print(ty)
#       print(ty.strip())
#       if (ty.strip() == 'N'):
#          PointNumber = fil1.readline().strip()
#          print(int(PointNumber))
#          for id in range(int(PointNumber)):
#              point = fil1.readline().split()
#              # print(int(len(point)))
#              # print(point)
#              leibie = ty.strip()
#              pointId = point[0]
#              coding = point[1]
#              name = point[2]
#              typec = point[3]
#              node = point[4]
#              level = point[5]
#              width = point[6]
#              pwidth = point[7]
#              print(leibie, pointId, coding, name, typec, node, level, width, pwidth)
#              cur.execute("insert into DN05490061_RSX007 (leibie,id,coding,name,typec,node,level,"
#                         "width,pwidth)"
#                         "values(?,?,?,?,?,?,?,?,?)",
#                         (ty.strip(), pointId, coding, name, typec, node, level, width, pwidth))
#          ty = fil1.read(6)
#     cur.close()
#     con.commit()
#     con.close()
#     return True
#
#
# def connectLSX():  #LSX
#     print("进入")
#     con = sqlite3.connect('tDN05490062.db')  # 连接桥
#     print("Open database successfully")  # 打开成功
#     cur = con.cursor()
#     sql1 = "create table DN05490061_LSX3 (leibie varchar(20),id int," \
#            "coding varchar(20) ,name varchar(20),typec varchar(20),node varchar(20)," \
#            "level varchar(20),width varchar(20),pwidth varchar(20),blength varchar(20)," \
#            "jklength varchar(20),ton varchar(20))"
#     cur.execute(sql1)
#     # res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     # for name in res:
#     # print(name[0])
#     fil1 = open(r'C:\Users\16855\Desktop\DN05490061.LSX', encoding="utf-8")  # 读文件
#     re = fil1.readline()  # 逐行读入
#     re = fil1.readline()
#     re = fil1.readline()
#     re = fil1.readline()
#     re = fil1.readline()
#     re = fil1.readline()
#     ty = fil1.read(6)
#     if (ty.strip() == "P"):
#         PointNumber = fil1.readline().strip()
#         # print(int(PointNumber))
#         for id in range(int(PointNumber)):
#             point = fil1.readline().split()
#             # print(int(len(point)))
#             # print(point)
#             leibie = ty.strip()
#             pointId = point[0]
#             coding = point[1]
#             name = point[2]
#             typec = point[3]
#             node = point[4]
#             level = point[5]
#             width = point[6]
#             pwidth = point[7]
#             blength = point[8]
#             jklength = point[9]
#             ton = point[10]
#             print(leibie, pointId, coding, name, typec, node, level, width, pwidth, blength, jklength,
#                   ton)
#             cur.execute("insert into DN05490061_LSX3(leibie,id,coding,name,typec,node,level,"
#                         "width,pwidth,blength,jklength,ton)"
#                         "values(?,?,?,?,?,?,?,?,?,?,?,?)",
#                         (ty.strip(), pointId, coding, name, typec, node, level, width, pwidth, blength, jklength,
#                          ton))
#         ty = fil1.read(6)
#     if (ty.strip() == 'L'):
#         LineNumber = fil1.readline().strip()
#         for i in range(int(LineNumber)):
#             line = fil1.readline().split()
#             leibie = ty.strip()
#             LineId = line[0]
#             coding = line[1]
#             name = line[2]
#             typec = line[3]
#             node = line[4]
#             level = line[5]
#             width = line[6]
#             pwidth = line[7]
#             blength = line[8]
#             jklength = line[9]
#             ton = line[10]
#             # for j in range(math.ceil(int(coding) / 5)):
#             # lines = fil.readline().split()
#             print(leibie, LineId, coding, name, typec, node, level, width, pwidth, blength, jklength, ton)
#             cur.execute(
#                 "insert into DN05490061_LSX3(leibie,id,coding,name,typec,node,level,width,pwidth,"
#                 "blength,jklength,ton)"
#                 "values(?,?,?,?,?,?,?,?,?,?,?,?)",
#                 (leibie, LineId, coding, name, typec, node, level, width, pwidth, blength, jklength, ton))
#         ty = fil1.read(6)
#     if (ty.strip() == 'A'):
#         AreaNumber = fil1.readline().strip()
#         for i in range(int(AreaNumber)):
#             area = fil1.readline().split()
#             leibie = ty.strip()
#             LineId = area[0]
#             coding = area[1]
#             name = area[2]
#             typec = area[3]
#             node = area[4]
#             level = area[5]
#             width = area[6]
#             pwidth = area[7]
#             blength = area[8]
#             jklength = area[9]
#             ton = area[10]
#             # for j in range(math.ceil(int(coding) / 5)):
#             # lines = fil.readline().split()
#             print(leibie, LineId, coding, name, typec, node, level, width, pwidth, blength, jklength, ton)
#             cur.execute(
#                 "insert into DN05490061_LSX3(leibie,id,coding,name,typec,node,level,width,pwidth,"
#                 "blength,jklength,ton)"
#                 "values(?,?,?,?,?,?,?,?,?,?,?,?)",
#                 (leibie, LineId, coding, name, typec, node, level, width, pwidth, blength, jklength, ton))
#     cur.close()
#     con.commit()
#     con.close()
#     return True
#
#
# def connectBSX():   #BSX
#     print("进入")
#     con = sqlite3.connect('tDN05490062.db')  # 连接桥
#     print("Open database successfully")  # 打开成功
#     cur = con.cursor()
#     sql1 = "create table DN05490061_BSX1 (leibie varchar(20),id int," \
#            "coding varchar(20) ,name varchar(20),typec varchar(20),node varchar(20)," \
#            "level varchar(20),width varchar(20),pwidth varchar(20),blength varchar(20)," \
#            "jklength varchar(20))"
#     cur.execute(sql1)
#     # res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     # for name in res:
#     # print(name[0])
#     fil1 = open(r'C:\Users\16855\Desktop\DN05490061.BSX', encoding="utf-8")  # 读文件
#     re = fil1.readline()  # 逐行读入
#     re = fil1.readline()
#     re = fil1.readline()
#     re = fil1.readline()
#     re = fil1.readline()
#     re = fil1.readline()
#     ty = fil1.read(6)
#     if (ty.strip() == "P"):
#         PointNumber = fil1.readline().strip()
#         # print(int(PointNumber))
#         for id in range(int(PointNumber)):
#             point = fil1.readline().split()
#             # print(int(len(point)))
#             # print(point)
#             leibie = ty.strip()
#             pointId = point[0]
#             coding = point[1]
#             name = point[2]
#             typec = point[3]
#             node = point[4]
#             level = point[5]
#             width = point[6]
#             pwidth = point[7]
#             blength = point[8]
#             jklength = point[9]
#             print(leibie, pointId, coding, name, typec, node, level, width, pwidth, blength, jklength,
#                   )
#             cur.execute("insert into DN05490061_BSX1(leibie,id,coding,name,typec,node,level,"
#                         "width,pwidth,blength,jklength)"
#                         "values(?,?,?,?,?,?,?,?,?,?,?)",
#                         (ty.strip(), pointId, coding, name, typec, node, level, width, pwidth, blength, jklength,
#                          ))
#         ty = fil1.read(6)
#     if (ty.strip() == 'L'):
#         LineNumber = fil1.readline().strip()
#         for i in range(int(LineNumber)):
#             line = fil1.readline().split()
#             leibie = ty.strip()
#             LineId = line[0]
#             coding = line[1]
#             name = line[2]
#             typec = line[3]
#             node = line[4]
#             level = line[5]
#             width = line[6]
#             pwidth = line[7]
#             blength = line[8]
#             jklength = line[9]
#             # for j in range(math.ceil(int(coding) / 5)):
#             # lines = fil.readline().split()
#             print(leibie, LineId, coding, name, typec, node, level, width, pwidth, blength, jklength)
#             cur.execute(
#                 "insert into DN05490061_BSX1(leibie,id,coding,name,typec,node,level,width,pwidth,"
#                 "blength,jklength)"
#                 "values(?,?,?,?,?,?,?,?,?,?,?)",
#                 (leibie, LineId, coding, name, typec, node, level, width, pwidth, blength, jklength))
#         ty = fil1.read(6)
#     if (ty.strip() == 'A'):
#         AreaNumber = fil1.readline().strip()
#         for i in range(int(AreaNumber)):
#             area = fil1.readline().split()
#             leibie = ty.strip()
#             LineId = area[0]
#             coding = area[1]
#             name = area[2]
#             typec = area[3]
#             node = area[4]
#             level = area[5]
#             width = area[6]
#             pwidth = area[7]
#             blength = area[8]
#             jklength = area[9]
#             # for j in range(math.ceil(int(coding) / 5)):
#             # lines = fil.readline().split()
#             print(leibie, LineId, coding, name, typec, node, level, width, pwidth, blength, jklength)
#             cur.execute(
#                 "insert into DN05490061_BSX1(leibie,id,coding,name,typec,node,level,width,pwidth,"
#                 "blength,jklength)"
#                 "values(?,?,?,?,?,?,?,?,?,?,?)",
#                 (leibie, LineId, coding, name, typec, node, level, width, pwidth, blength, jklength))
#     cur.close()
#     con.commit()
#     con.close()
#     return True
#
#
# def connectHZB():
#     print("进入")
#     con = sqlite3.connect('tDN05490062.db')  # 连接桥
#     print("Open database successfully")  # 打开成功
#     cur = con.cursor()
#     sql1 = "create table DN05490062_DZB89(leibie varchar(20),AX varchar(20),AY varchar(20) ," \
#            "ZX varchar(20),ZY varchar(20),LNUM varchar(20),LAX varchar(20),LAY varchar(20),ZNUM varchar(20)," \
#            "ZAX varchar(20),ZAY varchar(20),ZZX varchar(20),ZZY varchar(20))"
#     cur.execute(sql1)
#     # res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     # for name in res:
#     # print(name[0])
#     fil5 = open(r'C:\Users\16855\Desktop\HZB.HZB')  # 读文件
#     re = fil5.readline()  # 逐行读入
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     ty5 = fil5.read(6)
#     # print(ty5)
#     if (ty5.strip() == "P"):
#         PointNumber = fil5.readline().strip()
#         print(int(PointNumber))
#         for id in range(int(PointNumber)):
#             point5 = fil5.readline().split()
#             # print(int(len(point)))
#             # print(point3)
#             leibie = ty5.strip()
#             AX = point5[0]
#             AY = point5[1]
#             ZX = point5[2]
#             ZY = point5[3]
#             print(leibie, AX, AY, ZX, ZY)
#             cur.execute(
#                 "insert into DN05490062_DZB89(leibie,AX,AY,ZX,ZY)"
#                 "values(?,?,?,?,?)",
#                 (ty5.strip(), AX, AY, ZX, ZY))
#         ty5 = fil5.read(6)
#     if (ty5.strip() == 'L'):
#         listl = []
#         LineNumber = fil5.readline().strip()
#         leibie = ty5.strip()
#         print(LineNumber)
#         for i in range(int(LineNumber)):  # 从这里开始行位，点数
#             line5 = fil5.readline().split()
#             linenum = line5[0]  # 行位
#             pointnum = line5[1]  # 点数，对数
#             print(linenum, pointnum)
#             if int(int(pointnum) * 2 % 10) == 0:
#                 n = int(int(pointnum) * 2 / 10)
#             else:
#                 n = int(int(pointnum) * 2 / 10 + 1)
#             # print(n)
#             for i in range(n):
#                 fir = 0
#                 sec = 1
#                 re = fil5.readline()
#                 ll = re.split()
#                 # print(ll)
#                 ln = len(ll)
#                 # print(ln)
#                 for id in range(int(int(ln) / 2)):
#                     print(ty5.strip(), linenum, ll[fir], ll[sec])
#                     LNUM = linenum
#                     LAX = ll[fir]
#                     LAY = ll[sec]
#                     cur.execute("insert into DN05490062_DZB89(leibie,LNUM,LAX,LAY)"
#                                 "values(?,?,?,?)",
#                                 (leibie, LNUM, LAX, LAY))
#                     fir += 2
#                     sec += 2
#         ty5 = fil5.read(6)
#     if (ty5.strip() == 'A'):
#         listA = []
#         AreaNumber = fil5.readline().strip()  # 第一行，A坐标有多少块
#         leibie = ty5.strip()  # A标记
#         print(AreaNumber)
#         for i in range(int(AreaNumber)):  # 从这里开始行位，点数
#             area5 = fil5.readline().split()
#             linenum = area5[0]  # 行位
#             ZAX = area5[1]  # 界面横坐标
#             ZAY = area5[2]  # 界面纵坐标
#             JNUM = area5[3]  # 数量
#             print(linenum, ZAX, ZAY, JNUM)
#             if (JNUM == '0'):
#                 continue
#             else:
#                 if (JNUM == '1'):
#                     pointnum = fil5.readline().split()
#                     print(pointnum)
#                     if int(int(pointnum[0]) * 2 % 10) == 0:
#                         n = int(int(pointnum[0]) * 2 / 10)
#                     else:
#                         n = int(int(pointnum[0]) * 2 / 10 + 1)
#                     # print(n)
#                     for i in range(n):
#                         fir = 0
#                         sec = 1
#                         re = fil5.readline()
#                         ll = re.split()
#                         # print(ll)
#                         ln = len(ll)
#                         # print(ln)
#                         for id in range(int(int(ln) / 2)):
#                             print(ty5.strip(), linenum, ll[fir], ll[sec])
#                             ZNUM = linenum
#                             ZZX = ll[fir]
#                             ZZY = ll[sec]
#                             cur.execute("insert into DN05490062_DZB89(leibie,ZNUM,ZAX,ZAY, ZZX, ZZY)"
#                                         "values(?,?,?,?,?,?)",
#                                         (leibie, ZNUM, ZAX, ZAY, ZZX, ZZY))
#                             fir += 2
#                             sec += 2
#                 else:
#                     Mnum = int(JNUM)
#                     while (Mnum):
#                         pointnum = fil5.readline().split()
#                         print(pointnum)
#                         if int(int(pointnum[0]) * 2 % 10) == 0:
#                             n = int(int(pointnum[0]) * 2 / 10)
#                         else:
#                             n = int(int(pointnum[0]) * 2 / 10 + 1)
#                         # print(n)
#                         for i in range(n):
#                             fir = 0
#                             sec = 1
#                             re = fil5.readline()
#                             ll = re.split()
#                             # print(ll)
#                             ln = len(ll)
#                             # print(ln)
#                             for id in range(int(int(ln) / 2)):
#                                 print(ty5.strip(), linenum, ll[fir], ll[sec])
#                                 ZNUM = linenum
#                                 ZZX = ll[fir]
#                                 ZZY = ll[sec]
#                                 cur.execute("insert into DN05490062_DZB89(leibie,ZNUM,ZAX,ZAY, ZZX, ZZY)"
#                                             "values(?,?,?,?,?,?)",
#                                             (leibie, ZNUM, ZAX, ZAY, ZZX, ZZY))
#                                 fir += 2
#                                 sec += 2
#                         Mnum = Mnum - 1
#     cur.close()
#     con.commit()
#     con.close()
#     return True
#
#
# def connectJZB():
#     print("进入")
#     con = sqlite3.connect('tDN05490062.db')  # 连接桥
#     print("Open database successfully")  # 打开成功
#     cur = con.cursor()
#     sql1 = "create table DN05490062_JZB19(leibie varchar(20),AX varchar(20),AY varchar(20) ," \
#            "ZX varchar(20),ZY varchar(20),LNUM varchar(20),LAX varchar(20),LAY varchar(20),ZNUM varchar(20)," \
#            "ZAX varchar(20),ZAY varchar(20),ZZX varchar(20),ZZY varchar(20))"
#     cur.execute(sql1)
#     # res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     # for name in res:
#     # print(name[0])
#     fil5 = open(r'C:\Users\16855\Desktop\JZB.JZB')  # 读文件
#     re = fil5.readline()  # 逐行读入
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     ty5 = fil5.read(6)
#     # print(ty5)
#     if (ty5.strip() == "P"):
#         PointNumber = fil5.readline().strip()
#         print(int(PointNumber))
#         for id in range(int(PointNumber)):
#             point5 = fil5.readline().split()
#             # print(int(len(point)))
#             # print(point3)
#             leibie = ty5.strip()
#             AX = point5[0]
#             AY = point5[1]
#             ZX = point5[2]
#             ZY = point5[3]
#             print(leibie, AX, AY, ZX, ZY)
#             cur.execute(
#                 "insert into DN05490062_JZB19(leibie,AX,AY,ZX,ZY)"
#                 "values(?,?,?,?,?)",
#                 (ty5.strip(), AX, AY, ZX, ZY))
#         ty5 = fil5.read(6)
#     if (ty5.strip() == 'L'):
#         listl = []
#         LineNumber = fil5.readline().strip()
#         leibie = ty5.strip()
#         print(LineNumber)
#         for i in range(int(LineNumber)):  # 从这里开始行位，点数
#             line5 = fil5.readline().split()
#             linenum = line5[0]  # 行位
#             pointnum = line5[1]  # 点数，对数
#             print(linenum, pointnum)
#             if int(int(pointnum) * 2 % 10) == 0:
#                 n = int(int(pointnum) * 2 / 10)
#             else:
#                 n = int(int(pointnum) * 2 / 10 + 1)
#             # print(n)
#             for i in range(n):
#                 fir = 0
#                 sec = 1
#                 re = fil5.readline()
#                 ll = re.split()
#                 # print(ll)
#                 ln = len(ll)
#                 # print(ln)
#                 for id in range(int(int(ln) / 2)):
#                     print(ty5.strip(), linenum, ll[fir], ll[sec])
#                     LNUM = linenum
#                     LAX = ll[fir]
#                     LAY = ll[sec]
#                     cur.execute("insert into DN05490062_JZB19(leibie,LNUM,LAX,LAY)"
#                                 "values(?,?,?,?)",
#                                 (leibie, LNUM, LAX, LAY))
#                     fir += 2
#                     sec += 2
#         ty5 = fil5.read(6)
#     if (ty5.strip() == 'A'):
#         listA = []
#         AreaNumber = fil5.readline().strip()  # 第一行，A坐标有多少块
#         leibie = ty5.strip()  # A标记
#         print(AreaNumber)
#         for i in range(int(AreaNumber)):  # 从这里开始行位，点数
#             area5 = fil5.readline().split()
#             linenum = area5[0]  # 行位
#             ZAX = area5[1]  # 界面横坐标
#             ZAY = area5[2]  # 界面纵坐标
#             JNUM = area5[3]  # 数量
#             print(linenum, ZAX, ZAY, JNUM)
#             if (JNUM == '0'):
#                 continue
#             else:
#                 if (JNUM == '1'):
#                     pointnum = fil5.readline().split()
#                     print(pointnum)
#                     if int(int(pointnum[0]) * 2 % 10) == 0:
#                         n = int(int(pointnum[0]) * 2 / 10)
#                     else:
#                         n = int(int(pointnum[0]) * 2 / 10 + 1)
#                     # print(n)
#                     for i in range(n):
#                         fir = 0
#                         sec = 1
#                         re = fil5.readline()
#                         ll = re.split()
#                         # print(ll)
#                         ln = len(ll)
#                         # print(ln)
#                         for id in range(int(int(ln) / 2)):
#                             print(ty5.strip(), linenum, ll[fir], ll[sec])
#                             ZNUM = linenum
#                             ZZX = ll[fir]
#                             ZZY = ll[sec]
#                             cur.execute("insert into DN05490062_JZB19(leibie,ZNUM,ZAX,ZAY, ZZX, ZZY)"
#                                         "values(?,?,?,?,?,?)",
#                                         (leibie, ZNUM, ZAX, ZAY, ZZX, ZZY))
#                             fir += 2
#                             sec += 2
#                 else:
#                     Mnum = int(JNUM)
#                     while (Mnum):
#                         pointnum = fil5.readline().split()
#                         print(pointnum)
#                         if int(int(pointnum[0]) * 2 % 10) == 0:
#                             n = int(int(pointnum[0]) * 2 / 10)
#                         else:
#                             n = int(int(pointnum[0]) * 2 / 10 + 1)
#                         # print(n)
#                         for i in range(n):
#                             fir = 0
#                             sec = 1
#                             re = fil5.readline()
#                             ll = re.split()
#                             # print(ll)
#                             ln = len(ll)
#                             # print(ln)
#                             for id in range(int(int(ln) / 2)):
#                                 print(ty5.strip(), linenum, ll[fir], ll[sec])
#                                 ZNUM = linenum
#                                 ZZX = ll[fir]
#                                 ZZY = ll[sec]
#                                 cur.execute("insert into DN05490062_JZB19(leibie,ZNUM,ZAX,ZAY, ZZX, ZZY)"
#                                             "values(?,?,?,?,?,?)",
#                                             (leibie, ZNUM, ZAX, ZAY, ZZX, ZZY))
#                                 fir += 2
#                                 sec += 2
#                         Mnum = Mnum - 1
#     cur.close()
#     con.commit()
#     con.close()
#     return True
#
#
# def connectKZB():
#     print("进入")
#     con = sqlite3.connect('tDN05490062.db')  # 连接桥
#     print("Open database successfully")  # 打开成功
#     cur = con.cursor()
#     sql1 = "create table DN05490062_KZB19(leibie varchar(20),AX varchar(20),AY varchar(20) ," \
#            "ZX varchar(20),ZY varchar(20),LNUM varchar(20),LAX varchar(20),LAY varchar(20),ZNUM varchar(20)," \
#            "ZAX varchar(20),ZAY varchar(20),ZZX varchar(20),ZZY varchar(20))"
#     cur.execute(sql1)
#     # res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     # for name in res:
#     # print(name[0])
#     fil5 = open(r'C:\Users\16855\Desktop\KZB.KZB')  # 读文件
#     re = fil5.readline()  # 逐行读入
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     ty5 = fil5.read(6)
#     # print(ty5)
#     if (ty5.strip() == "P"):
#         PointNumber = fil5.readline().strip()
#         print(int(PointNumber))
#         for id in range(int(PointNumber)):
#             point5 = fil5.readline().split()
#             # print(int(len(point)))
#             # print(point3)
#             leibie = ty5.strip()
#             AX = point5[0]
#             AY = point5[1]
#             ZX = point5[2]
#             ZY = point5[3]
#             print(leibie, AX, AY, ZX, ZY)
#             cur.execute(
#                 "insert into DN05490062_KZB19(leibie,AX,AY,ZX,ZY)"
#                 "values(?,?,?,?,?)",
#                 (ty5.strip(), AX, AY, ZX, ZY))
#         ty5 = fil5.read(6)
#     if (ty5.strip() == 'L'):
#         listl = []
#         LineNumber = fil5.readline().strip()
#         leibie = ty5.strip()
#         print(LineNumber)
#         for i in range(int(LineNumber)):  # 从这里开始行位，点数
#             line5 = fil5.readline().split()
#             linenum = line5[0]  # 行位
#             pointnum = line5[1]  # 点数，对数
#             print(linenum, pointnum)
#             if int(int(pointnum) * 2 % 10) == 0:
#                 n = int(int(pointnum) * 2 / 10)
#             else:
#                 n = int(int(pointnum) * 2 / 10 + 1)
#             # print(n)
#             for i in range(n):
#                 fir = 0
#                 sec = 1
#                 re = fil5.readline()
#                 ll = re.split()
#                 # print(ll)
#                 ln = len(ll)
#                 # print(ln)
#                 for id in range(int(int(ln) / 2)):
#                     print(ty5.strip(), linenum, ll[fir], ll[sec])
#                     LNUM = linenum
#                     LAX = ll[fir]
#                     LAY = ll[sec]
#                     cur.execute("insert into DN05490062_KZB19(leibie,LNUM,LAX,LAY)"
#                                 "values(?,?,?,?)",
#                                 (leibie, LNUM, LAX, LAY))
#                     fir += 2
#                     sec += 2
#         ty5 = fil5.read(6)
#     if (ty5.strip() == 'A'):
#         listA = []
#         AreaNumber = fil5.readline().strip()  # 第一行，A坐标有多少块
#         leibie = ty5.strip()  # A标记
#         print(AreaNumber)
#         for i in range(int(AreaNumber)):  # 从这里开始行位，点数
#             area5 = fil5.readline().split()
#             linenum = area5[0]  # 行位
#             ZAX = area5[1]  # 界面横坐标
#             ZAY = area5[2]  # 界面纵坐标
#             JNUM = area5[3]  # 数量
#             print(linenum, ZAX, ZAY, JNUM)
#             if (JNUM == '0'):
#                 continue
#             else:
#                 if (JNUM == '1'):
#                     pointnum = fil5.readline().split()
#                     print(pointnum)
#                     if int(int(pointnum[0]) * 2 % 10) == 0:
#                         n = int(int(pointnum[0]) * 2 / 10)
#                     else:
#                         n = int(int(pointnum[0]) * 2 / 10 + 1)
#                     # print(n)
#                     for i in range(n):
#                         fir = 0
#                         sec = 1
#                         re = fil5.readline()
#                         ll = re.split()
#                         # print(ll)
#                         ln = len(ll)
#                         # print(ln)
#                         for id in range(int(int(ln) / 2)):
#                             print(ty5.strip(), linenum, ll[fir], ll[sec])
#                             ZNUM = linenum
#                             ZZX = ll[fir]
#                             ZZY = ll[sec]
#                             cur.execute("insert into DN05490062_KZB19(leibie,ZNUM,ZAX,ZAY, ZZX, ZZY)"
#                                         "values(?,?,?,?,?,?)",
#                                         (leibie, ZNUM, ZAX, ZAY, ZZX, ZZY))
#                             fir += 2
#                             sec += 2
#                 else:
#                     Mnum = int(JNUM)
#                     while (Mnum):
#                         pointnum = fil5.readline().split()
#                         print(pointnum)
#                         if int(int(pointnum[0]) * 2 % 10) == 0:
#                             n = int(int(pointnum[0]) * 2 / 10)
#                         else:
#                             n = int(int(pointnum[0]) * 2 / 10 + 1)
#                         # print(n)
#                         for i in range(n):
#                             fir = 0
#                             sec = 1
#                             re = fil5.readline()
#                             ll = re.split()
#                             # print(ll)
#                             ln = len(ll)
#                             # print(ln)
#                             for id in range(int(int(ln) / 2)):
#                                 print(ty5.strip(), linenum, ll[fir], ll[sec])
#                                 ZNUM = linenum
#                                 ZZX = ll[fir]
#                                 ZZY = ll[sec]
#                                 cur.execute("insert into DN05490062_KZB19(leibie,ZNUM,ZAX,ZAY, ZZX, ZZY)"
#                                             "values(?,?,?,?,?,?)",
#                                             (leibie, ZNUM, ZAX, ZAY, ZZX, ZZY))
#                                 fir += 2
#                                 sec += 2
#                         Mnum = Mnum - 1
#     cur.close()
#     con.commit()
#     con.close()
#     return True
#
#
# def connectDZB():
#     print("进入")
#     con = sqlite3.connect('data.db')  # 连接桥
#     print("Open database successfully")  # 打开成功
#     cur = con.cursor()
#     sql = 'drop table if exists DN05490062_DZB19'
#     cur.execute(sql)
#     sql1 = "create table DN05490062_DZB19(leibie varchar(20),AX varchar(20),AY varchar(20) ," \
#            "ZX varchar(20),ZY varchar(20),LNUM varchar(20),LAX varchar(20),LAY varchar(20),ZNUM varchar(20)," \
#            "ZAX varchar(20),ZAY varchar(20),ZZX varchar(20),ZZY varchar(20))"
#     cur.execute(sql1)
#     # res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     # for name in res:
#     # print(name[0])
#     fil5 = open(r'D:\DN05490062.DZB')  # 读文件
#     re = fil5.readline()  # 逐行读入
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     ty5 = fil5.read(6)
#     # print(ty5)
#     if (ty5.strip() == "P"):
#         PointNumber = fil5.readline().strip()
#         print(int(PointNumber))
#         for id in range(int(PointNumber)):
#             point5 = fil5.readline().split()
#             # print(int(len(point)))
#             # print(point3)
#             leibie = ty5.strip()
#             AX = point5[0]
#             AY = point5[1]
#             ZX = point5[2]
#             ZY = point5[3]
#             print(leibie, AX, AY, ZX, ZY)
#             cur.execute(
#                 "insert into DN05490062_DZB19(leibie,AX,AY,ZX,ZY)"
#                 "values(?,?,?,?,?)",
#                 (ty5.strip(), AX, AY, ZX, ZY))
#         ty5 = fil5.read(6)
#     if (ty5.strip() == 'L'):
#         listl = []
#         LineNumber = fil5.readline().strip()
#         leibie = ty5.strip()
#     #    print(LineNumber)
#         for i in range(int(LineNumber)):  # 从这里开始行位，点数
#             line5 = fil5.readline().split()
#             linenum = line5[0]  # 行位
#             pointnum = line5[1]  # 点数，对数
#     #        print(linenum, pointnum)
#             if int(int(pointnum) * 2 % 10) == 0:
#                 n = int(int(pointnum) * 2 / 10)
#             else:
#                 n = int(int(pointnum) * 2 / 10 + 1)
#             # print(n)
#             for i in range(n):
#                 fir = 0
#                 sec = 1
#                 re = fil5.readline()
#                 ll = re.split()
#                 # print(ll)
#                 ln = len(ll)
#                 # print(ln)
#                 for id in range(int(int(ln) / 2)):
#                     print(ty5.strip(), linenum, ll[fir], ll[sec])
#                     LNUM = linenum
#                     LAX = ll[fir]
#                     LAY = ll[sec]
#                     cur.execute("insert into DN05490062_DZB19(leibie,LNUM,LAX,LAY)"
#                                 "values(?,?,?,?)",
#                                 (leibie, LNUM, LAX, LAY))
#                     fir += 2
#                     sec += 2
#         ty5 = fil5.read(6)
#     if (ty5.strip() == 'A'):
#         listA = []
#         AreaNumber = fil5.readline().strip()  # 第一行，A坐标有多少块
#         leibie = ty5.strip()  # A标记
#      #   print(AreaNumber)
#         for i in range(int(AreaNumber)):  # 从这里开始行位，点数
#             area5 = fil5.readline().split()
#             linenum = area5[0]  # 行位
#             ZAX = area5[1]  # 界面横坐标
#             ZAY = area5[2]  # 界面纵坐标
#             JNUM = area5[3]  # 数量
#       #      print(linenum, ZAX, ZAY, JNUM)
#             if (JNUM == '0'):
#                 continue
#             else:
#                 if (JNUM == '1'):
#                     pointnum = fil5.readline().split()
#        #             print(pointnum)
#                     if int(int(pointnum[0]) * 2 % 10) == 0:
#                         n = int(int(pointnum[0]) * 2 / 10)
#                     else:
#                         n = int(int(pointnum[0]) * 2 / 10 + 1)
#                     # print(n)
#                     for i in range(n):
#                         fir = 0
#                         sec = 1
#                         re = fil5.readline()
#                         ll = re.split()
#                         # print(ll)
#                         ln = len(ll)
#                         # print(ln)
#                         for id in range(int(int(ln) / 2)):
#         #                    print(ty5.strip(), linenum, ll[fir], ll[sec])
#                             ZNUM = linenum
#                             ZZX = ll[fir]
#                             ZZY = ll[sec]
#                             cur.execute("insert into DN05490062_DZB19(leibie,ZNUM,ZAX,ZAY, ZZX, ZZY)"
#                                         "values(?,?,?,?,?,?)",
#                                         (leibie, ZNUM, ZAX, ZAY, ZZX, ZZY))
#                             fir += 2
#                             sec += 2
#                 else:
#                     Mnum = int(JNUM)
#                     while (Mnum):
#                         pointnum = fil5.readline().split()
#          #               print(pointnum)
#                         if int(int(pointnum[0]) * 2 % 10) == 0:
#                             n = int(int(pointnum[0]) * 2 / 10)
#                         else:
#                             n = int(int(pointnum[0]) * 2 / 10 + 1)
#                         # print(n)
#                         for i in range(n):
#                             fir = 0
#                             sec = 1
#                             re = fil5.readline()
#                             ll = re.split()
#                             # print(ll)
#                             ln = len(ll)
#                             # print(ln)
#                             for id in range(int(int(ln) / 2)):
#                                 print(ty5.strip(), linenum, ll[fir], ll[sec])
#                                 ZNUM = linenum
#                                 ZZX = ll[fir]
#                                 ZZY = ll[sec]
#                                 cur.execute("insert into DN05490062_DZB19(leibie,ZNUM,ZAX,ZAY, ZZX, ZZY)"
#                                             "values(?,?,?,?,?,?)",
#                                             (leibie, ZNUM, ZAX, ZAY, ZZX, ZZY))
#                                 fir += 2
#                                 sec += 2
#                         Mnum = Mnum - 1
#     cur.close()
#     con.commit()
#     con.close()
#     return True
#
#
# def connectRZB():
#     print("进入")
#     con = sqlite3.connect('tDN05490062.db')  # 连接桥
#     print("Open database successfully")  # 打开成功
#     cur = con.cursor()
#     sql = 'drop table if exists DN05490061_RZB19'
#     cur.execute(sql)
#     sql1 = "create table DN05490061_RZB19(leibie varchar(20),AX varchar(20),AY varchar(20) ," \
#            "ZX varchar(20),ZY varchar(20),LNUM varchar(20),LAX varchar(20),LAY varchar(20),ZNUM varchar(20)," \
#            "ZAX varchar(20),ZAY varchar(20),ZZX varchar(20),ZZY varchar(20))"
#     cur.execute(sql1)
#     # res = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     # for name in res:
#     # print(name[0])
#     fil5 = open(r'C:\Users\16855\Desktop\LZB.LZB')  # 读文件
#     re = fil5.readline()  # 逐行读入
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     ty5 = fil5.read(6)
#     # print(ty5)
#     if (ty5.strip() == "P"):
#         PointNumber = fil5.readline().strip()
#         print(int(PointNumber))
#         for id in range(int(PointNumber)):
#             point5 = fil5.readline().split()
#             # print(int(len(point)))
#             # print(point3)
#             leibie = ty5.strip()
#             AX = point5[0]
#             AY = point5[1]
#             ZX = point5[2]
#             ZY = point5[3]
#             print(leibie, AX, AY, ZX, ZY)
#             cur.execute(
#                 "insert into DN05490061_RZB19(leibie,AX,AY,ZX,ZY)"
#                 "values(?,?,?,?,?)",
#                 (ty5.strip(), AX, AY, ZX, ZY))
#         ty5 = fil5.read(6)
#     if (ty5.strip() == 'L'):
#         listl = []
#         LineNumber = fil5.readline().strip()
#         leibie = ty5.strip()
#         #print(LineNumber)
#         for i in range(int(LineNumber)):  # 从这里开始行位，点数
#             line5 = fil5.readline().split()
#             linenum = line5[0]  # 行位
#             pointnum = line5[1]  # 点数，对数
#             print(linenum, pointnum)
#             if int(int(pointnum) * 2 % 10) == 0:
#                 n = int(int(pointnum) * 2 / 10)
#             else:
#                 n = int(int(pointnum) * 2 / 10 + 1)
#             # print(n)
#             for i in range(n):
#                 fir = 0
#                 sec = 1
#                 re = fil5.readline()
#                 ll = re.split()
#                 # print(ll)
#                 ln = len(ll)
#                 # print(ln)
#                 for id in range(int(int(ln) / 2)):
#          #           print(ty5.strip(), linenum, ll[fir], ll[sec])
#                     LNUM = linenum
#                     LAX = ll[fir]
#                     LAY = ll[sec]
#                     cur.execute("insert into DN05490061_RZB19(leibie,LNUM,LAX,LAY)"
#                                 "values(?,?,?,?)",
#                                 (leibie, LNUM, LAX, LAY))
#                     fir += 2
#                     sec += 2
#         ty5 = fil5.read(6)
#     if (ty5.strip() == 'A'):
#         listA = []
#         AreaNumber = fil5.readline().strip()  # 第一行，A坐标有多少块
#         leibie = ty5.strip()  # A标记
#         #print(AreaNumber)
#         for i in range(int(AreaNumber)):  # 从这里开始行位，点数
#             area5 = fil5.readline().split()
#             linenum = area5[0]  # 行位
#             ZAX = area5[1]  # 界面横坐标
#             ZAY = area5[2]  # 界面纵坐标
#             JNUM = area5[3]  # 数量
#            # print(linenum, ZAX, ZAY, JNUM)
#             if (JNUM == '0'):
#                 continue
#             else:
#                 if (JNUM == '1'):
#                     pointnum = fil5.readline().split()
#                 #    print(pointnum)
#                     if int(int(pointnum[0]) * 2 % 10) == 0:
#                         n = int(int(pointnum[0]) * 2 / 10)
#                     else:
#                         n = int(int(pointnum[0]) * 2 / 10 + 1)
#                     # print(n)
#                     for i in range(n):
#                         fir = 0
#                         sec = 1
#                         re = fil5.readline()
#                         ll = re.split()
#                         # print(ll)
#                         ln = len(ll)
#                         # print(ln)
#                         for id in range(int(int(ln) / 2)):
#                             print(ty5.strip(), linenum, ll[fir], ll[sec])
#                             ZNUM = linenum
#                             ZZX = ll[fir]
#                             ZZY = ll[sec]
#                             cur.execute("insert into DN05490061_RZB19(leibie,ZNUM,ZAX,ZAY, ZZX, ZZY)"
#                                         "values(?,?,?,?,?,?)",
#                                         (leibie, ZNUM, ZAX, ZAY, ZZX, ZZY))
#                             fir += 2
#                             sec += 2
#                 else:
#                     Mnum = int(JNUM)
#                     while (Mnum):
#                         pointnum = fil5.readline().split()
#                  #       print(pointnum)
#                         if int(int(pointnum[0]) * 2 % 10) == 0:
#                             n = int(int(pointnum[0]) * 2 / 10)
#                         else:
#                             n = int(int(pointnum[0]) * 2 / 10 + 1)
#                         # print(n)
#                         for i in range(n):
#                             fir = 0
#                             sec = 1
#                             re = fil5.readline()
#                             ll = re.split()
#                             # print(ll)
#                             ln = len(ll)
#                             # print(ln)
#                             for id in range(int(int(ln) / 2)):
#                                 print(ty5.strip(), linenum, ll[fir], ll[sec])
#                                 ZNUM = linenum
#                                 ZZX = ll[fir]
#                                 ZZY = ll[sec]
#                                 cur.execute("insert into DN05490061_RZB19(leibie,ZNUM,ZAX,ZAY, ZZX, ZZY)"
#                                             "values(?,?,?,?,?,?)",
#                                             (leibie, ZNUM, ZAX, ZAY, ZZX, ZZY))
#                                 fir += 2
#                                 sec += 2
#                         Mnum = Mnum - 1
#     cur.close()
#     con.commit()
#     con.close()
#     return True
#
# def test():
#     b = 2
#     print(b)
# if __name__ == '__main__':
#     print("start")
#     # connectRSX()
#     # connectLSX()
#     # connectBSX()
#     # connectHZB()
#     # connectJZB()
#     # connectKZB()
#     # connectLZB()
#     # connectRZB()
#     #connectDZB()
#     test()

'''
name = ['137贝山桥', '151罗绵桥']
cla = 'D'
con = sqlite3.connect('data.db')
cur = con.cursor()
id = []

sql = 'select id,name from class' + cla
cur.execute(sql)
r = cur.fetchall()
for i in name:
    for j in r:
        if str(j[0])+j[1] == i:
            d = j[0]
            id.append(d)
            #加入类型
print(id)
'''

# def if_inPoly(polygon, Points):
#     line = geometry.LineString(polygon)
#     point = geometry.Point(Points)
#     polygon = geometry.Polygon(line)
#
#     return polygon.contains(point)
#
#
# con = sqlite3.connect('tDN05490062.db')
# cur = con.cursor()
# leixing = ['P', 'L']
# id = [137, 151]
# re = []
# for i in range(0, 2):
#     if leixing[i] == 'P':
#         sql = 'select AY,ZX from DN05490062_DZB19 where leibie="P" and AX=' + str(id[i])
#         cur.execute(sql)
#         result = cur.fetchall()
#         re.append(result)
#         # print(result)
#     elif leixing[i] == 'L':
#         sql = 'select LAX,LAY from DN05490062_DZB19 where leibie="L" and LNUM=' + str(id[i])
#         cur.execute(sql)
#         result = cur.fetchall()
#         re.append(result)
#         # print(result)
#     elif leixing[i] == 'A':
#         sql = 'select ZAX,ZAY from DN05490062_DZB19 where leibie="A" and ZNUM=' + str(id[i])
#         cur.execute(sql)
#         result = cur.fetchall()
#         re.append(result)
# coor = []
# xsum = 0.0
# ysum = 0.0
# print(xsum.__class__)
# for i in re:
#     # print(i)
#     for j in range(0, len(i)):
#         # print(float(i[j][0]))
#
#         xsum += float(i[j][0])
#         ysum += float(i[j][1])
#     # print(len(i))
#     x = xsum / len(i)
#     y = ysum / len(i)
#     coor.append((x, y))
# # print(coor)
# dx = 0.0
# dy = 0.0
# for point in coor:
#     dx = point[0] - dx
#     dy = point[1] - dy
# length = math.sqrt(pow(dx, 2) + pow(dy, 2))
# # 两点的代表坐标
# print(coor)
# width = length / 3
#
# # 可直接确定四个点的情况
# vertex = []
# if coor[0][0] == coor[1][0]:
#     vertex.append((float(coor[0][0]) - width / 2, coor[0][1]))
#     vertex.append((float(coor[0][0]) + width / 2, coor[0][1]))
#     vertex.append((float(coor[1][0]) + width / 2, coor[1][1]))
#     vertex.append((float(coor[1][0]) - width / 2, coor[1][1]))
# elif coor[0][1] == coor[1][1]:
#     vertex.append((coor[0][0], float(coor[0][1]) + width/2))
#     vertex.append((coor[0][0], float(coor[0][1]) - width/2))
#     vertex.append((coor[1][0], float(coor[1][1]) - width/2))
#     vertex.append((coor[1][0], float(coor[1][1]) + width/2))
# else:
#     k = dy/dx
#     if k > 0:
#         angle = math.atan(k)
#         temp = width / 2
#         ddx = temp * math.sin(angle)
#         ddy = temp * math.cos(angle)
#         vertex.append((float(coor[0][0]) + ddx, float(coor[0][1]) - ddy))
#         vertex.append((float(coor[0][0]) - ddx, float(coor[0][1]) + ddy))
#         vertex.append((float(coor[1][0]) - ddx, float(coor[1][1]) + ddy))
#         vertex.append((float(coor[1][0]) + ddx, float(coor[1][1]) - ddy))
#     elif k < 0:
#         k = abs(k)
#         angle = math.atan(k)
#         temp = width / 2
#         ddx = temp * math.sin(angle)
#         ddy = temp * math.cos(angle)
#         vertex.append((float(coor[0][0]) - ddx, float(coor[0][1]) - ddy))
#         vertex.append((float(coor[0][0]) + ddx, float(coor[0][1]) + ddy))
#         vertex.append((float(coor[1][0]) + ddx, float(coor[1][1]) + ddy))
#         vertex.append((float(coor[1][0]) - ddx, float(coor[1][1]) - ddy))
# # 矩形框顶点坐标
# print(vertex)
#
#
# # square = [(1, 5), (9, 9), (3, 3), (7, 11)]  # 多边形坐标
# # pt1 = (3, 3)  # 点坐标
# # pt2 = (3, 6.9)
# # print(if_inPoly(square, pt1))
# # print(if_inPoly(square, pt2))
#
#
# def connection():
#     # 前端添加上传文件，后端用于生成表格
#     # 建一个文件表，用于记录读过的表，下次读取时用于判断是否读过该文件，若重复可添加二次确认是否覆盖或者已读过的文件跳过不读
#     # 文件表可同时用于动态生成表格页面中的第一个下拉框内容（已有文件）
#
#     con = sqlite3.connect('tDN05490062.db')      #连接桥
# # s = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name = 'classD'"
#
#     cur = con.cursor()
# # cur.execute(s)
#
#     # 存放读过的文件名
#     sql2 = "create table if not exists document(id INTEGER PRIMARY KEY,name varchar(50))"
#     cur.execute(sql2)
#     sql3 = 'select name from document'
#     cur.execute(sql3)
#     resu = cur.fetchall()
#     if 'DN05490062' not in resu:
#         sql4 = 'insert into document values (NULL ,"DN05490062")'
#         cur.execute(sql4)
#
#
#
#     sql1 = "drop table if exists DN05490062_DSX"
#     cur.execute(sql1)
#     sql = "create table DN05490062_DSX( id int primary key,leixing varchar(20),coding varchar(20) ,name varchar(20),typec varchar(20),node varchar(20),level varchar(20),width varchar(20),pwidth varchar(20),blength varchar(20),jklength varchar(20),ton varchar(20),kilo varchar(20),bigao varchar(20),cmonth int,wdeep varchar(20),dizhi varchar(20),minbj varchar(20),maxzb varchar(20),spec varchar(20),zjzz varchar(20),wgbzz varchar(20))"
#     # if cur.fetchall()[0][0] == 0:
#     cur.execute(sql)
#     fil = open(r'C:\Users\Administrator.000\Desktop\DN05490062.DSX', encoding="utf-8")  # 读文件
#     re = fil.readline() # 逐行读入
#     re = fil.readline()
#     re = fil.readline()
#     re = fil.readline()
#     re = fil.readline()
#     re = fil.readline()
#     ty = fil.read(6)
#     Pleibie = 'P'
#     Lleibie = 'L'
#     Aleibie = "A"
#     if ty.strip() == "P":
#         PointNumber = fil.readline().strip()
#         # print(int(PointNumber))
#         for id in range(int(PointNumber)):
#             point = fil.readline().split()
#             # print(int(len(point)))
#             # print(point)
#
#             pointId = point[0]
#             coding = point[1]
#             name = point[2]
#             typec  = point[3]
#             node = point[4]
#             level = point[5]
#             width = point[6]
#             pwidth = point[7]
#             blength = point[8]
#             jklength = point[9]
#             ton = point[10]
#             kilo = point[11]
#             bigao = point[12]
#             cmonth = point[13]
#             wdeep = point[14]
#             dizhi = point[15]
#             minbj = point[16]
#             maxzb = point[17]
#             spec = point[18]
#             zjzz = point[19]
#             wgbzz = point[20]
#             # print(pointId,coding,name,typec,node,level,width,pwidth,blength,jklength,ton,kilo,bigao,cmonth,wdeep,dizhi,minbj,maxzb,spec,zjzz,wgbzz)
#             cur.execute("insert into DN05490062_DSX(id,leixing,coding,name,typec,node,level,width,pwidth,blength,jklength,ton,kilo,bigao,cmonth,wdeep,dizhi,minbj,maxzb,spec,zjzz,wgbzz)values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(pointId,Pleibie,coding,name,typec,node,level,width,pwidth,blength,jklength,ton,kilo,bigao,cmonth,wdeep,dizhi,minbj,maxzb,spec,zjzz,wgbzz))
#             ty = fil.read(6)
#     if ty.strip() == 'L':
#         LineNumber = fil.readline().strip()
#         for i in range(int(LineNumber)):
#             line = fil.readline().split()
#
#             LineId = line[0]
#             coding = line[1]
#             name = line[2]
#             typec = line[3]
#             node = line[4]
#             level = line[5]
#             width = line[6]
#             pwidth = line[7]
#             blength = line[8]
#             jklength = line[9]
#             ton = line[10]
#             kilo = line[11]
#             bigao = line[12]
#             cmonth = line[13]
#             wdeep = line[14]
#             dizhi = line[15]
#             minbj = line[16]
#             maxzb = line[17]
#             spec = line[18]
#             zjzz = line[19]
#             wgbzz = line[20]
#             # for j in range(math.ceil(int(coding) / 5)):
#             # lines = fil.readline().split()
#             # print(LineId,coding,name,typec,node,level,width,pwidth,blength,jklength,ton,kilo,bigao,cmonth,wdeep,dizhi,minbj,maxzb,spec,zjzz,wgbzz)
#             cur.execute(
#                 "insert into DN05490062_DSX(id,leixing,coding,name,typec,node,level,width,pwidth,blength,jklength,ton,kilo,bigao,cmonth,wdeep,dizhi,minbj,maxzb,spec,zjzz,wgbzz)values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
#                 ( LineId,Lleibie, coding, name, typec, node, level, width, pwidth, blength, jklength, ton, kilo, bigao, cmonth,
#                  wdeep, dizhi, minbj, maxzb, spec, zjzz, wgbzz))
#     cur.close()
#     con.commit()
#     con.close()
#
#
# def connectDZB():
#
#     con = sqlite3.connect('tDN05490062.db')  # 连接桥
#
#     cur = con.cursor()
#     sql = 'drop table if exists DN05490062_DZB'
#     cur.execute(sql)
#     sql1 = "create table DN05490062_DZB(leibie varchar(20),AX varchar(20),AY varchar(20) ," \
#            "ZX varchar(20),ZY varchar(20),LNUM varchar(20),LAX varchar(20),LAY varchar(20),ZNUM varchar(20)," \
#            "ZAX varchar(20),ZAY varchar(20),ZZX varchar(20),ZZY varchar(20))"
#     cur.execute(sql1)
#
#     fil5 = open(r'D:\DN054900622.DZB')  # 读文件
#     re = fil5.readline()  # 逐行读入
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     re = fil5.readline()
#     ty5 = fil5.read(6)
#     # print(ty5)
#     if ty5.strip() == "P":
#         PointNumber = fil5.readline().strip()
#         # print(int(PointNumber))
#         for id in range(int(PointNumber)):
#             point5 = fil5.readline().split()
#             # print(int(len(point)))
#             # print(point3)
#             leibie = ty5.strip()
#             AX = point5[0]
#             AY = point5[1]
#             ZX = point5[2]
#             ZY = point5[3]
#             # print(leibie, AX, AY, ZX, ZY)
#             cur.execute(
#                 "insert into DN05490062_DZB(leibie,AX,AY,ZX,ZY)"
#                 "values(?,?,?,?,?)",
#                 (ty5.strip(), AX, AY, ZX, ZY))
#         ty5 = fil5.read(6)
#     if ty5.strip() == 'L':
#         listl = []
#         LineNumber = fil5.readline().strip()
#         leibie = ty5.strip()
#         # print(LineNumber)
#         for i in range(int(LineNumber)):  # 从这里开始行位，点数
#             line5 = fil5.readline().split()
#             linenum = line5[0]  # 行位
#             pointnum = line5[1]  # 点数，对数
#             # print(linenum, pointnum)
#             if int(int(pointnum) * 2 % 10) == 0:
#                 n = int(int(pointnum) * 2 / 10)
#             else:
#                 n = int(int(pointnum) * 2 / 10 + 1)
#             # print(n)
#             for i in range(n):
#                 fir = 0
#                 sec = 1
#                 re = fil5.readline()
#                 ll = re.split()
#                 # print(ll)
#                 ln = len(ll)
#                 # print(ln)
#                 for id in range(int(int(ln) / 2)):
#                     print(ty5.strip(), linenum, ll[fir], ll[sec])
#                     LNUM = linenum
#                     LAX = ll[fir]
#                     LAY = ll[sec]
#                     cur.execute("insert into DN05490062_DZB(leibie,LNUM,LAX,LAY)"
#                                 "values(?,?,?,?)",
#                                 (leibie, LNUM, LAX, LAY))
#                     fir += 2
#                     sec += 2
#         ty5 = fil5.read(6)
#     if ty5.strip() == 'A':
#         listA = []
#         AreaNumber = fil5.readline().strip()  # 第一行，A坐标有多少块
#         leibie = ty5.strip()  # A标记
#         # print(AreaNumber)
#         for i in range(int(AreaNumber)):  # 从这里开始行位，点数
#             area5 = fil5.readline().split()
#             linenum = area5[0]  # 行位
#             ZAX = area5[1]  # 界面横坐标
#             ZAY = area5[2]  # 界面纵坐标
#             JNUM = area5[3]  # 数量
#             # print(linenum, ZAX, ZAY, JNUM)
#             if JNUM == '0':
#                 continue
#             else:
#                 if JNUM == '1':
#                     pointnum = fil5.readline().split()
#                     # print(pointnum)
#                     if int(int(pointnum[0]) * 2 % 10) == 0:
#                         n = int(int(pointnum[0]) * 2 / 10)
#                     else:
#                         n = int(int(pointnum[0]) * 2 / 10 + 1)
#                     # print(n)
#                     for i in range(n):
#                         fir = 0
#                         sec = 1
#                         re = fil5.readline()
#                         ll = re.split()
#                         # print(ll)
#                         ln = len(ll)
#                         # print(ln)
#                         for id in range(int(int(ln) / 2)):
#                             # print(ty5.strip(), linenum, ll[fir], ll[sec])
#                             ZNUM = linenum
#                             ZZX = ll[fir]
#                             ZZY = ll[sec]
#                             cur.execute("insert into DN05490062_DZB(leibie,ZNUM,ZAX,ZAY, ZZX, ZZY)"
#                                         "values(?,?,?,?,?,?)",
#                                         (leibie, ZNUM, ZAX, ZAY, ZZX, ZZY))
#                             fir += 2
#                             sec += 2
#                 else:
#                     Mnum = int(JNUM)
#                     while (Mnum):
#                         pointnum = fil5.readline().split()
#                         # print(pointnum)
#                         if int(int(pointnum[0]) * 2 % 10) == 0:
#                             n = int(int(pointnum[0]) * 2 / 10)
#                         else:
#                             n = int(int(pointnum[0]) * 2 / 10 + 1)
#                         # print(n)
#                         for i in range(n):
#                             fir = 0
#                             sec = 1
#                             re = fil5.readline()
#                             ll = re.split()
#                             # print(ll)
#                             ln = len(ll)
#                             # print(ln)
#                             for id in range(int(int(ln) / 2)):
#                                 print(ty5.strip(), linenum, ll[fir], ll[sec])
#                                 ZNUM = linenum
#                                 ZZX = ll[fir]
#                                 ZZY = ll[sec]
#                                 cur.execute("insert into DN05490062_DZB(leibie,ZNUM,ZAX,ZAY, ZZX, ZZY)"
#                                             "values(?,?,?,?,?,?)",
#                                             (leibie, ZNUM, ZAX, ZAY, ZZX, ZZY))
#                                 fir += 2
#                                 sec += 2
#                         Mnum = Mnum - 1
#     cur.close()
#     con.commit()
#     con.close()
# # connection()
# # connectDZB()
#
#
# con = sqlite3.connect('tDN05490062.db')
# cur = con.cursor()
# sql = 'select * from DN05490062_DZB'
# cur.execute(sql)
# # 遍历坐标，判断是否满足条件
# result = cur.fetchall()
# pinnerpoint = []
# linnerpoint = []
# ainnerpoint = []
# for i in result:
#     # 分PLA三种情况分别把对应id存入对应数组，以便回属性表查找对应点
#     if i[0] == 'P':
#         p = (float(i[2]), float(i[3]))
#         if if_inPoly(vertex, p):
#             pinnerpoint.append(i[1])
#     elif i[0] == 'L':
#         if i[5] not in linnerpoint:
#             p = (float(i[6]), float(i[7]))
#             if if_inPoly(vertex, p):
#                 linnerpoint.append(i[5])
#     elif i[0] == 'A':
#         if i[8] not in ainnerpoint:
#             p = (float(i[9]), float(i[10]))
#             if if_inPoly(vertex, p):
#                 ainnerpoint.append(i[8])
# # 符合条件的三类点的id值
# print(pinnerpoint)
# print(linnerpoint)
# print(ainnerpoint)
# # 在属性表寻找对应点的属性（可存id，name，级别，编码对应的类型）
# sql3 = 'select * from DN05490062_DSX'
# cur.execute(sql3)
# result_sx = cur.fetchall()
# # 新建数组用于保存最终符合要求的点及属性
# RealInner = list()
# for i in result_sx:
#     #print(i)
#     if i[1] == 'P':
#         if str(i[0]) in pinnerpoint:
#             temp = list()
#             temp.append((i[0], i[2], i[3], i[6]))
#             RealInner.append(temp)
#     elif i[1] == 'L':
#         if str(i[1]) in linnerpoint:
#             temp = list()
#             temp.append((i[0], i[2], i[3], i[6]))
#             RealInner.append(temp)
#     elif i[1] == 'A':
#         if str(i[1]) in ainnerpoint:
#             temp = list()
#             temp.append((i[0], i[2], i[3], i[6]))
#             RealInner.append(temp)
# print(RealInner)
# sql4 = 'select name from DN05490062_DSX'
# cur = con.cursor()
# cur.execute(sql4)
# # col_name_list = [tuple[0] for tuple in cur.description]
# # print(col_name_list)
# reee = cur.fetchall()
# print(reee)
# for doc in reee:
#     print(doc[0])


# def getdocumentname():
#
#     data = []
#     # entity = request.POST.get("entity", None)
#     # entity = str(entity)
#     con = sqlite3.connect('tDN05490062.db')
#     cur = con.cursor()
#     sql = 'select name from document'
#     cur.execute(sql)
#     result = cur.fetchall()
#     # col_name_list = [tuple[0] for tuple in cur.description]
#     j = 0
#     for i in result:
#         doc = dict()
#
#         doc['ID'] = j
#         doc['TAGNAME'] = i
#         j += 1
#         data.append(doc)
#     data = json.dumps(data, ensure_ascii=False)
#     print(data)
#
#
# def connection():
#     # 前端添加上传文件，后端用于生成表格
#     # 建一个文件表，用于记录读过的表，下次读取时用于判断是否读过该文件，若重复可添加二次确认是否覆盖或者已读过的文件跳过不读
#     # 文件表可同时用于动态生成表格页面中的第一个下拉框内容（已有文件）
#
#     con = sqlite3.connect('data.db')      # 连接桥
#     # s = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name = 'classD'"
#
#     cur = con.cursor()
#     # cur.execute(s)
#     # sql = 'drop table if exists document'
#     # cur.execute(sql)
#     # 存放读过的文件名
#     sql2 = "create table if not exists document(id INTEGER PRIMARY KEY,name varchar(50))"
#     cur.execute(sql2)
#     sql3 = 'select name from document'
#     cur.execute(sql3)
#     resu = cur.fetchall()
#     print(resu)
#     sql4 = 'insert into document values (NULL ,"DN05490062")'
#     if len(resu) == 0:
#         cur.execute(sql4)
#         cur.execute(sql3)
#         re = cur.fetchall()
#         print(re)
#     # if 'DN05490062' not in resu:
#     else:
#         count = 0
#         for i, in resu:
#             if i == 'DN05490062':
#                 break
#             else:
#                 count += 1
#
#         if count == len(resu):
#             cur.execute(sql4)
#             cur.execute(sql3)
#             cur1 = cur.fetchall()
#             print(cur1)
#     con.commit()
#     cur.close()
#     con.close()
#
#
#
# # getdocumentname()
# #connection()
#
# def tablecol():
#
#     data = []
#
#
#
#     con = sqlite3.connect('data.db')
#     cur = con.cursor()
#     sql = 'select * from classD'
#     cur.execute(sql)
#     col_name_list = [tuple[0] for tuple in cur.description]
#     col = dict()
#     name = dict()
#     col["type"] = 'checkbox'
#     col["fixed"] = 'left'
#     col = json.dumps(col,ensure_ascii=False)
#     col = col.replace('{\"', '{')
#     col = col.replace('\": \"', ":'")
#     col = col.replace('\", \"', "', ")
#     col = col.replace('\"',"'")
#     name['par'] = col
#     name['name'] = ''
#     data.append(name)
#     for i in range(len(col_name_list)):
#         a = dict()
#         b = dict()
#         a["field"] = col_name_list[i]
#         # a["title"] = col_name_list[i]
#         a["width"] = 80
#         a = json.dumps(a,ensure_ascii=False)
#         a = a.replace('{\"', '{')
#         a = a.replace('\": \"', ":'")
#         a = a.replace('\", \"', "', ")
#         a = a.replace('\"'," ")
#         b['par'] = a
#         b['name'] = col_name_list[i]
#
#         data.append(b)
#
#     right = dict()
#     pars = dict()
#     pars['fixed'] = 'right'
#     pars['width'] = 178
#     pars['align'] = 'center'
#     pars['toolbar'] = '#barDemo'
#     pars = json.dumps(pars,ensure_ascii=False)
#     pars = pars.replace('{\"', '{')
#     pars = pars.replace('\": \"', ":'")
#     pars = pars.replace('\", \"', "', ")
#     pars = pars.replace('\"',"")
#     pars = pars.replace('o}',"o'}")
#     right['par'] = pars
#     right['name'] = ''
#     data.append(right)
#     b = json.dumps(data, ensure_ascii=False)
#     print(b)
#
# tablecol()
#
#
# a = str({"id":"123465","leixing":"L","coding":"j","name":"","typec":"","node":"","level":"","width":"","pwidth":"","blength":"","jklength":"","ton":"","kilo":"","bigao":"","cmonth":"12","wdeep":"","dizhi":"","minbj":"","maxzb":"","spec":"","zjzz":"","wgbzz":""})
# print(type(a))
# a = json.loads(a)
# print(type(a))


'''
def Table1Json():
    try:

        conn = get_connect()
        cur = conn.cursor()
        sqlpro = "select * from pro"
        cur.execute(sqlpro)
        result_pro = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        conn = get_connect()
        cur2 = conn.cursor()
        sqlcity = "select * from city"
        cur2.execute(sqlcity)
        result_city = cur2.fetchall()
        conn.commit()
        cur2.close()
        conn.close()

        conn = get_connect()
        cur3 = conn.cursor()
        sqlcoun = "select * from country"
        cur3.execute(sqlcoun)
        result_coun = cur3.fetchall()
        conn.commit()
        cur3.close()
        conn.close()

        jsonData = []
        for row0 in result_coun:
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

        for row in result_pro:
          data = dict()
          interdata = dict()
          citys = ' '
          interdata['name'] = str(row[1])
          for row1 in result_city:

              if str(row1[6]) == str(row[0]):
                 citys = citys + row1[1] + " "
                 # citys.append(row1[1])
                 interdata['city'] = citys
          # print(interdata)
          temp = json.dumps(interdata, ensure_ascii=False)
          data[row[1]] = temp
          temp2 = str(data)

          for i in range(0, len(temp2)):
                if temp2[i] == ":":
                  #  print(jsonData)
                    jsonData.append(temp2[0:i+1]+temp2[i+3:len(temp2)-2])
                  #  print(jsonData)
                    break

        for row2 in result_city:
            interdata2 = {}
            data2 = {}
            interdata2['name'] = row2[1]
            interdata2['ZBX'] = str(row2[2])
            interdata2['ZBY'] = str(row2[3])
            interdata2['ZBA'] = str(row2[4])
            interdata2['ZBL'] = str(row2[5])
            temp = json.dumps(interdata2, ensure_ascii=False)
            data2[row2[1]] = temp
            temp2 = str(data2)

            for i in range(0, len(temp2)):

                if temp2[i] == ":":
                    jsonData.append(temp2[0:i+1]+temp2[i+3:len(temp2)-2])
                    break


        jsondatar = json.dumps(jsonData, ensure_ascii=False)
        '''
# jsondatar = jsondatar.replace('\\', '')
'''
        jsondatar = jsondatar.replace('}"', '}')
        jsondatar = jsondatar.replace('"{', '{')
        jsondatar = jsondatar.replace("{'", "'")
     #   jsondatar = jsondatar.replace()
        jsondatar = jsondatar[1:len(jsondatar) - 1]
        jsondatar = '{'+jsondatar+'}'
        jsondatar = jsondatar.replace("'",'"')

        return jsondatar

    #    print("连接成功")
       # print(jsonData[1:len(jsonData)-1])
    except Exception as e:
        print('MySQL connect fail ',e)


def Table2Json():  # 点线关系json制作    linkchina
    try:
        # conn = pymysql.Connect(host='localhost', user='root', passwd='123', db='geo', charset='utf8')
        conn = get_connect()
        cur = conn.cursor()
        sqlpro = "select * from pro"
        cur.execute(sqlpro)
        result_pro = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        # conn = pymysql.Connect(host='localhost', user='root', passwd='123', db='geo', charset='utf8')
        conn = get_connect()
        cur2 = conn.cursor()
        sqlcity = "select * from city"
        cur2.execute(sqlcity)
        result_city = cur2.fetchall()
        conn.commit()
        cur2.close()
        conn.close()

        #conn = pymysql.Connect(host='localhost', user='root', password='123', db='geo', charset='utf8')
        conn = get_connect()
        cur3 = conn.cursor()
        sqlcoun = "select * from country"
        cur3.execute(sqlcoun)
        result_coun = cur3.fetchall()
        conn.commit()
        cur3.close()
        conn.close()

        jsonData = []
        node = []
        link = []
        data = {}
        # 循环读取元组数据
        #     print("读到了数据")

        for row0 in result_coun:
            interdata0 = {}
            interdata0['name'] = row0[1]
            interdata0['class'] = "country"
            interdata0['group'] = 2
            interdata0['size'] = 40
            temp = json.dumps(interdata0, ensure_ascii=False)
            node.append(temp)

        for row in result_pro:
            #   data = {}
            interdata = {}
            interdata['name'] = row[1]
            interdata['class'] = "province"
            interdata['group'] = 0
            interdata['size'] = 20

            temp = json.dumps(interdata, ensure_ascii=False)
            #   temp = temp.replace("'"," ")
            node.append(temp)

        for row in result_city:
            interdata1 = {}
            interdata1['name'] = row[1]
            interdata1['class'] = "city"
            interdata1['group'] = 1
            interdata1['size'] = 10
            temp1 = json.dumps(interdata1, ensure_ascii=False)
            node.append(temp1)

        for row0 in result_coun:
            links = {}
            for row1 in result_pro:
                links['source'] = row0[1]
                links['target'] = row1[1]
                links['value'] = 6
                temp = json.dumps(links, ensure_ascii=False)
                link.append(temp)

        for row3 in result_pro:
            links = {}

            for row4 in result_city:
                if str(row4[6]) == str(row3[0]):
                    links['source'] = row3[1]
                    links['target'] = row4[1]
                    links['value'] = 3
                    temp = json.dumps(links, ensure_ascii=False)
                    link.append(temp)

        data['nodes'] = node
        data['links'] = link
        #     print(link)
        datar = json.dumps(data, ensure_ascii=False)
        '''
# datar = datar.replace('\\', '')
'''
        datar = datar.replace('"{', '{')
        datar = datar.replace('}"', '}')
        return datar

    except Exception as e:
        print('MySQL connect fail ', e)
'''
'''
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
    sql1 = "drop table if exists DN05490062_ESX"
    cur.execute(sql1)
    # sql = "create table DN05490062_CSX( 要素编号 int(20),所属类别 varchar(20),编码 varchar(20) ,名称 varchar(20),类型 varchar(20),编号 varchar(20),等级 varchar(20),宽度 varchar(20),铺宽 varchar(20),桥长 varchar(20),净空高 varchar(20),载重吨数 varchar(20),里程 varchar(20),比高 varchar(20),通行月份 int,水深 varchar(20),底质 varchar(20),最小曲率半径 varchar(20),最大纵坡 varchar(20),图形特征 varchar(20),注记指针 varchar(20),外挂表指针 varchar(20))"
    sql = "create table DN05490062_ESX( 要素编号 int(20),所属类别 varchar(20),编码 varchar(20) ,名称 varchar(20),类型 varchar(20),净空高 varchar(20),埋藏深度 varchar(20),存在状态 varchar(20),作用方式 varchar(20), 限制种类 varchar(20),图形特征 varchar(20),注记指针 varchar(20),外挂表指针 varchar(20))"
    # if cur.fetchall()[0][0] == 0:
    cur.execute(sql)
    '''
# fil = open(r'C:\Users\Administrator.000\Desktop\DN05490062\DN05490062.ESX', encoding='gbk')  # 读文件
'''
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
     #       bigao = point[12]
     #       cmonth = point[13]
     #       wdeep = point[14]
     #       dizhi = point[15]
     #       minbj = point[16]
     #       maxzb = point[17]
     #       spec = point[18]
     #       zjzz = point[19]
     #       wgbzz = point[20]
            #print(pointId,coding,name,typec,node,level,width,pwidth,blength,jklength,ton,kilo,bigao,cmonth,wdeep,dizhi,minbj,maxzb,spec,zjzz,wgbzz)
         #   print(pointId, coding, name, typec, node, level, width, pwidth, blength, jklength)
            # cur.execute("insert into DN05490062_CSX(要素编号,所属类别,编码,名称,类型,编号,等级,宽度,铺宽,桥长,净空高,载重吨数,里程,比高,通行月份,水深,底质,最小曲率半径,最大纵坡,图形特征,注记指针,外挂表指针)values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(pointId,Pleibie,coding,name,typec,node,level,width,pwidth,blength,jklength,ton,kilo,bigao,cmonth,wdeep,dizhi,minbj,maxzb,spec,zjzz,wgbzz))
            cur.execute(
                "insert into DN05490062_ESX(要素编号,所属类别,编码,名称,类型,净空高,埋藏深度,存在状态,作用方式,限制种类,图形特征,注记指针,外挂表指针)values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (pointId, Pleibie, coding, name, typec, node, level, width, pwidth, blength, jklength, ton, kilo))
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
            # bigao = line[12]
            # cmonth = line[13]
            # wdeep = line[14]
            # dizhi = line[15]
            # minbj = line[16]
            # maxzb = line[17]
            # spec = line[18]
            # zjzz = line[19]
            # wgbzz = line[20]
            # for j in range(math.ceil(int(coding) / 5)):
            # lines = fil.readline().split()
            # print(LineId,coding,name,typec,node,level,width,pwidth,blength,jklength,ton,kilo,bigao,cmonth,wdeep,dizhi,minbj,maxzb,spec,zjzz,wgbzz)
            cur.execute(
                "insert into DN05490062_ESX(要素编号,所属类别,编码,名称,类型,净空高,埋藏深度,存在状态,作用方式,限制种类,图形特征,注记指针,外挂表指针)values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (LineId, Lleibie, coding, name, typec, node, level, width, pwidth, blength, jklength, ton, kilo))
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
            # for j in range(math.ceil(int(coding) / 5)):
            # lines = fil.readline().split()
            # print(leibie, LineId, coding, name, typec, node, level, width, pwidth, blength, jklength, ton)
            cur.execute(
                "insert into DN05490062_ESX(要素编号,所属类别,编码,名称,类型,净空高,埋藏深度,存在状态,作用方式,限制种类,图形特征,注记指针,外挂表指针)values(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (LineId, Aleibie, coding, name, typec, node, level, width, pwidth, blength, jklength, ton, kilo))
    cur.close()
    con.commit()
    con.close()


# coding:utf-8
# 目标检测主要业务逻辑

import sqlite3
import math
from decimal import Decimal


# 点坐标
class Point:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def toString(self):
        return '(' + '经度：' + str(self.x) + ',纬度：' + str(self.y) + ')'


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
        self.unitGirls = [[set() for i in range(self.xUnitSize)] for j in range(self.yUnitSize)]  # set自动去重
        self.unitGirlsFuPo = [[0 for i in range(self.xUnitSize + 100)] for j in range(self.yUnitSize + 100)]
        self.maskGirls = [
            [[set(), 50000.0, -20000.0, 0] for i in range(self.xUnitSize - (math.ceil(self.maskLen / self.unitLen)))]
            for j in range(self.yUnitSize - (math.ceil(self.maskLen / self.unitLen)))]

        # 初始化单位网格二维数组

    def initUnitGirls(self, LineList):
        for line in LineList:
            i = math.floor((line.x - self.xMin) / self.unitLen)
            j = math.floor((line.y - self.yMin) / self.unitLen)
            self.unitGirls[j][i].add(line.id)

    # 初始化掩膜的二维数组
    def initMaskGirls(self, pointWithZList, FuPoDict):

        for key in FuPoDict.keys():
            xMin, xMax, yMin, yMax = getRectangleTuKe(FuPoDict[key])

            jMin = math.floor((xMin - self.xMin) / self.unitLen)
            iMin = math.floor((yMin - self.yMin) / self.unitLen)
            jMax = math.ceil((xMax - self.xMin) / self.unitLen)
            iMax = math.ceil((yMax - self.yMin) / self.unitLen)
            # (jMin," ",jMax," ",iMin," ",iMax)
            for j in range(jMin, jMax):
                for i in range(iMin, iMax):
                    self.unitGirlsFuPo[j][i] = 1

        # print(self.unitGirlsFuPo)
        maskSize = math.floor(self.maskLen / self.unitLen)
        # 合并单元格中道路条数
        for i in range(self.xUnitSize - (math.ceil(self.maskLen / self.unitLen))):
            for j in range(self.yUnitSize - (math.ceil(self.maskLen / self.unitLen))):
                for i_increment in range(maskSize):
                    for j_increment in range(maskSize):
                        self.maskGirls[j][i][0] |= self.unitGirls[j + j_increment][i + i_increment]
                        self.maskGirls[j][i][3] = self.maskGirls[j][i][3] or self.unitGirlsFuPo[j + j_increment][
                            i + i_increment]
                        # print("self.unitGirlsFuPo[j+j_increment][i+i_increment]=",self.unitGirlsFuPo[j+j_increment][i+i_increment])
        # 维护掩膜的高程值
        for p in pointWithZList:
            j = math.floor((p.x - self.xMin) / self.unitLen)
            i = math.floor((p.y - self.yMin) / self.unitLen)
            lenn = math.ceil(self.maskLen / self.unitLen)
            for a in range(lenn):
                for b in range(lenn):
                    if (j - a > 0 and i - b > 0 and j - a < len(self.maskGirls) and i - b < len(self.maskGirls)):
                        self.maskGirls[j - a][i - b][1] = min(self.maskGirls[j - a][i - b][1], p.z)
                        self.maskGirls[j - a][i - b][2] = max(self.maskGirls[j - a][i - b][2], p.z)

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

                if (self.maskGirls[j][i][1] > float(h_min) and self.maskGirls[j][i][2] < float(h_max) and
                        self.maskGirls[j][i][1] < self.maskGirls[j][i][2] and self.maskGirls[j][i][3] == int(isFuPo)):
                    # print(self.maskGirls[j][i][1])
                    print(self.maskGirls)
                    # print(self.unitGirlsFuPo)
                    if (len(self.maskGirls[j][i][0]) > maxDensity):
                        # Decimal(i*self.unitLen+self.yMin+self.maskLen).quantize(Decimal('0.000'))
                        workArray.append(Point(Decimal(j * self.unitLen + self.xMin).quantize(Decimal('0.000')),
                                               Decimal(i * self.unitLen + self.yMin).quantize(Decimal('0.000')),
                                               0).toString())
                        workArray.append(
                            Point(Decimal(j * self.unitLen + self.xMin + self.maskLen).quantize(Decimal('0.000')),
                                  Decimal(i * self.unitLen + self.yMin + self.maskLen).quantize(Decimal('0.000')),
                                  0).toString())
                        maxDensityResult.append(workArray)
                        maxDensityResult.append('<br>')
                    elif (len(self.maskGirls[j][i][0]) <= maxDensity and len(self.maskGirls[j][i][0]) > minDensity):
                        workArray.append(Point(Decimal(j * self.unitLen + self.xMin).quantize(Decimal('0.000')),
                                               Decimal(i * self.unitLen + self.yMin).quantize(Decimal('0.000')),
                                               0).toString())
                        workArray.append(
                            Point(Decimal(j * self.unitLen + self.xMin + self.maskLen).quantize(Decimal('0.000')),
                                  Decimal(i * self.unitLen + self.yMin + self.maskLen).quantize(Decimal('0.000')),
                                  0).toString())
                        middleDensityResult.append(workArray)
                        middleDensityResult.append('<br>')
                    else:
                        workArray.append(Point(Decimal(j * self.unitLen + self.xMin).quantize(Decimal('0.000')),
                                               Decimal(i * self.unitLen + self.yMin).quantize(Decimal('0.000')),
                                               0).toString())
                        workArray.append(
                            Point(Decimal(j * self.unitLen + self.xMin + self.maskLen).quantize(Decimal('0.000')),
                                  Decimal(i * self.unitLen + self.yMin + self.maskLen).quantize(Decimal('0.000')),
                                  0).toString())
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
    sql1 = "SELECT jzb.LAX as x,jzb.LAY as y,jsx.level as z FROM DN10510744_JZB jzb LEFT JOIN DN10510744_JSX jsx ON jzb.LNUM = jsx.id WHERE jzb.leibie = 'L' AND jsx.leibie = 'L' AND jsx.level is NOT '-32767.00'"
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
def readFuPo():
    # print("进入"+dbName)
    con = sqlite3.connect('tDN05490062.db')
    # con = sqlite3.connect(dbName)  # 连接桥
    # print("Open database successfully")  # 打开成功
    cur = con.cursor()
    sql1 = "sELECT ZNUM As fuPoiD, ZZX aS x,ZZY aS y fROM DN05490062_FZB FZB wHere leibie='A'"
    cur.execute(sql1)
    FuPoDict = dict()
    FuPoList = []
    print(cur.fetchall())
    print(FuPoDict.keys())
    for line in cur.fetchall():
        if line != None:
            if (line[0] in FuPoDict.keys()):
                print("in")
                FuPoDict[line[0]].append(Point(float(line[1]), float(line[2]), 0))
            else:
                FuPoDict[line[0]] = []
        if line != None:
            FuPoList.append(Point(float(line[1]), float(line[2]), 0))
    cur.close()
    con.commit()
    con.close()
    print(FuPoDict)
    print(FuPoList)
    return [FuPoDict, FuPoList]

# readFuPo()

# con = sqlite3.connect('data.db')
# cur = con.cursor()
# cur.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='cl'")
# cur = cur.fetchall()
# print(cur)
# if cur[0][0] == 0:
#     print("好耶")
# else:
#     print("给九九两巴掌")


def Table3Json():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    doc = 'DN05490062'
    sql = 'select * from tuceng'
    cur.execute(sql)
    result = cur.fetchall()
    jsonData = list()
    interdata1 = dict()
    data1 = dict()
    # 单加doc
    interdata1['name'] = doc
    temp = json.dumps(interdata1, ensure_ascii=False)
    data1[doc] = temp
    for tuceng in result:
        cur.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='" + doc + "_" + tuceng[2] + "SX'")
        flag = cur.fetchall()
        if flag[0][0] == 1:
            interdata1['name'] = tuceng[1]
            temp = json.dumps(interdata1, ensure_ascii=False)
            data1[tuceng[1]] = temp

            temp2 = str(data1)
            jsonData.append(temp2)

            sql = 'select * from ' + doc + '_' + tuceng[2] + 'SX'
            cur.execute(sql)
            sx = cur.fetchall()
            for row in sx:
                interdata = dict()
                data = dict()
                col_name_list = [tuple[0] for tuple in cur.description]
                for col in range(0, len(col_name_list)):
                    interdata[col_name_list[col]] = row[col]
                temp = json.dumps(interdata, ensure_ascii=False)
                data[row[3]] = temp
                temp2 = str(data)
                jsonData.append(temp2)
    jsondatar = json.dumps(jsonData, ensure_ascii=False)
    '''
# jsondatar = jsondatar.replace('\\', '')
'''
    jsondatar = jsondatar.replace('}"', '}')
    jsondatar = jsondatar.replace('"{', '{')
    jsondatar = jsondatar.replace("{'", "'")
    jsondatar = jsondatar[1:len(jsondatar) - 1]
    jsondatar = '{' + jsondatar + '}'
    jsondatar = jsondatar.replace("'", '"')
    jsondatar = jsondatar.replace('"{', '{')
    jsondatar = jsondatar.replace('}"}', '}')
    return jsondatar


def Table4Json():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    sql = 'select * from tuceng'
    cur.execute(sql)
    tuceng = cur.fetchall()
    doc = 'DN05490062'
    node = list()
    link = list()
    data = dict()

    for row in tuceng:
        group = 1
        cur.execute("SELECT COUNT(*) FROM sqlite_master where type='table' and name='" + doc + "_" + row[2] + "SX'")
        flag = cur.fetchall()
        if flag[0][0] == 1:
            sql = 'select * from ' + doc + '_' + row[2] + 'SX'
            cur.execute(sql)
            col_name_list = [tuple[0] for tuple in cur.description]
            res = cur.fetchall()
            for i in res:
                inter = dict()
                links = dict()
                inter['name'] = str(row[2] + str(i[0]) + ':' + i[3])
                inter['belong'] = row[2]
                inter['leixing'] = i[1]
                inter['group'] = group
                inter['size'] = 8
                links['source'] = row[1]
                links['target'] = str(row[2] + str(i[0]) + ':' + i[3])
                links['value'] = 20
                temp = json.dumps(inter, ensure_ascii=False)
                temp1 = json.dumps(links, ensure_ascii=False)
                node.append(temp)
                link.append(temp1)
        leixing = dict()
        docu = dict()
        docu['source'] = doc
        docu['target'] = row[1]
        docu['value'] = 20
        leixing['name'] = row[1]
        leixing['belong'] = row[2]
        leixing['group'] = group
        leixing['size'] = 10
        leixing = json.dumps(leixing, ensure_ascii=False)
        docu = json.dumps(docu, ensure_ascii=False)
        node.append(leixing)
        link.append(docu)
        group += 1
    document = dict()
    document['name'] = doc
    document['leixing'] = 'doc'
    document['group'] = 0
    document['size'] = 15
    document = json.dumps(document,ensure_ascii=False)
    node.append(document)
    # Table3Json 添加doc点
    data['nodes'] = node
    data['links'] = link
    datar = json.dumps(data, ensure_ascii=False)
    '''
# datar = datar.replace('\\', '')
'''
    datar = datar.replace('"{', '{')
    datar = datar.replace('}"', '}')
    return datar


data3 = Table3Json()
print(data3)
data4 = Table4Json()
print(data4)
'''
con = sqlite3.connect('data.db')      # 连接桥
b = 'DN05490062_ASX'
s = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name = " + "'" + b + "'"
cur = con.cursor()
cur.execute(s)
a = cur.fetchall()
if int(a[0][0]) == 1:
    print(a)
