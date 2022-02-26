from dataclasses import dataclass

import requests as requests


def check_type(value: any, ty: type) -> bool:
    try:
        ty(value)
        return True
    except ValueError:
        raise ValueError("invalid option input")


@dataclass
class BrokerItem:
    collector_id: str
    data_type: str
    timestamp: int
    url: str


class Broker:

    def __init__(self, api_url: str = "https://api.broker.bgpkit.com/v1", page_size: int = 100):
        self.base_url = api_url.strip()
        self.page_size = int(page_size)

    def query(self,
              start_ts: int = None,
              end_ts: int = None,
              collector: str = None,
              project: str = None,
              data_type: str = None,
              order: str = None,
              print_url: bool = False,
              ) -> [BrokerItem]:
        params = []
        if start_ts:
            check_type(start_ts, int)
            params.append(f"start_ts={start_ts}")
        if end_ts:
            check_type(end_ts, int)
            params.append(f"end_ts={end_ts}")
        if collector:
            check_type(collector, str)
            params.append(f"collector={collector}")
        if project:
            check_type(project, str)
            params.append(f"project={project}")
        if data_type:
            check_type(data_type, str)
            params.append(f"data_type={data_type}")
        if order:
            check_type(order, str)
            params.append(f"order={order}")
        params.append(f"page_size={self.page_size}")

        api_url = f"{self.base_url}/search?" + "&".join(params)
        page = 1

        data_items = []
        if print_url:
            print(api_url)
        res = requests.get(api_url).json()["data"]
        while res:
            if res["count"] > 0:
                data_items.extend([BrokerItem(**i) for i in res["items"]])

                if res["count"] < res["page_size"]:
                    break

                page += 1
                query_url = f"{api_url}&page={page}"
                if print_url:
                    print(query_url)
                res = requests.get(query_url).json()["data"]
            else:
                break

        return data_items
