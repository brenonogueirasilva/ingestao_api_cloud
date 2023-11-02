import random 
from datetime import datetime 
import logging 

random_number = random.randint(1000, 9999)
date_now = datetime.now()
trace_id_value = int(f"{random_number}{date_now.hour}{date_now.minute:02}{date_now.second:02}")
trace_id = {'trace_id': trace_id_value }