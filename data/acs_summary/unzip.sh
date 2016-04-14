#!/bin/bash
cd acs_summary

mkdir -p data/seq
ls data/zip|grep "\.zip$"|sed "s/\.zip//"|xargs -I{} -n 1 unzip data/zip/{}.zip -d data/seq
