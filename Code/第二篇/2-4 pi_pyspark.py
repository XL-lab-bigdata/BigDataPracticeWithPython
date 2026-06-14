import findspark
findspark.init()
from pyspark import SparkConf, SparkContext
import random

conf = SparkConf().setAppName("Pi").setMaster("spark://Node01:7077")
sc = SparkContext(conf=conf)

num_samples = 1000000000
	
def inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

count = sc.parallelize(range(0, num_samples)).filter(inside).count()
pi = 4 * count / num_samples/

print("Approximate value of pi is: {}".format(pi))
sc.stop()
