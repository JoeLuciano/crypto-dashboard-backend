from etherscan import Etherscan
import datetime as dt
import pandas as pd
import pytz


class EtherscanTools:
    def __init__(self, api_key, wallet_address):
        self.api = Etherscan(api_key)
        self.address = wallet_address
        try:
            self.erc20_txn_history = self.get_erc20_txn_history()
            self.erc20_txn_history_df = self.get_erc20_txn_history_dataframe()
        except:
            self.erc20_txn_history = None
            self.erc20_txn_history_df = None
        try:
            self.erc721_txn_history = self.get_erc721_txn_history()
            self.erc721_txn_history_df = self.get_erc721_txn_history_dataframe()
        except:
            self.erc721_txn_history = None
            self.erc721_txn_history_df = None

    def get_eth_balance(self, wallet_address=None):
        if wallet_address is None:
            wallet_address = self.address
        wei_balance = self.api.get_eth_balance(wallet_address)
        eth_balance = int(wei_balance) / 1e18
        return eth_balance

    def get_current_block(self):
        current_time = round(dt.datetime.now().timestamp())
        current_block = self.api.get_block_number_by_timestamp(
            current_time, closest='before')
        return current_block

    def get_normal_txns_on_day(self, start_of_txn_day, wallet_address=None):
        end_of_txn_day = start_of_txn_day + dt.timedelta(days=1)

        start_block = self.get_block_number_by_datetime(start_of_txn_day)
        end_block = self.get_block_number_by_datetime(end_of_txn_day)

        if wallet_address is None:
            wallet_address = self.address
        normal_txns = self.api.get_normal_txs_by_address(
            address=wallet_address, startblock=start_block, endblock=end_block, sort='asc')
        return normal_txns

    def get_normal_txns_for_year(self, year, wallet_address=None):
        start_of_year = dt.datetime(
            year=year,
            month=1,
            day=1,
            tzinfo=pytz.timezone('EST')
        )
        end_of_year = start_of_year + dt.timedelta(days=365)

        start_block = self.get_block_number_by_datetime(start_of_year)
        end_block = self.get_block_number_by_datetime(end_of_year)

        if wallet_address is None:
            wallet_address = self.address
        normal_txns = self.api.get_normal_txs_by_address(
            address=wallet_address, startblock=start_block, endblock=end_block, sort='asc')
        return normal_txns

    @staticmethod
    def get_column_list(structure):
        return list(structure[0].keys())

    def get_block_number_by_datetime(self, date_time):
        timestamp = round(date_time.timestamp())
        return self.api.get_block_number_by_timestamp(timestamp, closest='before')

    def get_erc20_txn_history(self, wallet_address=None):
        if wallet_address is None:
            wallet_address = self.address
        txns = self.api.get_erc20_token_transfer_events_by_address(
            address=wallet_address, startblock=0, endblock=99999999, sort='asc')
        return txns

    def get_erc20_txn_history_dataframe(self, erc20_txns=None):
        if erc20_txns is None:
            erc20_txns = self.erc20_txn_history
        erc20_cols = self.get_column_list(erc20_txns)
        erc20_df = pd.DataFrame(erc20_txns, columns=erc20_cols)
        return erc20_df

    def get_all_erc20_contract_addresses(self, erc20_df=None):
        if erc20_df is None:
            erc20_df = self.erc20_txn_history_df
        contract_addresses = erc20_df['contractAddress'].drop_duplicates()
        return contract_addresses

    def get_all_erc20_token_symbols(self, erc20_df=None):
        if erc20_df is None:
            erc20_df = self.erc20_txn_history_df
        token_symbols = erc20_df['tokenSymbol'].drop_duplicates()
        return token_symbols

    def get_erc20_token_balance(self, contract_address, wallet_address=None):
        if wallet_address is None:
            wallet_address = self.address
        wei_balance = self.api.get_acc_balance_by_token_and_contract_address(
            contract_address, wallet_address)

        if len(wei_balance) > 17:  # AGIX seems to function differently...?
            ether_balance = int(wei_balance)/1e18
        else:
            ether_balance = int(wei_balance)/1e8
        return ether_balance

    def get_erc721_txn_history(self, wallet_address=None):
        if wallet_address is None:
            wallet_address = self.address
        txns = self.api.get_erc721_token_transfer_events_by_address(
            address=wallet_address, startblock=0, endblock=99999999, sort='asc')
        return txns

    def get_erc721_txn_history_dataframe(self, erc721_txns=None):
        if erc721_txns is None:
            erc721_txns = self.erc721_txn_history
        erc721_cols = self.get_column_list(erc721_txns)
        erc721_df = pd.DataFrame(erc721_txns, columns=erc721_cols)
        return erc721_df

    def get_all_erc721_contract_addresses(self, erc721_df=None):
        if erc721_df is None:
            erc721_df = self.erc721_txn_history_df
        contract_addresses = erc721_df['contractAddress'].drop_duplicates()
        print(contract_addresses)
        return contract_addresses

    # How to test?

    def convert_days_ago_to_block_number(self, number_of_days):
        current_time = dt.datetime.now()
        time_into_past = dt.timedelta(days=number_of_days)
        start_time = current_time - time_into_past
        start_timestamp = round(start_time.timestamp())

        block = self.api.get_block_number_by_timestamp(
            start_timestamp, closest='before')
        return block
