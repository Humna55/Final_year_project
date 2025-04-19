from flask import request, Response, jsonify
from flask_restful import Resource
from database.models import Course

class courseApi(Course):
    def get(self):
        try:
            data=Course.objects().to_json()
            return Response(data,mimetype="application/json",status=200)
        except Exception as e:
            return Response(status=404)