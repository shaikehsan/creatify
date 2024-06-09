import requests
from bs4 import BeautifulSoup
import trafilatura
import random
import time
from datetime import datetime
import spacy
import matplotlib.pyplot as plt
import streamlit as st

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def get_useragent():
    _useragent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
    ]
    return random.choice(_useragent_list)

def split_in_sentences(text):
    sentences = [x.strip() for x in text.strip().replace('\n', '').split(". ")]
    return sentences

def generate_shingles(text, k):
    shingles = set()
    text = text.lower().split()  # Convert text to lowercase and split into words
    for i in range(len(text) - k + 1):
        shingle = ' '.join(text[i:i + k])  # Join k consecutive words to form a shingle
        shingles.add(shingle)
    return shingles

def similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    return (intersection / len(set1)) * 100

def similarity_score(input_text, collected_text, k=3):
    shingles1 = generate_shingles(input_text, k)
    shingles2 = generate_shingles(collected_text, k)
    similarity_score = similarity(shingles1, shingles2)
    return similarity_score

def semantic_similarity_score(input_text, collected_text):
    doc1 = nlp(input_text)
    doc2 = nlp(collected_text)
    return doc1.similarity(doc2) * 100

def get_content(url):
    for i in range(3):
        try:
            download = trafilatura.fetch_url(url)
            content = trafilatura.extract(download, include_comments=False, include_tables=False)
            if content:
                return content
        except Exception as e:
            print(f"Error fetching content from {url}: {e}")
        time.sleep(1)  # Add delay to avoid rapid repeated requests
    return ''

def google_search(query):
    links = []
    headers = {'User-Agent': get_useragent()}
    response = requests.get(
        url="https://www.google.com/search",
        headers=headers,
        params={"q": f'"{query}"', "num": 5, "hl": 'en'}
    )

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('h3')
        for idx, result in enumerate(search_results, start=1):
            link = result.find_parent('a')
            if link:
                link_text = link.get('href')
                if link_text and link_text.startswith('http'):
                    links.append(link_text)
    else:
        print("Failed to perform the Google search.")
    return links

def get_results(sentences):
    sources = {}
    url_content_cache = {}

    for sentence in sentences:
        serp_urls = google_search(sentence)
        temp = {}
        for url in serp_urls:
            if url in url_content_cache:
                content = url_content_cache[url]
            else:
                content = get_content(url)
                url_content_cache[url] = content
            shingle_score = similarity_score(sentence, content)
            semantic_score = semantic_similarity_score(sentence, content)
            combined_score = (shingle_score + semantic_score) / 2
            temp[url] = int(combined_score)
        
        if temp:
            max_score_url = max(temp, key=temp.get)
            max_score = temp[max_score_url]
            current_score = {'url': max_score_url, 'score': max_score}

            if sources:
                last_sentence = list(sources.keys())[-1]
                last_url = sources[last_sentence]['url']
                last_url_score = sources[last_sentence]['score']
                if last_url == max_score_url:
                    combined_sentence = last_sentence + ". " + sentence
                    sources[combined_sentence] = {'url': max_score_url, 'score': int((max_score + last_url_score) / 2)}
                    del sources[last_sentence]
                else:
                    sources[sentence] = current_score
            else:
                sources[sentence] = current_score
    
    return sources

def plagiarism_checker(input_text):
    sentences = split_in_sentences(input_text)
    print("Time =", datetime.now().strftime("%H:%M:%S"))
    result = get_results(sentences)
    print("scores Time =", datetime.now().strftime("%H:%M:%S"))
    return result

def generate_detailed_report(input_text):
    report = ""
    try:
        result = plagiarism_checker(str(input_text))
        all_scores = []
        for key, value in result.items():
            report += f'\n{"-"}\nSentence: {key}\nSource: {value["url"]}\nText Matches: {value["score"]}%\n'
            all_scores.append(value['score'])
        if all_scores:
            total_score = sum(all_scores) / len(all_scores)
            report += f'\n\nOverall Originality Score: {int(100 - total_score)}%\nPlagiarism Score: {int(total_score)}%\n'
        
        # Additional visual representation (e.g., using matplotlib for graphs)
        labels = 'Unique', 'Plagiarized'
        sizes = [100 - total_score, total_score]
        colors = ['#66b3ff', '#ff9999']
        explode = (0.1, 0)
        
        fig, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=140)
        ax.axis('equal')
        plt.title('Content Originality')
        st.pyplot(fig)
        
    except Exception as e:
        report = f'Error: {e}'
    return report

def main():
    st.title("Plagiarism Checker")
    input_text = st.text_area("Enter the text you want to check for plagiarism", height=200)
    if st.button("Check for Plagiarism"):
        if input_text.strip():
            with st.spinner("Checking..."):
                final_output = generate_detailed_report(input_text)
            st.success("Check complete!")
            st.markdown(final_output)
        else:
            st.error("Please enter some text to check for plagiarism.")

if __name__ == "__main__":
    main()
