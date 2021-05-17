from base_ticker import BaseTicker
from statistics import mean

class OrderBookTicker(BaseTicker):
  def get_sample(self, dataset, percentil):
    percentil_10th = int(len(dataset)*(percentil/100.0))
    return dataset[0:percentil_10th]

  def compute_rate(self, sample):
    prices = list(map(lambda x: x[0], sample))
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

  def _sort(self, dataset):
    dataset = map(lambda x: list(map(float, x)), dataset)
    result = sorted(dataset,
                    reverse=True, key=lambda x: x[1]
                    )
    return list(result)

  def prepare(self):
    return {
        'bids': self._sort(self.dataset['bids']),
        'asks': self._sort(self.dataset['asks']),
    }
