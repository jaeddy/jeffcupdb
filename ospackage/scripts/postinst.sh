#!/bin/bash

echo "Reloading daemon"
systemctl daemon-reload
echo "Restarting jeffcupdb.service"
systemctl restart jeffcupdb.service
echo "Restarting jeffcupdb-update.timer"
systemctl restart jeffcupdb-update.timer