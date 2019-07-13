from pyspark.sql import SparkSession
from pyspark.sql import DataFrameWriter
from pyspark import SparkContext, SparkConf


conf = (SparkConf()
        .setAppName("eddb_data")
        .setMaster('spark://LVS-02:7077')
        .set("spark.cassandra.connection.host","172.17.0.2")
        )
context = SparkContext(conf=conf)
spark = SparkSession(context)

#spark = SparkSession \
#        .builder \
#        .appName("eddb_listings") \
#        .config("spark.cassandra.connection.host","172.17.0.2") \ 
#        .getOrCreate()


df_data = spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="eddb_data", keyspace="eddb_db") \
    .load()

df_data.show()

#better way but doesn't work 
#df_data.write.csv(path='/tmp/check_cass_data', header=True)

#critical function! use only when export small datasets, all data will load in memory when use pandas.dataframe
df_data.toPandas().to_csv('/tmp/check_cass_data.csv', header=True, encoding='utf8')