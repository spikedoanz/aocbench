#!/bin/sh

find . | grep day | sort | xargs -I {} sh -c 'echo "Running: {}" && python {}'
