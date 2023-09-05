import requests
import urllib3
import time
import logging

# HEADERS = {
#     "Accept":"*/*",
#     "Accept-Encoding":"gzip, deflate, br",
#     "Accept-Language":"en-US,en;q=0.9",
#     "Referer":"https://www.alsuper.com/",
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62"
# }

logging.basicConfig(level=logging.INFO)

HEADERS ={
    'Accept':'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en,es-ES;q=0.9,es;q=0.8',
'Connection': 'keep-alive',
'Host': 'api2.alsuper.com',
'Origin':'https://alsuper.com',
'Referer': 'https://alsuper.com/',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
'sec-ch-ua-platform': "Windows"
}

class Alsuflation(object):
    def __init__(
        self,
        limit=15,
        store_id=1000
    ):
        self.base_url = 'https://api2.alsuper.com/'
        self.store_id = store_id
        self.params = {
                        'page':1,'limit':limit,'keyword':'','department':'','category':'',
                        'subcategory':'','brand':'','promotion':'','min_price':'','max_price':'',
                        'order_price':'','order_name':'','characteristics':'','orden':'undefined','ecommerce':'true'
                       }

        self._build_session()



    def _build_session(self):
        self._session = requests.Session()


        retry = urllib3.Retry(
        total=10,
        connect=5,
        read=5,
        allowed_methods=frozenset(['GET', 'POST', 'PUT', 'DELETE']),
        status=5,
        backoff_factor=.5,
        other=10,
        status_forcelist=(429, 500, 501, 502, 503, 504)
        )

        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        self._session.mount('http://', adapter)
        self._session.mount('https://', adapter)

    def _process_url(self,endpoint=None, params=None):
            if params is None:
                par_str = ''
            else:
                par_str = '?'
                for k, v in params.items():
                    if k != 'page':
                        k = f"&{k}"
                    par_str += str(f"{k}={v}")

            return f"{self.base_url}{endpoint}/{par_str}"

    def _get(self, url):
        for _ in range(3):
            try:
                with self._session as s:
                    response = s.request("GET", url, headers=HEADERS)
                    response.raise_for_status()
                    result = response.json()
                    return result
            except urllib3.exceptions.ProtocolError:
                logging.warning("retrying urllib3.exceptions.ProtocolError")
                time.sleep(5)
            except urllib3.exceptions.IncompleteRead:
                logging.warning("retrying urllib3.exceptions.IncompleteRead")
                time.sleep(5)
            except requests.exceptions.ChunkedEncodingError:
                logging.warning("retrying requests.exceptions.ChunkedEncodingError")
                HEADERS['Referer'] = url
                time.sleep(5)
            except urllib3.exceptions.ResponseError:
                return ''

           

        
    
    def get_stores(self):
        url = self._process_url(endpoint="v1/stores")
        stores_data = self._get(url)['data']
        return stores_data
    

    
    def get_items(self, page=1):
        self.params["page"] = page
        url = self._process_url(endpoint=f"v1/ms-products/branch/{self.store_id}", params=self.params)
        return self._get(url)