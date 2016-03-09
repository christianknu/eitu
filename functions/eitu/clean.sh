#!/bin/bash
ls | grep -v -E "$(cat safe.txt)" | xargs rm -rf
rm safe.txt
