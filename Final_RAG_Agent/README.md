# Personal Wellness Agent

The **Personal Wellness Agent** is an AI-powered tool designed to provide personalized wellness advice based on user queries and biometric data. It leverages advanced natural language processing and document retrieval techniques to deliver actionable insights and recommendations for improving mental and physical health.

---

## Features

- **Biometric Data Integration**: Accepts user-provided biometric data such as heart rate, mood, exercise status, and sleep quality.
- **Document Retrieval**: Dynamically loads and retrieves relevant information from a knowledge base of `.docx` and `.pdf` files.
- **Personalized Advice**: Generates professional wellness advice tailored to the user's query and biometric data.
- **Input Validation**: Ensures user queries are appropriate and free from harmful or inappropriate content.
- **Health Synopsis**: Summarizes user health data and provides motivational or concern-based feedback.

---

## Project Structure


---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. Set up a virtual environment:
   ```bash
   python3 -m venv personal_wellness_agent
   source personal_wellness_agent/bin/activate  # On Windows, use personal_wellness_agent\Scripts\activate

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Configure environment variables:

- Create a .env file in the root directory.
- Add the following variables:

   ```bash
   OPENAI_API_KEY=<your_openai_api_key>
   FOLDER_PATH=<path_to_RAG_Documents_folder>

---

## Usage

1. Run the application:
   ```bash
   python main.py

2. Follow the prompts to:

- Enter your query.
- Provide biometric data (heart rate, mood, exercise status, and sleep description).

3. Receive personalized wellness advice based on your input.

---

Workflow Overview
The application uses the following workflow:

1. **Input Validation**: Ensures the query is appropriate.
2. **Document Loading**: Loads and processes .docx and .pdf files from the knowledge base.
3. **Document Retrieval**: Retrieves relevant documents based on the query and biometric data.
4. **Health Synopsis**: Summarizes user health data and retrieved content.
5. **Advice Generation**: Provides professional advice tailored to the user's query and health synopsis.

---

## Dependencies

The project uses the following Python libraries:

- langchain
- langchain-openai
- langchain_community
- langgraph
- pypdf
- pydantic
- python-dotenv
- python-docx
- faiss-cpu
- docx2txt

Install all dependencies using the requirements.txt file.

---

## Knowledge Base

The knowledge base was created from a folder that contained categorized .docx and .pdf files on topics such as:

- Common sicknesses and remedies
- Mental health problems and coping strategies
- Motivation and affirmations
- Sleep issues and remedies

