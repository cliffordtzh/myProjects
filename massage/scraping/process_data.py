from functions.parser import *

import pandas as pd
import json
import os
import io

from io import UnsupportedOperation

basic_info_path = "./scraping/round 3/processed data/basic info.csv"
opening_hours_path = "./scraping/round 3/processed data/opening hours.csv"
review_path = "./scraping/round 3/processed data/reviews"

basic_info = pd.DataFrame(columns = ["Name", "Address", "Rating", "Phone", "Website"])
opening_hours = pd.DataFrame(columns = ["Name", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

all_jsons = os.listdir("./scraping/round 3/raw_data")
for json_data in all_jsons:
    with open(f"./scraping/round 3/raw_data/{json_data}") as f:
        try:
            data = json.load(f)
            basic_info = parse_basic_info(basic_info, data)
            opening_hours = parse_opening_hours(opening_hours, data)
            parse_reviews(data, review_path)

        except io.UnsupportedOperation:
            pass

basic_info.to_csv(basic_info_path, index = False)
opening_hours.to_csv(opening_hours_path, index = False)
