import pandas as pd
import datetime
from datetime import timedelta, timezone

def convert_to_utc(row):

    try:

        # Get the datetime and timezone offset from the row
        dt = row['datetime']
        tz_offset_str = row['utc_zone']
        
        # Parse the timezone offset
        offset_hours = int(tz_offset_str[:3])
        offset_minutes = int(tz_offset_str[0] + tz_offset_str[3:])
        offset = timedelta(hours=offset_hours, minutes=offset_minutes)
        
        # Create a timezone with the offset
        tz = timezone(offset)
        
        # Assign the timezone to the datetime
        dt = dt.replace(tzinfo=tz)
        
        # Convert the datetime to UTC
        return dt.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    except Exception as e:
        print(e)
        return None

def create_utc_date_column(df):

    try:

        df['datetime'] = pd.to_datetime(df['date'].str[:-6], errors='coerce')
        df['utc_zone'] = df['date'].str[-5:]
        df['utc_datetime'] = df.apply(convert_to_utc, axis=1)

        return df
    
    except Exception as e: 
        print(e)
        return None