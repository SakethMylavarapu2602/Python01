#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
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

"""Google Cloud Speech API sample application using the streaming API.

Example usage:
    python transcribe_streaming.py resources/audio.raw
"""

# [START import_libraries]
import argparse
import io
# [END import_libraries]


def transcribe_streaming(stream_file):
    """Streams transcription of the given audio file."""
    from google.cloud.speech import SpeechClient
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = SpeechClient()

    with io.open(stream_file, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
        request = types.StreamingRecognizeRequest(audio_content=content)

        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
        sample_rate_hertz = 16000
        language_code = 'en-US'
        config = types.RecognitionConfig(
              encoding=encoding,
              sample_rate_hertz=sample_rate_hertz,
              language_code=language_code)

        config = types.StreamingRecognitionConfig(config=config)

        requests = [request]

        for response in client.streaming_recognize(config, requests):
            for result in response.results:
                print('Finished: {}'.format(result.is_final))
                print('Stability: {}'.format(result.stability))
                alternatives = result.alternatives
            for alternative in alternatives:
                print('Confidence: {}'.format(alternative.confidence))
                print('Transcript: {}'.format(alternative.transcript))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('stream', help='File to stream to the API')
    args = parser.parse_args()
    transcribe_streaming(args.stream)
