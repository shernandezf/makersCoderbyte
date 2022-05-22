from email import message
import sqlite3
from turtle import title
from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

import nasapy
import os
from datetime import datetime
import urllib
import pandas as pd

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
    def post(self,photo_id):
        if photo_id==0:
            abort(400,message="El id 0, está reservado, porfavor usar otro")
        check=PhotoModel.query.filter_by(id=photo_id).first()
        if check:
            abort(409, message="Ya existe esa foto con ese id")
        body=photo_put_args.parse_args()
        photo=PhotoModel(id=photo_id,explanation=body["explanation"],hdurl=body["hdurl"],title=body["title"],url=body["url"])
        db.session.add(photo)
        db.session.commit()
        return photo
    @marshal_with(resource_fields)
    def get(self,photo_id):
        if photo_id==0:
            ROWS_PER_PAGE=5
            args = request.args
            args.to_dict()
            args.get("filter", default="", type=str)
            args.get("filter_value", default="", type=str)
            if args.get("filter") is not None or args.get("filter_value") is not None:
                expresion='%'+str(args.get("filter_value"))+'%'
                if args.get("filter")=='id':
                    result=PhotoModel.query.filter(PhotoModel.id.ilike(expresion)).all()
                elif args.get("filter")=='explanation':
                    result=PhotoModel.query.filter(PhotoModel.explanation.ilike(expresion)).all()
                elif args.get("filter")=='hdurl':
                    result=PhotoModel.query.filter(PhotoModel.hdurl.ilike(expresion)).all()
                elif args.get("filter")=='title':
                    result=PhotoModel.query.filter(PhotoModel.title.ilike(expresion)).all()
                elif args.get("filter")=='url':
                    result=PhotoModel.query.filter(PhotoModel.url.ilike(expresion)).all()
            else:
                result=PhotoModel.query.all()
        else:
            result=PhotoModel.query.filter_by(id=photo_id).first()
        if not result:
            abort(404,message="La imagen no existe.")
        return result
    @marshal_with(resource_fields)
    def put(self, photo_id,fecha):
        if photo_id==0:
            abort(400,message="El id 0, está reservado, porfavor usar otro")
        apod = nasa.picture_of_the_day(fecha, hd=True)
        codigo=204
        if apod["media_type"] == "image":
            if "hdurl" in apod.keys():
                photo=PhotoModel(id=photo_id,explanation=apod["explanation"],hdurl=apod["hdurl"],title=apod["title"],url=apod["url"])
                db.session.add(photo)
                db.session.commit()
        else:
            codigo=404

        return photo
    def delete(self,photo_id):
        resultado=PhotoModel.query.filter_by(id=photo_id).first()
        if not resultado:
            abort(404,message="La imagen no existe.")
        else:
            PhotoModel.query.filter_by(id=photo_id).delete()
        db.session.commit()
        return {},204
    @marshal_with(resource_fields)
    def patch(self,photo_id):
        if photo_id==0:
            abort(400,message="El id 0, está reservado, porfavor usar otro")
        body=photo_update_args.parse_args()
        resultado=PhotoModel.query.filter_by(id=photo_id).first()
        if not resultado:
            abort(404,message="La imagen no existe.")
        else:
           for i in body:
               if body[i] is not None:
                   if i=='title':
                        resultado.title=body[i]
                   elif i=='explanation':
                        resultado.explanation=body[i]
                   elif i=='hdurl':
                        resultado.hdurl=body[i]
                   elif i=='url':
                        resultado.url=body[i]
        db.session.commit()
        return resultado  
api.add_resource(Photo, "/put_photo_create/<int:photo_id>/",endpoint='/put_photo_create')   
api.add_resource(Photo, "/put_photo/<int:photo_id>/<string:fecha>",endpoint='/put_photo')
api.add_resource(Photo, "/get_photo/<int:photo_id>/",endpoint='/get_photo') 
api.add_resource(Photo, "/delete_photo/<int:photo_id>/",endpoint='/delete_photo')
api.add_resource(Photo, "/update_photo/<int:photo_id>/",endpoint='/update_photo')
if __name__ == "__main__":
    init_db()
    app.run()
    