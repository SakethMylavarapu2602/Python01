# Copyright 2019 Google
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid

from google.cloud import storage

import vision_async_batch_annotate_images

RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
GCS_ROOT = 'gs://cloud-samples-data/vision/'

BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
OUTPUT_PREFIX = 'TEST_OUTPUT_{}'.format(uuid.uuid4())
GCS_DESTINATION_URI = 'gs://{}/{}/'.format(BUCKET, OUTPUT_PREFIX)


def test_sample_asyn_batch_annotate_images(capsys):
  storage_client = storage.Client()
  bucket = storage_client.get_bucket(BUCKET)
  if len(list(bucket.list_blobs(prefix=OUTPUT_PREFIX))) > 0:
    for blob in bucket.list_blobs(prefix=OUTPUT_PREFIX):
      blob.delete()

  assert len(list(bucket.list_blobs(prefix=OUTPUT_PREFIX))) == 0

  input_image_uri = os.path.join(GCS_ROOT, 'label/wakeupcat.jpg')

  vision_async_batch_annotate_images.sample_async_batch_annotate_images(
    input_image_uri=input_image_uri, output_uri=GCS_DESTINATION_URI)

  out, _ = capsys.readouterr()
  
  assert 'Output written to GCS' in out
  assert len(list(bucket.list_blobs(prefix=OUTPUT_PREFIX))) > 0

  for blob in bucket.list_blobs(prefix=OUTPUT_PREFIX):
    blob.delete()

  assert len(list(bucket.list_blobs(prefix=OUTPUT_PREFIX))) == 0

