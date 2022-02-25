# TEMPORARY FILE FOR TESTING
# Should write data to a local text file
# However, this rewrites all pre-existing data and replaces it with new data

import json


def store(lines):
    with open("data.txt", 'w') as f:
        for line in lines:
            f.write(json.dumps(line))
            f.write("\n")
