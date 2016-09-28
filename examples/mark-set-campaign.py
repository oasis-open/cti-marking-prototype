# Copyright (c) 2016, OASIS Open. All rights reserved.
# See LICENSE.txt for complete terms.


import json
from stixmarker import api


def main():
    file = open("campaign-marked.json")
    campaign = json.load(file)

    new_markings = ["marking-definition--3a3d3484-d67d-41b3-8e28-7ab3ddb16f3b",
                    "marking-definition--7e38ee56-abf2-47dd-9bab-28a3c598c84e"]

    api.set_markings(campaign, "created_by_ref", new_markings)

    print(json.dumps(campaign, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()
