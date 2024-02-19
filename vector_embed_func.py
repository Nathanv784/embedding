import os
from langchain_openai import OpenAI
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.vectorstores.pgvector import PGVector
import openai
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA,RetrievalQAWithSourcesChain

def process_text():
    try:
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')

        # Load
        loader = TextLoader('msd.txt', encoding='utf-8')
        documents = loader.load()
        print(len(documents))

        # Split
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=80)
        texts = text_splitter.split_documents(documents)
        print(len(texts))

        # Embedding
        embeddings = OpenAIEmbeddings()

        CONNECTION_STRING = os.getenv('DATABASE_URL')
        COLLECTION_NAME = 'state_of_union_vectors'

        # PG Vector
        db = PGVector.from_documents(
            embedding=embeddings,
            documents=texts,
            collection_name=COLLECTION_NAME,
            connection_string=CONNECTION_STRING,
        )
        print("Embedded successfully")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Call the function
process_text()
