**📄 PaperPal – Chat with Your PDF Using AI 🤖**

**Tech Stack**: Python · Streamlit · LangChain · FAISS · Google Generative AI · PyPDF2 · dotenv

**🔍 What is PaperPal?**

PaperPal is an AI-powered web app that lets you upload any PDF and ask questions about it. It uses Google's Gemini Pro model with LangChain to give smart, accurate answers based only on the content of your uploaded file.

---

### ✨ Features

* ✅ Upload multiple PDF files
* ✅ Extract and process text automatically
* ✅ Ask questions in natural language
* ✅ Uses FAISS for fast document search
* ✅ Context-aware answers using Gemini AI
* ✅ Simple and clean Streamlit interface
* ✅ Secure API key handling with `.env`

---

How It Works

1. **Upload** your PDF(s) via the sidebar.
2. **Text is extracted** and split into chunks.
3. **FAISS** creates a vector database for semantic search.
4. Ask questions in the text box — the app fetches relevant chunks and replies using Gemini.

---

Project Structure

```
📦 PaperPal
├── app.py                 # Main Streamlit app
├── requirements.txt       # Required Python packages
├── .env                   # API key (not pushed to GitHub)
├── faiss_index/           # Folder where FAISS vector data is stored
```

---

Setup Instructions

1. Clone the repo
   `git clone https://github.com/your-username/paperpal.git`

2. Install dependencies
   `pip install -r requirements.txt`

3. Add your API key to a `.env` file:

   ```
   GOOGLE_API_KEY=your-key-here
   ```

4. Run the app
   `streamlit run app.py`

---

