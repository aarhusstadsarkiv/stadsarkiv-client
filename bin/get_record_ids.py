#!/usr/bin/env python

# export CONFIG_DIR=example-config-aarhus

from stadsarkiv_client.core import api
from stadsarkiv_client.core.logging import get_log

# import sleep
from time import sleep
import json


log = get_log()


async def main():

    size = 10000

    # Example with a small search result
    # params_init = [
    #     ("view", "ids"),
    #     ("size", size),
    #     ("sort", "date_from"),
    #     ("direction", "asc"),
    #     ("content_types", 87),
    # ]
    # Full result:
    params_init = [
        ("view", "ids"),
        ("size", size),
        ("sort", "date_from"),
        ("direction", "asc"),
    ]

    done = False
    records_all = []

    while not done:

        res = await api.proxies_view_ids_from_list(params_init)
        records_all.extend(res["result"])

        if "next_cursor" not in res:
            done = True
        else:
            params_init = [params for params in params_init if params[0] != "cursor"]
            params_init.append(("cursor", res["next_cursor"]))

        log.info(f"Total records: {len(records_all)}")
        sleep(0.5)

    # save as ./data/all_records.json
    with open("./data/records_all.json", "w") as f:
        json.dump(records_all, f)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
