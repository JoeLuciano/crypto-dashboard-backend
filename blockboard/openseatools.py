from opensea import OpenseaAPI


class OpenseaTools:
    def __init__(self, wallet_address):
        self.api = OpenseaAPI()
        self.address = wallet_address

    def get_all_erc721_tokens(self, wallet_address=None):
        if wallet_address is None:
            wallet_address = self.address
        return self.api.assets(owner=wallet_address)
    # How to test?

    def get_erc721_floor_prices(self, wallet_address=None):
        if wallet_address is None:
            wallet_address = self.address
        owned_tokens = self.opensea.assets(owner=wallet_address)
        floor_prices = []
        for token in owned_tokens['assets']:
            slug = token['collection']['slug']
            stats = self.opensea.collection_stats(
                collection_slug=slug)['stats']
            floor_prices.append(stats['floor_price'])
        return floor_prices
