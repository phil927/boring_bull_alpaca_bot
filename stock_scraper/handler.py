from yahoo_fin import stock_info as si
import time
import boto3
from botocore.config import Config


STOCK_TICKERS = ["spxl", "aapl", "pltr"]
DATABASE_NAME = 'StockData'
TABLE_NAME = 'StockDataTable'
AWS_ACCESS_KEY_ID = 'AKIAYAJNGB7AHOAJZFMH'
AWS_SECRET_ACCESS_KEY = '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'


def get_stock_price(stock_ticker: str) -> float:
    stock_price = si.get_live_price(stock_ticker)
    print(f"{stock_ticker} price at {stock_price}")
    return stock_price


def current_milli_time():
    return str(int(round(time.time() * 1000)))


def write_to_db(stock_prices: dict):
    print("Writing records")
    current_time = current_milli_time()

    records = []
    for stock_ticker in stock_prices:
        dimensions = [
            {'Name': 'stock-ticker', 'Value': stock_ticker}
        ]
        stock_record = {
            'Dimensions': dimensions,
            'MeasureName': 'stock-price',
            'MeasureValue': str(stock_prices[stock_ticker]),
            'MeasureValueType': 'DOUBLE',
            'Time': current_time
        }
        records.append(stock_record)

    session = boto3.Session()
    write_client = session.client('timestream-write', region_name='us-east-1', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                  config=Config(read_timeout=20, max_pool_connections=5000,
                                                retries={'max_attempts': 10}))
    try:
        result = write_client.write_records(DatabaseName=DATABASE_NAME, TableName=TABLE_NAME,
                                            Records=records, CommonAttributes={})
        print("WriteRecords Status: [%s]" %
              result['ResponseMetadata']['HTTPStatusCode'])
    except write_client.exceptions.RejectedRecordsException as err:
        print("RejectedRecordException:", err)
    except Exception as err:
        print("Error:", err)


def lambda_handler(event, context):
    stock_prices = {}
    for stock_ticker in STOCK_TICKERS:
        stock_prices[stock_ticker] = get_stock_price(stock_ticker)
    write_to_db(stock_prices)
    return stock_prices


if __name__ == '__main__':
    lambda_handler(None, None)
