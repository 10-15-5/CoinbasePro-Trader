import cbpro
import os


def buycrypto():

    btc_order = auth_client.buy(order_type="market",
                                product_id='BTC-EUR',
                                funds="10")  # Amount you want to buy

    btc_orderid = btc_order["id"]  # Uses the order ID to get extra, specific details of transaction

    ltc_order = auth_client.buy(order_type="market",
                                product_id='LTC-EUR',
                                funds="10")

    ltc_orderid = ltc_order["id"]

    eth_order = auth_client.buy(order_type="market",
                                product_id='ETH-EUR',
                                funds="10")

    eth_orderid = eth_order["id"]

    return btc_orderid, ltc_orderid, eth_orderid


def writetofile(orders):

    btcno = orders[0]
    ltcno = orders[1]
    ethno = orders[2]

    # Bitcoin Details
    btcdets = auth_client.get_order(btcno)  # Uses the order ID to get extra, specific details of transaction

    try:
        msg = "Date & Time:\t" + btcdets["created_at"] + "\tGross Spent:\t" + btcdets["specified_funds"] \
              + "\tFees:\t" + btcdets["fill_fees"] + "\tNet Spent:\t" + btcdets["funds"] + \
              "\tAmount Bought:\t" + btcdets["filled_size"]
    except:
        msg = "Error printing Bitcoin details"  # Don't want to break the whole program so it prints this instead

    f = open(os.environ.get("CoinbaseDirectory") + "btc.txt", "a")
    f.write(msg + "\n")
    f.close()

    # Litecoin Details
    ltcdets = auth_client.get_order(ltcno)

    try:
        msg = "Date & Time:\t" + ltcdets["created_at"] + "\tGross Spent:\t" + ltcdets["specified_funds"] \
              + "\tFees:\t" + ltcdets["fill_fees"] + "\tNet Spent:\t" + ltcdets["funds"] + \
              "\tAmount Bought:\t" + ltcdets["filled_size"]
    except:
        msg = "Error printing Litecoin details"

    f = open(os.environ.get("CoinbaseDirectory") + "ltc.txt", "a")
    f.write(msg + "\n")
    f.close()

    # Ethereum Details
    ethdets = auth_client.get_order(ethno)

    try:
        msg = "Date & Time:\t" + ethdets["created_at"] + "\tGross Spent:\t" + ethdets["specified_funds"] \
              + "\tFees:\t" + ethdets["fill_fees"] + "\tNet Spent:\t" + ethdets["funds"] + \
              "\tAmount Bought:\t" + ethdets["filled_size"]
    except:
        msg = "Error printing Ethereum details"

    f = open(os.environ.get("CoinbaseDirectory") + "eth.txt", "a")
    f.write(msg + "\n")
    f.close()


auth_client = cbpro.AuthenticatedClient(os.environ.get("CoinbasePro_API_Public"),
                                            os.environ.get("CoinbasePro_API_Secret"),
                                            os.environ.get("CoinbasePro_Passphrase"))

orders = buycrypto()
writetofile(orders)
