import gdax
import time
import threading
import pandas as pd
import numpy as  np
import os
import datetime
import s3upload


INTERVAL = 5.0
EXPORT_TRESHOLD = 2

def createCoinDataFrame(df, public_client):
    """ Returns dataframe of all data extracted from GDAX API"""
    combined_data = {}

    # Access GDAX API to get exchange data
    orderbook = public_client.get_product_order_book('LTC-USD', level=2)
    day_stats = public_client.get_product_24hr_stats('LTC-USD')
    price = public_client.get_product_ticker(product_id='LTC-USD')

    # Combine data into a single Dictionary
    combined_data.update(price)
    combined_data.update(day_stats)
    combined_data.update(orderbook)

    newdf = pd.DataFrame([combined_data], columns=combined_data.keys())
    newdf.set_index("time", inplace = True)

    df = pd.concat([df, newdf])

    return df

def resetCoinDataFrame():
    """ Return an Empty Dataframe """
    df = pd.DataFrame(columns=['trade_id', 'price', 'size', 'bid', 'ask', 'volume', 'time', 'open',
       'high', 'low', 'last', 'volume_30day', 'sequence', 'bids', 'asks'])
    df.set_index("time", inplace = True)
    return df

def prepareDataFrame():
    """ Returns function with dataframe created in parent scope """
    df = resetCoinDataFrame()

    public_client = gdax.PublicClient()
    count = 0
    now = datetime.datetime.now()
    prevdate = now.strftime("%Y-%m-%d")

    def loopExtraction():
        """ Run data extraction after time indicated in INTERVAL constant """
        """ DATA: USD SPREAD, price, somesimplification of orderbook(STD DEV, mean, mode, median ...)
        """
        nonlocal df, count, public_client, prevdate
        upload = False

        threading.Timer(INTERVAL, loopExtraction).start()

        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d")
        file_name = "data/{}.csv".format(today)

        # Checks if there is a change in day
        # If there is, reset pandas DataFrame and reset datacount
        if today != prevdate:
            upload = True
            df = resetCoinDataFrame()
            count == 0


        # Collect GDAX data into a single row DataFrame
        df = createCoinDataFrame(df, public_client)


        # Every (EXPORT_TRESHOLD) iterations, export dataframe to csv
        count = count + 1
        if count % EXPORT_TRESHOLD == 1:

            # if file does not exist write header
            if not os.path.isfile(file_name):
                df.to_csv(file_name, sep=',')
                df = resetCoinDataFrame()
            else: # else it exists so append without writing the header
                df.to_csv(file_name, mode = 'a', sep=',', header=False)
                df = resetCoinDataFrame()

        #Upload CSV To Amazon S3 Database, then delete file in order to conserve storage space.
        if upload:
            yesterday_file = "data/{}.csv".format(prevdate)
            s3upload.uploadToS3(yesterday_file)
            print("Sent {} to S3".format(yesterday_file))
            os.remove(yesterday_file)
            upload = False
        prevdate = today
        # if count % 5 == 0:
        #     print("Size of Dataset: {}".format(count))


    return loopExtraction



if __name__ == "__main__":
    loop = prepareDataFrame()
    print("Starting Data Extraction...")
    loop()
