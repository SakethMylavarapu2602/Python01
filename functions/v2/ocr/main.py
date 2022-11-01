# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START functions_cloudevent_ocr]
from google.cloud import storage
from google.cloud import translate_v2 as translate
from google.cloud import vision

import functions_framework


vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()
publisher = pubsub_v1.PublisherClient()
storage_client = storage.Client()

project_id = os.environ["GCP_PROJECT"]


# [START functions_cloudevent_ocr_detect]
@functions_framework.cloud_event
def detect_text(cloud_event):
    """ Extract the text from an image when uploaded to Cloud Storage, then
        trigger events requesting the text be translated to each target language.
    """

    # Check that the received event is of the expected type, return error if not
    expected_type = "google.cloud.storage.object.v1.finalized"
    received_type = cloud_event.type
    if received_type != expected_type:
        return "Expected {expected_type} but received {received_type}", 400

    # Extract the bucket and file names of the uploaded image for processing
    data = cloud_event.data
    bucket = data["bucket"]
    filename = data["name"]

    # Use the Vision API to extract text from the image
    image = vision.Image(
        source=vision.ImageSource(gcs_image_uri=f"gs://{bucket}/{filename}")
    )

    text_detection_response = vision_client.text_detection(image=image)
    annotations = text_detection_response.text_annotations

    if len(annotations) > 0:
            text = annotations[0].description
    else:
        text = ""
    print("Extracted text {} from image ({} chars).".format(text, len(text)))

    detect_language_response = translate_client.detect_language(text)
    src_lang = detect_language_response["language"]
    print("Detected language {} for text {}.".format(src_lang, text))



# [END functions_cloudevent_storage]
