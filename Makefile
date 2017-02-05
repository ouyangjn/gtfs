all:
	gtfs_feeds/gtfs2sqlite sample_data/general_transit_CleverTripID_1609.zip

clean:
	rm general_transit_CleverTripID_1609.sqlite3
