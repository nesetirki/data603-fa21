import time

import matplotlib.pyplot as plt
from pyspark.sql import SparkSession

spark = (SparkSession
         .builder
         .appName("issStreamer")
         .getOrCreate()
        )

lines = (
	spark.readStream
	.format("socket")
	.option("host", "localhost")
	.option("port", 22225)
	.load()
)

stream_df = lines.selectExpr("CAST(value AS STRING) AS payload")

writer = (
	stream_df.writeStream
	.queryName('iss')
	.format('memory')
	.outputMode('append')
)

streamer = writer.start()

for i in range(5):
	all_df = spark.sql("select * from iss")
	all_df.show()
	temp_df = spark.sql("""
SELECT
	get_json_object(payload, '$.iss_position.latitude') AS latitude,
	get_json_object(payload, '$.iss_position.longitude') AS longitude
FROM iss
""").toPandas()

	print(temp_df)
	time.sleep(5)

streamer.awaitTermination(timeout=30)
print('streaming done')
temp_df.plot.line(x='latitude', y='longitude')
plt.show()



