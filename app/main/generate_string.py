# -*- coding: utf-8 -*-

import random, string

def random_string():
    poolOfChars  = string.ascii_letters + string.digits
    random_codes = lambda x, y: ''.join([random.choice(x) for i in range(y)])
    return random_codes(poolOfChars, 20)