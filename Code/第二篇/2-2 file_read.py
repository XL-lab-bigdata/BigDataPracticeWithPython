from pyspark.sql import SparkSession
#创建SparkSession对象
spark = SparkSession.builder.appName("FileRead").getOrCreate()
#读取csv文件
df = spark.read.format("csv").load("file_path" , sep=',', header=True, inferSchema=True)
#查看数据
df.show()
#关闭SparkSession对象
spark.stop()
