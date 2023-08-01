# app.py

from flask import Flask, request, jsonify, render_template
import pdfkit
import requests
from dotenv import load_dotenv
try:
    from langchain.document_loaders import PyPDFLoader
    from langchain.indexes import VectorstoreIndexCreator #vectorize db index with chromadb
    from langchain.embeddings import HuggingFaceEmbeddings #for using HugginFace embedding models
    from langchain.text_splitter import CharacterTextSplitter #text splitter
except ImportError:
    raise ImportError("Could not import langchain: Please install ibm-generative-ai[langchain] extension.")
import os
from genai.extensions.langchain import LangChainInterface
from genai.model import Credentials
from genai.schemas import GenerateParams, ModelType

load_dotenv()
api_key = os.getenv("GENAI_KEY", None)
api_endpoint = os.getenv("GENAI_API", None)
if api_key is None or api_endpoint is None:
    print("ERROR: Ensure you copied the .env file that you created earlier into the same directory as this notebook")
else:
    creds = Credentials(api_key=api_key, api_endpoint=api_endpoint)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_pdf_and_summarize', methods=['POST'])
def generate_pdf_and_summarize():
    try:
        url = request.form['url']

        pdfkit.from_url(url, 'output.pdf')

        summary = summarize_pdf_with_langchain('output.pdf')
        # os.remove('output.pdf')
        # Return the summary to the client
        return jsonify({'summary': summary})

    except Exception as e:
        return jsonify({'error': str(e)})

def summarize_pdf_with_langchain(pdf_file_path):
    # Load the PDF file and summarize using LangChain

    loaders = [PyPDFLoader(pdf_file_path)]
    index = VectorstoreIndexCreator(
        embedding=HuggingFaceEmbeddings(),
        text_splitter=CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)).from_loaders(loaders)

    params = GenerateParams(
        decoding_method="sample",
        max_new_tokens=300,
        min_new_tokens=50,
        stream=False,
        temperature=0.2,
        top_k=100,
        top_p=1,
    )

    model = LangChainInterface(model=ModelType.FLAN_UL2, credentials=creds, params=params)
    from langchain.chains import RetrievalQA
    chain = RetrievalQA.from_chain_type(llm=model, 
                                        chain_type="stuff", 
                                        retriever=index.vectorstore.as_retriever(), input_key="question") 
                              
    thing = chain.run("give a summary about this passage")
    return thing

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
