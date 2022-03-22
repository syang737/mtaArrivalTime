#Link to station id mapping: http://web.mta.info/developers/data/nyct/subway/Stations.csv

from google.transit import gtfs_realtime_pb2
import time
import requests
from datetime import datetime, date

def getArrivalTimes(feed, stop_id):
	"""
	Returns all arrival times for a specific stop_id in the given feed
	"""

	arrivalTimes = []
	for feed_entity in feed.entity:
		if feed_entity.HasField('trip_update'):
			tu = feed_entity.trip_update
			for stu in tu.stop_time_update:
				if stu.stop_id == stop_id:
				#formatted_stu = time.strftime('%H:%M:%S', time.localtime(stu.arrival.time))
					arrivalTimes.append(datetime.fromtimestamp(stu.arrival.time))

	return arrivalTimes

#Initialize protobuf feed and get trip data by querying MTA api

feed = gtfs_realtime_pb2.FeedMessage()

api_key = 'lveqR42dVC8ekUUaDmdQx9ZXh6tPPmRt2SMyPfL1'
url = r'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs'

headers = {'x-api-key': api_key}
r = requests.get(url, headers = headers)

feed.ParseFromString(r.content)

flushing_bound_times = getArrivalTimes(feed, '721N')
herald_bound_times = getArrivalTimes(feed, '721S')

future_flushing_bound_times = sorted([i for i in flushing_bound_times if i > datetime.now()])
future_herald_bound_times = sorted([i for i in herald_bound_times if i > datetime.now()])

flushing_bound_time_away = future_flushing_bound_times[0] - datetime.now()
herald_bound_time_away = future_herald_bound_times[0] - datetime.now()

print('Flushing: In ' + str(flushing_bound_time_away.seconds//60) + ' min')
print('34th Street Herald Square: In ' + str(herald_bound_time_away.seconds//60) + ' min')
