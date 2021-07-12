import json
import csv
from typing import Dict, List, Union

def get_items_list(filename: str) -> List:
    """Loads items data from formatted csv files and returns
    the items list
    """
    
    primary_title_column = 0
    secondary_title_column = 1
    rarity_column = 2
    name_column = 3
    # stats are messy and aren't applicable, so not used
    # stats_column = 4
    description_column = 5

    primary_title = ''
    secondary_title = ''

    output = []

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        index = 1

        for row in reader:
            if row[primary_title_column] != '':
                primary_title = row[primary_title_column]
                secondary_title = ''
                continue

            if row[secondary_title_column] != '':
                secondary_title = row[secondary_title_column]
                continue
            
            item = {}
            # passed through titles, so here's data only
            # no EOF because reader iterates over not empty rows only
            if row[name_column] == '':
                # TODO: push error to log
                print(f'No name on line {index}, under {primary_title}{" - " + secondary_title if secondary_title != "" else ""}')
                continue

            if row[description_column] == '':
                # TODO: push error to log
                print(f'No description on line {index}, under {primary_title}{" - " + secondary_title if secondary_title != "" else ""}')
                continue

            item['primary_title'] = primary_title
            if secondary_title != '':
                item['secondary_title'] = secondary_title

            if row[rarity_column] != '':
                item['rarity'] = int(row[rarity_column])

            item['name'] = row[name_column]
            item['description'] = row[description_column]
            
            print(f'Got a {item["primary_title"]} item{"" if "secondary_title" not in item else " for " + item["secondary_title"]}: {item["name"]}. \"{item["description"]}\"')

            output.append(item)

            index += 1

        return output

def save_list_to_json(list: List, output_filename: str) -> None:
    with open(output_filename, 'a+') as output:
        json.dump(list, output)


if __name__ == '__main__':
    files = [
        ['generation-items/anno/csv/academy-items.csv', 'generation-items/anno/json/academy-items.json'],
        ['generation-items/anno/csv/ark-items.csv', 'generation-items/anno/json/ark-items.json'],
        ['generation-items/anno/csv/lab-items.csv', 'generation-items/anno/json/lab-items.json'],
        ['generation-items/anno/csv/vehicle-items.csv', 'generation-items/anno/json/vehicle-items.json'],
        ['generation-items/anno/csv/warehouse-items.csv', 'generation-items/anno/json/warehouse-items.json']
    ]

    for file_pair in files:
        save_list_to_json(
            get_items_list(file_pair[0]),
            file_pair[1]
        )

