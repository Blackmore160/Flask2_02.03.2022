from api import db
from api.models.author import AuthorModel


class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
    rate = db.Column(db.Integer, nullable=False, server_default="0", default="1")
    text = db.Column(db.String(255), unique=False)

    def __init__(self, author: AuthorModel, text: str, rate):
        self.author_id = author.id
        self.text = text
        self.rate = rate

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "quote": self.text,
    #         "author": self.author.to_dict(),
    #         "rate": self.rate
    #     }
