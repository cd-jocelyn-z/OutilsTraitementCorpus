import json
from pathlib import Path
from dataclasses import asdict
from datastructures import Corpus, Episode, Track

def save_json(corpus: Corpus, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8") as fp:
        json.dump(asdict(corpus), fp, ensure_ascii=False, indent=2, sort_keys=True)

def load_json(input_file: Path) -> Corpus:
    with input_file.open("r", encoding="utf-8") as fp:
        data = json.load(fp)

    episodes = []
    for episode_dict in data.get("episodes", []):
        tracks = [Track(**t) for t in episode_dict.get("tracks", [])]
        ep = Episode(**{**episode_dict, "tracks": tracks})
        episodes.append(ep)

    return Corpus(episodes=episodes)