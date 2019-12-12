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
fileName = 'data/storyViewers' + now + '.json'
f = open(fileName, "w")

## STORY ##
hasNextPage = True
endCursor = ''
countViewers = dict()
userViewers = dict()
storyInfoAux = dict()

try:
    while hasNextPage == True:
        # URL
        cookie = config.Cookie
        query_hash = '1ae3f0bfeb29b11f7e5e842f9e9e1c85'
        variables = '{"reel_ids":["'+config.UserId+'"],"tag_names":[],"location_ids":[],"highlight_reel_ids":[],"precomposed_overlay":false,"show_story_viewer_list":true,"story_viewer_fetch_count":50,"story_viewer_cursor":"'+endCursor+'","stories_video_dash_manifest":false}'
        rStoryInfo = requests.get('https://www.instagram.com/graphql/query/?query_hash='+query_hash+'&variables='+variables, headers={'Cookie':cookie})

        data = rStoryInfo.json().get('data').get('reels_media')[0]

        ## Si hay error:
        if rStoryInfo.json().get('errors'):
            raise Exception("Error de Instagram al obtener la info.")

        # DATOS DEL USUARIO ##
        username = data.get('owner').get('username')
        
        # STORIES
        i = 0
        for story in data.get('items'):
            i = i + 1
            userViewers.setdefault(i, {})
            storyInfoAux.setdefault(i, {})
            countViewers.update({i: story.get('edge_story_media_viewers').get('count')})

            edges = story.get('edge_story_media_viewers').get('edges')
            pageInfo = story.get('edge_story_media_viewers').get('page_info')

            storyInfoAux[i]['story_info'] = {}

            # Info (se obtiene una sola vez, al principio)
            storyInfoAux[i]['story_info']['taken_at_timestamp'] = story.get('taken_at_timestamp')
            storyInfoAux[i]['story_info']['expiring_at_timestamp'] = story.get('expiring_at_timestamp')
            storyInfoAux[i]['story_info']['src'] = story.get('video_resources')[0].get('src') if story.get('is_video') == True else story.get('display_url')

            if userViewers[i].get('story_info') == None:
                userViewers[i]['story_info'] = storyInfoAux[i]['story_info']

            for user in edges:
                userViewers[i][user.get('node').get('id')] = user.get('node').get('username')

            endCursor = pageInfo.get('end_cursor')
            if pageInfo.get('has_next_page') == False:
                hasNextPage = False

    json.dump(userViewers, f)
    f.close()
    print(countViewers)
except Exception as e:
    os.remove(fileName)
    print("Hubo un error al leer la info: " + str(e))