from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Track:
    """
    Classe utilisée pour représenter un morceau dans une playlist radio.

    Attributs
    artist : str
        Nom de l'artiste.
    track : str
        Titre du morceau.
    album : Optional[str]
        Nom de l'album (si disponible).
    label : Optional[str]
        Nom du label (si disponible).
    year : Optional[str]
        Année de sortie (si connue).
    """ 
    artist: str
    track: str
    album: Optional[str] = None
    label: Optional[str] = None
    year: Optional[str] = None

@dataclass
class Episode:
    """
    Classe utilisée pour représenter un épisode de radio avec ses métadonnées.

    Attributs
    program_name : str
        Nom de l’émission de radio.
    program_url : str
        URL de la page principale de l’émission.
    dj_name : Optional[str]
        Nom de l’animateur ou DJ (si disponible).
    schedule_time : Optional[str]
        Horaire de diffusion (si disponible).
    short_description : Optional[str]
        Courte description de l’émission (si disponible).
    episode_title : Optional[str]
        Titre de l’épisode (si disponible).
    episode_date : Optional[str]
        Date de diffusion de l’épisode.
    playlist_url : Optional[str]
        URL de la playlist associée à l’épisode.
    tracks : List[Track]
        Liste des morceaux diffusés pendant l’épisode.
    synthetic_desc : Optional[str]
        Description synthétique ou générée (par exemple par un modèle IA).
    """

    program_name: str
    program_url: str
    dj_name: Optional[str] = None
    schedule_time: Optional[str] = None
    short_description: Optional[str] = None
    episode_title: Optional[str] = None
    episode_date: Optional[str] = None
    playlist_url: Optional[str] = None
    tracks: List[Track] = field(default_factory=list)
    synthetic_desc: Optional[str] = None

@dataclass
class Corpus:
    """
    Classe utilisée pour représenter un corpus constitué d’épisodes radio.

    Attributs
    episodes : List[Episode]
        Liste des objets Episode qui composent le corpus.
    """
    episodes: List[Episode] = field(default_factory=list)