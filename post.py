from time import sleep
from random import choice


def wait_for_posts(api, row, messages, delay, mode):
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
                if mode == 1:
                    random_message(messages, api, group_id, post)
                elif mode == 2:
                    several_messages(messages, api, group_id, post)
        sleep(delay)


def random_message(messages, api, group_id, post):
    message = choice(messages)
    api.wall.createComment(owner_id=group_id, post_id=post['id'], message=message)
    print(f"Оставил коммент под постом https://vk.com/feed?w=wall{group_id}_{post['id']} с текстом: {message}")


def several_messages(messages, api, group_id, post):
    count = 1
    for message in messages:
        api.wall.createComment(owner_id=group_id, post_id=post['id'], message=message)
        print(f"Оставил " + str(count) +
              f" коммент под постом https://vk.com/feed?w=wall{group_id}_{post['id']} с текстом: {message}")
        count += 1