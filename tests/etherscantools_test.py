from blockboard.etherscanTools import EtherscanTools
import datetime as dt
import pytz

api_key = 'VEQSPWESY5P3P9AZSUQ7J6C89HUZHZ5BM5'
wallet_address = '0x2e96bf59b58ed7dc0fab4af637d643727dd87e54'
etherscanTools = EtherscanTools(api_key, wallet_address)


def test_get_eth_balance():
    eth_balance = etherscanTools.get_eth_balance(wallet_address)
    # will change after using this wallet
    assert eth_balance == 0.081734632852418899


def test_get_current_block():
    current_block = etherscanTools.get_current_block()
    assert isinstance(current_block, str)


def test_get_eastern_us_date_time():
    date_time = dt.datetime(
        year=2021,
        month=12,
        day=24,
        hour=10,
        minute=0,
        tzinfo=pytz.timezone('EST')
    )
    timestamp = date_time.timestamp()
    assert timestamp == 1640358000.0


def test_get_normal_txns_on_day():
    txn_day = dt.datetime(
        year=2021,
        month=10,
        day=4,
        tzinfo=pytz.timezone('EST')
    )
    txns = etherscanTools.get_normal_txns_on_day(txn_day)
    assert len(txns) == 1
    txn = txns[0]
    assert txn['from'] == '0x96245791fee4dc3c85045c5eed425c488bd02e67'
    assert txn['to'] == wallet_address
    assert txn['value'] == '30000000000000000'


def test_get_column_list():
    txn_day = dt.datetime(
        year=2021,
        month=10,
        day=4,
        tzinfo=pytz.timezone('EST')
    )
    txns = etherscanTools.get_normal_txns_on_day(txn_day)
    test = etherscanTools.get_column_list(txns)
    normal_txns_cols = ["blockNumber", "timeStamp", "hash", "nonce", "blockHash",
                        "transactionIndex", "from", "to", "value", "gas", "gasPrice",
                        "isError", "txreceipt_status", "input", "contractAddress",
                        "cumulativeGasUsed", "gasUsed", "confirmations"]
    assert normal_txns_cols == test


def test_get_all_erc20_contract_addresses():
    erc20_txns = etherscanTools.get_erc20_txn_history()
    assert int(erc20_txns[0]['blockNumber']) == 13025946
    erc20_df = etherscanTools.get_erc20_txn_history_dataframe()
    assert erc20_df['tokenSymbol'][0] == 'N1'
    erc20_addresses = etherscanTools.get_all_erc20_contract_addresses()
    assert erc20_addresses[0] == '0xacbd826394189cf2623c6df98a18b41fc8ffc16d'


def test_get_all_erc20_token_symbols():
    erc20_tokens = etherscanTools.get_all_erc20_token_symbols()
    assert erc20_tokens[0] == 'N1'


def test_get_erc20_token_balance():
    font_contract_address = '0x4c25bdf026ea05f32713f00f73ca55857fbf6342'
    erc20_token_balance = etherscanTools.get_erc20_token_balance(
        font_contract_address)
    assert erc20_token_balance == 47.780271931955994


def test_get_all_erc721_contract_addresses():
    erc721_txns = etherscanTools.get_erc721_txn_history()
    assert int(erc721_txns[0]['blockNumber']) == 13032058
    erc721_df = etherscanTools.get_erc721_txn_history_dataframe()
    assert erc721_df['tokenSymbol'][0] == 'DEAD'
    erc721_addresses = etherscanTools.get_all_erc721_contract_addresses()
    assert erc721_addresses[0] == '0x6fc355d4e0ee44b292e50878f49798ff755a5bbc'

    # def test_convert_days_ago_to_block_number()
