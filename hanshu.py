
def Gauss_to_Latitude(request):
    # 高斯坐标转经纬度坐标
    if request.method != "POST":
        return JsonResponse(
            {
                "status": 201,
                "message": "method error."
            }
        )
    # 需要前端界面传参A点和B点的参数
    P_coordinate = request.POST.get("A_coordinate", None)   # A点高斯坐标，格式为list[]形式
    Maxcnt = 5
    a = 6378137.0   # 椭球长半径
    b = 6356752.3142 # 椭球短半径
    e2 = (a*a-b*b)/a/a
    _e2 = (a * a - b * b) / b / b
    c = a * a / b
    bata0 = 1 - 3. / 4 * _e2 + 45. / 64 * _e2 * _e2 - 175. / 256 * pow(_e2, 3) + 11025. / 16384 * pow(_e2, 4)
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
    x = P_coordinate[0]
    Daihao = int(P_coordinate[1] / 1000000)
    y = P_coordinate[1] - Daihao * 1000000 - 500000
    Bf = P_coordinate[0] / C0
    cnt = 0
    # 构造do...while
    Bf1 = Bf
    FBf1 = -a2 / 2 * math.sin(2 * Bf1) + a4 / 4 * math.sin(4 * Bf1) - a6 / 6 * math.sin(6 * Bf1)
    Bf = (P_coordinate[0] - FBf1) / C0
    cnt =cnt+1
    while (math.fabs(Bf - Bf1) >= 0.0000001 and cnt < Maxcnt):
        Bf1 = Bf
        FBf1 = -a2 / 2 * math.sin(2 * Bf1) + a4 / 4 * math.sin(4 * Bf1) - a6 / 6 * math.sin(6 * Bf1)
        Bf = (P_coordinate[0] - FBf1) / C0
        cnt = cnt + 1
    if (cnt == Maxcnt and math.fabs(Bf - Bf1) >= 0.0000001):
        exit(0)
    else:
        Vf = math.sqrt(1 + _e2 * math.cos(Bf) * math.cos(Bf))
        Nf = c / Vf
        Nf2 = Nf * Nf
        Mf = c / (Vf * Vf * Vf)
        tf2 = math.tan(Bf) * math.tan(Bf)
        etarf2 = _e2 * math.cos(Bf) * math.cos(Bf)
        y2 = y * y
        tb = math.tan(Bf) / (Mf * Nf) * y2
        B = Bf - tb / 2 + tb / (24 * Nf2) * y2 * (5 + 3 * tf2 + etarf2 - 9 * etarf2 * tf2) - tb / (
                    720 * Nf2 * Nf2) * y2 * y2 * (61 + 90 * tf2 + 45 * tf2 * tf2)
        tl = y / Nf / math.cos(Bf)
        L = tl - tl / (6 * Nf2) * y2 * (1 + 2 * tf2 + etarf2) + tl / (120 * Nf2 * Nf2) * y2 * y2 * (
                    5 + 28 * tf2 + 24 * tf2 * tf2 + 6 * etarf2 + 8 * etarf2 * tf2)
    return B,L


def Calculate_Gdis(request):
    # 返回在区域内的道路有哪些，给出地理方位
    if request.method != "POST":
        return JsonResponse(
            {
                "status": 201,
                "message": "method error."
            }
        )
    # 需要前端界面传参A点和B点的参数
    A_coordinate = request.POST.get("A_coordinate", None)   # A点高斯坐标，格式为list[]形式
    B_coordinate = request.POST.get("B_coordinate", None)   # B点高斯坐标
    dis_A_to_B = math.sqrt(pow((A_coordinate[0]-B_coordinate[0]),2)+pow((A_coordinate[1]-B_coordinate[1]),2))
    center = [(A_coordinate[0]+B_coordinate[0])/2, (A_coordinate[1]+B_coordinate[1])/2]
    # 求矩阵的四个顶点 A_point(x_min,y_max) B_point(x_max,y_max) C_point(x_min,y_min) D_point(x_max,y_min)
    #A_point = [center[0] - 1/2 * dis_A_to_B, center[1] + 1/6 * dis_A_to_B]
    #B_point = [center[0] + 1/2 * dis_A_to_B, center[1] + 1/6 * dis_A_to_B]
    #C_point = [center[0] - 1/2 * dis_A_to_B, center[1] - 1/6 * dis_A_to_B]
    #D_point = [center[0] + 1/2 * dis_A_to_B, center[1] - 1/6 * dis_A_to_B]
    X_min = center[0] - 1/2 * dis_A_to_B
    X_max = center[0] + 1/2 * dis_A_to_B
    Y_min = center[1] - 1/6 * dis_A_to_B
    Y_max = center[1] + 1/6 * dis_A_to_B
    #查询数据库
    conn = get_connect()
    cursor = conn.cursor()
    sql_road = 'SELECT id,x,y FROM Road' # 搜索道路表的数据，返回在给定范围道路的id
    cursor.execute(sql_road)# 执行查询语句
    result_pro = cursor.fetchall() #得到结果
    conn.commit()
    cursor.close()
    conn.close()# 结束关闭链接
    # 目标：查询 result_pro 中在给定范围道路的 id，不单是一个结果  查询范围在 [X_min,Y_min] 至 [X_max,Y_max]之间

    # 得到道路后，还需要根据道路周边的水域，草丛等设置权重信息，做出资源最少 或 路径最短的道路推荐

    # 获取道路周边的属性和实体，



