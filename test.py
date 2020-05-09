import requests
import datetime
import json

API_ENDPOINT = 'https://still-cliffs-15715.herokuapp.com/maniac/'
REPO_NAME = 'Maniac-Bot-Test'


saved_flags = {
    "test_fn": {
    "file_path": "test/test.py",
    "is_stale": True,
    "is_missing": False,
    "time_behind": datetime.timedelta(days=1, hours=2, minutes=3),
    "last_doc_commit": "https://github.com/dawoodkhan82/Maniac-Bot-Test/commit/3cf6fb9e1c10f7dc2e00a3d484ac1bf1caee812f",
    "code_author": "dawoodkhan82"
    }
}

# TODO(aliabd): fix this
data = json.dumps(saved_flags, indent=4, sort_keys=True, default=str)

r = requests.post(url=API_ENDPOINT + REPO_NAME + '/commit/',
                  data=data)
print(r)
