import urllib, sys
import urllib.request as urllib2
import ssl
import base64
import os
import json
import time
import xlsxwriter

host = 'https://aip.baidubce.com/rest/2.0/face/v3/match?access_token=24.1cd907cb9574a56ff66133a97781f35a.2592000.1571315441.282335-17266916'

def list_jpg(path, file_list, name_list):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            list_jpg(file_path, file_list, name_list)
        elif os.path.splitext(file_path)[1]=='.jpg':
            file_list.append(file_path)
            name_list.append(file)

def compare(file1, file2, name1, name2):
    # 获取图片
    with open(file1, 'rb') as file1:
        dataOrigin = base64.b64encode(file1.read())
    with open(file2, 'rb') as file2:
        dataTarget = base64.b64encode(file2.read())
    # print(dataOrigin)
    # print(dataTarget)
    # p = []
    # pdata = json.loads(json.dumps(p))
    postData = [
        {
            "image": dataOrigin.decode(),
            "image_type": "BASE64",
            "face_type": "LIVE",
            "quality_control": "NONE",
            "liveness_control": "NONE"
        },
        {
            "image": dataTarget.decode(),
            "image_type": "BASE64",
            "face_type": "LIVE",
            "quality_control": "NONE",
            "liveness_control": "NONE"
        }
    ]
    postJson = json.dumps(postData)
    httpPostJson = bytes(postJson, 'utf8')
    request = urllib2.Request(host, data=httpPostJson)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        # print(content)
        # content = content.decode
        content = str(content,'utf-8')
        content = json.loads(content)
        if content['error_msg'] == 'SUCCESS':
            dict[name1 + "&" + name2] = content['result']['score']
            print(name1 + "&" + name2)
        else:
            dict[name1 + "&" + name2] = 'NONE'
            print(name1 + "&" + name2)
        # print(content['error_msg'])
    else:
        print("error")

def export_excel(dict):
    workbook = xlsxwriter.Workbook('./result_data.xlsx')
    worksheet = workbook.add_worksheet()
    bold_format = workbook.add_format({'bold': True})

    worksheet.write('A1', 'image1', bold_format)
    worksheet.write('B1', 'image2', bold_format)
    worksheet.write('C1', 'score', bold_format)
    worksheet.write('D1', 'predition', bold_format)

    row = 1
    col = 0
    for key, value in dict.items():
        image1 = str(key).split('&')[0]
        image2 = str(key).split('&')[1]
        if value == 'NONE':
            predition = 'NULL'
        elif float(value) > 80:
            predition = 'T'
        else:
            predition = "F"
        worksheet.write_string(row, col, image1)
        worksheet.write_string(row, col+1, image2)
        worksheet.write_string(row, col+2, str(value))
        worksheet.write_string(row, col+3, predition)
        row+=1
    workbook.close()

file_list = []
name_list = []
dict = {}
list_jpg("/Users/liuhuanchao/Documents/faces2/faces", file_list, name_list)
print(len(file_list))
print(len(name_list))
for i in range(0, len(file_list)):
    # for j, val2 in enumerate(file_list, i):
    for j in range(0, len(file_list)):
        compare(file_list[i], file_list[j], name_list[i], name_list[j])
        time.sleep(0.5)
for key, value in dict.items():
    print('{key} : {value}'.format(key = key, value=value))

# 导出excel
export_excel(dict)