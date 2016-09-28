# Copyright (c) 2016, OASIS Open. All rights reserved.
# See LICENSE.txt for complete terms.


import json
from stixmarker import api


def main():
    file = open("campaign-marked.json")
    campaign = json.load(file)

    to_clear = ["title", "created_by_ref", "description"]

    api.clear_markings(campaign, to_clear)

    print(json.dumps(campaign, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()
