import streamlit as st
import pandas as pd
import uuid
import chromadb
import re  # for URL validation
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.document_loaders import WebBaseLoader
import requests  # for URL validation and error handling

# Sidebar for API key and model name
st.sidebar.title("Configuration")
groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
model_name = st.sidebar.text_input("Enter Model Name", "llama-3.1-70b-versatile")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")

# Initialize ChromaDB client and collection
client = chromadb.PersistentClient('vectorstore')
collection = client.get_or_create_collection(name="portfolio")

# Initialize LangChain model only if API key is provided
if groq_api_key:
    llm = ChatGroq(
        temperature=0,
        groq_api_key=groq_api_key,
        model_name=model_name
    )

# Main Section
st.title("Cold Email and Cover Letter Generator")
st.write("Upload a CSV file with `Techstack` and `Links` columns on the sidebar, then enter a job URL to generate a cover letter and email.")

# Step 1: CSV Upload with Validation
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        # st.write("Columns in the CSV file:", df.columns)
        
        # Validate required columns in CSV file
        if "Techstack" not in df.columns or "Links" not in df.columns:
            st.error("The uploaded CSV should contain 'Techstack' and 'Links' columns.")
        else:
            # Populate ChromaDB if empty
            if collection.count() == 0:
                for _, row in df.iterrows():
                    techstack = row["Techstack"]
                    link = row["Links"]
                    collection.add(
                        documents=[techstack],
                        metadatas={"links": link},
                        ids=[str(uuid.uuid4())]
                    )
                st.write(f"Total documents in collection: {collection.count()}")
            else:
                st.write("Collection already populated.")
    except Exception as e:
        st.error(f"Error reading the CSV file: {e}")
else:
    st.info("Please upload a CSV file from the sidebar.")

# Step 2: Job URL Input with Validation (Always visible)
job_url = st.text_input("Enter the Job URL")

# Validate URL format
url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

# Step 3: Validation for Job URL Submission
if job_url:
    # Check if the URL format is valid
    if not url_pattern.match(job_url):
        st.error("Please enter a valid Job URL (starting with http:// or https://).")
    else:
        # Check if API Key and CSV file are provided
        if not groq_api_key or not uploaded_file:
            st.error("Please enter your Groq API Key and upload a CSV file before proceeding.")
        else:
            try:
                # Load the webpage content
                loader = WebBaseLoader(job_url)
                page_data = loader.load().pop().page_content
                
                # Extract job description
                prompt_extract = PromptTemplate.from_template(
                    """
                    ### SCRAPED TEXT FROM WEBSITE:
                    {page_data}
                    ### INSTRUCTION:
                    Extract job postings in JSON format with keys: `role`, `experience`, `skills`, `description`.
                    ### VALID JSON (NO PREAMBLE):
                    """
                )
                
                # Chain for extraction
                chain_extract = prompt_extract | llm
                res = chain_extract.invoke(input={'page_data': page_data})
                
                # Parse JSON result
                json_parser = JsonOutputParser()
                job_data = json_parser.parse(res.content)
                
                # Display extracted job data
                st.write("Extracted Job Data:", job_data)
                
                # Step 4: Query Portfolio Links
                job_skills = job_data.get('skills', '')
                query_result = collection.query(
                    query_texts=job_skills,
                    n_results=2
                )
                links = [metadata['links'] for metadata_list in query_result['metadatas'] for metadata in metadata_list]
                st.write("Matched Portfolio Links:", links)
                
                # Step 5: Generate Cover Letter
                job_description = job_data.get('description', '')
                prompt_email = PromptTemplate.from_template(
                    """
                    ### JOB DESCRIPTION:
                    {job_description}
                    
                    ### INSTRUCTION:
                    Write a cover letter from Hamid Hussain, BDE at Technity Solutions, detailing how Technity Solutions can meet the company's needs.
                    Use portfolio examples: {link_list}.
                    ### COVER LETTER (NO PREAMBLE):
                    """
                )
                
                chain_email = prompt_email | llm
                email_res = chain_email.invoke({"job_description": job_description, "link_list": links})
                
                # Display generated cover letter
                st.subheader("Generated Cover Letter")
                st.write(email_res.content)
            except requests.exceptions.RequestException as e:
                st.error(f"Error loading the job URL: {e}")
else:
    st.info("Please enter the Job URL to proceed.")
