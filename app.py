import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS  # vector embeddings
from langchain_google_genai import ChatGoogleGenerativeAI  # chatgooglegenai
from langchain.chains.question_answering import load_qa_chain  # do the chat and prompt
from langchain.prompts import PromptTemplate  # the main prompt
from dotenv import load_dotenv  # load env

load_dotenv()

# config the API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# function to read the PDF and extract text
def get_pdf_text(pdf_docs):
    text = ""
    if pdf_docs is None:
        return text
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)  # read specific PDF
        for page in pdf_reader.pages:  # to get the info in form of list
            text += page.extract_text() or ""  # extract all the text (added or "" for safety)
    return text


# function to divide it into smaller chunks
def get_text_chunks(text):
    if not text:
        return []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


# take chunks and save in vectors
def get_vector_store(text_chunks):
    if not text_chunks:
        st.warning("No text chunks to process!")
        return
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")  # save entire info in folder as vectors so when I ask Q, it gives answers from vectors


# question-answering system that answers based only on a given context
def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)  # Prompt + Model → Chain: Combines the prompt and model into a QA chain
    return chain


# fetch similar docs and pass to chain
def user_input(user_question):
    if not os.path.exists("faiss_index"):
        st.warning("Please upload and process PDF files first!")
        return

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    try:
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)

        chain = get_conversational_chain()

        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

        st.write("Reply: ", response["output_text"])
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


# main app structure
def main():
    st.set_page_config("PaperPal")
    st.header(" :green[PaperPal - Chat with PDF!]")

    user_question = st.text_input(":blue[Ask a Question from the PDF Files]")

    if user_question:
        user_input(user_question)


    with st.sidebar:
        st.title(":blue[Menu:]")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button(":red[Submit & Process]"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")
    with st.sidebar:
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")
            st.markdown("---")
            st.markdown("Powered by GenAI & FAISS | Built with ❤️ by Shreya Joshi")
                        



if __name__ == "__main__":
    main()