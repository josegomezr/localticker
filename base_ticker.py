class BaseTicker:
  def __init__(self, dataset, BTC_TO_USD_RATE):
    self.dataset = dataset
    self.BTC_TO_USD_RATE = BTC_TO_USD_RATE

  def compute(self):
    raise NotImplementedError()

  def prepare(self, dataset):
    raise NotImplementedError()
