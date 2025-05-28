import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from langchain_community.vectorstores import Chroma

load_dotenv()
word_embedding_model = os.getenv("WORD_EMBEDDING_MODEL")

# Change working directory to the one containing scrapped data
os.chdir(os.pardir)
os.chdir('ScrappedData')
scrapped_data = os.getcwd()
stock_data_3m = os.path.join(scrapped_data, "NESTLEIND_3m.txt")

# Load the text
with open(stock_data_3m, 'r', encoding='utf-8') as f:
    text = f.read()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_text(text)

# Load the embedding model
embedding = HuggingFaceEmbeddings(
    model_name=word_embedding_model,
    model_kwargs={"trust_remote_code": True}
)

# Store chunks in Chroma vector DB
vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=embedding,
    persist_directory="D:/Selenium/ChatBot/db"
)
