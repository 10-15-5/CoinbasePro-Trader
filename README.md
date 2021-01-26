# CoinbasePro-Trader README

This very simple program uses the CoinbasePro API to buy a specific amount of crypto at a fixed time, (at time of 
writing I am just using the Windows Task Scheduler to make it run once a week) it then writes the detials of the 
purchase to a .log file and sends an SMS through a Telegram bot to tell me how much I have bought and at what
price.

Uses the cbpro python client to interact with the Coinbase API.

If someone wants to use this program they will have to change:
* The three CoinbasePro API keys, Public, Secret and Passphrase
* The token for the Telegram bot they have set up, you can use my Telegram bot that I have set up although there
is nothing special about it.
* Their Telegram chat ID, without this the Telegram bot won't know where to send the transaction details.  
* You will also have to swap in your username in the directory for logging setup, it's auto set to the main C
Drive
* Finally, update the amount of each crypto you want to buy. 
  
To add a transaction for a crypto just copy-paste one of the existing crypto setups and just change the variable
names to the new one you want.

To remove a transaction just comment out/delete all instances of the transaction you want.

***You need to have funds in your CoinbasePro account for this program to work***

*NB This program is not perfect and there may be a few bugs in it, just let me know if you find anything and
I will try to fix it ASAP.*

*Some of this program does need to be changed to be more efficient, or to just use less code, I will be doing 
this soon I just haven't gotten around to it yet*