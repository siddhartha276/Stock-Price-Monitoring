import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import re

# Load environment variables
load_dotenv()

class ChatBot:
    def __init__(self):
        # Initialize once
        HUGGING_FACE_HUB_API_TOKEN = os.getenv("HUGGING_FACE_API_KEY")
        model = os.getenv("HUGGING_FACE_MODEL")
        embedding_model = os.getenv("WORD_EMBEDDING_MODEL")

        self.client = InferenceClient(
            model=model,
            token=HUGGING_FACE_HUB_API_TOKEN
        )

        self.embedding = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={"trust_remote_code": True}
        )

        self.vectorstore = Chroma(
            persist_directory="D:/Selenium/ChatBot/db",
            embedding_function=self.embedding
        )

    def generate_response(self, query):
        # Retrieve similar documents
        docs = self.vectorstore.similarity_search(query, k=4)
        context = "\n\n".join([doc.page_content for doc in docs])

        # Construct prompt
        prompt = f"Use the following context to answer the question:\n\nContext:\n{context}\n\nQuestion:\n{query}"

        # Make a text generation request to Hugging Face
        response = self.client.text_generation(
            prompt=prompt,
            max_new_tokens=200,
            temperature=0.7,
            do_sample=True,
        )

        # Split and clean
        lines = re.split(r'\.(?!\d)', response)
        output = [line.strip() for line in lines if line.strip()]
        return output

    def print_answer(self, lines):
        for line in lines:
            print(line)

# Usage
if __name__ == "__main__":
    bot = ChatBot()
    ans = bot.generate_response("What is the opening price, closing price and previous day's closing price of TATACOMM's stock on 27th May 2025")
    bot.print_answer(ans)
