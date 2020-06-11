# Copyright 2015 Google Inc. All rights reserved.
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

# [START all]
from flask import Flask, escape, redirect, request
from google.cloud import ndb

try:
    from urllib import urlencode
except Exception:
    from urllib.parse import urlencode

app = Flask(__name__)
client = ndb.Client()


# [START greeting]
class Greeting(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]

# [START query]
    with client.context():
        @classmethod
        def query_book(cls, ancestor_key):
            return cls.query(ancestor=ancestor_key).order(-cls.date)

@app.route('/', methods=['GET'])
def display_guestbook():
    page = '<html><body>'

    guestbook_name = request.args.get('guestbook_name', '')
    with client.context():
        ancestor_key = ndb.Key("Book", guestbook_name or "*notitle*")
        greetings = Greeting.query_book(ancestor_key).fetch(20)
# [END query]

    greeting_blockquotes = []
    for greeting in greetings:
        greeting_blockquotes.append(
            '<blockquote>%s</blockquote>' % escape(greeting.content))

    body = """
        <html>
          <body>
            {blockquotes}
            <form action="/sign" method="post">
              <div>
                <textarea name="content" rows="3" cols="60">
                </textarea>
              </div>
              <div>
                <input type="submit" value="Sign Guestbook">
              </div>
            </form>
            <hr>
            <form>
              Guestbook name:
                <input value="{guestbook_name}" name="guestbook_name">
                <input type="submit" value="switch">
            </form>
          </body>
        </html >
    """

    page += body.format(
        blockquotes='\n'.join(greeting_blockquotes),
        guestbook_name = escape(guestbook_name)
    )

    return page


# [START submit]
@app.route('/sign', methods=['POST'])
def update_guestbook():
    # We set the parent key on each 'Greeting' to ensure each guestbook's
    # greetings are in the same entity group.
    with client.context():
        guestbook_name = request.args.get('guestbook_name', '')
        greeting = Greeting(
                parent=ndb.Key("Book",
                guestbook_name or "*notitle*"
            ),
            content = request.form.get('content', None)
        )
        greeting.put()
# [END submit]
    return redirect('/?' + urlencode(
        {'guestbook_name': request.form.get('guestbook_name', '')}))


if __name__ == '__main__':
    # This is used when running locally.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END all]
