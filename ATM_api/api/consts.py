from decimal import Decimal

# region bills

BILL_200 = 'B200'
BILL_100 = 'B100'
BILL_50 = 'B50'
BILL_20 = 'B20'

VALID_BILLS = [BILL_200, BILL_100, BILL_50, BILL_20]

BILLS_VALUES = {
    BILL_200: 200,
    BILL_100: 100,
    BILL_50: 50,
    BILL_20: 20,
}

# endregion

# region coins

COIN_10 = 'C10'
COIN_5 = 'C5'
COIN_1 = 'C1'
COIN_01 = 'C0_1'
COIN_001 = 'C0_01'

VALID_COINS = [COIN_10, COIN_5, COIN_1, COIN_01, COIN_001]

COINS_VALUES = {
    COIN_10: Decimal('10.0'),
    COIN_5: Decimal('5.0'),
    COIN_1: Decimal('1.0'),
    COIN_01: Decimal('0.1'),
    COIN_001: Decimal('0.01'),
}

# endregion

# region responses

ERROR_AMOUNT_RES = {"result": {"error": "ATM does not have enough funds, please try to withdraw a different amount!"}}

# endregion

CURRENCY = 'currency'
AMOUNT = 'amount'

PK = 'pk'

VALID_CURRENCIES = ['ILS', 'USD']


