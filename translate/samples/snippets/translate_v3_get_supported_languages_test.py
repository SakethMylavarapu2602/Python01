# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import pytest

import translate_v3_get_supported_languages


PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]


def test_list_languages(capsys: pytest.LogCaptureFixture) -> None:
    response = translate_v3_get_supported_languages.get_supported_languages(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert "zh" in response.languages
