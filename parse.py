import requests
import time
import datetime
from database import create_connection
import os


def execute_sql_query(select_db, todo, params, insert_db):
    conn = create_connection(os.getenv("name"), os.getenv("user"), os.getenv("password"),"database")
    value = str(params).replace("[", '(').replace("]", ')')
    if todo == "insert":
        insert_query = (
            f"INSERT INTO {insert_db} VALUES {value}"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(insert_query, select_db)
        conn.close()
        cursor.close()
    if todo == "select":
        select_query = select_db
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(select_query)
        return cursor.fetchall()
    if todo == "update":
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(select_db)


def add_to_db(address_from, address_to, value, hashes, asset, block, key):
    dt_now = str(datetime.datetime.now())
    execute_sql_query("SELECT * FROM users", "insert",
                      [address_from, address_to, value, hashes, asset, block, dt_now, "False", key], "transactions")


def take_from_db():
    print()
    a = str(execute_sql_query(f"SELECT address FROM public.maintable", "select", "", ""))
    a = a.replace('[', "").replace(',', "").replace(',)', "").replace('(', "") \
        .replace(']', "").replace(')', "").replace("'", '')
    b = a.split()
    print(b)
    return b


def watch_data(method, params, url):
    headers = {
        "Content-Type": "application/json",
        "api_key": 'a9adc54c-871d-4388-a19f-fbe10d048896'
    }
    body1 = {"jsonrpc": "2.0", "method": method, "id": 1, "params": params}
    resp = requests.post(url, headers=headers, json=body1)
    b = resp.json()
    return b


def get_last_block_number():
    url = "https://goerli.api.watchdata.io/node/jsonrpc"
    b = watch_data("eth_blockNumber", [], url)
    block = int(b['result'], 16)
    return block - 4  # из- за этого парс ломается


def sync_transfers(from_block):
    to_block = get_last_block_number()
    while True:
        q = take_from_db()
        blockchains = {'goerli': "https://goerli.api.watchdata.io/node/jsonrpc"}
        for key in blockchains:
            a = watch_data("watch_getTransfersByAddress",
                           [{"addresses": q, "fromBlock": from_block, "toBlock": to_block, }], blockchains.get(key))
            print(a, from_block, to_block)
            for trx in a.get('result', []):
                add_to_db(trx['from'], trx['to'],
                          trx['value'], trx['transactionHash'],
                          # trx['asset'],
                          "ETH", trx['blockNumber'], key)
                from_block = trx['blockNumber'] + 1
            time.sleep(1)
        time.sleep(30)  # Delay for 1 minute (10 seconds)
        to_block = get_last_block_number()


def main():
    a = execute_sql_query(f"SELECT block_number FROM public.transactions order by (block_number);", "select", "", "")
    print(a)
    if not a:
        sync_transfers(get_last_block_number())
    block = str(a[len(a) - 1]).replace("(Decimal('", '').replace("'),)", "")
    print(block)
    sync_transfers(int(block) + 1)


if __name__ == "__main__":
    main()
