import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
import openai
from flask_migrate import Migrate

# Initialize Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the model
class Query(db.Model):
    __tablename__ = "queries"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text())
    response = db.Column(db.Text())

def process_text():
    try:
        with app.app_context():
            # Set up OpenAI API key
            openai.api_key = os.getenv('OPENAI_API_KEY')

            # Load text documents
            loader = TextLoader('msd.txt', encoding='utf-8')
            documents = loader.load()

            # Split text documents
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=80)
            texts = text_splitter.split_documents(documents)

            # Embedding
            embeddings = OpenAIEmbeddings()

            # PG Vector
            COLLECTION_NAME = 'state_of_union_vectors'
            db_vector = PGVector.from_documents(
                embedding=embeddings,
                documents=texts,
                collection_name=COLLECTION_NAME,
                connection_string=os.getenv('DATABASE_URL')
            )
            print("Embedded successfully")

            # Retrieval
            retriever = db_vector.as_retriever(search_kwargs={"k": 3})

            llm = ChatOpenAI(temperature=0.0, model='gpt-3.5-turbo-16k')
            qa_stuff = RetrievalQAWithSourcesChain.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                verbose=True,
                return_source_documents=False
            )

            query = str(input("Enter: "))
            response = qa_stuff.invoke(query)
            print(response)

            # Store in database
            query_entry = Query(question=query, response=response['answer'])
            db.session.add(query_entry)
            db.session.commit()
            print("Data stored in the database successfully.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Call the function
if __name__ == "__main__":
    process_text()
