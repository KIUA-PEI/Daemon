from influxdb import InfluxDBClient

# start influxDBClient
influx = InfluxDBClient(host='127.0.0.1', port=8086)
influx.create_database("Metrics")