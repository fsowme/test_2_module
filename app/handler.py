import os

import dotenv
import faust

dotenv.load_dotenv()

app = faust.App(
    'test-2', broker=os.environ['BROKER'], value_serializer="raw", store=os.environ['STORE']
)

input_topic = app.topic(os.environ['TOPIC'])
