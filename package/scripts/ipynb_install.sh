set -eu

ROOT_DIR=$1
FILES_DIR=$2
BASH_PROFILE=$ROOT_DIR/.bashrc

# Abort if ipynb already installed
if [ -d $ROOT_DIR/.ipython/profile_default ]; then
  echo "IPython Notebook already installed. Exiting."
  exit 0
fi

echo "export HADOOP_HOME=/usr/hdp/current/hadoop-client" >> $BASH_PROFILE
echo "export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk.x86_64"  >> $BASH_PROFILE
echo "export YARN_CONF_DIR=/etc/hadoop/conf" >> $BASH_PROFILE
echo "export HADOOP_CONF_DIR=/etc/hadoop/conf" >> $BASH_PROFILE
echo "export PATH=$PATH:/usr/local/bin" >> $BASH_PROFILE

export SPARK_HOME=$ROOT_DIR/spark
cp -R $FILES_DIR/profile_default $ROOT_DIR/.ipython/
# Copy & configure kernels 
cp -R $FILES_DIR/kernels $ROOT_DIR/.ipython/
sed -i.bak 's@SPARK_HOME@'$SPARK_HOME'@g' $ROOT_DIR/.ipython/kernels/scala/kernel.json
sed -i.bak 's@ROOT_DIR@'$ROOT_DIR'@g' $ROOT_DIR/.ipython/kernels/scala/kernel.json
#sed -i.bak 's@SPARK_HOME@'$SPARK_HOME'@g' $ROOT_DIR/.ipython/kernels/pyspark/kernel.json
cp -R $FILES_DIR/notebooks/* $ROOT_DIR/notebooks/

echo Downloading Spark with REPL API enabled..
#cp -R $FILES_DIR/spark $ROOT_DIR/
wget https://dl.dropboxusercontent.com/u/114020/spark-1.2.zip -O $ROOT_DIR/spark.zip
unzip $ROOT_DIR/spark.zip -d $ROOT_DIR/
mv $ROOT_DIR/spark-1.2 $ROOT_DIR/spark
chmod +x $ROOT_DIR/spark/bin/*
HDP_VERSION=$(hdp-select status hadoop-client | sed 's/hadoop-client - \(.*\)/\1/')
echo "spark.driver.extraJavaOptions -Dhdp.version=$HDP_VERSION" >> $ROOT_DIR/spark/conf/spark-defaults.conf
echo "spark.yarn.am.extraJavaOptions -Dhdp.version=$HDP_VERSION" >> $ROOT_DIR/spark/conf/spark-defaults.conf

echo "export SPARK_HOME=$SPARK_HOME" >> $BASH_PROFILE
echo 'export PYSPARK_SUBMIT_ARGS="--master yarn-client"' >> $BASH_PROFILE
echo 'export PYSPARK_PYTHON="python2.7"' >>  $BASH_PROFILE
echo "export PYTHONPATH=$SPARK_HOME/python/:$SPARK_HOME/python/lib/py4j-*.zip:/usr/local/bin/python2.7" >> $BASH_PROFILE
echo "export IPYTHON=1" >> $BASH_PROFILE
echo "export IPYTHON_OPTS=\"notebook --profile=default --ipython-dir $ROOT_DIR/.ipython --notebook-dir $ROOT_DIR/notebooks\"" >> $BASH_PROFILE
