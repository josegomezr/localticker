from base_ticker import BaseTicker
from statistics import mean
import math 

class AdListingTicker(BaseTicker):
  def __init__(self, dataset, BTC_TO_USD_RATE, min=0):
    super().__init__(dataset, BTC_TO_USD_RATE)
    self.min = min

  def get_sample(self, dataset, percentil):
    ads = list(filter(lambda x: x['min_amount'] > self.min, dataset))
    return dataset[0:percentil]

  def compute_rate(self, sample):
    prices = list(map(lambda x: x['temp_price'], sample))
    return round(mean(prices) / self.BTC_TO_USD_RATE, 2)

  def compute(self):
    self.prepared_dataset = self.prepare()

    buys = self.get_sample(self.prepared_dataset['bids'], 10)
    sells = self.get_sample(self.prepared_dataset['asks'], 10)

    buy_rate = self.compute_rate(buys)
    sell_rate = self.compute_rate(sells)

    return {
        'buy': buy_rate,
        'sell': sell_rate,
        'avg': round(mean([buy_rate, sell_rate]), 2)
    }

  def _prepare_listings(self, dataset):
    def inner(ad):
      ad = ad['data']
      if ad.get('max_amount'):
        ad['max_amount'] = float(ad['max_amount'])
      else:
        ad['max_amount'] = math.inf

      if not ad.get('min_amount'):
        ad['min_amount'] = 0

      ad['min_amount'] = float()
      ad['temp_price'] = float(ad['temp_price'])

      return ad
    
    dataset = map(inner, dataset['data']['ad_list'])
    return list(dataset)

  def prepare(self):
    return {
        'bids': self._prepare_listings(self.dataset['bids']),
        'asks': self._prepare_listings(self.dataset['asks']),
    }
