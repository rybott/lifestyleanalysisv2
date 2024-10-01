import imaplib
import email
from datetime import datetime, timedelta
import re
import pandas as pd
from bs4 import BeautifulSoup

database = ""

# Chase

imap_server = "imap.gmail.com"
email_address = "r.bonannibott@gmail.com"
pw = "aaed bssv hrij tgfa "
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_address, pw)

# Start End Date
end_date = datetime.now()
start_date = end_date - timedelta(days=730)
start_str = start_date.strftime("%d-%b-%Y")
end_str = (end_date + timedelta(days=1)).strftime("%d-%b-%Y")

# Search Email
imap.select('"Chase Transactions"')
_, msgnums = imap.search(None, f'(SINCE "{start_str}" BEFORE "{end_str}")')

types = []
accounts = []
dates = []
amounts = []
descriptions = []

counter = 0

for msgnum in msgnums[0].split():
    typ, data = imap.fetch(msgnum, "(RFC822)")
    message = email.message_from_bytes(data[0][1])
    subject = message['subject']
    date = message['date']
    sender = message['from']


    for part in message.walk():
        if part.get_content_type() == "text/html":
            html_content = part.get_payload(decode=True)
            soup = BeautifulSoup(html_content, 'html.parser')
            try:
                if "debit_card" in subject:
                    transaction_type = "Checking Account Transaction"
                    account_info = soup.find('td', string=lambda text: text and 'Account ending in' in text).find_next('td').text.strip()
                    date_info = soup.find('td', string=lambda text: text and 'Made on' in text).find_next('td').text.strip()
                    amount_info = soup.find('td', string=lambda text: text and 'Amount' in text).find_next('td').text.strip()
                    merchant_info = soup.find('td', string=lambda text: text and 'Description' in text).find_next('td').text.strip()

                elif "(..." in subject:
                    transaction_type = "Debit Card Transaction"
                    account_info = soup.find('td', string=lambda text: text and 'Account ending in' in text).find_next('td').text.strip()
                    date_info = soup.find('td', string=lambda text: text and 'Sent on' in text).find_next('td').text.strip()
                    merchant_info = soup.find('td', string=lambda text: text and 'Recipient' in text).find_next('td').text.strip()
                    amount_info = soup.find('td', string=lambda text: text and 'Amount' in text).find_next('td').text.strip()

                elif "deposit" in subject:
                    transaction_type = "Check Deposit"
                    account_info = soup.find('td', string=lambda text: text and 'Account' in text).find_next('td').text.strip()
                    date_info = soup.find('td', string=lambda text: text and 'Received' in text).find_next('td').text.strip()
                    amount_info = soup.find('td', string=lambda text: text and 'Amount' in text).find_next('td').text.strip()
                    merchant_info = "Deposit" 

                else:
                    transaction_type = "Credit Card Transaction"
                    account_info = soup.find_all('td', string='Account')[0].find_next('td').text.strip()
                    date_info = soup.find_all('td', string='Date')[0].find_next('td').text.strip()
                    merchant_info = soup.find_all('td', string='Merchant')[0].find_next('td').text.strip()
                    amount_info = soup.find_all('td', string='Amount')[0].find_next('td').text.strip()

                counter = counter +1


            except:
                # Add the Error Handling for Chase and then discover
                break
        
    types.append(transaction_type)
    accounts.append(account_info)
    dates.append(date_info)
    descriptions.append(merchant_info)
    amounts.append(amount_info)

# print(len(dates),len(types),len(accounts),len(amounts),len(descriptions))

Transactions_df = pd.DataFrame({
  'Date': dates,
  'Type': types,
  'Account': accounts,
  'Amount': amounts,
  'Description': descriptions,
})

imap.close()
imap.logout()

