#导入必要的库和模块
import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import col 

# 创建SparkSession
spark = SparkSession.builder.appName("diabetesClassification").getOrCreate()

# 加载数据集
data = spark.read.csv("diabetes.csv", header=True, inferSchema=True)

# 显示数据前10条
data.show(10)

# 选择数值列  
numeric_columns = [field.name for field in data.schema.fields if field.dataType.typeName() in ["integer", "long", "double", "float"]]  

# 使用 describe() 方法获取基本统计信息  
stats = data.select(numeric_columns).describe()  
stats.show()  

# 使用 summary() 方法获取更详细的统计信息  
summary = data.select(numeric_columns).summary()  
summary.show() 