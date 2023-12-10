from vk_api import VkApi
from time import sleep
from random import choice
import config


def wait_for_posts(api, row, messages, delay):
    while True:
        for group_id, latest_post_id in row.items():
            wall = api.wall.get(owner_id=group_id, filter='all', extended=1, count=1)
            post = wall['items'][0] if wall['items'] else None

            try:
                post = wall['items'][0]
            except IndexError:
                group = wall['groups'][0]
                print('Группа', group['name'], '(vk.com/' + group['screen_name'] + ') ' +
                      'будет проигнорирована, т.к у нее больше нет постов.')

            if post and post['id'] > latest_post_id:
                row.update({group_id: post['id']})
                message = choice(messages)
                api.wall.createComment(owner_id=group_id, post_id=post['id'], message=message)
                print(f"Оставил коммент под постом https://vk.com/feed?w=wall{group_id}_{post['id']} с текстом: {message}")

        sleep(delay)
