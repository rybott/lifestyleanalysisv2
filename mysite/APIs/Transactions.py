import imaplib
import email
from datetime import datetime, timedelta
import re
import pandas as pd
from bs4 import BeautifulSoup
from pytz import timezone, utc

def parse_date_with_formats(date_str):
    formats = [
        "%b %d, %Y at %I:%M %p ET",  # Abbreviated month with "at" and "ET"
        "%B %d, %Y at %I:%M %p ET",  # Full month with "at" and "ET"
        "%b %d, %Y %I:%M %p",        # Abbreviated month without "at" and "ET"
        "%B %d, %Y %I:%M %p"         # Full month without "at" and "ET"
    ]
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            continue
    raise ValueError(f"Date string '{date_str}' does not match any known formats.")


class Chase:
    def __init__(self):
        pass
    def Get(self,day):
        # Email Server
        imap_server = "imap.gmail.com"
        email_address = "r.bonannibott@gmail.com"
        pw = "aaed bssv hrij tgfa "
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(email_address, pw)

        # Start End Date
        end_date = datetime.now()
        start_date = end_date - timedelta(days=day)
        local_tz = timezone("America/New_York")
        utc_start_date = local_tz.localize(start_date).astimezone(utc)
        utc_end_date = local_tz.localize(end_date).astimezone(utc)

        # Correct date string calculations
        start_str = utc_start_date.strftime("%d-%b-%Y")
        end_str = (utc_end_date + timedelta(days=1)).strftime("%d-%b-%Y")

        print('Starting Date: ',start_str,' Ending Date: ',end_str)

        # Get Transactions
        imap.select('"Chase Transactions"')
        _, msgnums = imap.search(None, f'(SINCE "{start_str}" BEFORE "{end_str}")')

        types = []
        accounts = []
        dates = []
        amounts = []
        descriptions = []

        for msgnum in msgnums[0].split():
            typ, data = imap.fetch(msgnum, "(RFC822)")
            message = email.message_from_bytes(data[0][1])
            subject = message['subject']

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



                    except:
                        break

            if account_info == "(…3699)" or "(...3699)":
                account_info = "Chase Debit 3699"
            elif account_info == "Chase Sapphire Preferred (...9133)":
                account_info = "Chase Sapphire 9133"
            else:
                print("Issue with Account: ", account_info)


            types.append(transaction_type)
            accounts.append(account_info)
            dates.append(date_info)
            descriptions.append(merchant_info)
            amounts.append(amount_info)

        Transactions_df = pd.DataFrame({
        'date': dates,
        'account': accounts,
        'transaction_type': types,
        'description': descriptions,
        'amount': amounts
        })

        # Transform Date into Datetime format
        Transactions_df['date'] = Transactions_df['date'].str.replace(r' at| ET', '', regex=True)
        Transactions_df['date'] = Transactions_df['date'].apply(parse_date_with_formats)

        # Transform Amount from $ to float
        # Step 1: Ensure all '$' symbols are removed
        Transactions_df['amount'] = Transactions_df['amount'].str.replace(r'[$,]', '', regex=True)

        # Step 2: Convert the column to float
        try:
            Transactions_df['amount'] = Transactions_df['amount'].astype(float)
        except ValueError as e:
            print(f"Error converting to float: {e}")
            # Identify problematic rows
            problematic_rows = Transactions_df[~Transactions_df['amount'].str.replace(r'[.]', '', regex=True).str.isnumeric()]
            print("Problematic rows:\n", problematic_rows)

        imap.close()
        imap.logout()
        return Transactions_df

class Discover:
    def __init__(self):
        pass
    def Get(self,day):
        # Email Server
        imap_server = "imap.gmail.com"
        email_address = "r.bonannibott@gmail.com"
        pw = "aaed bssv hrij tgfa "
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(email_address, pw)

        # Start End Date
        end_date = datetime.now()
        start_date = end_date - timedelta(days=day)
        start_str = start_date.strftime("%d-%b-%Y")
        end_str = (end_date + timedelta(days=1)).strftime("%d-%b-%Y")

        imap.select('"Discover Transactions"')
        _, msgnums = imap.search(None, f'(SINCE "{start_str}" BEFORE "{end_str}")')

        types = []
        accounts = []
        dates = []
        amounts = []
        descriptions = []

        for msgnum in msgnums[0].split():
            typ, data = imap.fetch(msgnum, "(RFC822)")
            message = email.message_from_bytes(data[0][1])
            for part in message.walk():
                if part.get_content_type() == "text/html":
                    html_content = part.get_payload(decode=True).decode('utf-8')
                    try:
                        # Extract data using regex
                        transaction_date_match = re.search(r"Transaction Date:\s+([A-Za-z]+\s\d{1,2},\s\d{4})", html_content)
                        merchant_match = re.search(r"Merchant:\s+(.+?)<br", html_content)
                        amount_match = re.search(r"Amount:\s+\$([\d\.]+)", html_content)

                        # Assign extracted data
                        transaction_type = "Credit Card Transaction"
                        account_info = "Discover 1494"
                        transaction_date = datetime.strptime(transaction_date_match.group(1), "%B %d, %Y") if transaction_date_match else None
                        merchant = merchant_match.group(1).strip() if merchant_match else None
                        amount = float(amount_match.group(1)) if amount_match else None

                        # Append data to lists
                        types.append(transaction_type)
                        accounts.append(account_info)
                        dates.append(transaction_date)
                        amounts.append(amount)
                        descriptions.append(merchant)

                    except AttributeError as e:
                        print(f"Error parsing transaction: {e}")

        Transactions_df = pd.DataFrame({
        'date': dates,
        'account': accounts,
        'transaction_type': types,
        'description': descriptions,
        'amount': amounts
        })

        imap.close()
        imap.logout()
        return Transactions_df

Days= 1

category_map = pd.read_excel(r"C:\Users\rybot\OneDrive\Desktop\Good Transactions\AutoCategory.xlsx", header=None, names=['text', 'id'])

mapping_dict = category_map.set_index('text')['id'].to_dict()

def map_category(description):
    description_lower = description.lower()  # Convert description to lowercase
    for text, category_id in mapping_dict.items():
        if text.lower() in description_lower:  # Case-insensitive substring matching
            return category_id
    return 30

Cdf = Chase().Get(day=Days)
Ddf = Discover().Get(day=Days)

df = pd.concat([Cdf,Ddf])

df['category_id'] = df['description'].apply(map_category)

print(df)
