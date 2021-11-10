#!/bin/bash
echo "Общее количество запросов">output.txt;
cat access.log |wc -l >>output.txt;
echo "Общее количество запросов по типу">>output.txt;
awk '{print substr($6,2)}' access.log | sort | uniq -c | sort -rn >>output.txt;
echo "Топ 10 самых частых запросов">>output.txt;
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -n 10 >>output.txt;
echo "Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой">>output.txt;
awk '(substr($9,1) ~ /4/)' access.log|awk '{print $7,$9,$10,$1}'| sort -k3rn | head -n 5 >>output.txt;
echo "Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой">>output.txt;
awk '(substr($9,1) ~ /5/)' access.log|awk '{print $1}'|sort| uniq -c | sort -rn | head -n 5 >>output.txt;