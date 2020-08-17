import requests
import pandas as pd
import argparse
import time
import tqdm


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
        return r


def pull_data(session: requests.sessions, token: str, url: str):
    """
    Pulls data using the WaniKani RESTful API for an associated user and the collection/resource specified by the url.
    :param session: Requests session object, potential shared by different resources (see process_ functions).
    :param token: Authentication token associated with the user.
    :param url: URL suffix associated with the desired collection or resource (e.g. reviews table, kanji info, etc.)
    :return: Yields dictionary objects (parsed json) containing collection/resource data.
    """
    headers = {"Wanikani-Revision": "20170710"}  # May need to modify if api changes.
    first_page = session.get(url=url, headers=headers, auth=BearerAuth(token)).json()
    yield first_page['data']
    time.sleep(1)

    # cursor based pagination
    next_url = first_page['pages']['next_url']
    while next_url is not None:
        next_page = session.get(url=next_url, headers=headers, auth=BearerAuth(token)).json()
        yield next_page['data']
        next_url = next_page['pages']['next_url']
        time.sleep(1)


# TODO: fix for subject
def process_collection(session: requests.sessions, token: str, url: str) -> pd.DataFrame:
    """
    Processes collection
    :param session:
    :param token:
    :param url:
    :return:
    """
    temp = []
    for page in pull_data(session, token=token, url=url):
        for item in page:
            if 'subjects' not in url:
                data = item['data']
                data['data_updated_at'] = item['data_updated_at']
                temp.append(data)
            # else:
            #     if item['data']['object'] == 'radical':
            #         asi = item['data']['data']['amalgamation_subject_ids']
            #         aux = item['data']['data']['auxiliary_meanings']
            #     meanings = item['data']['data']['meanings']
            #     readings = item['data']['data']['readings']

    df = pd.DataFrame(temp)
    return df


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", "-t", help="user authentication token")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    wk_token = args.token
    wk_prefix = "https://api.wanikani.com/v2/"
    suffixes = ['review_statistics', 'assignments', 'level_progressions', 'reviews', 'subjects']
    sess = requests.session()

    for i in tqdm.tqdm(suffixes):
        collection_df = process_collection(sess, wk_token, wk_prefix + i)
        collection_df.to_csv(path_or_buf='data/{}.csv'.format(i), index=False)

    sess.close()
