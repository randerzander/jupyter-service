set -eu

FILES_DIR=$1

# Abort if python2.7 already installed
if [ -e /usr/local/bin/python2.7 ]; then
  echo "Python2.7 already installed. Exiting."
  exit 0
fi

export PATH=$PATH:/usr/local/bin

tar -xzvf $FILES_DIR/Python-2.7.9.tgz
echo Installing Python-2.7.9..
cd Python-2.7.9
make altinstall
python2.7 $FILES_DIR/ez_setup.py
easy_install pip
cd /usr/local/lib/python2.7
rm -rf site-packages
# extract preconfigured site-packages
tar -xzvf $FILES_DIR/site-packages.tgz
cd site-packages
# scipy too big to package with site-packages
tar -xzvf $FILES_DIR/scipy.tgz
cd /usr/local/bin
cp $FILES_DIR/bin/* .
chmod +x *
