import logging

from bs4 import BeautifulSoup
from lxml import etree

from dateutil.parser import parse
from flask import Flask, jsonify
from nltk import sent_tokenize
import requests


PLANET_PYTHON_FEED_URL = "http://planetpython.org/rss20.xml"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)


@app.route("/")
def main():
    with requests.Session() as session:
        session.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }

        response = session.get(PLANET_PYTHON_FEED_URL)
        data = response.content

        root = etree.fromstring(data)

        return jsonify([
            {
                "uid": topic.findtext("guid"),
                "updateDate": parse(topic.findtext("pubDate")).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),  # "2016-04-10T00:00:00.0Z"
                "titleText": topic.findtext("title"),
                "mainText": sent_tokenize(BeautifulSoup(topic.findtext("description"), "lxml").text)[0],
                "redirectionUrl": topic.findtext("link")
            }
            for topic in root.xpath("/rss/channel/item")
        ])


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
