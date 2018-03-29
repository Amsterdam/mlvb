#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error
set -x

# Test module mdbtools
python mdb_to_csv.py /data/beheerassets/noord/vm_stadsdeel_noord.mdb /data

