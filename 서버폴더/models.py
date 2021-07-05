from application import db

class Sickness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sick = db.Column(db.String(30), nullable=False) #병명
    cha = db.Column(db.Text(), nullable=False) #특징
    symp = db.Column(db.Text(), nullable=False) #증상
    cop = db.Column(db.Text(), nullable=False) #대처법

    
class AED_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lon = db.Column(db.String(15), nullable=False) #경도
    lat = db.Column(db.String(15), nullable=False) #위도
    add = db.Column(db.Text(), nullable=False) #주소
    place = db.Column(db.Text(), nullable=False) #상세위치
    mng = db.Column(db.String(30), nullable=False) #관리자
    mng_t = db.Column(db.String(15), nullable=False) #전화번호
