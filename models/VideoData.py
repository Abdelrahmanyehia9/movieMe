from dataclasses import dataclass
from typing import List
from models.Scene import Scene

@dataclass
class GeneratedVideo:
    scenes: List[Scene]
    videoUrl: str
    isVoiceOver: bool
    photos: List[str]
    voiceOverLang: str
    duration: float
    status: str
    voiceOverText: str
    voiceOverGender: str
