from email import message
import sqlite3
from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

import nasapy
import os
from datetime import datetime
import urllib
import pandas as pd
from requests import delete

app = Flask(__name__)

api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class PhotoModel(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    explanation=db.Column(db.String(450),nullable=False)
    hdurl=db.Column(db.String(250),nullable=False)
    title=db.Column(db.String(100),nullable=False)
    url=db.Column(db.String(250),nullable=False)

    def __repr__(self) -> str:
        return f"PhotoModel(explanation={self.explanation},hdurl={self.hdurl},title={self.title},url={self.url})"
def init_db():
    db.create_all()
    db.session.commit()

      
photo_put_args=reqparse.RequestParser()
photo_put_args.add_argument("explanation",type=str,help="Explanation of the photo",required=True)
photo_put_args.add_argument("hdurl",type=str,help="hdurl of the photo",required=True)
photo_put_args.add_argument("title",type=str,help="title of the photo",required=True)
photo_put_args.add_argument("url",type=str,help="url of the photo",required=True)

photo_update_args=reqparse.RequestParser()
photo_update_args.add_argument("explanation",type=str,help="Explanation of the photo")
photo_update_args.add_argument("hdurl",type=str,help="hdurl of the photo")
photo_update_args.add_argument("title",type=str,help="title of the photo")
photo_update_args.add_argument("url",type=str,help="url of the photo")


llave="aX3a4dvx7RPjBpjyhaf0ex75BWN5bDgwImZmQETm"
nasa=nasapy.Nasa(key=llave)


    
resource_fields={
    'id': fields.Integer,
    'explanation': fields.String,
    'hdurl': fields.String,
    'title': fields.String,
    'url': fields.String

}

class Photo(Resource):
    
    @marshal_with(resource_fields)
    def get(self,photo_id):
        result=PhotoModel.query.filter_by(id=photo_id).first()
        return result
    @marshal_with(resource_fields)
    def put(self, photo_id,fecha):
        #fechaPoner=datetime.strptime(fecha,'%Y-%m-%d').date()
        apod = nasa.picture_of_the_day(fecha, hd=True)
        codigo=204
        if apod["media_type"] == "image":
            if "hdurl" in apod.keys():
                photo=PhotoModel(id=photo_id,explanation=apod["explanation"],hdurl=apod["hdurl"],title=apod["title"],url=apod["url"])
                db.session.add(photo)
                db.session.commit()
                print(photo)
        else:
            codigo=404

        return codigo
    def delete(self,photo_id):
        PhotoModel.query.filter_by(id=photo_id).delete()
        db.session.commit()
        return 204
    @marshal_with(resource_fields)
    def patch(self,photo_id):
        body=photo_update_args.parse_args()
        resultado=PhotoModel.query.filter_by(id=photo_id).first()
        if not resultado:
            abort(404,message="La imagen no existe.")
        else:
           for i in body:
               if body[i] is not None:
                   resultado.i=i
        db.session.commit()
        return resultado     
api.add_resource(Photo, "/put_photo/<int:photo_id>/<string:fecha>",endpoint='/put_photo')
api.add_resource(Photo, "/get_photo/<int:photo_id>/") 
api.add_resource(Photo, "/delete_photo/<int:photo_id>/",endpoint='/delete_photo')
api.add_resource(Photo, "/update_photo/<int:photo_id>/",endpoint='/update_photo')
if __name__ == "__main__":
    init_db()
    app.run()
    