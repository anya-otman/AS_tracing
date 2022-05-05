# Трассировка автономных систем + опрделение страны и провайдера
______
# Подготовка к запуску
В скрипте используется модуль Requests, поэтому перед запуском необходимо установить его через терминал:
```
pip install requests
```
# Запуск скрипта
Для запуска используйте команду:
```
python tracing.py 'имя домена или ip'
```
После выполнения в файле `out.txt` будет таблица с IP адресами, номерами автономных систем, странами и провайдерами
# Примеры запусков
## №1
```
python tracing.py yandex.ru
```
![Image alt](https://github.com/anya-otman/AS_tracing/blob/main/example1.png)
## №2
```
python tracing.py 173.196.20.34
```
![Image alt](https://github.com/anya-otman/AS_tracing/blob/main/example2.png)
## №3
```
python tracing.py abcde
```
![Image alt](https://github.com/anya-otman/AS_tracing/blob/main/example3.png)
