#!/usr/bin/env python

import requests

response = requests.get("https://blok.ugent.be/data.json")
data = response.json()

for location in data:
    print(
        "\t".join(
            [
                str(location["geometry"]["coordinates"][1]),
                str(location["geometry"]["coordinates"][0]),
                str(location["properties"]["name"]),
                str(location["properties"]["address"]),
                str(location["properties"]["capacity"]),
                str(location["properties"]["period"]["start"]),
                str(location["properties"]["period"]["end"]),
                str(location["properties"]["hours"]["monday"]),
                str(location["properties"]["hours"]["tuesday"]),
                str(location["properties"]["hours"]["wednesday"]),
                str(location["properties"]["hours"]["thursday"]),
                str(location["properties"]["hours"]["friday"]),
                str(location["properties"]["hours"]["saturday"]),
                str(location["properties"]["hours"]["sunday"]),
                str(location["properties"]["extra"]),
                str(location["properties"]["type"]),
            ]
        )
    )
