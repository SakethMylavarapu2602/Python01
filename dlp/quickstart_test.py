# Copyright 2017 Google Inc.
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

import os

import google.cloud.dlp
import mock

import quickstart


GCLOUD_PROJECT = os.getenv('GCLOUD_PROJECT')


def test_quickstart(capsys):
    # Mock out project_path to use the test runner's project ID.
    with mock.patch.object(
            google.cloud.dlp.DlpServiceClient,
            'project_path',
            return_value='projects/{}'.format(GCLOUD_PROJECT)):
        quickstart.quickstart()

    out, _ = capsys.readouterr()
    assert 'FIRST_NAME' in out
    assert 'LAST_NAME' in out
