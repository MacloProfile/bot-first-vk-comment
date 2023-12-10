from vk_api import VkApi
from time import sleep
from random import choice
import config

def main():
    cfg = config.load()

    group_ids = cfg['group_ids']
    messages = cfg['messages']
    access_token = cfg['token']
    delay = cfg['delay']

    vk_session = VkApi(token=access_token)
    api = vk_session.get_api()

    row = {}

    for group_id in group_ids:
        group_id = -group_id if group_id > 0 else group_id
        wall = api.wall.get(owner_id=group_id, filter='all', extended=1, count=1)

        try:
            row.update({group_id: wall['items'][0]['id']})
        except IndexError:
            print('Error: Возможно в группе', group_id, 'нет постов')

    print('Бот ждёт постов...')

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


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
