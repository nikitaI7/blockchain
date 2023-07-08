from jinja2 import Environment, FileSystemLoader
import os
import requests
import time
from parse import execute_sql_query


def send_telegram(id, text: str):
    url = "https://api.telegram.org/bot"
    channel_id = id
    url += os.getenv("TELEGA_TOKEN")
    method = url + "/sendMessage"

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    tm = env.get_template('message')
    msg = tm.render(info=text)

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": msg})

    if r.status_code != 200:
        raise Exception("post_text error")
    else:
        update_db2 = f"UPDATE public.transactions SET is_sent = true WHERE from_address LIKE '{text[0]}' ESCAPE '#'" \
                     f" AND to_address LIKE '{text[1]}' ESCAPE '#'" \
                     f" AND block_number = {text[5]} "
        execute_sql_query(update_db2, "update", "", "")


def send_message_to_id(current_address, info, chain):
    db1 = execute_sql_query(f"SELECT * from maintable", "select", "", "")
    for i in range(len(db1)):
        if db1[i][1].casefold() == current_address.casefold():
            if db1[i][2] == chain:
                send_telegram(db1[i][0], info)


def send_info_and_id():
    db2 = execute_sql_query(f"SELECT * from transactions", "select", "", "")
    for i in range(len(db2)):
        if not db2[i][7]:
            send_message_to_id(db2[i][0], db2[i], db2[i][8])
            send_message_to_id(db2[i][1], db2[i], db2[i][8])


if __name__ == "__main__":
    send_info_and_id()
    while True:
        send_info_and_id()
        time.sleep(60)
