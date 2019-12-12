# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from datetime import datetime, timedelta

import json

import requests
import re
import os
import config

# API Core
now = datetime.now().strftime('%d%m%Y%H%M')
fileName = 'data/followers' + now + '.json'
f = open(fileName, "w")

## STORY ##
hasNextPage = True
endCursor = ''
countFollowers = dict()
users = dict()

try:
    while hasNextPage == True:
        # URL
        cookie = config.Cookie
        query_hash = 'c76146de99bb02f6415203be841dd25a'
        variables = '{"id":"'+config.UserId+'","include_reel":true,"fetch_mutual":false,"first":24,"after":"'+endCursor+'"}'
        rFollowersInfo = requests.get('https://www.instagram.com/graphql/query/?query_hash='+query_hash+'&variables='+variables, headers={'Cookie':cookie})

        data = rFollowersInfo.json().get('data').get('user')

        ## Si hay error:
        if rFollowersInfo.json().get('errors'):
            raise Exception("Error de Instagram al obtener la info.")
        
        # FOLLOWERS
        countFollowers.update({0: data.get('edge_followed_by').get('count')})

        edges = data.get('edge_followed_by').get('edges')
        pageInfo = data.get('edge_followed_by').get('page_info')

        for user in edges:
            users[user.get('node').get('id')] = user.get('node').get('username')

        endCursor = pageInfo.get('end_cursor')
        if pageInfo.get('has_next_page') == False:
            hasNextPage = False

    json.dump(users, f)
    f.close()
    print(countFollowers)
except Exception as e:
    os.remove(fileName)
    print("Hubo un error al leer la info: " + str(e))