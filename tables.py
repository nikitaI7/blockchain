a = '''CREATE TABLE IF NOT EXISTS transactions(
    from_address VARCHAR(42),
    to_address VARCHAR(42),
    value  DECIMAL,
    hash VARCHAR(66),
    asset_symbol VARCHAR ,
    block_number DECIMAL,
    created_date timestamp,
    is_sent boolean,
    blockchain VARCHAR(42),
    PRIMARY KEY(from_address,to_address,block_number));'''
b = '''CREATE TABLE IF NOT EXISTS maintable(
        Id SERIAL,
    address VARCHAR(42) NOT NULL,
    blockchain VARCHAR(42),
    PRIMARY KEY(Id,address,blockchain));'''