# 1）导入必要的库和模块  
import findspark  
findspark.init()  
from pyspark.sql import SparkSession  
from pyspark.ml.feature import VectorAssembler  
from pyspark.ml.classification import LogisticRegression  

import matplotlib.pyplot as plt  
from sklearn.metrics import roc_curve, auc  

# 2）创建SparkSession  
spark = SparkSession.builder.appName("diabetesClassification").getOrCreate()  
    
# 3）加载数据集  
data = spark.read.csv("diabetes.csv", header=True, inferSchema=True)  

# 4）数据预处理  
# 将特征列组合为一个向量  
assembler = VectorAssembler(inputCols=data.columns[:-1], outputCol="features")  
data = assembler.transform(data)  
# 重命名标签列为"label"  
data = data.withColumnRenamed("Outcome", "label")  
# 仅保留特征向量和标签列  
data = data.select("features", "label")  

# 5）划分数据集为训练集和测试集  
train_data, test_data = data.randomSplit([0.8, 0.2], seed=123)  

# 6）定义并训练二分类模型（本案例用逻辑回归模型）  
lr = LogisticRegression()  
model = lr.fit(train_data)  

# 7）在测试集上进行预测  
predictions = model.transform(test_data)  

# 8）评估模型性能  
# 提取预测分数和标签  
preds_and_labels = predictions.select("probability", "label").collect()  

# 将数据转换为适合绘图的格式  
y_true = [float(label) for _, label in preds_and_labels]  
y_scores = [float(prob[1]) for prob, _ in preds_and_labels]   

# 绘制AUC-ROC曲线  
fpr, tpr, _ = roc_curve(y_true, y_scores)  
roc_auc = auc(fpr, tpr)  

plt.figure()  
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (auc = {roc_auc:.3f})')  
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')  
plt.xlim([0.0, 1.0])  
plt.ylim([0.0, 1.05])  
plt.xlabel('FPR')  
plt.ylabel('TPR')  
plt.legend(loc="lower right")  
plt.savefig('roc curve.svg')
plt.show()  

# 9）关闭SparkSession  
spark.stop()  