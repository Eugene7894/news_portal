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



