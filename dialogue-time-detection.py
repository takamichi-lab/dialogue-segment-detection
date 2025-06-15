from pyannote.audio import Pipeline
import torch
from util import segmentation, annotate_mono_diag

# pyannote settings
ACCESS_TOKEN = ""
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=ACCESS_TOKEN)
pipeline.to(torch.device("cuda"))

def speaker_diarization(in_wav_path):
    diarization = pipeline(in_wav_path)
    
    return [
        {"start": turn.start, "end": turn.end, "speaker": speaker}
        for turn, _, speaker in diarization.itertracks(yield_label=True)
    ]


def dialogue_time_detection(diarization):
    segment = segmentation([x["speaker"] for x in diarization])
    annotated_segment = annotate_mono_diag(segment)
    annotated_segment = sum(annotated_segment, [])

    return annotated_segment

if __name__ == "__main__":
    in_wav_path = "2spkr-dialogue_then_monologue.wav"

    diarization = speaker_diarization(in_wav_path)
    dial_mono = dialogue_time_detection(diarization)

    print(diarization)

    for d, m in zip(diarization, dial_mono):
        print(f"{d['start']:.1f} - {d['end']:.1f}[sec]: {d['speaker']} {m}")

