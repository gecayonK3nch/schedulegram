import requests
import json

def get_json() -> None:
    url = "https://api.rasp.yandex.net/v3.0/stations_list/?"
    api_key = "b4711317-8f39-4259-9221-41c8a4250c77"
    response_json = requests.get(url=url, params={"apikey":api_key, "lang":"ru_RU", "format":"json"}).text

    with open('stations.json', 'w', encoding='utf-8') as file:
        json.dump(parse_json(response_json), file, ensure_ascii=False, indent=4)


def parse_json(file: str) -> dict[str, str]:
    json_dict = json.loads(file)
    res: dict[str, str] = {}
    for value in json_dict.values():
        for country in value:
            for region in country['regions']: 
                for settlement in region['settlements']: 
                    if settlement['codes']:
                        temp = {f"{settlement['codes']['yandex_code']}": f"{settlement['title']}"}
                        res.update(temp)
                    for station in settlement['stations']:
                        if station['codes']:
                            temp = {f"{station['codes']['yandex_code']}": f"{station['title']}"} 
                            res.update(temp)
    
    return res


stations = json.load(open('bot/stations.json', 'r', encoding='utf-8'))

if __name__ == "__main__":
    get_json()
