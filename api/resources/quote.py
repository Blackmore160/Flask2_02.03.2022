from api import Resource, reqparse, db
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
from api.schemas.quote import quote_schema, quotes_schema


class QuoteResource(Resource):
    def get(self, author_id=None, quote_id=None):
        """
        Обрабатываем GET запросы
        :param id: id цитаты
        :return: http-response("текст ответа", статус)
        """
        if author_id is None and quote_id is None:
            quotes = QuoteModel.query.all()
            return quotes_schema.dump(quotes)

        author = AuthorModel.query.get(author_id)
        if quote_id is None:
            quotes = author.quotes.all()
            return quotes_schema.dump(quotes), 200

        quote = QuoteModel.query.get(quote_id)
        if quote is not None:
            return quote_schema.dump(quote), 200
        return {"Error": "Quote not found"}, 404

    def post(self, author_id):
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        parser.add_argument("rate", required=False)
        quote_data = parser.parse_args()
        author = AuthorModel.query.get(author_id)
        if author:
            quote = QuoteModel(author, **quote_data)
            db.session.add(quote)
            db.session.commit()
            return quote_schema.dump(quote), 201
        return {"Error": f"Author id={author_id} not found"}, 404

    def put(self, author_id, quote_id):
        parser = reqparse.RequestParser()
        parser.add_argument("text")
        parser.add_argument("rate")
        new_data = parser.parse_args()
        quote = QuoteModel.query.get(quote_id)
        author = AuthorModel.query.get(author_id)
        if quote is None:
            quote = QuoteModel(author, **new_data)
            db.session.add(quote)
            db.session.commit()
            return quote_schema.dump(quote), 201
        if new_data["text"]:
            quote.text = new_data["text"]
        if new_data["rate"]:
            quote.rate = new_data["rate"]
        db.session.commit()
        return quote_schema.dump(quote), 200

    def delete(self, quote_id):
        quote = QuoteModel.query.get(quote_id)
        if quote is None:
            return f"Quote with id {quote_id} not found", 404
        db.session.delete(quote)
        db.session.commit()
        return quote_schema.dump(quote), 200
