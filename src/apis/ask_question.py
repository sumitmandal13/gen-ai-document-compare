from flask import request,session
from flask_restx import Namespace,Resource
import boto3,tempfile
import json 
import uuid 
from config.config import S3_EMBEDDINGS_PATH
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter



ns_ask_question_api = Namespace('ask_question',description = "api for asking question")
runtime = boto3.Session().client("sagemaker-runtime",verify=False)

@ns_ask_question_api.route('/',methods=['POST'])
class Redirect(Resource):
    def post(self):
        session_id_1 = request.form.get("session_id_1")
        print("Session_id",session_id_1)
        session_id_2 = request.form.get("session_id_2")
        question = request.form.get("question")

        file_1 = request.files.get('file_path_1')
        file_2 = request.files.get('file_path_2')
        # filepath = data.get('file_path')
        temp_dir = tempfile.mkdtemp()
        # print("filepath",filepath)


        file_1.save(f"{temp_dir}/file_1.pdf")
        file_2.save(f"{temp_dir}/file_2.pdf")
        
        loader = PyPDFLoader(f"{temp_dir}/file_1.pdf")
        document_1 = loader.load()

        
        
        embeddings = HuggingFaceEmbeddings()
        # docsearch_1 = FAISS.from_documents(texts, embeddings).save_local("/tmp/faiss_store", 'meidcare')


        loader2 = PyPDFLoader(f"{temp_dir}/file_2.pdf")
        document_2 = loader2.load()

        print(document_1,"document_2\n\n",document_2)
        

        text_splitter1 = RecursiveCharacterTextSplitter(chunk_size=300,
                                                    separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
                                                    chunk_overlap=0)

        texts1 = text_splitter1.split_documents(document_1)
        texts2 = text_splitter1.split_documents(document_2)

        vector_db1 = FAISS.from_documents(documents=texts1, embedding=embeddings)
        vector_db2 = FAISS.from_documents(documents=texts2, embedding=embeddings)

        score = 0.90

        # Use "mmr" or "similarity_score_threshold"
        retriever1 = vector_db1.as_retriever(search_type='mmr', search_kwargs={"k": 10, "score_threshold" : score})
        retriever2 = vector_db2.as_retriever(search_type='mmr', search_kwargs={"k": 10, "score_threshold" : score})


        relevant_docs1 = retriever1.get_relevant_documents(question)
        relevant_docs2 = retriever2.get_relevant_documents(question)


        full_context1 = str()
        full_context2 = str()

        for doc in relevant_docs1:
            full_context1 += doc.page_content+" "
            
        for doc in relevant_docs2:
            full_context2 += doc.page_content+" "


        import json
        from langchain import PromptTemplate, LLMChain

        from langchain.llms.sagemaker_endpoint import LLMContentHandler, SagemakerEndpoint

        parameters ={
                "max_new_tokens": 100,
                "num_return_sequences": 1,
                "top_k": 50,
                "top_p": 0.95,
                "do_sample": False,
                "return_full_text": False,
                "temperature": 0.2
            }

        class ContentHandler(LLMContentHandler):
            content_type = "application/json"
            accepts = "application/json"

            def transform_input(self, prompt: str, model_kwargs={}) -> bytes:
                input_str = json.dumps({"inputs": prompt, "parameters": model_kwargs})
                return input_str.encode("utf-8")

            def transform_output(self, output: bytes) -> str:
                response_json = json.loads(output.read().decode("utf-8"))
                return response_json[0]["generated_text"]


        content_handler = ContentHandler()

        sm_llm_falcon_instruct = SagemakerEndpoint(
            endpoint_name="pdf-endpoint",
            region_name="ap-south-1",
            model_kwargs=parameters,
            content_handler=content_handler,
        )


        template = """

        Human: Assume you are an insurance broker. Answer the {question} using the provided text. Skip any preamble text and reasoning and give just the answer. Answer in the same language as the question.


        <question>{question}</question>
        <text>{doc1}</text>
        <text>{doc2}</text>
        <answer>


        Assistant:"""

        prompt = PromptTemplate(template=template, input_variables=["doc1","doc2","question"])

        
        llm_chain = LLMChain(prompt=prompt, llm=sm_llm_falcon_instruct)

        answer = llm_chain.run(doc1 = full_context1, doc2 = full_context2, question = question )
        print(answer.strip())



        return answer