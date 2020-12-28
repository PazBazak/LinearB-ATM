from rest_framework import viewsets
from .models import Bill, Coin
from .serializers import CoinSerializer, BillSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .consts import *
from rest_framework import status
from decimal import Decimal
from .atm_exceptions import TooMuchCoinsException

# region functions


def is_float(string):
    """
    Checking wether a string could be of type float
    :param string: string that might be converted to float
    :return:
    """
    is_float_ = False
    try:
        float(string)
        is_float_ = True
    except ValueError:
        pass

    return is_float_


def withdraw_from_atm(inventory: dict, amount: float) -> dict:
    """
    withdraw the amount from the inventory in the most optimal way!
    :param inventory: current ATM inventory
    :param amount: amount that user wishes to withdraw
    :return: most optimal way the ATM should withdraw that amount
    """
    returned_money = {}
    amount = Decimal(str(amount))

    # todo - clean code

    while amount >= Decimal("200.0"):
        if inventory[BILL_200] > 0:

            if BILL_200 not in returned_money:
                returned_money[BILL_200] = 0

            amount -= Decimal("200.0")
            inventory[BILL_200] -= 1
            returned_money[BILL_200] += 1

        else:
            break

    while amount >= Decimal("100.0"):
        if inventory[BILL_100] > 0:

            if BILL_100 not in returned_money:
                returned_money[BILL_100] = 0

            amount -= Decimal("100.0")
            inventory[BILL_100] -= 1
            returned_money[BILL_100] += 1

        else:
            break

    while amount >= Decimal("50.0"):
        if inventory[BILL_50] > 0:

            if BILL_50 not in returned_money:
                returned_money[BILL_50] = 0

            amount -= Decimal("50.0")
            inventory[BILL_50] -= 1
            returned_money[BILL_50] += 1

        else:
            break

    while amount >= Decimal("20.0"):
        if inventory[BILL_20] > 0:

            if BILL_20 not in returned_money:
                returned_money[BILL_20] = 0

            amount -= Decimal("20.0")
            inventory[BILL_20] -= 1
            returned_money[BILL_20] += 1

        else:
            break

    while amount >= Decimal("10.0"):
        if inventory[COIN_10] > 0:

            if COIN_10 not in returned_money:
                returned_money[COIN_10] = 0

            amount -= Decimal("10.0")
            inventory[COIN_10] -= 1
            returned_money[COIN_10] += 1

        else:
            break

    while amount >= Decimal("5.0"):
        if inventory[COIN_5] > 0:

            if COIN_5 not in returned_money:
                returned_money[COIN_5] = 0

            amount -= Decimal("5.0")
            inventory[COIN_5] -= 1
            returned_money[COIN_5] += 1

        else:
            break

    while amount >= Decimal("1.0"):
        if inventory[COIN_1] > 0:

            if COIN_1 not in returned_money:
                returned_money[COIN_1] = 0

            amount -= Decimal("1.0")
            inventory[COIN_1] -= 1
            returned_money[COIN_1] += 1

        else:
            break

    while amount >= Decimal("0.1"):
        if inventory[COIN_01] > 0:

            if COIN_01 not in returned_money:
                returned_money[COIN_01] = 0

            amount -= Decimal("0.1")
            inventory[COIN_01] -= 1
            returned_money[COIN_01] += 1

        else:
            break

    while amount >= Decimal("0.01"):
        if inventory[COIN_001] > 0:

            if COIN_001 not in returned_money:
                returned_money[COIN_001] = 0

            amount -= Decimal("0.01")
            inventory[COIN_001] -= 1
            returned_money[COIN_001] += 1

        else:
            break

    # counting the number of coins and bills
    coins = {money_type: count for money_type, count in returned_money.items() if money_type in VALID_COINS}
    bills = {money_type: count for money_type, count in returned_money.items() if money_type in VALID_BILLS}

    num_of_coins = sum(coins.values())

    if num_of_coins > 50:
        raise TooMuchCoinsException("There are too many coins requested! cannot perform this action!")

    # the ATM could not give the user all the money!
    if amount != 0:
        return ERROR_AMOUNT_RES

    return {"results": {
        "bills": bills,
        "coins": coins
    }}


def get_inventory(currency: str) -> dict:
    bills = Bill.objects.filter(currency__name=currency)
    coins = Coin.objects.filter(currency__name=currency)

    data = {
        BILL_200: 0,
        BILL_100: 0,
        BILL_50: 0,
        BILL_20: 0,

        COIN_10: 0,
        COIN_5: 0,
        COIN_1: 0,
        COIN_01: 0,
        COIN_001: 0,
    }

    for bill in bills:
        if bill.value == 200:
            data[BILL_200] += 1
        elif bill.value == 100:
            data[BILL_100] += 1
        elif bill.value == 50:
            data[BILL_50] += 1
        elif bill.value == 20:
            data[BILL_20] += 1

    for coin in coins:
        if coin.value == 10.0:
            data[COIN_10] += 1
        elif coin.value == 5.0:
            data[COIN_5] += 1
        elif coin.value == 1.0:
            data[COIN_1] += 1
        elif float(coin.value) == 0.1:
            data[COIN_01] += 1
        elif float(coin.value) == 0.01:
            data[COIN_001] += 1

    return data


# endregion


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


class CoinViewSet(viewsets.ModelViewSet):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer


@api_view(['GET'])
def show_inventory(request):
    # todo - make it show everything!
    data = get_inventory('ILS')
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def withdrawal(request):
    data = request.data

    # validation currency
    if CURRENCY not in data:
        return Response("Please include currency!", status=status.HTTP_400_BAD_REQUEST)
    else:
        if data[CURRENCY] not in VALID_CURRENCIES:
            return Response("Please include a valid currency!", status=status.HTTP_400_BAD_REQUEST)

    # validation amount
    if AMOUNT not in data:
        return Response("Please include the amount you wish to withdrawal!", status=status.HTTP_400_BAD_REQUEST)
    else:
        if not is_float(data[AMOUNT]):
            return Response("Please include a valid amount in decimal!", status=status.HTTP_400_BAD_REQUEST)
        else:
            if float(data[AMOUNT]) <= 0:
                return Response("Enter a valid amount that is higher than 0!", status=status.HTTP_400_BAD_REQUEST)

    inventory = get_inventory(data[CURRENCY])

    money = withdraw_from_atm(inventory, float(data[AMOUNT]))

    return Response(money)




