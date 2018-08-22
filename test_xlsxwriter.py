# -*- coding: utf-8 -*-
# @Time    : 2018/8/22 下午4:08
# @Author  : Rdxer
# @Email   : Rdxer@foxmail.com
# @File    : test_xlsxwriter.py
# @Software: PyCharm

import xlsxwriter
import random
from datetime import date
import collections


def xlwt_chart(xl_obj,table):

  #生成柱状图
  column_chart = xl_obj.add_chart({'type':'column'})
  column_chart.add_series({
    'name':'=sheet1!$D$1',
    'categories':'=sheet1!$4$2:$4$7',
    'values':'=sheet1!$E$2:$E$7'
  })
  table.insert_chart('G2',column_chart)

  #生成饼图
  column_chart2 = xl_obj.add_chart({'type':'pie'})
  column_chart2.add_series({
    'name': '=sheet1!$D$1',
    'categories':'=sheet1!$D$2:$D$7',
    'values': '=sheet1!$E$2:$E$7'
  })
  table.insert_chart('G20', column_chart2)


def xlwt_run():
  data_base = ['0-50','50-60','60-70','70-80','80-90','90-100']

  #生成一个有序的字典
  chart_dict = collections.OrderedDict.fromkeys(data_base,0)

  xl_obj = xlsxwriter.Workbook('/Users/Rdxer/Desktop/chart.xlsx')
  table = xl_obj.add_worksheet('sheet1')
  table.write_string(0,0,'姓名')
  table.write_string(0,1,'成绩')
  table.write_string(0,2,'日期')
  table.merge_range('D1:E1', '成绩分布')
  table.set_column('C:E',15)

  #定义格式
  date_format = xl_obj.add_format({'num_format':'yyyy-mm-dd'})
  color_format = xl_obj.add_format({'color':'red'})
  font_format = xl_obj.add_format({'font_color':'green','bold':True})


  mm = 1
  for i in range(1,40):
    name = 'name_%d' % i
    score = random.randint(30,100)
    if score <= 50:
      chart_dict['0-50'] += 1
    elif score>50 and score<=60:
      chart_dict['50-60'] += 1
    elif score>60 and score<=70:
      chart_dict['60-70'] += 1
    elif score>70 and score<=80:
      chart_dict['70-80'] += 1
    elif score>80 and score<=90:
      chart_dict['80-90'] += 1
    else:
      chart_dict['90-100'] += 1

    if score > 60:
      table.write_string(i, 0, name)
      table.write_number(i, 1, score)
    else:
      table.write_string(i, 0, name, color_format)
      table.write_number(i, 1, score, color_format)

    table.write_datetime(i, 2,date.today(), date_format)
    mm = mm + 1

  #生成图表数据
  row = 1
  for k,v in chart_dict.items():
    table.write_string(row, 3, k, font_format)
    table.write_number(row, 4, v, font_format)
    row = row+1

  xlwt_chart(xl_obj,table)
  #使用公式
  table.write_formula(mm,1,'=AVERAGE(B2:B40)')

  #插入带链接的图片
  #table.insert_image('D20',r'/Users/Rdxer/Desktop/pilot.png',{'url':'https://www.baidu.com'})

  #关闭excel句柄
  xl_obj.close()

if __name__ == '__main__':
  xlwt_run()
