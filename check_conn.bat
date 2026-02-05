@echo off
echo Testing Ping... > conn_test.txt
ping -n 4 141.147.83.137 >> conn_test.txt
echo. >> conn_test.txt
echo Testing SSH... >> conn_test.txt
ssh -i oracle/oracle_key.key -o ConnectTimeout=5 ubuntu@141.147.83.137 echo SSH_OK >> conn_test.txt 2>&1
