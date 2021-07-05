from flask import Flask, jsonify, render_template, request
import pandas as pd
import pickle
from sklearn.externals import joblib

from flask_migrate import Migrate 
from flask_sqlalchemy import SQLAlchemy 

import sys

db = SQLAlchemy()
migrate = Migrate()

import config

app = Flask(__name__)

app.config.from_object(config)
    
#ORM
db.init_app(app)
migrate.init_app(app,db)



#route

@app.route('/')
def home():
    return "this is home!"

@app.route('/checklist',methods=['GET', 'POST'])
def checklist():
    clf_from_joblib = joblib.load('ml_mod/model.pkl') #머신러닝 모델 호출
    data = request.form['values']#앱에서 데이터를 str
    indexing_data = data[1:-1]#받아온 str 스라이싱하여 데이터전처리
    target = indexing_data.split(', ')#str list화를 위해 str 분리
    value =[]#true,false로 온 데이터를 1,0 으로 대체 
    for i in target:
        if i == 'true':
            value.append('1')
        elif i == 'false':
            value.append('0')
   #DataFrame화를 위한 columns 명  
    col = ['의식 존재', '출혈', '움직일 수 있는가', '통증', '발작','구토', '발열', '피부가 창백한가', '땀을 흘리는가(식은 땀)', '기침', '입술이 말랐는가', '호흡이 가파른가', '어지러움을 느끼는가', '통증 유지가 30분이 넘는가', '더운 곳에 오래 노출되어있었는가']
    new_value = [value] #DataFrame에 씌우기 위해 형변환
    value_df = pd.DataFrame(new_value, columns=col) #DataFrame화
    result = clf_from_joblib.predict(value_df) # 머신러닝 학습 모델에 애에서 받아온 데이터를 입력하여 예측
    print("your disease number is ",result)
    from models import Sickness
    th = Sickness.query.get(result[0])
    df = pd.read_sql(th.statement, th.session.bind)
    return jsonify(sick = th[1], cha = th[2], symp = th[3], cop = th[4])

@app.route("/map",methods=['POST'] )
def map():
    value = list(request.form['values'])
    c_loca = value[0]
    delta = value[1]
    #a=models.AED_info.query.filter_by(lon <= c_loca[0]+delta[0] && lon >= c_loca[0]-delta[0] && lat <= c_loca[1]+delta[1] && lat >= c_loca[1]-delta[1])
    return jsonify('a')

@app.route("/admin")
def admin():
    return "this is admin!"

@app.route('/test')
def test():
    return render_template('post.html')

@app.route('/post', methods=['POST'])
def post():
    value = request.form['values']
    return value  


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=55556, debug=True)
