import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datastructures import Episode, Track
from typing import List, Optional, Tuple

def scrape_schedule(url: str) -> List[Episode]:
    """
    Fonction qui permet de scraper la page contenant le tableau 
    des programmes de diffusion de la radio.

    Args :
        url (str) : Lien vers la page à traiter.
    
    Retour :
        episodes (List[Episode]) : Liste d'objets Episode contenant 
        les informations de chaque diffusion, telles que le nom du programme, 
        le DJ, la description courte et le créneau horaire de diffusion.
    """

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    program_cells = soup.find_all("td", class_="program")

    episodes = []
    for cell in program_cells:
        program_tag = cell.find("span", class_="show-title")
        dj_tag = cell.find("span", class_="djs")
        time_tag = cell.find("span", class_="program_time")

        program_name = program_url = short_description = None
        if program_tag:
            a_tag = program_tag.find("a")
            if a_tag:
                program_name = a_tag.get_text(strip=True)
                program_url = urljoin("https://www.wfmu.org", a_tag.get("href", ""))
                short_description = " ".join(a_tag.get("title", "").split())

        dj_name = dj_tag.get_text(strip=True).replace("with", "").strip() if dj_tag else None
        program_time = time_tag.get_text(strip=True) if time_tag else None

        episode = Episode(
            program_name=program_name,
            program_url=program_url,
            short_description=short_description,
            dj_name=dj_name,
            schedule_time=program_time
        )
        episodes.append(episode)
    return episodes

def scrape_playlist(url: str) -> Tuple[List[Track], Optional[str], Optional[str]]:
    """
    Fonction qui permet de scraper la page de la playlist radio
    et d’en extraire les morceaux diffusés ainsi que les métadonnées de l’épisode.

    Args :
        url (str) : Lien vers la page de la playlist à traiter.

    Retour :
        Tuple contenant :
            - tracks (List[Track]) : Liste d’objets Track représentant les morceaux diffusés.
            - episode_title (Optional[str]) : Titre de l’épisode (s’il est disponible).
            - episode_date (Optional[str]) : Date de diffusion de l’épisode (si disponible).
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    tracks = []

    episode_title = episode_date = None
    p = soup.find("p", id="date_desc_archive_section")
    if p:
        text = p.get_text(separator="\n", strip=True)
        if ":" in text:
            date_part, title_part = text.split(":", 1)
            episode_date = date_part.strip()
            episode_title = title_part.split("Listen", 1)[0].strip()

    table = soup.find("table", id="drop_table")
    if not table:
        return [], episode_title, episode_date

    for row in table.find_all("tr"):
        artist_td = row.find("td", class_="song col_artist")
        title_td = row.find("td", class_="song col_song_title")
        album_td = row.find("td", class_="song col_album_title")
        label_td = row.find("td", class_="song col_record_label")
        year_td = row.find("td", class_="song col_year")

        if title_td:
            summary_span = title_td.find("span", id=lambda x: x and x.endswith("_summary_html"))
            if summary_span:
                full_text = summary_span.get_text(strip=True).strip('"')
                if ' by ' in full_text:
                    title_str, artist_str = full_text.split(' by ', 1)
                    song_title = title_str.strip('" ')
                    artist_name = artist_str.strip('" ')
                else:
                    song_title = title_td.get_text(strip=True)
                    artist_name = artist_td.get_text(strip=True) if artist_td else None
            else:
                song_title = title_td.get_text(strip=True)
                artist_name = artist_td.get_text(strip=True) if artist_td else None

            track = Track(
                artist=artist_name,
                track=song_title,
                album=album_td.get_text(strip=True) if album_td else None,
                label=label_td.get_text(strip=True) if label_td else None,
                year=year_td.get_text(strip=True) if year_td else None,
            )
            tracks.append(track)

    return tracks, episode_title, episode_date
