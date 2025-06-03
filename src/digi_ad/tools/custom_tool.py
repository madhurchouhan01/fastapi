import os
from typing import Type

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

from pathlib import Path
# Load environment variables
load_dotenv()

# FAISS_DB_PATH = "vectorstore"
FAISS_DB_PATH = (Path(__file__).parent / "vectorstore").resolve()


class RAGToolInput(BaseModel):
    """Input schema for the RAGTool."""
    question: str = Field(..., description="The question to ask using the RAG pipeline.")


class FAQTool(BaseTool):
    name: str = "Cohere RAG QA Tool"
    description: str = (
        "This tool uses a Cohere-powered RAG pipeline with a FAISS vectorstore to answer "
        "questions based on the stored document context."
    )
    args_schema: Type[BaseModel] = RAGToolInput

    def _run(self, question: str) -> str:
        try:
            # Set up embeddings and load vectorstore
            embedding_model = CohereEmbeddings(
                model="embed-english-v3.0",
                user_agent="xalt_chatbot@example.com"
            )
            db = FAISS.load_local(
                FAISS_DB_PATH,
                embedding_model,
                allow_dangerous_deserialization=True
            )

            # Build retriever and prompt
            retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
            llm = ChatCohere(model="command-xlarge-nightly", temperature=0)

            prompt_template = """
                    You are a helpful assistant. Use ONLY the context below to answer the question.
                    If the answer is not contained within the context, say :
                    "I can't provide an answer to that question as it is not covered in the information available to me. To get the best results, try asking questions related to DigiAd's features, functionality, or supported platforms. For example, you could ask: 'How does DigiAd help with ad targeting?' or 'What payment methods does DigiAd accept?' If you're looking for information outside of DigiAd's scope, I recommend reaching out to our support team at support@digiad.com for further assistance."
            
                    Context:
                    {context}

                    Question:
                    {question}

                    Answer:
                    """
            PROMPT = PromptTemplate(
                input_variables=["context", "question"],
                template=prompt_template
            )

            # Create RAG QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=False,
                chain_type_kwargs={"prompt": PROMPT}
            )

            # Run the query
            result = qa_chain.invoke(question)
            return result["result"]

        except Exception as e:
            return f"An error occurred while processing the question: {str(e)}"
