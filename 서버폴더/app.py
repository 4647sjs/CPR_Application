from flask import Flask, request, jsonify, Response
import pandas as pd
import pickle
import numpy as np
from sklearn.externals import joblib
import xml.etree.ElementTree as ET
import pymysql
app = Flask(__name__)



@app.route('/',methods=['GET','POST'])
def main():
	say="hello CPR server!!\n"
	maker = "Dankook Univ. CPR team "
	date = "2020"
	return say+maker+date
		
@app.route('/checklist',methods=['GET','POST'])
def hello_world():
		
	values=[]
	values.append(request.args.get('f1', ''))
	values.append(request.args.get('f2', ''))
	values.append(request.args.get('f3', ''))
	values.append(request.args.get('f4', ''))
	values.append(request.args.get('f5', ''))
	values.append(request.args.get('f6', ''))
	values.append(request.args.get('f7', ''))
	values.append(request.args.get('f8', ''))
	values.append(request.args.get('f9', ''))
	values.append(request.args.get('f10', ''))
	values.append(request.args.get('f11', ''))
	values.append(request.args.get('f12', ''))
	values.append(request.args.get('f13', ''))
	values.append(request.args.get('f14', ''))
	values.append(request.args.get('f15', ''))
	values.append(request.args.get('f16', ''))
	values.append(request.args.get('f17', ''))
	
	value=[]
	for i in values:
		if i =='true':
			value.append(1)
		elif i =='false':
			value.append(0)
	
	
	clf_from_joblib = joblib.load('ml_mod/model.pkl') #머신러닝 모델 호출
	
	col = ['의식 여부', '출혈', '움직임가능', '통증', '발작', '구토', '발열', '피부_창백', '식은땀', '기침', '입술건조', '가파른호흡',
	       '어지러움', '통증유지30분이상', '더위노출','어눌한 발음','이상한 걸음']
	target = ['열사병','일사병','천식','골절','협심증','심근경색','뇌졸중']

	new_value = [value] #DataFrame에 씌우기 위해 형변환
	value_df = pd.DataFrame(new_value, columns=col) #DataFrame화
	result = clf_from_joblib.predict(value_df) # 머신러닝 학습 모델에 애에서 받아온 데이터를 입력하여 예측
	result_start_zero = int(result)-1 #질병 번호
	result2 = str(result_start_zero) #질병 번호 문자열화
	result3 = target[result_start_zero] #질병명
	
	root = ET.Element("CPR")
	disease_num = ET.Element("disease_num")
	disease_num.text = str(int(result))
	disease_name = ET.Element("disease_name")
	disease_name.text = result3

	root.append(disease_num)
	root.append(disease_name)
	xmlfile = ET.tostring(root)
	return Response(xmlfile, mimetype='text/xml')


@app.route('/disease', methods=['GET', 'POST'])
def bye_world():

	disease_name = request.args.get('disease_name', '')

	disease = pymysql.connect(user='cpr_man',passwd='1q2w3e4r',db='CPR',charset='utf8')
	cursor = disease.cursor()

	target = ['열사병', '일사병', '천식', '골절', '협심증', '심근경색','뇌졸중']


	sql_sick_info = "SELECT * FROM emrg_feat where sick_name='%s';" %disease_name
	cursor.execute(sql_sick_info)
	sql_result = cursor.fetchall()

	root = ET.Element("CPR")
	#disease_num = ET.Element("disease_num")
	#disease_num.text = sql_result[0][0]
	disease_name = ET.Element("disease_name")
	disease_name.text = sql_result[0][1]
	disease_info = ET.Element("disease_info")
	disease_info.text = sql_result[0][2]
	disease_feat = ET.Element("disease_feat")
	disease_feat.text = sql_result[0][3]
	disease_treat = ET.Element("disease_treat")
	disease_treat.text = sql_result[0][4]

	#root.append(disease_num)
	root.append(disease_name)
	root.append(disease_info)
	root.append(disease_feat)
	root.append(disease_treat)
	xmlfile = ET.tostring(root)

	disease.close()
	return Response(xmlfile, mimetype='text/xml')

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=55556,debug=True)
