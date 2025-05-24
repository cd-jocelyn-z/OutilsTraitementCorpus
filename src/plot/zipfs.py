from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from process.corpus_utils import load_json 
from typing import List

def extract_corpus(path: Path) -> List[str]:
    corpus = load_json(path)
    docs = []
    episodes = corpus.episodes

    for ep in episodes:
        title = ep.episode_title.strip() if ep.episode_title else ""
        desc = ep.short_description.strip() if ep.short_description else ""
        combined = f"{title}. {desc}".strip()
        docs.append(combined)

    return docs


def plot_zipfs(docs):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(docs)
    vocab = vectorizer.get_feature_names_out()
    frequencies = np.asarray(X.sum(axis=0)).flatten()
    sorted_freqs = sorted(frequencies, reverse=True)
    ranks = np.arange(1, len(sorted_freqs) + 1)

    plt.figure(figsize=(8, 5))
    plt.loglog(ranks, sorted_freqs)
    plt.title("Loi de Zipf sur le corpus (titre + description)")
    plt.xlabel("Rang du mot")
    plt.ylabel("Fréquence")
    plt.grid(True)
    plt.show()



def main():
    docs = extract_corpus(Path("data/clean/full_corpus.json"))
    plot_zipfs(docs)

if __name__ == "__main__":
    main()