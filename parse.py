import json
import requests
import time
import psycopg2
from psycopg2 import OperationalError


def create_connection(db, user, user_password, db_host):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db,
            user=user,
            password=user_password,
            host=db_host,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def Answer(address_from, address_to, value, hash, asset, block):
    conn = create_connection('blockchainbot', 'blockchainbot', 'blockchainbot123', '185.137.234.101')
    select_db ="SELECT * FROM users"
    insert_query = (
        f"INSERT INTO secondtable VALUES {address_from,address_to,value,hash,asset,block}"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(insert_query, select_db)


def EthBlockNumber():
    headers = {
        "Content-Type": "application/json",
        "api_key": "a9adc54c-871d-4388-a19f-fbe10d048896"
    }

    body1 = {"jsonrpc": "2.0", "method": "eth_blockNumber", "id": 0, "params": []}
    resp = requests.post("https://ropsten.api.watchdata.io/node/jsonrpc", headers=headers, data=json.dumps(body1))
    b = json.loads(resp.content)
    return b['result']


def parse(q, a):
    headers = {
        "Content-Type": "application/json",
        "api_key": "a9adc54c-871d-4388-a19f-fbe10d048896"
    }

    body = {"jsonrpc": "2.0", "method": "watch_getTransfersByAddress", "id": 1,
            "params": [{"addresses": q,
                        "fromBlock": a,
                        }]}

    begin_block = int(EthBlockNumber(), 16)
    a = [0, 0, 0]
    while True:
        body['params'][0]['fromBlock'] = begin_block
        response = requests.post("https://ropsten.api.watchdata.io/node/jsonrpc", headers=headers,
                                 json=body)
        a = response.json()
        for i in range(len(a['result'])):
            new_block = a['result'][i]['blockNumber']
            if new_block >= begin_block:
                print(new_block, a['result'][i]['from'])
                Answer(a['result'][i]['from'], a['result'][i]['to'],
                       a['result'][i]['value'], a['result'][i]['transactionHash'],
                       a['result'][i]['asset'], a['result'][i]['blockNumber'])
        time.sleep(10)  # Delay for 1 minute (10 seconds)
        begin_block = int(EthBlockNumber(), 16)


def main():
    parse(['0x1507432C275811B588D5350d6A5770CA601AA7c3','0xa421B8b5A88041B13FE2546C894D25a53F548215'],EthBlockNumber())


if __name__ == "__main__":
    main()
