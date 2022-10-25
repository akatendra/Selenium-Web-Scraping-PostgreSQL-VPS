import requests
import config_vps


def send_message(message):
    token = config_vps.TELEGRAM_TOKEN
    chat_id = config_vps.CHAT_ID
    url = 'https://api.telegram.org/bot'
    url += token
    url = url + '/sendMessage'
    response = requests.post(url, data={
        'chat_id': chat_id,
        'text': message
    })

    if response.status_code != 200:
        raise Exception("post_text error")


if __name__ == '__main__':
    send_message('Привет! Проверка связи')
