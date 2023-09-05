from alsuflation import Alsuflation
import pandas as pd
from datetime import datetime
import os
from pathlib import Path

import argparse



def all_items(object_alsuflation):

    assert isinstance(object_alsuflation,Alsuflation)

    items_base = object_alsuflation.get_items()

    items_list = items_base["data"]["data"]
    items_total = items_base["data"]["total_items"]

    page = 2
    while len(items_list) < items_total:
        next_items = object_alsuflation.get_items(page=page)
        items_list.extend(next_items["data"]["data"])
        page += 1
    print(f"branch {object_alsuflation.store_id} items wrote {len(items_list)} vs items expected: {items_total}")

    return items_list



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--cron")
    args = parser.parse_args()

    if args.cron == 'hourly':
        stores = Alsuflation()
        stores_dict = stores.get_stores()
        stores_df = pd.DataFrame(stores_dict)

        date = datetime.now().strftime("%Y%m%d_%H")
        ssh_path = f"{os.getenv('HOME')}/programs/alsuflation/data/stores_hrl"
        ssh = Path(ssh_path)
        ssh.mkdir(parents=True, exist_ok=True)

        stores_df.to_csv(f'{ssh_path}/{date}_al_stores.csv', index=False)
        quit()


    data_base  = Alsuflation(limit=1000)
    stores = data_base.get_stores()


    al_stores = pd.DataFrame(stores)
    al_stores["orders"] = al_stores['orders'].astype('int')
    al_stores["branch_id"] = al_stores['branch_id'].astype('int')


    date = datetime.now().strftime("%Y%m%d%H")

    ssh_path = f"{os.getenv('HOME')}/programs/alsuflation/data/{date}"
    ssh = Path(ssh_path)
    ssh.mkdir(parents=True, exist_ok=True)

    al_stores.to_csv(f'{ssh_path}/al_stores.csv', index=False)
    all_items_in_store_base = all_items(data_base)

    items_df = pd.DataFrame(all_items_in_store_base)

    items_df.to_csv(f'{ssh_path}/base_al_items.csv', index=False)


    stores_id = al_stores[(al_stores['ecommerce']==True) & (al_stores['state'] == True)]['branch_id']

    for store_id in stores_id:
        data_c = Alsuflation(store_id=store_id, limit=1000)
        all_items_in_store = all_items(data_c)
        items_df = pd.DataFrame(all_items_in_store)

        items_df.to_csv(f'{ssh_path}/{store_id}_al_items.csv', index=False)