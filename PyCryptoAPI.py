from requests import get, post
from json import loads
from web3 import Web3
import sqlalchemy as sql

class DataAPI:
    def __init__(self) -> None:
        self.engine = sql.create_engine('sqlite:///config.db')
        self.CovalentApikey = self.engine.execute('SELECT apikey_covalent FROM config WHERE type="prod"').fetchone()[0]
        self.GraphqlApikey = self.engine.execute('SELECT apikey_graphql FROM config WHERE type="prod"').fetchone()[0]

        self.base = 'https://api.covalenthq.com/v1/'
        self.bsc = "https://bsc-dataseed.binance.org/"
        self.engine = Web3(Web3.HTTPProvider(self.bsc))

        print('\t\t\t CryptoAPI v2.1 initialized. Ready to serve!')

    def get_sender_address(self):
        data = self.engine.execute('SELECT sender_address FROM config WHERE type="prod"').fetchone()[0]

        return data
    
    def get_private_key(self):
        data = self.engine.execute('SELECT private_key FROM config WHERE type="prod"').fetchone()[0]

        return data
    
    def get_sender_address(self):
        data = self.engine.execute('SELECT sender_address FROM config WHERE type="prod"').fetchone()

        return data
        
    
    def humanizeWei(self, value):
        return self.engine.fromWei(value, 'ether')
    
    def get_address_balance(self, chainID, address, token):
        query = f'{chainID}/address/{address}/balances_v2/?&key={self.CovalentApikey}'
        
        data = get(self.base + query)
        portfolio = loads(data.content)['data']['items']
        for record in portfolio:
            if record['contract_ticker_symbol'] == token:
                result = round(float(record['balance']), 2)
                return float(self.humanizeWei(result))
        
        print(portfolio)
        return None

    def get_price_hard(self, symbol='STEMX'):
        if symbol == 'STEMX':
            busd_balance = None
            token_balance = None
            while busd_balance  == None or token_balance == None:
                busd_balance = self.get_address_balance(56, '0x55469453E760ba6eE3D8275E1c20Ec8fEE01E8ff', 'BUSD')
                token_balance = self.get_address_balance(56, '0x55469453E760ba6eE3D8275E1c20Ec8fEE01E8ff', 'STEMX')

            return float(busd_balance / token_balance)