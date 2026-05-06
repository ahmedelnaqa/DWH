from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession.builder.appName("TestApp").getOrCreate()
    data = [(1, "one"), (2, "two"), (3, "three")]
    df = spark.createDataFrame(data, ["id", "text"])
    df.show()
    print("✅ Spark test job completed successfully!")
    spark.stop()
