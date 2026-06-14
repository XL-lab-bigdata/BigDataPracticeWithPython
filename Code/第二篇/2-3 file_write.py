#创建SparkSession对象
import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("FileWrite").getOrCreate()
#创建DataFrame对象
data = [("Apple Inc.", 57411000000), ("Microsoft Corp.", 61271000000), ("Tesla Inc.", 7210000000)]
df = spark.createDataFrame(data, ["Company Name", "Net Profit"])
#查看DataFrame
df.show()
#将DataFrame写入文件
df.write.format("csv").option("header", "true").mode("overwrite").save("file_path")
#关闭SparkSession对象
spark.stop()