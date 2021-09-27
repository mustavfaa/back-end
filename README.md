Ekitaphana.kz - единая база учебных книг
===
> - Версия python = 3.6
> - Версия Django = 2.1.4 
> - Все настройки в settings.txt
> - Добавления или изменения settings.py пишите где файл settings.py - edit-settings.txt вместе с коментом
> - Добавил .gitignore
> - все изменения кроме settings.py  писать в edit.txt
> - Поменяйте в transmeta в папке init.py 
> - from django.utils.datastructures import SortedDict на from collections import OrderedDict as SortedDict
> - появление, исчезновение файла reload приводит к перезапуску проекта (touch reload rm reload)
> - Строка запуска: uwsgi --socket 127.0.0.1:9056 --ini project.ini --thunder-lock --harakiri-verbose --protocol=http
> - Добавить в setting.py


