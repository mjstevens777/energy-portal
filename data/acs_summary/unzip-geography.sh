#!/bin/bash
cd acs_summary

mkdir -p data/geography
rm data/geography/*
unzip data/2014_ACS_Geography_Files.zip -d data/geography
rm data/geography/*.txt
