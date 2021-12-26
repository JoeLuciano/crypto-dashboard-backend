from blockboard.openseatools import OpenseaTools

wallet_address = '0x2e96bf59b58ed7dc0fab4af637d643727dd87e54'
openseaTools = OpenseaTools(wallet_address)


def test_get_all_erc721_tokens():
    erc721_tokens = openseaTools.get_all_erc721_tokens()
    assert erc721_tokens['assets'][0]['name'] == '#4864'
