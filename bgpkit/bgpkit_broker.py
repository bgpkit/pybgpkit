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
    ts_start: str
    ts_end: str
    collector_id: str
    data_type: str
    url: str
    rough_size: int
    exact_size: int


class Broker:

    def __init__(self, api_url: str = "https://api.broker.bgpkit.com/v2", page_size: int = 100):
        self.base_url = api_url.strip()
        self.page_size = int(page_size)

    def query(self,
              ts_start: str = None,
              ts_end: str = None,
              collector_id: str = None,
              project: str = None,
              data_type: str = None,
              print_url: bool = False,
              ) -> [BrokerItem]:
        params = []
        if ts_start:
            params.append(f"ts_start={ts_start}")
        if ts_end:
            params.append(f"ts_end={ts_end}")
        if collector_id:
            check_type(collector_id, str)
            params.append(f"collector_id={collector_id}")
        if project:
            check_type(project, str)
            params.append(f"project={project}")
        if data_type:
            check_type(data_type, str)
            params.append(f"data_type={data_type}")
        params.append(f"page_size={self.page_size}")

        api_url = f"{self.base_url}/search?" + "&".join(params)
        page = 1

        data_items = []
        if print_url:
            print(api_url)
        res = requests.get(api_url).json()
        while res:
            if res["count"] > 0:
                data_items.extend([BrokerItem(**i) for i in res["data"]])

                if res["count"] < res["page_size"]:
                    break

                page += 1
                query_url = f"{api_url}&page={page}"
                if print_url:
                    print(query_url)
                res = requests.get(query_url).json()
            else:
                break

        return data_items
