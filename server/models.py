from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here
class Research(db.Model,SerializerMixin):
    __tablename__ = "researches"

    id = db.Column(db.Integer, primary_key = True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    researchauthors = db.relationship("ResearchAuthor", back_populates="research")
    authors = association_proxy('researchauthors', 'author',
                                 creator=lambda author_obj: ResearchAuthor(author=author_obj))

    serialize_rules = ('-researchauthors.research',)

    @validates('year')
    def validate_year(self,key,value):
        if 1000<=value<=9999:
            return value
        else:
            raise ValueError(value)


class Author(db.Model,SerializerMixin):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    researchauthors = db.relationship("ResearchAuthor", back_populates="author")

    serialize_rules = ('-researchauthors.author',)

    @validates('field_of_study')
    def validate_fos(self,key,value):
        valid_studies = ["AI", "Robotics", "Machine Learning", "Vision", "Cybersecurity"]
        if value in valid_studies:
            return value
        else:
            raise ValueError("Not valid study")


class ResearchAuthor(db.Model,SerializerMixin):
    __tablename__ = "researchauthors"

    id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
    research_id = db.Column(db.Integer,  db.ForeignKey("researches.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    author = db.relationship("Author", back_populates="researchauthors")
    research = db.relationship("Reseach", back_populates="researchauthors")

    serialize_rules = ('-research.researchauthors','-author.researchauthors')
