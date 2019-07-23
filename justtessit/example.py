#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from justtessit.observations import checkList, checkStar

#example with 5 stars
example_file = "utils/list_of_stars.txt"

#lets check the list with checkList
results = checkList(example_file)

#and print our final results
print(results)

#We can also check a individual star with checkStar
result = checkStar('Glise581')

#and print the result
print(result)