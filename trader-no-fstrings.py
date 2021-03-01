import cbpro
import os
import logging
import time
import requests
import configparser
import sys

# ------------------------------------------------------------------
#   Logging Setup
# ------------------------------------------------------------------

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(message)s')

file_handler = logging.FileHandler("settings\\logs.log", encoding='utf8')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# ------------------------------------------------------------------

config = configparser.RawConfigParser()
configFilePath = r"settings/config.txt"
config.read(configFilePath, encoding="utf-8")

# Global variables
auth_client = cbpro.AuthenticatedClient(config.get("CONFIG", "CB_PRO_PUBLIC"),
                                        config.get("CONFIG", "CB_PRO_PRIVATE"),
                                        config.get("CONFIG", "CB_PRO_PASSPHRASE")
                                        )
public_client = cbpro.PublicClient()


def getcoins():
    print("Please enter the symbol of the coins you want to buy (if buying multiple, seperate them with commas):")
    coins = input().upper()
    coins = coins.replace(" ", "")
    coins = coins.split(",")
    for i in range(len(coins)):
        # Check to see if coin can be bought on CoinbasePro
        pair = coins[i] + "-" + config.get("CONFIG", "CURRENCY")
        response = public_client.get_product_order_book(pair)

        if "message" in response:
            print(pair + " is an invalid trading pair for CoinbasePro, please re-run the program and try again")
            sys.exit()

    getpurchaseamount(coins)


def getpurchaseamount(coins):
    amount = []
    currency = config.get("CONFIG", "CURRENCY")
    print("How much do you want to spend? (Minimum amount per transaction is 10" + currency + ")")
    for i in range(len(coins)):
        spend = input(coins[i] + ":\t" + currency)
        try:
            spend = float(spend)
            amount.append(str(spend))
            if spend < 10:
                print("Has to be more than 10, Try again!")
                sys.exit()
        except ValueError:
            print("Please only enter digits, Try again!")
            sys.exit()

    with open("settings/coins.txt", "w") as file:
        for i in range(len(coins)):
            value_to_write = coins[i] + "," + amount[i] + "\n"
            file.write(value_to_write)


def buycrypto(specs):
    order = auth_client.buy(order_type="market",
                            product_id=specs["coin"] + "-" + config.get("CONFIG", "CURRENCY"),
                            funds=specs["amount"])  # Amount you want to buy

    order_id = order["id"]  # Uses the order ID to get specific details of transaction

    return order_id


def writetolog(dets):
    try:
        msg = dets["product_id"] + " - Date & Time: " + dets["created_at"] + \
              " - Gross Spent: " + dets["specified_funds"] + " - Fees: " + dets["fill_fees"] + \
              " - Net Spent: " + dets["funds"] + " - Amount Bought: " + dets["filled_size"]
    except:
        msg = "Error getting order details"  # Don't want to break the whole program so it prints this instead

    logger.info(msg)


def sendmsg(order_details):
    try:
        bought_rounded = round(float(order_details["specified_funds"]), 2)
        msg = order_details["product_id"] + "- You got " + order_details["filled_size"] + " for " + \
              bought_rounded + config.get("CONFIG", "CURRENCY")
    except:
        msg = "You bought some crypto but for some reason the messaging part of it fucked up!"

    url = "https://api.telegram.org/bot" + config.get('CONFIG', 'TELEGRAM_BOT_TOKEN') + "/sendMessage?chat_id=" + \
          config.get('CONFIG', 'TELEGRAM_CHAT_ID') + "&text=" + msg

    # send the msg
    requests.get(url)


def main():
    if not os.path.isfile("settings/coins.txt"):
        getcoins()

    order_ids = []
    with open("settings/coins.txt", "r") as coins:
        coin_and_amount = coins.read().splitlines()
        for i in range(len(coin_and_amount)):
            split = coin_and_amount[i].split(",")
            specs = {"coin": split[0], "amount": split[1]}
            order_ids.append(buycrypto(specs))

    time.sleep(10)  # Wait 10 seconds for CB to catch up and log all the transactions

    for i in range(len(order_ids)):
        # Uses the order ID to get specific details of transaction
        dets = auth_client.get_order(order_ids[i])
        writetolog(dets)
        sendmsg(dets)


if __name__ == '__main__':
    main()
