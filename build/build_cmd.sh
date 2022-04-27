#!/bin/sh

cmake -DCMAKE_INSTALL_PREFIX=/usr .. /usr && make && sudo make install && sudo ldconfig
