set -eu

ROOT_DIR=$1
FILES_DIR=$2
SPARK_HOME=$3
JUPYTER_PORT=$4
BASH_PROFILE=$ROOT_DIR/.bashrc

# Copy and configure profile and example notebooks
cp -R $FILES_DIR/profile_default $ROOT_DIR/.ipython/
cp -R $FILES_DIR/notebooks/* $ROOT_DIR/notebooks/
sed -i '6s@.*@c.NotebookApp.port = '$JUPYTER_PORT'@' $ROOT_DIR/.ipython/profile_default/ipython_notebook_config.py

# Copy & configure kernels 
cp -R $FILES_DIR/kernels $ROOT_DIR/.ipython/
# Set params for Scala kernel
sed -i '5s@.*@"'$SPARK_HOME'bin/spark-submit",@' $ROOT_DIR/.ipython/kernels/scala/kernel.json
sed -i '8s@.*@"'$ROOT_DIR'/.ipython/kernels/scala/ispark-core-assembly-0.2.0-SNAPSHOT.jar",@' $ROOT_DIR/.ipython/kernels/scala/kernel.json

# Set up bashrc for ipython user
echo "export HADOOP_HOME=/usr/hdp/current/hadoop-client" > $BASH_PROFILE
echo "export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk.x86_64"  >> $BASH_PROFILE
echo "export YARN_CONF_DIR=/etc/hadoop/conf" >> $BASH_PROFILE
echo "export HADOOP_CONF_DIR=/etc/hadoop/conf" >> $BASH_PROFILE
echo "export PATH=$PATH:/usr/local/bin" >> $BASH_PROFILE
echo "export SPARK_HOME=$SPARK_HOME" >> $BASH_PROFILE
echo 'export PYSPARK_PYTHON="/usr/local/bin/python2.7"' >>  $BASH_PROFILE
echo "export IPYTHON=1" >> $BASH_PROFILE
echo "export IPYTHON_OPTS=\"notebook --profile=default --ipython-dir $ROOT_DIR/.ipython --notebook-dir $ROOT_DIR/notebooks\"" >> $BASH_PROFILE
