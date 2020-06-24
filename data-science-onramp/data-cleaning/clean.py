import sys
import re
import datetime

from py4j.protocol import Py4JJavaError
from pyspark.sql import SparkSession
from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql.types import StringType, IntegerType, FloatType


PROJECT_ID = sys.argv[1]
BUCKET_NAME = sys.argv[2]
TABLE = f'{PROJECT_ID}.new_york_citibike_trips.RAW_DATA'

def trip_duration_udf(duration):
    '''Convert trip duration to seconds.'''
    if not duration:
        return None
    
    time = re.match('\d*.\d', duration)

    if not time:
        return None

    time = float(time[0])

    if time < 0:
        return None

    if 'm' in duration:
        time *= 60
    elif 'h' in duration:
        time *= 60 * 60
    
    return int(time)

def station_name_udf(name):
    '''Replaces '/' with '&'.'''
    return name.replace('/', '&') if name else None

def user_type_udf(user):
    '''Converts user type to 'Subscriber' or 'Customer'.'''
    if not user:
        return None
    
    if user.lower().startswith('sub'):
        return 'Subscriber'
    elif user.lower().startswith('cust'):
        return 'Customer'

def gender_udf(gender):
    '''Converts gender to 'Male' or 'Female'.'''
    if not gender:
        return None
    
    if gender.lower().startswith('m'):
        return 'Male'
    elif gender.lower().startswith('f'):
        return 'Female'

def angle_udf(angle):
    '''Converts DMS notation to angles.'''
    if not angle:
        return None
    
    dms = re.match('(-?\d*).(-?\d*)\'(-?\d*)"', angle)
    if dms:
        return int(dms[1]) + int(dms[2])/60 + int(dms[3])/(60 * 60)
    
    try:
        return float(angle)
    except ValueError:
        return None

def compute_time(duration, start, end):
    '''Calculates duration, start time, and end time from each other if one value is null.'''
    time_format = '%Y-%m-%dT%H:%M:%S'

    # Transform to datetime objects
    if start:
        # Round to nearest second
        if '.' in start:
            start = start[:start.index('.')]
        # Convert to datetime
        start = datetime.datetime.strptime(start, time_format)
    if end:
        # Round to nearest second
        if '.' in end:
            end = end[:end.index('.')]
        # Convert to datetime
        end = datetime.datetime.strptime(end, time_format)
    if duration:
        # Convert to timedelta
        duration = datetime.timedelta(seconds=duration)

    # Calculate missing value
    if start and end and not duration:
        duration = end - start
    elif duration and end and not start:
        start = end - duration
    elif duration and start and not end:
        end = start + duration

    # Transform to primitive types
    if duration:
        duration = int(duration.total_seconds())
    if start:
        start = start.strftime(time_format)
    if end:
        end = end.strftime(time_format)

    return (duration, start, end)
        
def compute_duration_udf(duration, start, end):
    '''Calculates duration from start and end time if null.'''
    return compute_time(duration, start, end)[0]

def compute_start_udf(duration, start, end):
    '''Calculates start time from duration and end time if null.'''
    return compute_time(duration, start, end)[1]

def compute_end_udf(duration, start, end):
    '''Calculates end time from duration and start time if null.'''
    return compute_time(duration, start, end)[2]


if __name__ == '__main__':
    # Create a SparkSession, viewable via the Spark UI
    spark = SparkSession.builder.appName('data_cleaning').getOrCreate()

    # Load data into dataframe if table exists
    try:
        df = spark.read.format('bigquery').option('table', TABLE).load()
    except Py4JJavaError:
        print(f'{TABLE} does not exist.')
        raise 

    # Single-parameter udfs
    udfs = {
        'start_station_name': UserDefinedFunction(station_name_udf, StringType()),
        'end_station_name': UserDefinedFunction(station_name_udf, StringType()),
        'tripduration': UserDefinedFunction(trip_duration_udf, IntegerType()),
        'usertype': UserDefinedFunction(user_type_udf, StringType()),
        'gender': UserDefinedFunction(gender_udf, StringType()),
        'start_station_latitude': UserDefinedFunction(angle_udf, FloatType()),
        'start_station_longitude': UserDefinedFunction(angle_udf, FloatType()),
        'end_station_latitude': UserDefinedFunction(angle_udf, FloatType()),
        'end_station_longitude': UserDefinedFunction(angle_udf, FloatType())
    }

    for name, udf in udfs.items():
        df = df.withColumn(name, udf(name))

    # Multi-parameter udfs
    multi_udfs = {
        'tripduration': {
            'udf': UserDefinedFunction(compute_duration_udf, IntegerType()),
            'params': ('tripduration', 'starttime', 'stoptime')
        },
        'starttime': {
            'udf': UserDefinedFunction(compute_start_udf, StringType()),
            'params': ('tripduration', 'starttime', 'stoptime')
        },
        'stoptime': {
            'udf': UserDefinedFunction(compute_end_udf, StringType()),
            'params': ('tripduration', 'starttime', 'stoptime')
        }
    }

    for name, obj in multi_udfs.items():
        df = df.withColumn(name, obj['udf'](*obj['params']))

    # Display sample of 100 rows
    df.sample(False, 0.001).show(n=100)

    # Write results to GCS
    if '--test' in sys.argv:
        print('Data will not be uploaded to GCS')
    else:
        path = 'gs://' + BUCKET_NAME + '/clean_citibike_data' + '.csv.gz'
        df.write.options(codec='org.apache.hadoop.io.compress.GzipCodec').csv(path, mode='overwrite')
        print('Data successfully uploaded to ' + path)
    