# Copyright (c) 2016, OASIS Open. All rights reserved.
# See LICENSE.txt for complete terms.


import json
from stixmarker import api


def main():
    file = open("campaign-marked.json")
    campaign = json.load(file)

    results = api.get_markings(campaign, ["title", "description"])

    print(results)

if __name__ == '__main__':
    main()
