from db import db
class Query(db.Model):
    __tablename__ = "queries"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text())
    response = db.Column(db.Text())