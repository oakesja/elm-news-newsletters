"""Hello Analytics Reporting API V4."""

import argparse

from apiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
import json
import datetime
from collections import OrderedDict


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
CLIENT_SECRETS_PATH = 'client_secrets.json'
VIEW_ID = '124487241'


def initialize_analyticsreporting():
    """Initializes the analyticsreporting service object.

    Returns:
      analytics an authorized analyticsreporting service object.
    """
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[tools.argparser])
    flags = parser.parse_args([])

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRETS_PATH, scope=SCOPES,
        message=tools.message_if_missing(CLIENT_SECRETS_PATH))

    # Prepare credentials, and authorize HTTP object with them.
    # If the credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to a file.
    storage = file.Storage('analyticsreporting.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=httplib2.Http())

    # Build the service object.
    analytics = build('analytics', 'v4', http=http,
                      discoveryServiceUrl=DISCOVERY_URI)

    return analytics


def get_report(analytics):
    # Use the Analytics Service Object to query the Analytics Reporting API V4.
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    "viewId": VIEW_ID,
                    "dateRanges": [
                        {
                            "startDate": "{:%Y-%m-%d}".format(last_monday()),
                            "endDate": "{:%Y-%m-%d}".format(last_sunday())
                        }
                    ],
                    "metrics": [
                        {
                            "expression": "ga:totalEvents"
                        }
                    ],
                    "pageSize": 10,
                    "dimensions": [
                        {
                            "name": "ga:eventLabel"
                        },
                        {
                            "name": "ga:dimension1"
                        },
                        # {
                        #     "name": "ga:dimension2"
                        # }
                    ],
                    "orderBys": [
                        {
                            "fieldName": "ga:totalEvents",
                            "sortOrder": "DESCENDING"
                        }
                    ]
                }]
        }
    ).execute()


def get_top_news(response):
    """Parses and prints the Analytics Reporting API V4 response"""
    report = response.get('reports', [])[0]
    rows = report.get('data', {}).get('rows', [])
    articles = []
    for row in rows:
        dimensions = row.get('dimensions', [])
        totalEvents = row.get('metrics', [])[0].get('values', [])[0]
        topNewsArticle = {
            "url": dimensions[0],
            "title": dimensions[1],
            "author": "",
            "tag": "",
            "hits": totalEvents
        }
        articles.append(topNewsArticle)
    return articles


def last_monday():
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7
    return today - datetime.timedelta(6 + idx)


def last_sunday():
    return last_monday() + datetime.timedelta(6)


def output_top_news(articles):
    news = OrderedDict([
        ("start_date", "{:%B %d}".format(last_monday())),
        ("end_date", "{:%B %d}".format(last_sunday())),
        ("year", str(datetime.date.today().year)),
        ("articles", articles)
    ])
    with open('test.json', 'w') as outfile:
        json.dump(news, outfile, indent=4, separators=(',', ': '))


def main():
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    news = get_top_news(response)
    output_top_news(news)

if __name__ == '__main__':
    main()
