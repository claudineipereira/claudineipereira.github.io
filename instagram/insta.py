#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
import json
import os
import requests
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)

posts_json = os.path.join(basedir, 'posts.json')

user_id = os.environ.get('user_id')
token = os.environ.get('token')


def get_posts():
    request = requests.get(f'https://graph.instagram.com/{user_id}/media?access_token={token}')
    data = json.loads(request.content)
    posts = data.get('data')

    media_id = []
    media_url = {'media': []}

    for item in posts:
        media_id.append(item['id'])
    
    print(media_id)

    for media in media_id:
        url = requests.get(f'https://graph.instagram.com/{media}?access_token={token}&fields=media_url')
        if 'dst-jpg' in url.text:
            media_url['media'].append({
                'id': media,
                'url': url.json()['media_url']
            })

    media = dict(itertools.islice(media_url.items(), 8))
    json_object = json.dumps(media)

    with open(posts_json, 'w') as f:
        f.write(json_object)

if __name__ == '__main__':
    get_posts()