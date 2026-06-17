import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.logger import logger

def build_chain(vectorstore):
    """
    Takes the populated ChromaDB vector store and builds the LangChain 
    retrieval-augmented generation (RAG) pipeline using Gemini 1.5 Flash.
    """
    logger.info("Building RAG chain...")
    
    try:
        # 1. Verify API Key
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            logger.error("GOOGLE_API_KEY environment variable is missing!")
            raise ValueError("GOOGLE_API_KEY is not set. Please set it before running the app.")

        # 2. Initialize the LLM
        logger.debug("Initializing Gemini 1.5 Flash model...")
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

        # 3. Setup the Retriever
        # k=4 ensures it pulls the top 4 most relevant chunks from ChromaDB
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

        # 4. Define the Prompt Template (Guardrails against hallucinations)
        template = PromptTemplate.from_template("""
        You are a helpful AI assistant. Answer the user's question using ONLY the provided context from the uploaded document.
        If you cannot find the answer in the text, politely say "I cannot find the answer to that in the provided document."

        <context>
        {context}
        </context>

        Question: {query}
        Answer:
        """)

        # 5. Helper function to combine document chunks into a single string
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # 6. Build the LangChain Expression Language (LCEL) Pipeline
        chain = (
            {"context": retriever | format_docs, "query": RunnablePassthrough()}
            | template
            | llm
            | StrOutputParser()
        )
        
        logger.info("Successfully built RAG chain.")
        
        # Return the fully compiled chain back to app.py
        return chain

    except Exception as e:
        logger.error(f"Failed to build RAG chain: {str(e)}", exc_info=True)
        raise e