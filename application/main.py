from traders import randy_random, trader, cassandra_classic
import api_controller
import json


if __name__ == '__main__':
    #randy_random.run_randy()
    #cassandra_classic.run_cassandra()
    trader.value_of_stock('AAPL')
