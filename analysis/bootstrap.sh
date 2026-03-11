# Set up the necessary libs to install the dependencies
apt-get update 
apt-get install -qq -y wget lzip build-essential cmake gcc m4 pkg-config libcairo2-dev unzip git zlib1g

# Install GMP (GNU Multiple Precision Arithmetic Library)
wget --no-check-certificate https://gmplib.org/download/gmp/gmp-6.2.1.tar.lz -O gmp-6.2.1.tar.lz 
tar -xf gmp-6.2.1.tar.lz 
rm gmp-6.2.1.tar.lz 
cd gmp-6.2.1 
./configure 
make 
make check 
make install 
cd ..

# Install the PPMD compressor
wget http://archive.ubuntu.com/ubuntu/pool/universe/p/ppmd/ppmd_10.1-5_amd64.deb -O ppmd_10.1-5_amd64.deb
dpkg -i ppmd_10.1-5_amd64.deb
rm ppmd_10.1-5_amd64.deb

# Install DAMICORE
unzip damicore-python3-main.zip
# rm damicore-python3-main.zip
mv damicore-python3-main /tmp/damicore-python3
#cd /tmp/damicore-python3
# sed -i 's/infile.read(1000)/infile.readline()/' damicore/ncd_base.py && \
# python3 setup.py install && \
pip3 install /tmp/damicore-python3
#cd /opt/tricorder/analysis