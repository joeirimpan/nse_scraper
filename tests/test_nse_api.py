# -*- coding: utf-8 -*-
from conftest import nse_vcr


@nse_vcr.use_cassette('tests/fixtures/nse_api.yml', record='once')
def test_nse_api(nse_api):
    gainers_data = nse_api.get_stocks_data('gainers')
    gainer = gainers_data[0]
    assert gainer['symbol'] == 'DRREDDY'
    assert gainer['openPrice'] == '1,925.05'
    losers_data = nse_api.get_stocks_data('losers')
    loser = losers_data[0]
    assert loser['symbol'] == 'HINDALCO'
    assert loser['openPrice'] == '235.00'
