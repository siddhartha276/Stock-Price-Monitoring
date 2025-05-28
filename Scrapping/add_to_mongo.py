from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client['StockHistory']
collection = db['TradingData']

class AddData:

    def append_data(self, row, name):
        date = row[0].text
        open_price = row[2].text
        high = row[3].text
        low = row[4].text
        prev_close = row[5].text
        close = row[7].text
        volume = row[11].text
        value = row[12].text
        trades = row[13].text
        try:
            data = {
                "open": open_price,
                "high": high,
                "low": low,
                "previousClose": prev_close,
                "close": close,
                "volume": volume,
                "value": value,
                "numberOfTrades": trades,
            }

            # Upsert into MongoDB
            collection.update_one(
                {"company.name": name},
                {
                    "$set": {
                        "company": {
                            "name": name,
                        },
                        f"stockHistory.{date}": data
                    }
                },
                upsert=True
            )
            print(f"{name} data for {date} saved to MongoDB")

        except Exception as e:
            print(f"Error Appending the data to the database: {e}")