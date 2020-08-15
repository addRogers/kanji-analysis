import requests
import pandas as pd
import argparse

wk_prefix = "https://api.wanikani.com/v2/"


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
        return r


# TODO: introduce mechanism to avoid exceeding request limits
def pull_data(session: requests.sessions, token: str, url: str):
    headers = {"Wanikani-Revision": "20170710"}
    first_page = session.get(url=url, headers=headers, auth=BearerAuth(token)).json()
    yield first_page['data']

    # cursor based pagination
    next_url = first_page['pages']['next_url']
    while next_url is not None:
        next_page = session.get(url=next_url, headers=headers, auth=BearerAuth(token)).json()
        yield next_page['data']


# TODO: test this
def process_review_statistics(session: requests.sessions, token: str) -> pd.DataFrame:
    url = wk_prefix + 'review_statistics'
    temp = []
    for page in pull_data(session, token=token, url=url):
        for item in page:
            data = item['data']
            data['data_updated_at'] = item['data_updated_at']
            temp.append(data)

    rev_stats_df = pd.DataFrame(temp)
    return rev_stats_df


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", "-t", help="provide API token")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    wk_token = args.token
    sess = requests.session()

    review_df = process_review_statistics(sess, wk_token)
