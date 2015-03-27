set -eu

ROOT_DIR=$1
FILES_DIR=$2
BASH_PROFILE=$ROOT_DIR/.bashrc

# Abort if ipynb already installed
if [ -d $ROOT_DIR/profiles ]; then
  echo "IPython Notebook already installed. Exiting."
  exit 0
fi

export HDP_VER=`ls /usr/hdp/ | grep 2`
if [ -e /usr/hdp/$HDP_VER/hadoop/bin/hdfs ]
then
	export HADOOP_HOME=/usr/hdp/$HDP_VER/hadoop
	export HADOOP_VERSION=2.6.0.$HDP_VER
	export HDP_VERSION=2.2
	export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk.x86_64
else
	export HADOOP_HOME=/usr/lib/hadoop
	export JDK_VER=`ls /usr/jdk64/`
	export JAVA_HOME=/usr/jdk64/$JDK_VER	
	export HDP_VERSION=2.1
fi
export YARN_CONF_DIR=/etc/hadoop/conf
export HADOOP_CONF_DIR=/etc/hadoop/conf

echo "export HADOOP_HOME=$HADOOP_HOME" >> $BASH_PROFILE
echo "export HADOOP_VERSION=$HADOOP_VERSION" >> $BASH_PROFILE
echo "export JAVA_HOME=$JAVA_HOME"  >> $BASH_PROFILE
echo "export YARN_CONF_DIR=/etc/hadoop/conf" >> $BASH_PROFILE
echo "export HADOOP_CONF_DIR=/etc/hadoop/conf" >> $BASH_PROFILE
echo "export PATH=$PATH:/usr/local/bin" >> $BASH_PROFILE

cp -R $FILES_DIR/profiles $ROOT_DIR/
cp -R $FILES_DIR/WordCount.ipynb $ROOT_DIR/notebooks/

echo Downloading Spark with REPL API enabled..
#cp -R $FILES_DIR/spark $ROOT_DIR/
wget https://dl.dropboxusercontent.com/u/114020/spark-1.2.zip -O $ROOT_DIR/spark.zip
unzip $ROOT_DIR/spark.zip -d $ROOT_DIR/
mv $ROOT_DIR/spark-1.2 $ROOT_DIR/spark

chmod +x $ROOT_DIR/spark/bin/*
echo "spark.driver.extraJavaOptions -Dhdp.version=2.2.0.0-2041" >> $ROOT_DIR/spark/conf/spark-defaults.conf
echo "spark.yarn.am.extraJavaOptions -Dhdp.version=2.2.0.0-2041" >> $ROOT_DIR/spark/conf/spark-defaults.conf

export SPARK_HOME=$ROOT_DIR/spark
echo "export SPARK_HOME=$SPARK_HOME" >> $BASH_PROFILE
echo 'export PYSPARK_SUBMIT_ARGS="--master yarn-client"' >> $BASH_PROFILE
echo 'export PYSPARK_PYTHON="python2.7"' >>  $BASH_PROFILE
echo "export PYTHONPATH=$SPARK_HOME/python/:$SPARK_HOME/python/lib/py4j-*.zip:/usr/local/bin/python2.7" >> $BASH_PROFILE
echo "export IPYTHON=1" >> $BASH_PROFILE
echo "export IPYTHON_OPTS=\"notebook --profile=default --ipython-dir $ROOT_DIR/profiles --notebook-dir=$ROOT_DIR/notebooks\"" >> $BASH_PROFILE

exit 0
