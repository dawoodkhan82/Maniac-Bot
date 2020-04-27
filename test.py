import sys, json, maniac
from urllib.parse import urlparse


#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return lines[0], json.loads(lines[1])

def main():
    #get our data as an array from read_in()
    #file is download_url string for file contents
    #data is json object of git blame response:

    file_url_string, data = read_in()

    blame_ranges = data['repositoryOwner']['repository']['object'][
            'blame']['ranges']

    blame_output = []
    for blame_range in blame_ranges:
        if blame_range['startingLine'] == blame_range['endingLine']:
            blame_output.append({
                'line': blame_range['startingLine'],
                'commit': blame_range['commit']['oid'],
                'date': blame_range['commit']['authoredDate'],
                'author': blame_range['commit']['name']
            })
        else:
            for i in range(blame_range['endingLine'] - blame_range[\
                    'startingLine'] + 1):
                blame_output.append({
                    'line': blame_range['startingLine'] + i,
                    'commit': blame_range['commit']['oid'],
                    'date': blame_range['commit']['authoredDate'],
                    'author': blame_range['commit']['name']
                })

    parsedURL = urlparse(file_url_string)
    flags = maniac.run_flags(parsedURL.geturl(), blame_output)
    # print("flags: ", flags)

#start process
if __name__ == '__main__':
    main()

# {'repositoryOwner': {'repository': {'object': {'blame': {'ranges': [
#     {'startingLine': 1, 'endingLine': 1, 'age': 1,
#      'commit': {'oid': 'e040c58542952848e298611a67daded63b414680',
#                 'authoredDate': '2020-04-27T15:31:40Z',
#                 'author': {'name': 'dawoodkhan82'}}},
#     {'startingLine': 2, 'endingLine': 2, 'age': 1,
#      'commit': {'oid': '47042e9a5f05e7adb877afd37681c6ba72445f64',
#                 'authoredDate': '2020-04-27T15:33:00Z',
#                 'author': {'name': 'dawoodkhan82'}}},
#     {'startingLine': 3, 'endingLine': 24, 'age': 1,
#      'commit': {'oid': 'e040c58542952848e298611a67daded63b414680',
#                 'authoredDate': '2020-04-27T15:31:40Z',
#                 'author': {'name': 'dawoodkhan82'}}},
#     {'startingLine': 25, 'endingLine': 25, 'age': 1,
#      'commit': {'oid': 'a5aec8dc6dc3dae616661128045c0ab3147714fb',
#                 'authoredDate': '2020-04-27T15:34:54Z',
#                 'author': {'name': 'dawoodkhan82'}}}]}}}}}
