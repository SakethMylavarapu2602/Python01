#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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

"""Simple application that performs a query with BigQuery."""
# [START all]
# [START create_client]
from google.cloud import bigquery


def query_shakespeare():
    client = bigquery.Client()
    # [END create_client]
    # [START run_query]
    # See: https://cloud.google.com/bigquery/sql-reference/
    query_results = client.run_sync_query("""
        #standardSQL
        SELECT corpus AS title, COUNT(*) AS unique_words
        FROM `publicdata.samples.shakespeare`
        GROUP BY title
        ORDER BY unique_words DESC
        LIMIT 10""")

    query_results.run()
    # [END run_query]

    # [START print_results]
    rows = query_results.fetch_data()

    for row in rows:
        print(row)
    # [END print_results]


if __name__ == '__main__':
    query_shakespeare()
# [END all]
