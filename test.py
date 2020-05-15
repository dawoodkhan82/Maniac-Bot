import requests
import datetime
import json
import sys

# API_ENDPOINT = 'https://maniac-dashboard.herokuapp.com/'
API_ENDPOINT = 'http://localhost:8000/'
REPO_NAME = 'Maniac-Bot-Test'


saved_flags = {
    "test_commit_right_url": {
    "file_path": "test/test_commit2.py",
    "is_stale": True,
    "is_missing": False,
    "time_behind": datetime.timedelta(days=1, hours=2, minutes=3),
    "last_doc_commit": "https://github.com/dawoodkhan82/Maniac-Bot-Test/commit/3cf6fb9e1c10f7dc2e00a3d484ac1bf1caee812f",
    "code_author": "dawoodkhan82"
    }
}

if __name__ == '__main__':

    if sys.argv[1] == 'setup':
        setup = json.dumps({"repo_name": REPO_NAME})
        r = requests.post(url=API_ENDPOINT + 'setup/',
                          data=setup)

        print(r.text)

    elif sys.argv[1] == 'commit':
        url = sys.argv[2]

        # TODO(aliabd): fix this
        data = json.dumps(saved_flags, indent=4, sort_keys=True, default=str)

        r = requests.post(url=API_ENDPOINT + url + '/commit/',
                          data=data)
        print(r)
        print(r.text)
    else:
        print("not a valid arg")