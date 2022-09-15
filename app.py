#restful api coba2 wkwkwk
#test
from urllib import response
from flask import Flask, request
from flask_restful import Resource,Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os


#inisiasi object flask
app= Flask(__name__)

#inisiasi project flask restful
api=Api(app)

#inisiasi CORS
CORS(app)

#inisiasi object flask sqlalchemy
db = SQLAlchemy(app)

#konfigurasi database
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

#membuat database model
class ModelDatabase(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    age = db.Column(db.Float)
    sex = db.Column(db.Float)
    cp = db.Column(db.Float)
    trestbps = db.Column(db.Float)
    chol = db.Column(db.Float)
    fbs = db.Column(db.Float)
    restecg = db.Column(db.Float)
    thalach = db.Column(db.Float) 
    exang = db.Column(db.Float)
    oldpeak = db.Column(db.Float)
    slope = db.Column(db.Float)

    #method utk menyimpan data
    def save(self):
        try: 
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

#creating database
db.create_all()


#inisiasi variabel kosong berupa dictionary
identitas={} #variabel global, json

#membuat class resource, punya method get sama post
class ContohResource(Resource):

    #method
    def get(self):

        #menampilkan data dari database sql 
        query = ModelDatabase.query.all()

        #iterasi data pada modelDatabase memakai list comprehension
        output = [
            {
                "id" : data.id,
                "age" : data.age,
                "sex" : data.sex,
                "cp" : data.cp,
                "trestbps" : data.trestbps,
                "chol" : data.chol,
                "fbs" : data.fbs,
                "restecg" : data.restecg,
                "thalach" : data.thalach, 
                "exang" : data.exang,
                "oldpeak" : data.oldpeak,
                "slope" : data.slope
            }
            for data in query
                 ]
        
        response = {
            "code":200,
            "msg":"query sukses",
            "data":output

        }

        return response,200

    def post(self):
        ageData = request.form["age"]
        sexData = request.form["sex"]
        cpData = request.form["cp"]
        trestbpsData = request.form["trestbps"]
        cholData = request.form["chol"]
        fbsData = request.form["fbs"]
        restecgData = request.form["restecg"]
        thalachData = request.form["thalach"] 
        exangData = request.form["exang"]
        oldpeakData = request.form["oldpeak"]
        slopeData = request.form["slope"]

        #dalam json ada key sama value, keynya yg dalam kurung kotak valuenya yg habis tanda sama dengan
        #identitas["nama"] = nama
        #identitas["umur"] = umur
 
        #masukkan data ke dalam database model
        model = ModelDatabase(
            age = ageData,
            sex = sexData,
            cp = cpData,
            trestbps = trestbpsData,
            chol = cholData,
            fbs = fbsData,
            restecg = restecgData,
            thalach = thalachData, 
            exang = exangData,
            oldpeak = oldpeakData,
            slope = slopeData

            )
        model.save()
        response = {"msg":"data berhasil dimasukkan", "code":200,}
        return response,200

    def delete(self):

        #hapus semua data
        query = ModelDatabase.query.all()

        #looping utk mengambil semua data
        for data in query:
            db.session.delete(data)
            db.session.commit()

        response = {
            "msg":"hapus semua data berhasil",
            "code": 200
        }
        return response

#class update database
class UpdateDatabase(Resource):

    #method
    def put(self,id):

        #pilih data yang ingin diedit berdasarkan id
        query = ModelDatabase.query.get(id)

        #form untuk edit
        ageEdit = request.form["age"]
        sexEdit = request.form["sex"]
        cpEdit = request.form["cp"]
        trestbpsEdit = request.form["trestbps"]
        cholEdit = request.form["chol"]
        fbsEdit = request.form["fbs"]
        restecgEdit = request.form["restecg"]
        thalachEdit = request.form["thalach"] 
        exangEdit = request.form["exang"]
        oldpeakEdit = request.form["oldpeak"]
        slopeEdit = request.form["slope"]
        
        #replace nilai yg ada di kolom
        query.age = ageEdit
        query.sex = sexEdit
        query.cp = cpEdit
        query.trestbps = trestbpsEdit
        query.chol = cholEdit
        query.fbs = fbsEdit
        query.restecg = restecgEdit
        query.thalach = thalachEdit
        query.exang = exangEdit
        query.oldpeak = oldpeakEdit
        query.slope = slopeEdit
    
        db.session.commit()

        response = {
            "msg":"edit data berhasil",
            "code": 200
        }
        return response



    def delete(self,id):   

         #pilih data yang ingin di hapus berdasarkan id
        queryData = ModelDatabase.query.get(id)
        db.session.delete(queryData)
        db.session.commit()

        response = {
            "msg":"hapus data berhasil",
            "code": 200
        }
        return response

#setup resource
#urlnya ada di /
api.add_resource(ContohResource, "/", methods=["GET","POST","DELETE"])
api.add_resource(UpdateDatabase, "/<id>", methods=["PUT","DELETE"])

if __name__=="__main__":
    app.run(debug=True, port=5005)
