#!/bin/sh

find . | grep day | grep 2016 | sort | xargs -I {} sh -c 'echo "Running: {}" && python {}'
