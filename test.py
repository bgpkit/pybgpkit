import bgpkit
parser = bgpkit.Parser(url="https://spaces.bgpkit.org/parser/update-example",
                       filters={"peer_ips": "185.1.8.65, 2001:7f8:73:0:3:fa4:0:1"},
                       cache_dir="cache"
                       )
elems = parser.parse_all()
assert len(elems) == 4227
import json
print(json.dumps(elems[0], indent=4))
