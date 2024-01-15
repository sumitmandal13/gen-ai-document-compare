import uuid,json,ast 
from flask_restx import Namespace,Resource
from services.s3_helper import put_presigned_url,convert_s3_url
from config.config import S3_SAVE_INPUT_BUCKET
from flask import session

ns_session_api = Namespace('session_api',description = "api for creating session")

@ns_session_api.route('/',methods=['POST'])
class Redirect(Resource):
    def post(self):
        session_id = str(uuid.uuid4())
        session_id_1 = session_id+"_doc_1"
        session_id_2 = session_id+"_doc_2"
        file_name_presigned_url = put_presigned_url(session_id_1)
        file_name_presigned_url_2 = put_presigned_url(session_id_2)
        
        session_data = {"session_id_1":session_id_1,
                        "session_id_2":session_id_2,
                        "file_name_presigned_url":file_name_presigned_url,
                        "file_name_presigned_url_2":file_name_presigned_url_2}
        
        return session_data
    
    
