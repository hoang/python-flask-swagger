from restplus import api
from flask_restplus import Resource
from serializers import welcome_output

ns = api.namespace('test', description='Operations related to tests')


@ns.route('/')
class TestCollection(Resource):

    @api.marshal_with(welcome_output)
    def get(self):
        return {"message": "welcome to test api", "version": 1.17}
