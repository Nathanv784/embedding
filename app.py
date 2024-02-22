from flask import Flask, request
import os
from langchain_community.document_loaders import TextLoader ,PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.memory import ConversationBufferMemory
import openai
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from prompt import PROMPT

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

# Function to process text based on file type
def process_text(file_path):
    try:
        with app.app_context():
            # Set up OpenAI API key
            openai.api_key = os.getenv('OPENAI_API_KEY')

            # Load documents based on file type
            if file_path.lower().endswith('.txt'):
                loader = TextLoader(file_path, encoding='utf-8')
            elif file_path.lower().endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            else:
                raise ValueError("Unsupported file format")

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

            # Conversation history
            chat_history = []

            memory = ConversationBufferMemory(memory_key="chat_history", input_key='question', output_key='answer', return_messages=True)
            
            # Retrieval
            retriever = db_vector.as_retriever(search_kwargs={"k": 3})
            
            llm = ChatOpenAI(temperature=0.0, model='gpt-4-1106-preview')
            qa_stuff = RetrievalQAWithSourcesChain.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                verbose=True,
                memory=memory,
                return_source_documents=False
            )

            # Interaction loop
            while True:
                user_query = input("You: ").strip()  # Get and strip user input
                
                # Prepare the full prompt with the user's query
                full_prompt = PROMPT.format(user_query=user_query)
              
                # Invoke the AI model
                response = qa_stuff.invoke(full_prompt)

                # Print the response 
                print("Bot:", response.get('answer'))

                # Store the query and response in the database
                query_entry = Query(question=user_query, response=response.get('answer'))
                db.session.add(query_entry)
                db.session.commit()
                print("Data stored in the database successfully.")
                
                # Append the conversation to the chat history
                chat_history.append({"User": user_query, "Assistant": response})

    except Exception as e:
        print(f"An error occurred: {str(e)}")

import os

# Function to ensure directory exists
def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    # breakpoint()
    file = request.files['file']
    if 'file' not in request.files:
        return 'No file part'
    
    else:
        upload_directory = './uploads'
        ensure_directory(upload_directory)  # Ensure the directory exists
        file_path = os.path.join(upload_directory, file.filename)
        file.save(file_path)
        process_text(file_path)
        return 'File uploaded and processed successfully'


if __name__ == "__main__":
    app.run(debug=True)
