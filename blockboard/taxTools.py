from etherscanTools import EtherscanTools
from pycoingecko import CoinGeckoAPI


class TaxTools:
    def __init__(self, api_key, wallet_address):
        self.etherscanTools = EtherscanTools(api_key, wallet_address)
        self.cg = CoinGeckoAPI()

    def get_eth_spot_price(self, timestamp):
        start_timestamp = round(int(timestamp), -4)
        end_timestamp = start_timestamp + 10**4
        market_data = self.cg.get_coin_market_chart_range_by_id(
            id='ethereum', vs_currency='usd', from_timestamp=start_timestamp, to_timestamp=end_timestamp)
        spot_prices = [time_price_pair[1] for time_price_pair in market_data['prices']]
        return max(spot_prices)

    def get_yearly_gas_costs_in_USD(self, year):
        gwei_in_one_eth = 10**9
        total_gas_costs = 0
        yearlyTxns = self.etherscanTools.get_normal_txns_for_year(year)
        for txn in yearlyTxns:
            gas_units_used = int(txn['gasUsed'])
            gas_price_in_eth = int(txn['gasPrice']) / gwei_in_one_eth / gwei_in_one_eth
            eth_price_at_time_of_txn = self.get_eth_spot_price(txn['timeStamp'])
            txn_gas_cost = gas_units_used * gas_price_in_eth * eth_price_at_time_of_txn
            total_gas_costs += txn_gas_cost
        return total_gas_costs
