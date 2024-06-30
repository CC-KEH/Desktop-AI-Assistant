import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader

from saved_data.prompts import *

load_dotenv()

pdfs_path = "saved_data/pdfs/"
genai.configure(api_key = os.environ["gemini_api_key"])

class VectorStorePipeline:
    def get_pdfs(self,pdfs_path):
        pdfs = []
        for pdf in os.listdir(pdfs_path):
            pdfs.append(pdfs_path + pdf)
        return pdfs
    
    def get_pdf_text(self,pdf_docs):
        text = ""
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    def get_text_chunks(self,text):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=1000)
        chunks = text_splitter.split_text(text)
        return chunks


    def get_vector_store(self,text_chunks):
        embeddings = GoogleGenerativeAIEmbeddings(google_api_key=os.environ["gemini_api_key"],model='models/embedding-001')
        vector_store = FAISS.from_texts(text_chunks, embeddings)
        vector_store.save_local('faiss_index')


class Brain:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(google_api_key=os.environ["gemini_api_key"],model='gemini-pro',temperature=0.3)
    
    def get_conversational_chain(self):
        self.prompt = PromptTemplate(template=rag_prompt,input_variables=['context','question'])
        self.chain = load_qa_chain(self.llm,chain_type='stuff',prompt=self.prompt)
        return self.chain

    def ask(self,question):
        response = self.llm.invoke(question)
        return dict(response)['content']
    
    def process_user_input(self,question):
        embeddings = GoogleGenerativeAIEmbeddings(google_api_key=os.environ["gemini_api_key"],model='models/embedding-001')
        new_db = FAISS.load_local('faiss_index',embeddings,allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(question)
        chain = self.get_conversational_chain()
        response = chain({"input_documents": docs,"question": question},return_only_outputs=True)
        return response['output_text']
    
if __name__ == '__main__':
    brain = Brain()
    context = context_str
    question = "What is your name?"
    response = brain.ask(f"{context},+question: {question}")
    print(response)
    # Rag
    vs = VectorStorePipeline()
    pdfs = vs.get_pdfs(pdfs_path)
    text = vs.get_pdf_text(pdfs)
    chunks = vs.get_text_chunks(text)
    vs.get_vector_store(chunks)
    
    print(brain.process_user_input("What is Advanced RAG?"))