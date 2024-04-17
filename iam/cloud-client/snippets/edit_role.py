#!/usr/bin/env python

# Copyright 2024 Google Inc. All Rights Reserved.
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

# [START iam_edit_role]
from google.cloud.iam_admin_v1 import (
    IAMClient,
    Role,
)
from google.api_core.exceptions import NotFound

from get_role import get_role


def edit_role(role: Role) -> Role:
    client = IAMClient()
    request = {
        "name": role.name,
        "role": role,
    }
    try:
        role = client.update_role(request)
        print(f"Edited role: {role.name}: {role}")
        return role
    except NotFound:
        print(f"Role [{role.name}] not found, take some actions")
# [END iam_edit_role]


if __name__ == "__main__":
    import os

    PROJECT_ID = os.environ["IAM_PROJECT_ID"]
    role_id = "custom1_python_duplicate5"
    role = get_role(PROJECT_ID, role_id + "sadf")

    role.title = "Update_python_title2"
    upd_role = edit_role(role)
