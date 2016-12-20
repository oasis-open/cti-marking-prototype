# Copyright (c) 2016, OASIS Open. All rights reserved.
# See LICENSE.txt for complete terms.

import json

from stixmarker import api


def main():
    file = open("campaign-marked.json")
    campaign = json.load(file)

    to_remove = api.get_markings(campaign, "title")

    api.remove_markings(campaign, "title", to_remove)

    print(json.dumps(campaign, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()
