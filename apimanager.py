from concurrent.futures import ThreadPoolExecutor, as_completed
from config import AppConfig
from datetime import datetime
import db
import logger
import requests


class ApiManager:

    def __init__(self, base_url):
        self.base_url = base_url
        self.api_calls_count = 0

    def download_and_store_items(self, items):
        raise NotImplementedError


class MeliApiManager(ApiManager):

    def send_api_request(self, path, elem_id, attributes):
        self.api_calls_count += 1
        try:
            r = requests.get(
                "%s/%s/%s?attributes=%s" % (
                    self.base_url,
                    path,
                    elem_id,
                    ','.join(attributes)
                )
            )
            return r
        except requests.exceptions.ConnectionError:
            logger.file_logger.log("Connection error on path /%s/%s" % (path, elem_id))
            return None

    def get_item(self, item):
        item_id = item[0] + item[1]
        r = self.send_api_request('items', item_id, ['price', 'category_id', 'seller_id', 'currency_id', 'start_time'])
        if r is not None:
            if r.status_code == 404:
                logger.file_logger.log("Item not found: " + item_id)
                return None
            elif r.status_code == 200:
                details = self.get_item_details(
                    {
                        'category_id': r.json().get("category_id", None),
                        'seller_id': r.json().get("seller_id", None),
                        'currency_id': r.json().get("currency_id", None)
                    }
                )
                start_time = None
                if 'start_time' in r.json():
                    start_time = datetime.strptime(r.json()['start_time'], AppConfig.date_format)
                current_item = db.Item(
                    site=item[0],
                    item_id=item_id,
                    price=r.json().get('price', None),
                    name=details.get('name', None),
                    description=details.get('description', None),
                    nickname=details.get('nickname', None),
                    start_time=start_time
                )
                db.db_connection.store_record(current_item)
                return current_item
        else:
            return None

    def get_item_details(self, details_request):
        processes = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            if details_request['category_id']:
                processes.append(
                    executor.submit(self.send_api_request, 'categories', details_request['category_id'], ['name'])
                )
            if details_request['seller_id']:
                processes.append(
                    executor.submit(self.send_api_request, 'users', details_request['seller_id'], ['nickname'])
                )
            if details_request['currency_id']:
                processes.append(
                    executor.submit(self.send_api_request, 'currencies', details_request['currency_id'],
                                    ['description'])
                )
        responses = {}
        for task in as_completed(processes):
            result = task.result()
            if result:
                responses.update(result.json() if result.status_code == 200 else {})
        return responses

    def download_and_store_items(self, items):
        processes = []
        with ThreadPoolExecutor(max_workers=30) as executor:
            for item in items:
                if item[0] != "" and item[1] != "":
                    processes.append(executor.submit(self.get_item, item))
                else:
                    logger.file_logger.log("Bad element: %s,%s" % (item[0], item[1]))
        for task in as_completed(processes):
            current_item = task.result()
            if current_item:
                pass
                #db.db_connection.store_record(current_item)
