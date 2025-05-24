from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Track:
    artist: str
    track: str
    album: Optional[str] = None
    label: Optional[str] = None
    year: Optional[str] = None

@dataclass
class Episode:
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
    episodes: List[Episode] = field(default_factory=list)