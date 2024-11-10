# **Cold Email and Cover Letter Generator**

This project is a web-based tool designed to help job applicants generate personalized cold emails and cover letters for job applications in the tech industry. It extracts job postings from URLs, processes the data using AI, and matches the applicant’s portfolio based on required skills. The solution uses machine learning models, ChromaDB for portfolio storage, and LangChain for natural language generation. Additionally, the tool leverages Groq for AI model integration.

## **Features**
- **Job URL Parsing:** Allows users to input the URL of a company's careers page to extract job listings.
- **Portfolio Matching:** Uses ChromaDB to store and query portfolio links based on the required skills for the job position.
- **AI-Powered Email Generation:** Uses LangChain and Groq to generate personalized cold emails, including relevant portfolio links.
- **Streamlit Interface:** Provides an interactive and easy-to-use web interface for uploading portfolios, inputting job URLs, and viewing generated content.

---

## **Installation**

### **Requirements**
- Python 3.8+
- Streamlit
- LangChain
- ChromaDB
- Groq (API Key Required)
- Pandas
- Requests
- Regex (for URL validation)

### **Steps to Set Up:**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Cold-Email-Generator.git
   cd Cold-Email-Generator



2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Otain Your API KEY from Groq:**
4. **Run the Application:**
   ```bash
   streamlit run app.py

## **How It Works**

1. **CSV Upload:** 
   The portfolio CSV file is uploaded via the sidebar. The file should contain two columns: `Techstack` and `Links`.

2. **Job Description Extraction:** 
   A URL is provided, and the tool scrapes the job description and required skills using a web scraping technique.

3. **Portfolio Querying:** 
   The tool queries the portfolio stored in ChromaDB for relevant skills and links.

4. **AI-Powered Content Generation:** 
   Using Groq LLM and LangChain, the system generates a personalized cold email and cover letter tailored to the job description.
