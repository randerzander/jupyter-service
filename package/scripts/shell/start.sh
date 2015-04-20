#!/bin/bash
set -eu

START_CMD=$1
LOG=$2
PIDFILE=$3

$START_CMD >> $LOG 2>&1 &
echo $! > $PIDFILE
