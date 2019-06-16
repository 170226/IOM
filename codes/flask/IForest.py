# -*- coding: utf-8 -*-
import time
from datetime import datetime
import csv
from sklearn.ensemble import IsolationForest
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import pytz
from flask import Flask
app = Flask(__name__)


def processData( data ):
    """处理csv格式文件中采集的原始数据

        参数：
            data：转换成数组格式的原始数据
                包括时间戳、2个cpu指标:系统cpu利用率usage_system、用户cpu利用率usage_user
                以及2个net指标：网络数据包收发数packets_recv、packets_send

        返回值：
            d2：处理后的数据，元素类型为浮点数
            result：处理后的数据，元素类型为字符串
    """
    n = 0
    data1 = []
    for item in data[:,0]:
        if item == 'time':
            break           
        # 时间戳1的不同指标的list的元素索引
        y = np.where(data == data[n][0])
        d1 = data[y[0]]
        # 数据填充，将同一时间的不同样本纳入同一行
        for i in range(1, len(d1)):
            z = np.where(d1[i] != '')
            d1[0][z[0][1]] = d1[i][z[0][1]]
            d1[0][z[0][2]] = d1[i][z[0][2]]
            if i == (len(d1)-1): 
                if '' not in d1[0]:
                    data1.append(d1[0])
        n = n + 1
    result = np.array(list(data1))
    d2 = []
    # 将result中的数据转换成浮点数类型
    for item in result:
        result_new = [it.astype(np.float32) for it in item]
        d2.append(result_new)
    return d2, result

def generate_time(timestp):
	"""时间格式转换

        参数：
            timestp：时间戳list

        返回值：
            otherStyleTime：年/月/日 时/分/ list
    """
    otherStyleTime = []
    tz = pytz.timezone('Asia/Shanghai')
    for i in range(len(timestp)):    
        dat = timestp[i].astype(np.int64) // 10**9
        dateArray = datetime.fromtimestamp(dat,tz)
        otherStyleTime.append(dateArray.strftime("%Y-%m-%d %H:%M:%S"))
    return otherStyleTime

@app.route('/')
def IForest():
	"""时间格式转换

        返回值：
            s：异常出现时间
    """
    # 读取csv格式文件，去掉原始数据首行首列
	csvFile = open("test.csv", "r")
	reader = csv.reader(csvFile)
	m = np.array(list(reader))
	data_origin = m[1:,1:]

	data, res = processData( data_origin )

	# 计算单位时间（每5秒）网络数据包收发数
	for i in range(1, len(data)):
	    data[i-1][3] = data[i][3]-data[i-1][3]
	    data[i-1][4] = data[i][4]-data[i-1][4]
	data = data[0:len(data)-1]
	out = pd.DataFrame(data)

    # 使用孤立森林算法检测异常
	ilf = IsolationForest(n_estimators=300, max_features=2, max_samples=481, contamination=0.03, random_state=None)
	ilf.fit(data)
	output_table = pd.DataFrame({'isAnomal':ilf.predict(data),'Decision':ilf.decision_function(data)},)

    # 记录异常点索引与其相对应的时间戳，如果15s内有多个异常，则只返回首次出现异常的时间
	y = output_table[output_table.isAnomal == -1].index.tolist()
	time_show = []
	y_ = []
	for i in range(len(y)):
	    if i == 0:
	        y_.append(y[0])
	    elif y[i] > y_[-1] + 3:
	        y_.append(y[i])
	print(y_)
	for i in y_:
	    time_show.append(float(data[i][0]))
	timestp_ = generate_time(np.array(time_show))

	s = ""
	for i in timestp_:
		s = s + str(i) + '\n\r'
	csvFile.close()
	return s

if __name__=="__main__":
	app.run(
		host='192.168.188.128',
      	port= 5000,
      	debug=True
	)

