import requests
import json

def get_json() -> None:
    """
    Fetches the list of stations from the Yandex Rasp API and saves the parsed result to a JSON file.
    """
    print('getting json...')
    url = "https://api.rasp.yandex.net/v3.0/stations_list/?"
    api_key = "b4711317-8f39-4259-9221-41c8a4250c77"
    # Make a GET request to the API to retrieve station data in JSON format
    response_json = requests.get(url=url, params={"apikey":api_key, "lang":"ru_RU", "format":"json"}).text

    # Parse the JSON and write the result to a file
    with open('bot/stations.json', 'w', encoding='utf-8') as file:
        json.dump(parse_json(response_json), file, ensure_ascii=False, indent=4)


def parse_json(file: str) -> dict[str, str]:
    """
    Parses the raw JSON string from the API and extracts a dictionary mapping station codes to station names.
    Only includes stations of certain types.
    """
    print('parsing json....')
    json_dict = json.loads(file)
    res: dict[str, str] = {}
    # Traverse the nested structure to extract station codes and titles
    for value in json_dict.values():
        for country in value:
            for region in country['regions']: 
                for settlement in region['settlements']: 
                    for station in settlement['stations']:
                        # Only include stations with codes and of specific types
                        if station['codes'] and station['station_type'] in ('station', 'platform', 'train_station'):
                            temp = {f"{station['codes']['yandex_code']}": f"{station['title']}"} 
                            res.update(temp)
    
    return res


if __name__ == "__main__":
    # If run as a script, fetch and parse the stations JSON
    get_json()


# Load the stations dictionary from the generated JSON file for use elsewhere in the project
stations: dict[str, str] = json.load(open('bot/stations.json', 'r', encoding='utf-8'))
