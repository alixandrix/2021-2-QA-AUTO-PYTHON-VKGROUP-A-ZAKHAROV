1) ACTIVE and TIME = 0, NULL when auth(надо логин и логаут)
2) max 2 active users
3) username like "_____smth" on site shows like "smth"
4) при переходе к маленькому окну едет верстка
5) centOS != Fedora
6) 2 email одинаковых = 500 "POST /reg HTTP/1.0" 500 
7) "GET /static/scripts/findMeError.js HTTP/1.1" 404 -
8) При логине, затем разлогине и добавления пробелов после логина логинется и выводится
ошибка о неверной длине логина.
9) Игра при 404 ответе всего лишь гифка!))))
10) без LOGOUT активность не сбрасывается(на сайте в ручную)
11) при logout api активность не сбрасывается
12) 500 при длинном пароле
13) при добавлении в конец пароле пробелов, идет регистрация даже если длина больше допустимого, 
но при добавлении пробелов в логин и почту регистрация не успешна
14) auth + logout, time is NULL
15) пробелы по середине пароля
16) 