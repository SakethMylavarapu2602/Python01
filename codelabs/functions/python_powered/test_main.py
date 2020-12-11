# Copyright 2017 Google Inc. All Rights Reserved.
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

import unittest
import unittest.mock

import main


class TestHello(unittest.TestCase):
    @staticmethod
    def test_hello_world():
        req = unittest.mock.Mock()

        # Call tested function
        assert main.hello_world(req) == "Hello World!"

    @staticmethod
    def test_hello_name_no_name():
        req = unittest.mock.Mock(args={})

        # Call tested function
        assert main.hello_name(req) == "Hello World!"

    @staticmethod
    def test_hello_name_with_name():
        name = "test"
        req = unittest.mock.Mock(args={"name": name})

        # Call tested function
        assert main.hello_name(req) == "Hello {}!".format(name)
