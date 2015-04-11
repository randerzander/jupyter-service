set -eu

ROOT_DIR=$1
FILES_DIR=$2
BASH_PROFILE=$ROOT_DIR/.bashrc

# Abort if ipynb already installed
if [ -d $ROOT_DIR/.ipython/profile_default ]; then
  echo "IPython Notebook already installed. Exiting."
  exit 0
fi

export SPARK_HOME=/usr/hdp/current/spark-client/
cp -R $FILES_DIR/profile_default $ROOT_DIR/.ipython/
cp -R $FILES_DIR/notebooks/* $ROOT_DIR/notebooks/
# Copy & configure kernels 
cp -R $FILES_DIR/kernels $ROOT_DIR/.ipython/
sed -i.bak 's@SPARK_HOME@'$SPARK_HOME'@g' $ROOT_DIR/.ipython/kernels/scala/kernel.json
sed -i.bak 's@ROOT_DIR@'$ROOT_DIR'@g' $ROOT_DIR/.ipython/kernels/scala/kernel.json

# Set up bashrc for ipython user
echo "export HADOOP_HOME=/usr/hdp/current/hadoop-client" >> $BASH_PROFILE
echo "export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk.x86_64"  >> $BASH_PROFILE
echo "export YARN_CONF_DIR=/etc/hadoop/conf" >> $BASH_PROFILE
echo "export HADOOP_CONF_DIR=/etc/hadoop/conf" >> $BASH_PROFILE
echo "export PATH=$PATH:/usr/local/bin" >> $BASH_PROFILE
echo "export SPARK_HOME=/usr/hdp/current/spark-client" >> $BASH_PROFILE
echo 'export PYSPARK_PYTHON="/usr/local/bin/python2.7"' >>  $BASH_PROFILE
echo "export IPYTHON=1" >> $BASH_PROFILE
echo "export IPYTHON_OPTS=\"notebook --profile=default --ipython-dir $ROOT_DIR/.ipython --notebook-dir $ROOT_DIR/notebooks\"" >> $BASH_PROFILE
