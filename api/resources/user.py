from api import Resource, reqparse, db, auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema


class UserResource(Resource):
    def get(self, user_id=None):
        if user_id is not None:
            user = UserModel.query.get(user_id)
            if not user:
                return {"Error": f"User with id={user_id} not found"}, 404
            return user_schema.dump(user), 200
        users = UserModel.query.all()
        return users_schema.dump(users)

    # @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        parser.add_argument("role")
        data = parser.parse_args()
        user = UserModel(**data)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("password")
        data = parser.parse_args()
        user = UserModel.query.get(user_id)
        if data["username"]:
            user.username = data["username"]
        if data["password"]:
            user.hash_password(data["password"])
        db.session.commit()
        return user_schema.dump(user)
