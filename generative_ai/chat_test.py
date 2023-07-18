# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHcontent WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import backoff
from google.api_core.exceptions import ResourceExhausted

import chat


_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
_LOCATION = "us-central1"


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_science_tutoring() -> None:
    assert (
        "There are eight planets in the solar system."
        == chat.science_tutoring(
            temperature=0, project_id=_PROJECT_ID, location=_LOCATION)
    )
