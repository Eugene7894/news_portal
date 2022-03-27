D8
# В settings.py добавлены настройки CACHES , используя файл.сист FileBasedCache
# В news.urls добавлено кеширование представления cache_page(60*10)(PostsList.as_view()),
cache_page(60*5)(CatPostsList.as_view())
# Закеширована панель наваигации в default.html
# Добавлено кеширование для статей в news.views.PostDetails. Пока статья не изменилась, она должна сохраняться в кэше.
Переопределен метод save в news.models.Post, чтобы при изменении объекта, тот удалялся из кеша.

D7
# Установлены(pip install) celery, redis, -U "celery[redis]".
# Создан NewsPaper.celery , где произведена базовая настройка Celery + код расписания для задачи ежен. дайджеста.
# В NewsPaper.settings внесены настройки(5 констант для настройки Celery+Redis).
# Добавлены две задачи в news.tasks(письмо с новой статьей и еженедельный дайджест),
 таска send_sub_mail_after_post вызывается из news.signals при срабатывании сигнала.
# Для Windows Celery не поддерживатеся, использовались обходные пути:
-установлен пакет eventlet;
-запуск Celery командой "celery -A NewsPaper worker -l info -P eventlet";
-отдельный(в новом окне терминала) запуск beat для задачи по расписанию командой "celery -A NewsPaper beat".
Всего было запущено 3 терминала для работы(runsrver, запуск Celery beat, запуск Celery воркера).
См https://stackoverflow.com/questions/62524908/task-receive-but-doesnt-excute ,
https://www.distributedpython.com/2018/10/26/celery-execution-pool/ .
Можно было использовать gevent https://stackoverflow.com/questions/62524908/task-receive-but-doesnt-excute .


D11
# Добвалены дампы бд:
py manage.py dumpdata --format=json > dump_db.json и
py manage.py dumpdata --format=xml > dump_db.xml
# Добавлена управляющая команда(для manage.py), которая принимает в качестве аругмента название категории и удаляет
связанные с ней новости.
# В news/admin добавлены классы для кастомизированного отображения моделей в админ-панели, а также добавлены два
варианта фильтрации объектов сущностей; в news/models добавлены методы в классы моделей, которые позволяют отображать
поля со связью м2м в админ-панели в таблице сущности(эти методы добавлены в news/admin в кортежи list_display
вместо полей с м2м). 
