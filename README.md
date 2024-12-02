# Semantic Prompt with LangChain and FastAPI

This repository implements a semantic similarity-based example selector and few-shot prompting using LangChain, Chroma for vector storage, and FastAPI for building a RESTful API. The application dynamically generates AI responses using OpenAI's GPT models by leveraging stored examples for context and semantic relevance.

---

## **Features**

1. **Semantic Similarity Example Selector:**
   - Utilizes Chroma vector store and OpenAI embeddings to find the most relevant examples based on the query.

2. **Few-Shot Prompting:**
   - Dynamically generates responses tailored to the input query by referencing similar examples stored in the vector database.

3. **Dynamic Date Handling:**
   - Automatically substitutes relative date ranges (e.g., last week, last quarter) with accurate start and end dates in responses.

4. **FastAPI Integration:**
   - Exposes a RESTful endpoint for sending queries and receiving AI-generated responses.

5. **CORS Middleware:**
   - Enables cross-origin resource sharing (CORS) for seamless integration with frontend applications.

---

## **Repository Structure**

- **`app.py`:** Main FastAPI application containing the LangChain pipeline and REST API logic.
- **`chroma_db/`:** Directory to store Chroma vector database (created at runtime).
- **`.env`:** Environment variables file for storing the OpenAI API key securely.

---

## **Setup Instructions**

### 1. **Clone the Repository**
```bash
git clone <repository_url>
cd <repository_folder>
```

### 2. **Install Dependencies**
Ensure you have Python installed, then install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. **Set OpenAI API Key**
- Create a `.env` file in the project directory:
  ```plaintext
  OPENAI_KEY=your_openai_api_key
  ```
- The application will automatically load this key.

### 4. **Run the Application**
Start the FastAPI server:
```bash
uvicorn app:app --reload
```
The server will run at `http://127.0.0.1:8000` by default.

---

## **API Documentation**

FastAPI provides interactive API documentation at:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### **Endpoint: `/run/`**
- **Method:** `POST`
- **Description:** Processes a query and generates a response using the LangChain pipeline.
- **Request Body:**
  ```json
  {
    "query": "Your query text here"
  }
  ```
- **Response:**
  - If successful:
    ```json
    {
      "key1": "value1",
      "key2": "value2",
      ...
    }
    ```
  - If there is an error:
    ```json
    {
      "error": "Error message"
    }
    ```

---

## **Usage**

### **Input Examples**
- "What steps are involved in refreshing all our records from the electronic health records?"
- "Showcase sales data for the last quarter."

### **Output**
- The response will include semantically relevant examples and tailored responses, including accurate date substitutions for relative timeframes.

---

## **Customization**

### **1. Chroma Vector Store**
- Add or update examples in the `chroma_db/` directory to improve response relevance.
- Use `OpenAIEmbeddings` for creating embeddings for new data.

### **2. Few-Shot Prompt Template**
- Modify the `few_shot_prompt` or the `final_prompt` in `app.py` to customize the response structure.

### **3. Model Parameters**
- Adjust model parameters (e.g., temperature, model type) in the `ChatOpenAI` configuration:
  ```python
  chain = final_prompt | ChatOpenAI(openai_api_key=OPENAI_KEY, model='gpt-4', temperature=0.7)
  ```

---

## **Dependencies**

- Python 3.7+
- LangChain
- Chroma
- OpenAI Python Library
- FastAPI
- Pydantic
- dotenv
- Uvicorn

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## **Notes**

1. **Persistent Database:**
   - The Chroma vector store is stored locally in the `./chroma_db` directory. Ensure this directory is accessible for the application.

2. **Cross-Origin Requests:**
   - The CORS middleware allows all origins by default. Restrict `origins` in `app.py` to specific domains for production use.

3. **Dynamic Date Handling:**
   - The system automatically handles relative date queries and substitutes them with precise date ranges.

---

## **License**
This project is licensed under the MIT License.

---
