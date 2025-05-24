from typing import List
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from datastructures import Episode


def crawl_program_index(program_url: str, base_episode: Episode) -> List[Episode]:
    r = requests.get(program_url)
    soup = BeautifulSoup(r.text, "html.parser")
    episodes = []

    for li in soup.select("ul > li"):
        text = li.get_text(strip=True)
        if ":" not in text:
            continue

        date_part, rest = text.split(":", 1)
        date_str = date_part.strip()

        # Try parsing date for storage (not filtering)
        for fmt in ("%B %d, %Y", "%B %d"):
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                if fmt == "%B %d":
                    parsed_date = parsed_date.replace(year=2025)
                date_str = parsed_date.strftime("%B %d, %Y")
                break
            except ValueError:
                continue

        title_tag = li.find("b")
        title = title_tag.get_text(strip=True) if title_tag else rest.strip()
        playlist_link_tag = li.find("a", string=lambda s: s and ("See the playlist" in s or "Listen here" in s))
        if not playlist_link_tag:
            continue

        playlist_url = urljoin("https://www.wfmu.org", playlist_link_tag["href"])

        episode = Episode(
            program_name=base_episode.program_name,
            program_url=base_episode.program_url,
            dj_name=base_episode.dj_name,
            schedule_time=base_episode.schedule_time,
            short_description=base_episode.short_description,
            episode_title=title,
            episode_date=date_str,
            playlist_url=playlist_url
        )
        episodes.append(episode)

    return episodes