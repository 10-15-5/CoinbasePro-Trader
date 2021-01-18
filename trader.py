import cbpro
import os
import logging
import time
import requests


def buycrypto():
    btc_order = auth_client.buy(order_type="market",
                                product_id='BTC-EUR',
                                funds="90")  # Amount you want to buy

    btc_orderid = btc_order["id"]  # Uses the order ID to get extra, specific details of transaction

    ltc_order = auth_client.buy(order_type="market",
                                product_id='LTC-EUR',
                                funds="15")

    ltc_orderid = ltc_order["id"]

    eth_order = auth_client.buy(order_type="market",
                                product_id='ETH-EUR',
                                funds="45")

    eth_orderid = eth_order["id"]

    link_order = auth_client.buy(order_type="market",
                                 product_id='LINK-EUR',
                                 funds="10")

    link_orderid = link_order["id"]

    return btc_orderid, ltc_orderid, eth_orderid, link_orderid


def sendmsg(orders, chatid, bot_token):
    # Bitcoin Details
    btcdets = auth_client.get_order(orders[0])  # Uses the order ID to get extra, specific details of transaction

    try:
        msg = f'\u20BFitcoin - Date & Time:{btcdets["created_at"]} - Gross Spent: {btcdets["specified_funds"]}' \
              f' - Fees: {btcdets["fill_fees"]} - Net Spent: {btcdets["funds"]}' \
              f' - Amount Bought: {btcdets["filled_size"]}'
    except:
        msg = "Error getting \u20BFitcoin details"  # Don't want to break the whole program so it prints this instead

    logger.info(msg)

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chatid}&text={msg}"

    # send the msg
    requests.get(url)

    # Litecoin Details
    ltcdets = auth_client.get_order(orders[1])

    try:
        msg = f'Litecoin - Date & Time:{ltcdets["created_at"]} - Gross Spent: {ltcdets["specified_funds"]}' \
              f' - Fees: {ltcdets["fill_fees"]} - Net Spent: {ltcdets["funds"]}' \
              f' - Amount Bought: {ltcdets["filled_size"]}'
    except:
        msg = "Error getting Litecoin details"

    logger.info(msg)

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chatid}&text={msg}"

    # send the msg
    requests.get(url)

    # Ethereum Details
    ethdets = auth_client.get_order(orders[2])

    try:
        msg = f'Ethereum - Date & Time:{ethdets["created_at"]} - Gross Spent: {ethdets["specified_funds"]}' \
              f' - Fees: {ethdets["fill_fees"]} - Net Spent: {ethdets["funds"]}' \
              f' - Amount Bought: {ethdets["filled_size"]}'
    except:
        msg = "Error getting Ethereum details"

    logger.info(msg)

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chatid}&text={msg}"

    # send the msg
    requests.get(url)

    # Chainlink Details
    linkdets = auth_client.get_order(orders[3])

    try:
        msg = f'Chainlink - Date & Time:{linkdets["created_at"]} - Gross Spent: {linkdets["specified_funds"]}' \
              f' - Fees: {linkdets["fill_fees"]} - Net Spent: {linkdets["funds"]}' \
              f' - Amount Bought: {linkdets["filled_size"]}'
    except:
        msg = "Error getting Ethereum details"

    logger.info(msg)

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chatid}&text={msg}"

    # send the msg
    requests.get(url)


# ------------------------------------------------------------------
#   Logging Setup
# ------------------------------------------------------------------

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(message)s')

file_handler = logging.FileHandler(os.environ.get("CoinbaseDirectory") + "CoinbasePro-Trader.log", encoding='utf8')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# ------------------------------------------------------------------


auth_client = cbpro.AuthenticatedClient(os.environ.get("CoinbasePro_API_Public"),
                                        os.environ.get("CoinbasePro_API_Secret"),
                                        os.environ.get("CoinbasePro_Passphrase"))

bot_token = os.environ.get("CryptoTrackerBotToken")
chatid = os.environ.get("TelegramChatID")

orders = buycrypto()
time.sleep(10)  # Wait 10 seconds for CB to catch up and log the transaction
sendmsg(orders, chatid, bot_token)
