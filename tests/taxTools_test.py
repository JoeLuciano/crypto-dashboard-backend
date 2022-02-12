from blockboard.taxTools import TaxTools

api_key = 'VEQSPWESY5P3P9AZSUQ7J6C89HUZHZ5BM5'
wallet_address = '0x2e96bf59b58ed7dc0fab4af637d643727dd87e54'
taxTools = TaxTools(api_key, wallet_address)

def test_get_eth_spot_price():
    timestamp = 1628978844 # August 14th
    assert taxTools.get_eth_spot_price(timestamp) == 3271.8249124435442

def test_get_yearly_gas_costs_in_USD():
    year = 2021
    assert taxTools.get_yearly_gas_costs_in_USD(year) == 369.1386854093108