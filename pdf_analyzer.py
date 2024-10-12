import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt
import io
import base64
import os

def download_nltk_data():
    required_resources = ['punkt', 'stopwords']
    for resource in required_resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            print(f"Downloading {resource}...")
            nltk.download(resource, quiet=True)

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    return tokens

def analyze_text(tokens):
    word_freq = Counter(tokens)
    most_common = word_freq.most_common(10)
    return most_common

def generate_word_cloud(tokens):
    plt.figure(figsize=(10, 5))
    plt.bar(*zip(*analyze_text(tokens)))
    plt.title("Top 10 Most Common Words")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return img_str

def generate_html_report(pdf_path, tokens, most_common, word_cloud_img):
    html = f"""
    <html>
    <head>
        <title>PDF Analysis Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0 auto; max-width: 800px; padding: 20px; }}
            h1, h2 {{ color: #333; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>PDF Analysis Report</h1>
        <h2>File: {os.path.basename(pdf_path)}</h2>
        <h2>Word Count: {len(tokens)}</h2>
        <h2>Top 10 Most Common Words:</h2>
        <table>
            <tr><th>Word</th><th>Frequency</th></tr>
            {''.join(f'<tr><td>{word}</td><td>{count}</td></tr>' for word, count in most_common)}
        </table>
        <h2>Word Frequency Visualization:</h2>
        <img src="data:image/png;base64,{word_cloud_img}" alt="Word Frequency Chart">
    </body>
    </html>
    """
    return html

def analyze_pdf_file(pdf_path, report_folder):
    download_nltk_data()
    text = extract_text_from_pdf(pdf_path)
    tokens = preprocess_text(text)
    most_common = analyze_text(tokens)
    word_cloud_img = generate_word_cloud(tokens)
    html_report = generate_html_report(pdf_path, tokens, most_common, word_cloud_img)
    
    report_filename = f"report_{os.path.basename(pdf_path)}.html"
    report_path = os.path.join(report_folder, report_filename)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    return report_filename

if __name__ == "__main__":
    # This block is for testing the script independently
    pdf_path = "input.pdf"  # Replace with your PDF file path
    report_folder = "reports"  # Replace with your report folder path
    report_filename = analyze_pdf_file(pdf_path, report_folder)
    print(f"Analysis complete. HTML report saved as {report_filename}")