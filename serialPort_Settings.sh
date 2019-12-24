#!/bin/bash
sudo echo KERNEL=="ttyUSB[0-9]*", MODE="0666" >> /etc/udev/rules.d/70-ttyusb.rules
sudo echo KERNEL=="ttyS[0-30]*", MODE="0666" >> /etc/udev/rules.d/70-ttyusb.rules
sudo chmod 666 /dev/ttyS*
sudo chmod 666 /dev/ttyUSB*


