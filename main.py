from alsuflation import Alsuflation
import pandas as pd
from datetime import datetime
import os




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
    # data  = Alsuflation(store_id=1000)
    # print(data.get_items())


    data_base  = Alsuflation(limit=1000)
    stores = data_base.get_stores()

   

    
    # print(stores)

    al_stores = pd.DataFrame(stores)
    al_stores["orders"] = al_stores['orders'].astype('int')
    al_stores["branch_id"] = al_stores['branch_id'].astype('int')


    date = datetime.now().strftime("%Y%m%d%H")
    os.mkdir(f"data/{date}/")
    al_stores.to_csv(f'data/{date}/al_stores.csv', index=False)
    all_items_in_store_base = all_items(data_base)

    items_df = pd.DataFrame(all_items_in_store_base)

    items_df.to_csv(f'data/{date}/base_al_items.csv', index=False)

    # print(al_stores)

    stores_id = al_stores[(al_stores['ecommerce']==True) & (al_stores['state'] == True)]['branch_id']
    # print(stores_id)
    # quit()

    for store_id in stores_id:
        data_c = Alsuflation(store_id=store_id, limit=500)
        all_items_in_store = all_items(data_c)
        items_df = pd.DataFrame(all_items_in_store)

        items_df.to_csv(f'data/{date}/{store_id}_al_items.csv', index=False)


    # al_items = pd.DataFrame(all_items(data))

    
    


    # items_base = data.get_items()
    # while len(items_base) < 

    # print(items_base)

 

    # print(items_base[0].keys())
   

