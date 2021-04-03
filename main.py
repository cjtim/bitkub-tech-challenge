import urllib.request
import json
import pandas as pd
import time

KEY_API = '7VGM2ZKZ92VRXI4IPDIMXFC2CPA3A1HH2M'


def getAccountTransaction(account: str):
    f = urllib.request.urlopen(
        'https://api-ropsten.etherscan.io/api?module=account&action=tokentx&address=' + account +
        '&startblock=0&endblock=999999999&sort=asc&apikey=' + KEY_API
    )
    time.sleep(1)
    data = json.loads(f.read().decode('utf-8'))
    return data['result']


def getData(accountId: str) -> list:
    outputData = []
    toAccount = []
    transaction = getAccountTransaction(accountId.lower())
    for i in transaction:
        if (i['from'] == accountId.lower() and i['tokenSymbol'] == 'BKTC'):
            outputData.append({
                'txHash': i['hash'],
                'from': i['from'],
                'to': i['to'],
                'value': float(int(i['value']) / 10**18)
            })
            toAccount.append(i['to'])
    toAccount = list(dict.fromkeys(toAccount))  # remove dup
    if (len(toAccount) > 0):
        for account in toAccount:
            nextAccount = getData(account)
            outputData.extend(nextAccount)
    return outputData


if __name__ == "__main__":
    global CSVoutput
    name = input('Name: ')
    email = input('Email: ')
    wallet_account = input('Wallet Address: ')
    CSVoutput = getData(wallet_account)
    df = pd.DataFrame(CSVoutput)
    df.to_csv('transaction.csv')
    accountBalance = df.groupby('to').sum().loc[:, ['value']]
    accountBalance.to_csv('accountBalance.csv')
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)
        print(accountBalance)
    print()
    print('All Transaction saved to transaction.csv')
    print('Account Balance saved to accountBalance.csv')
