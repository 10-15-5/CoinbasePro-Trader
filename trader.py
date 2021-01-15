import cbpro
import os

auth_client = cbpro.AuthenticatedClient(os.environ.get("CoinbasePro_API_Public"),
                                        os.environ.get("CoinbasePro_API_Secret"),
                                        os.environ.get("CoinbasePro_Passphrase"))

#######################################################################
#                       Bitcoin Order Section                         #
#######################################################################
btc_order = auth_client.buy(order_type="market",
                            product_id='BTC-EUR',
                            funds="90")  # Amount you want to buy

orderdets = auth_client.get_order(btc_order["id"])  # Uses the order ID to get extra, specific details of transaction

try:
    msg = "Date & Time:\t" + orderdets["created_at"] + "\tGross Spent:\t" + orderdets["specified_funds"] \
          + "\tFees:\t" + orderdets["fill_fees"] + "\tNet Spent:\t" + orderdets["funds"] + \
          "\tAmount Bought:\t" + orderdets["filled_size"]
except:
    msg = "Error printing Bitcoin details"    # Don't want to break the whole program so it prints this instead

f = open(os.environ.get("CoinbaseDirectory") + "btc.txt", "a")
f.write(msg + "\n")
f.close()

#######################################################################
#                       Litecoin Order Section                        #
#######################################################################

ltc_order = auth_client.buy(order_type="market",
                            product_id='LTC-EUR',
                            funds="15")

orderdets = auth_client.get_order(ltc_order["id"])

try:
    msg = "Date & Time:\t" + orderdets["created_at"] + "\tGross Spent:\t" + orderdets["specified_funds"] \
          + "\tFees:\t" + orderdets["fill_fees"] + "\tNet Spent:\t" + orderdets["funds"] + \
          "\tAmount Bought:\t" + orderdets["filled_size"]
except:
    msg = "Error printing Litecoin details"

f = open(os.environ.get("CoinbaseDirectory") + "ltc.txt", "a")
f.write(msg + "\n")
f.close()

#######################################################################
#                       Ethereum Order Section                        #
#######################################################################

eth_order = auth_client.buy(order_type="market",
                            product_id='ETH-EUR',
                            funds="45")

# At time of writing this program, Coinbase doesnt seem to be sending a message back when Ethereum is bought!
"""
orderdets = auth_client.get_order(eth_order["id"])

try:
    msg = "Date & Time:\t" + orderdets["created_at"] + "\tGross Spent:\t" + orderdets["specified_funds"] \
          + "\tFees:\t" + orderdets["fill_fees"] + "\tNet Spent:\t" + orderdets["funds"] + \
          "\tAmount Bought:\t" + orderdets["filled_size"]
except:
    msg = "Error printing Ethereum details"

f = open(os.environ.get("CoinbaseDirectory") + "eth.txt", "a")
f.write(msg + "\n")
f.close()
"""