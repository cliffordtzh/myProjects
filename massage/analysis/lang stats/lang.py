from pprint import pprint
from functools import reduce
import numpy as np
import re
import os

import matplotlib.pyplot as plt


def get_parlour_review(name, review_path):
    # Each element in the return is a separate review.

    path = f"{review_path}\\{name}"
    with open(path, 'r') as f:
        data = f.readlines()

    rating_idx = [i for i in range(len(data)) if re.search("Rated", data[i])]
    range_idx = [y - x for x, y in zip(rating_idx, rating_idx[1:])]

    split_reviews = []
    for idx, r_idx in zip(rating_idx, range_idx):
        reviews = data[idx+1: idx + r_idx-2]
        cleaned = " ".join(clean_reviews(reviews)).lower()
        split_reviews.extend([cleaned])
        
    return [x for x in split_reviews if x != ""]


def clean_reviews(reviews):
    strip_newline = [x for x in map(lambda x: x.strip("\n"), reviews) if x != ""]
    leave_alphabets = ["".join(list(filter(lambda x: x.isalnum() or x == " ", y))) for y in strip_newline]
    remove_spaces = [x for x in list(map(lambda x: x.strip(" "), leave_alphabets)) if x != ""]
    
    return remove_spaces


def get_hist(reviews):
    word_count = {}
    for review in reviews:
        review_word_count = {}
        all_words = review.split(" ")
        review_len = len(all_words)
        for word in all_words:
            if word not in review_word_count:
                review_word_count[word] = 1
            else:
                review_word_count[word] += 1

        for k, v in review_word_count.items():
            prop = v/review_len
            if k not in word_count:
                word_count[k] = [prop]
            else:
                word_count[k].append(prop)

    return word_count


def pop_dist(review_path, exclude = None):
    names = os.listdir(review_path)
    pop_dist = {}
    if exclude:
        names = [name for name in names if name != exclude]

    all_word_counts = [get_hist(get_parlour_review(name, review_path)) for name in names]
    for word_count in all_word_counts:
        for k, v in word_count.items():
            if k not in pop_dist.keys():
                pop_dist[k] = v
            else:
                pop_dist[k].extend(v)
        
    return pop_dist


if __name__ == '__main__':
    review_path = "scraping\\round 3\\processed data\\reviews"
    names = os.listdir(review_path)
    name = names[7]
    pop_dist = pop_dist()
    parlour_dist = get_hist(get_parlour_review(name))
    word = "great"

    with open("output.txt", "w") as f:
        pprint(parlour_dist, f)

