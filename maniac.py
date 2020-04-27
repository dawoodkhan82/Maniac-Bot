from datetime import datetime
import ast
import urllib.request


FLAGS_TEXT_PATH = 'flags.txt'
TEST_FILE_PATH = 'test_file.py'

NODE_TYPES = {
    ast.ClassDef: 'Class',
    ast.FunctionDef: 'Function/Method',
    ast.AsyncFunctionDef: 'AsyncFunction/Method',
}

# blame_output = [{
#     'line': blame_ranges['startingLine'],
#     'commit': blame_ranges['commit']['oid'],
#     'date': blame_ranges['commit']['authoredDate'],
#     'author': blame_ranges['commit']['name']
# },]


def download_file(url):
    filename, _ = urllib.request.urlretrieve(url)
    return filename


def get_line_numbers(source):
    tree = ast.parse(source)
    line_numbers = {}

    for node in ast.walk(tree):
        if isinstance(node, tuple(NODE_TYPES)):
            name = getattr(node, 'name', None)
            function_lineno = getattr(node, 'lineno', None)
            doc_lineno_start, doc_lineno_end = None, None
            code_lines = [body.lineno for body in node.body
                          if not isinstance(body, ast.Expr)]
            code_lineno_start, code_lineno_end = min(code_lines) - 1, \
                                                 max(code_lines) - 1

            if (node.body and isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Str)):
                doc_lineno_end = node.body[0].lineno - 1
                doc_lineno_start = doc_lineno_end - len(node.body[
                                                0].value.s.splitlines())
            line_numbers[name] = {
                "type": NODE_TYPES[(type(node))],
                "function_lineno": function_lineno,
                "doc_lineno_start": doc_lineno_start,
                "doc_lineno_end": doc_lineno_end,
                "code_lineno_start": code_lineno_start,
                "code_lineno_end": code_lineno_end
            }
    return line_numbers


def convert_to_datetime(string):
    datetime_object = datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ')
    return datetime_object


def get_dates(blame_output, lines, name):
    if lines[name]["doc_lineno_start"]:
        if lines[name]["doc_lineno_start"] == \
                lines[name]["doc_lineno_end"]:
            doc_lines = blame_output[lines[name]["doc_lineno_start"]]
            doc_dates = doc_lines['date']
            latest_doc_date = convert_to_datetime(doc_dates)
            doc_index = None
        else:
            doc_lines = blame_output[lines[name]["doc_lineno_start"]:lines[
                name]["doc_lineno_end"]]
            doc_dates = [doc_line['date'] for doc_line in doc_lines]
            doc_dates = [convert_to_datetime(t) for t in doc_dates]
            latest_doc_date = max(doc_dates)
            doc_index = doc_dates.index(latest_doc_date)
    else:
        latest_doc_date = None
        doc_index = None

    if lines[name]["code_lineno_start"] == lines[name]["code_lineno_end"]:
        code_lines = blame_output[lines[name]["code_lineno_start"]]
        code_dates = code_lines['date']
        latest_code_date = convert_to_datetime(code_dates)
        code_index = None
    else:
        code_lines = blame_output[lines[name]["code_lineno_start"]:lines[name][
            "code_lineno_end"]]
        code_dates = [code_line['date'] for code_line in code_lines]
        code_output_dates = [convert_to_datetime(item) for item in
                             code_dates]
        latest_code_date = max(code_output_dates)
        code_index = code_dates.index(latest_code_date)

    return latest_doc_date, latest_code_date, doc_index, code_index


def get_author(blame_output, lines, name, code_index):
    if lines[name]["code_lineno_start"] == \
            lines[name]["code_lineno_end"]:
        author = blame_output[lines[name]["code_lineno_start"]]['author']
    else:
        author = blame_output[lines[name]["code_lineno_start"]:lines[name][
                "code_lineno_end"]][code_index]['author']
    return author


def get_last_doc_commit(blame_output, lines, name, doc_index):
    if lines[name]["doc_lineno_start"] == \
            lines[name]["doc_lineno_end"]:
        last_doc_commit = blame_output[lines[name]["doc_lineno_start"]][
            'commit']
    else:
        last_doc_commit = blame_output[lines[name]["doc_lineno_start"]:lines[
            name][
                "doc_lineno_end"]][doc_index]['commit']
    return last_doc_commit


def run_flags(url, blame_output):

    filename = download_file(url)
    with open(filename) as file:
        source = file.read()

    lines = get_line_numbers(source)

    flags = {}

    for name in lines.keys():
        latest_doc_date, latest_code_date, doc_index, code_index = \
            get_dates(blame_output, lines, name)

        if not latest_doc_date:
            missing = True
            stale = True
            time_behind = None
            last_doc_commit = None
            author = get_author(blame_output, lines, name, code_index)

        elif latest_code_date > latest_doc_date:
            stale = True
            missing = False
            time_behind = latest_code_date - latest_doc_date
            last_doc_commit = get_last_doc_commit(blame_output, lines, name,
                                                  doc_index)
            author = get_author(blame_output, lines, name, code_index)

        else:
            stale = False
            missing = False
            time_behind = None
            last_doc_commit = None
            author = None

        if stale:
            if missing:
                comment = f"WARNING @{author}: {name} is missing a " \
                          f"docstring! " \

            else:
                comment = f"WARNING @{author}: {name}'s docstring is stale! " \
                          f"It was last updated in {last_doc_commit}. " \
                          f"Time behind: {time_behind}"

            flags[lines[name]["function_lineno"]] = comment

    return flags
