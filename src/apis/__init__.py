from flask_restx import Api

from apis.create_session import ns_session_api
from apis.ask_question import ns_ask_question_api

rest_api = Api()

rest_api.add_namespace(ns_session_api)
rest_api.add_namespace(ns_ask_question_api)
