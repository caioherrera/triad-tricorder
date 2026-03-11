#!/bin/bash

# INSTALLATION STEPS FOR TRICORDER/DAMICORE/DECISION TREE

  apt-get install -qq -y python-tk libjpeg-dev zlib1g-dev
  python3 -m pip install Pillow matplotlib scikit-learn psutil tk pandas prettytable ipython h5py cairocffi #igraph python-igraph
  mkdir /home/kevin
  touch /home/kevin/testtime.csv

# INSTALATION STEPS FOR NETWORK TELEMETRY

# apt install -qq -y git libqt5core5a libqt5network5 qt5-default qt5-qmake qtbase5-dev

# git clone https://gitlab.com/vmontes/networktelemetry.git

# cd networktelemetry

# git checkout 70d20c7e

# sed -i 's/__declspec(dllexport)/Q_DECL_EXPORT/g' src/dataprocessinglib/dataprocessor.h
# sed -i 's/__declspec(dllexport)/Q_DECL_EXPORT/g' src/dataprocessinglib/binprocessor.h
# sed -i 's/__declspec(dllexport)/Q_DECL_EXPORT/g' src/dataprocessinglib/csvprocessor.h
# sed -i 's;#include "common/pkt.h";#include "dataprocessinglib_global.h"\n#include "common/pkt.h";g' src/dataprocessinglib/dataprocessor.h
# sed -i 's;#include "common/pkt.h";#include "dataprocessinglib_global.h"\n#include "common/pkt.h";g' src/dataprocessinglib/binprocessor.h
# sed -i 's;#include "common/pkt.h";#include "dataprocessinglib_global.h"\n#include "common/pkt.h";g' src/dataprocessinglib/csvprocessor.h

# sed -i "s;1234;50035;g" src/client/pktsendercontrol.cpp
# sed -i "s;1234;50035;g" src/server/dataserver.cpp

# qmake linux/workloadgenerator.pro
# make clean
# make
# make clean

# qmake linux/client.pro
# make clean
# make
# make clean

# CompileLib () {
#    echo "Compiling $1"
#    qmake linux/dataprocessing.pro DEFINES+="$1"
#    make clean
#    make
#    make clean
#    rm libdataprocessing.so libdataprocessing.so.1 libdataprocessing.so.1.0
#    mv libdataprocessing.so.1.0.0 libdataprocessing$2.so.1.0.0
#    return 0
# }

# CompileLib FAULT_BINPKTPROCESSOR_PROCESS_CLEANUP BCLEAN
# CompileLib FAULT_CSVPKTPROCESSOR_PROCESS_INFINITE INFINITE
# CompileLib FAULT_DATAPROCESSOR_MONOLITHIC MONO
# CompileLib FAULT_BINPKTPROCESSOR_PROCESS_SLEEP SLEEP
# CompileLib FAULT_NETWORK_PKT_WINDOWSIZE_ACQNUM_SWAP SWAP
# CompileLib FAULT_PROCESSOR_BUSY_UNLOCK UNLOCK
# CompileLib FAULT_DATAPROCESSOR_RUN_NO_BREAK NOBREAK
# CompileLib NO_FAULT CONTROL
# CompileLib NO_FAULT

# ln -s $PWD/libdataprocessing.so.1.0.0 /usr/lib/x86_64-linux-gnu/libdataprocessing.so
# qmake linux/server.pro
# make clean
# make
# make clean

# cd ..
# mkdir -p bin/
# cp -r networktelemetry/windows/data/ defs
# cp networktelemetry/{server,client,workloadgenerator,libdataprocessing*} bin

# find defs/ -type f -exec sed -i 's;\\;\/;g' {} \;
# find defs/ -type f -exec sed -i 's;//;/;g' {} \;
# find defs/ -type f -exec sed -i "s;c:/datalab/network;$PWD/out;gi" {} \;