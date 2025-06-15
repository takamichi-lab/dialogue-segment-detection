# Spoken dialogue segment detection / 音声対話区間検出
This script labels segments of audio files as either dialogue or non-dialogue.

このスクリプトでは，音声ファイルから，音声対話の時間区間とそれ以外の時間区間をラベリングします．


## Setup / 事前準備
Please follow the instructions in [pyannote](https://github.com/pyannote/pyannote-audio) to enable `pyannote/speaker-diarization-3.1`. Agree to the terms of use and issue an access token (`hf_xxx`). Insert the access token into the `ACCESS_TOKEN = ""` field in `dialogue-time-detection.py`.

[pyannote](https://github.com/pyannote/pyannote-audio)にしたがって，`pyannote/speaker-diarization-3.1` を使用可能にしてください．利用条件に同意して，access token (`hf_xxx`)を発行してください．その access token を，`dialogue-time-detection.py` の `ACCESS_TOKEN = ""` に書いてください．

## Usage / 使い方
```
python dialogue-time-detection.py
```
The script will run on `2spkr-dialogue.wav`. The output will look like the following:

`2spkr-dialogue.wav` に対してスクリプトを実行します．実行結果は以下のように表示されます．
```
0.0 - 0.8[sec]: SPEAKER_01 dialogue_000
1.2 - 2.0[sec]: SPEAKER_00 dialogue_000
2.6 - 3.3[sec]: SPEAKER_00 dialogue_000
4.1 - 4.9[sec]: SPEAKER_01 dialogue_000
```
- `{%1.1f} - {%1.1f}[sec]`: Start and end time of the utterance
- `SPEAKER_{%2d}`: Label for the speaker; `{%2d}` is the speaker number
- `{dialogue, monologue}_{%03d}`: Indicates whether the segment is a dialogue (`dialogue`) or non-dialogue (`monologue`) segment; `{%03d}` is the segment index
In the above example, a segment between 0.0 - 4.9 sec is identified as dialogue.


- `{%1.1f} - {%1.1f}[sec]`: 発話の開始終了時刻
- `SPEAKER_{%2d}`: その発話の話者ラベル．`{%2d}` が話者番号
- `{dialogue, monologue}_{%03d}`: 対話区間 (`{dialogue}`) か非対話区間 (`{monologue}`) の別．`{%03d}` は区間番号．
- このファイルの例では，0.0 - 4.9秒が，1つの対話区間になります．

## Paper / 参考文献
TBA