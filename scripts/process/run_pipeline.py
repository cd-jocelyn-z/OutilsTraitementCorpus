from pathlib import Path
from scraper import scrape_schedule, scrape_playlist
from crawler import crawl_program_index
from corpus_utils import save_json
from datastructures import Corpus
import time

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def main():
    print("Scraping WFMU schedule...")
    base_episodes = scrape_schedule("https://www.wfmu.org/table")

    target_titles = {
        "why do we only listen to dead people?",
        "feelings",
        "radio futura",
        "radio ravioli",
        "weekly world blues",
        "polyglot",
        "strength through failure"
    }

    filtered_episodes = [ep for ep in base_episodes if ep.program_name.lower() in target_titles]

    corpus = Corpus(episodes=filtered_episodes)
    raw_path = PROJECT_ROOT / "data/raw/schedule_stub.json"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    save_json(corpus, raw_path)
    print(f"Saved base schedule: {raw_path}")

    full_episodes = []
    for base_episode in filtered_episodes:
        print(f"\nProcessing program: {base_episode.program_name} ({base_episode.program_url})")
        episodes = crawl_program_index(base_episode.program_url, base_episode)
        for ep in episodes[:5]:
            print(f"Fetching playlist: {ep.playlist_url}")
            time.sleep(3)
            tracks, title, date = scrape_playlist(ep.playlist_url)
            ep.tracks = tracks
            ep.episode_title = title or ep.episode_title
            ep.episode_date = date or ep.episode_date
            full_episodes.append(ep)

    enriched_corpus = Corpus(episodes=full_episodes)
    clean_path = PROJECT_ROOT / "data/clean/full_corpus.json"
    clean_path.parent.mkdir(parents=True, exist_ok=True)
    save_json(enriched_corpus, clean_path)
    print(f"\nSaved enriched corpus: {clean_path}")

if __name__ == "__main__":
    main()
