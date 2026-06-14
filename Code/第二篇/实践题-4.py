#导入必要的库和模块
import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, LinearSVC
from pyspark.ml.evaluation import BinaryClassificationEvaluator

# 创建SparkSession
spark = SparkSession.builder.appName("diabetesClassification").getOrCreate()

# 加载数据集
data = spark.read.csv("diabetes.csv", header=True, inferSchema=True)

# 数据预处理
# 将特征列组合为一个向量
assembler = VectorAssembler(inputCols=data.columns[:-1], outputCol="features")
data = assembler.transform(data)
# 重命名标签列为"label"
data = data.withColumnRenamed("Outcome", "label")
# 仅保留特征向量和标签列
data = data.select("features", "label")

# 划分数据集为训练集和测试集
train_data, test_data = data.randomSplit([0.8, 0.2], seed=123)

# 定义并训练逻辑回归模型
lr = LogisticRegression()
lr_model = lr.fit(train_data)

# 定义并训练决策树模型
dt = DecisionTreeClassifier()
dt_model = dt.fit(train_data)

# 定义并训练线性支持向量机模型
lsvc = LinearSVC()
lsvc_model = lsvc.fit(train_data)

# 在测试集上进行预测
lr_predictions = lr_model.transform(test_data)
dt_predictions = dt_model.transform(test_data)
lsvc_predictions = lsvc_model.transform(test_data)

# 评估模型性能
evaluator = BinaryClassificationEvaluator()

# 逻辑回归模型性能评估
lr_auc = evaluator.evaluate(lr_predictions)
print("Logistic Regression AUC: ", lr_auc)

# 决策树模型性能评估
dt_auc = evaluator.evaluate(dt_predictions)
print("Decision Tree AUC: ", dt_auc)

# 线性支持向量机模型性能评估
lsvc_auc = evaluator.evaluate(lsvc_predictions)
print("Linear SVC AUC: ", lsvc_auc)

# 关闭SparkSession
spark.stop()