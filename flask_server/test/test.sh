filename=$(date +"%k-%M-%S")
echo $filename
# ab -n 2 -c 2 -T "multipart/form-data; boundary=1234567890" -p turtle.txt http://localhost:5555/run
# 空行
nvidia-smi >> $filename.log
echo >> $filename.log
ab -n 400 -c 40 -T "application/json" -p testdata.json http://localhost:5005/getBase64Res >> $filename.log
echo >> $filename.log
nvidia-smi >> $filename.log