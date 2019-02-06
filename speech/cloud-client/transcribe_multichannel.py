#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample that demonstrates enhanced models
and recognition metadata.

Example usage:
    python transcribe_multichannel.py resources/audio.raw
    python transcribe_multichannel.py \
        gs://cloud-samples-tests/speech/Google_Gnome.wav
"""

import argparse
import io


def transcribe_file_with_multichannel(speech_file):
    """Transcribe the given audio file synchronously with
      multi channel."""
    # [START speech_transcribe_multichannel]
    from google.cloud import speech
    client = speech.SpeechClient()

    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        audio_channel_count=1,
        enable_separate_recognition_per_channel=True)

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print(u'Transcript: {}'.format(alternative.transcript))
        print(u'Channel Tag: {}'.format(result.channel_tag))
    # [END speech_transcribe_multichannel]


def transcribe_gcs_with_multichannel(gcs_uri):
    """Transcribe the given audio file on GCS with
      multi channel."""
    # [START speech_transcribe_multichannel_gcs]
    from google.cloud import speech
    client = speech.SpeechClient()

    audio = speech.types.RecognitionAudio(uri=gcs_uri)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        audio_channel_count=1,
        enable_separate_recognition_per_channel=True)

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print(u'Transcript: {}'.format(alternative.transcript))
        print(u'Channel Tag: {}'.format(result.channel_tag))
    # [END speech_transcribe_multichannel_gcs]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs_with_multichannel(args.path)
    else:
        transcribe_file_with_multichannel(args.path)
