from dataclasses import dataclass, field
from typing import Literal, Dict


@dataclass
class InputStructure:
    format: Literal["audio"] = "audio"
    filename: str = "input_audio.mp3"
    process_key: None = None

    @property
    def data_example(self):
        return None

    @property
    def process_type(self):
        return str(self.__annotations__[self.process_key]) if self.process_key is not None else None


@dataclass
class OutputStructure:
    format: Literal["json"] = "json"
    filename: str = "filename_example.json"
    process_key: str = "transcript"
    transcript: str = "This is the full transcript."

    segments: list = field(
        default_factory=lambda: [
            {
                "id": 1,
                "seek": 0,
                "start": 0.0,
                "end": 10.0,
                "text": "This is the",
                "tokens": [20, 34],
                "temperature": 0.0,
                "avg_logprob": 0.0,
                "compression_ratio": 0.0,
                "no_speech_prob": 0.0,
                "confidence": 0.0,
                "words": [
                    {"text": "This", "start": 0.0, "end": 1.0, "confidence": 0.5},
                    {"text": "is the", "start": 1.0, "end": 2.0, "confidence": 0.6},
                ],
            },
            {
                "id": 2,
                "seek": 10,
                "start": 10.0,
                "end": 20.0,
                "text": "main text",
                "tokens": [44, 101],
                "temperature": 0.0,
                "avg_logprob": 0.0,
                "compression_ratio": 0.0,
                "no_speech_prob": 0.0,
                "confidence": 0.0,
                "words": [
                    {"text": "main", "start": 10.0, "end": 11.0, "confidence": 0.7},
                    {"text": "text", "start": 11.0, "end": 12.0, "confidence": 0.8},
                ],
            },
        ]
    )
    language: Dict[str, str] = field(default_factory=lambda: {"language": "English"})

    @property
    def process_type(self):
        return str(self.__annotations__[self.process_key]) if self.process_key is not None else None

    @property
    def data_example(self):
        return {
            "transcript": self.transcript,
            "segments": self.segments,
            "language": self.language["language"],
        }
