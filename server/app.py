#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Research, Author, ResearchAuthor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

class Research_Route(Resource):
    def get(self):
        all_research = Research.query.all()
        ar_to_dict = []
        for research in all_research:
            ar_to_dict.append(research.to_dict(rules = ('-researchauthors','-authors')))
        return ar_to_dict,200
    
class One_Research_Route(Resource):
    def get(self, id):
        research = Research.query.filter(Research.id==id).first()
        if research:
            return research.to_dict(),200
        else:
            return {"error": "Research paper not found"},400
    def delete(self,id):
        research = Research.query.filter(Research.id==id).first()
        if research:
            db.session.delete(research)
            db.session.commit()
            return {},200
        else:
            return {"error": "Research paper not found"},400

class Authors_Route(Resource):
    def get(self):
        all_author = Author.query.all()
        aa_to_dict = []
        for research in all_author:
            aa_to_dict.append(research.to_dict(rules = ('-researchauthors')))
        return aa_to_dict,200
    
class ResearchAuthor_Route(Resource):
    def post(self):
        data = request.get_json()
        try:
            ra = ResearchAuthor(
                author_id = data["author_id"],
                research_id = data["research_id"]
            )
            db.session.add(ra)
            db.session.commit()
            return ra.to_dict(),201
        except:
            return {"errors": ["validation errors"]},400
    

api.add_resource(Research_Route,'/research')
api.add_resource(One_Research_Route,'/research/<int:id>')
api.add_resource(Authors_Route,'/author')
api.add_resource(ResearchAuthor_Route,'/researchauthor')
if __name__ == '__main__':
    app.run(port=5555, debug=True)
