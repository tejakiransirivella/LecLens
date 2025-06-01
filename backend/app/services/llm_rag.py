from typing import List
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate

from pathlib import Path

class LLMRAGService:

    def __init__(self):
        load_dotenv()
        self.llm = init_chat_model("gemini-2.0-flash",model_provider="google_genai")
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=400)
        self.home_dir = Path(__file__).resolve(strict=True).parents[3]

    def create_vector_store(self,transcript: str) -> FAISS:
        chunks = self.text_splitter.split_documents([Document(page_content=transcript)])
        vector_store = FAISS.from_documents(chunks,embedding=self.embeddings)
        return vector_store
        
    def get_context(self,vector_store:FAISS, question: str) -> str:
        matching_chunks = vector_store.similarity_search(question, k=3)
        context = "\n\n".join([chunk.page_content for chunk in matching_chunks])
        return context

    def answer_user_query(self,vector_store: FAISS, question: str) -> str:
        context = self.get_context(vector_store, question)
        prompt = self.get_prompt(f"{self.home_dir}/data/prompts/user_query.txt")
        prompt = self.replace_placeholders(prompt, context, question)
        response = self.llm.invoke(prompt)
        response = self.extract_text(response)
        return response
    
    def generate_notes(self, vector_store: FAISS) -> str:
        chunks = list(vector_store.docstore._dict.values())
        print(f"Number of chunks: {len(chunks)}")
        map_prompt = PromptTemplate.from_template(self.get_prompt(f"{self.home_dir}/data/prompts/map.txt"))
        reduce_prompt = PromptTemplate.from_template(self.get_prompt(f"{self.home_dir}/data/prompts/reduce.txt"))
        chain = load_summarize_chain(self.llm, chain_type="map_reduce",map_prompt =map_prompt, combine_prompt=reduce_prompt)
        result = chain.invoke({"input_documents": chunks})
        summary = result['output_text']
        return summary

    def get_prompt(self,file: str) -> str:
        prompt = None
        with open(file, "r") as file:
            prompt = file.read()
        return prompt
    
    def replace_placeholders(self,prompt:str, transcript: str, user_parameter: str) -> str:
        transcript_placeholder = "[Insert the lecture transcript here.]"
        user_submitted_placeholder = "[Insert the user submitted parameter here]"
        prompt = prompt.replace(transcript_placeholder, transcript)
        prompt = prompt.replace(user_submitted_placeholder, user_parameter)
        return prompt
    
    def extract_text(self,response: str) -> str:
        return response.content.strip()

def main():
    llm_rag_service = LLMRAGService()
   
    transcript_path =  f"{llm_rag_service.home_dir}/data/transcripts/transcript1.txt"
    with open(transcript_path, "r") as file:
        transcript = file.read()
    question = "what are main types of AI?"
    vector_store = llm_rag_service.create_vector_store(transcript)
    # response = llm_rag_service.answer_user_query(vector_store, question)
    response = llm_rag_service.generate_notes(vector_store)
    print(response)

if __name__ == "__main__":
    main()








