#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from justtessit.observations import checkList

#example with 5 stars
example_file = "utils/list_of_stars.txt"

#lets check the list
results = checkList(example_file)

#and print our final results
print(results)