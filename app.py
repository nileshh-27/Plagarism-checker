from flask import Flask, request, jsonify
import requests 
from bs4 import BeautifulSoup 
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity 
import fitz  # PyMuPDF 
import numpy as np 
from PIL import Image 

app = Flask(__name__)

# Add your actual API keys here
API_KEY = 'your api key'
CSE_ID = 'your cse key'

# Your helper functions
def google_search(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CSE_ID}&q={query}"
    response = requests.get(url)
    results = response.json()
    return [item['link'] for item in results.get('items', [])]

def fetch_webpage_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text
    except Exception as e:
        return ""

def calculate_similarity(input_text, web_text):
    documents = [input_text, web_text]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0] * 100

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text += page.get_text()
    return text

@app.route('/check_plagiarism', methods=['POST'])
def check_plagiarism():
    file = request.files.get('file')
    text = request.form.get('text')

    if text:
        phrases = text.split('. ')[:3]
        results = []
        for phrase in phrases:
            urls = google_search(phrase)
            for url in urls:
                web_text = fetch_webpage_text(url)
                if web_text:
                    similarity_percentage = calculate_similarity(text, web_text)
                    results.append({"url": url, "similarity": f"{similarity_percentage:.2f}%"})
        return jsonify(results=results)

    elif file:
        file_path = f"./temp/{file.filename}"
        file.save(file_path)
        extracted_text = extract_text_from_pdf(file_path)
        phrases = extracted_text.split('. ')[:3]
        results = []
        for phrase in phrases:
            urls = google_search(phrase)
            for url in urls:
                web_text = fetch_webpage_text(url)
                if web_text:
                    similarity_percentage = calculate_similarity(extracted_text, web_text)
                    results.append({"url": url, "similarity": f"{similarity_percentage:.2f}%"})
        return jsonify(results=results)

    return jsonify({"error": "No input provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
