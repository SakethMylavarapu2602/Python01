# Copyright 2022 Google LLC
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
import re
import uuid

import pytest
from snippets.create_key import create_key
from snippets.create_service_account import create_service_account
from snippets.delete_service_account import delete_service_account


PROJECT_ID = os.environ["IAM_PROJECT_ID"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["IAM_CREDENTIALS"]


@pytest.fixture(scope="module")
def service_account() -> str:
    name = f"test-{uuid.uuid4().hex[:25]}"
    create_service_account(PROJECT_ID, name)
    account_id = f"{name}@{PROJECT_ID}.iam.gserviceaccount.com"
    yield account_id
    delete_service_account(PROJECT_ID, account_id)


def test_create_service_account_key(capsys: "pytest.CaptureFixture[str]", service_account: str) -> None:
    key_id = create_key(PROJECT_ID, service_account)
    out, _ = capsys.readouterr()
    assert re.search(f"Created a key: {key_id}", out)
