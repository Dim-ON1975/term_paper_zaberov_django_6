# Курсовая работа № 6
## «Разработка сервиса рассылки писем. Блог»
### Заберов Дмитрий, Python IND 27.0

## Технологии
Проект разработан на ЯП Python 3.11

## Использование
Реализован сервис управления рассылками, администрирования и получения статистики, разделены права доступа для различных пользователей и добавлен раздел блога для развития популярности сервиса в интернете.
## Разработка
### Требования
Для запуска проекта (разработка велась на базе ОС Windows 11) необходимо:
- установить сервиcа Redis на ПК (Windows 11): https://community.chocolatey.org/packages/redis-64/3.0.501
- установить необходимые зависимости (см. файл pyproject.toml)
- запустить сервер django (в отдельной консоли): python manage.py runserver
- запустить сервер redis (в отдельной консоли): redis-server
- запустить celery worker (в отдельной консоли): celery -A core worker -P eventlet -l info
- запустить celery (в отдельной консоли): celery -A core.celery beat -l info

Кроме того, следует учитывать, что настройки вынесены в файл .env, который не выкладывается в репозиторий, однако имеется файл .env.simple, позволяющий разработчику (пользователю приложения) определить перечень необходимых ключей и настроек для работы приложений.
## Особенности
### Проект содержит несколько приложений:
1.	account – приложение для регистрации и авторизации пользователей проекта.
2.	clients – приложение для внесения в проект клиентов и работы с ними (CRUD), которым можно делать рассылки писем.
3.	mailings – приложение для настройки рассылок писем, их создания, просмотра, редактирования и удаления (CRUD).
4.	logs – приложение для сбора и обработки логов рассылок, формирования отчёта о проведённых и запущенных рассылках.
5.	blog – приложение для ведения блога: создания, просмотра, редактирования и удаления постов (CRUD).
### Группы пользователей:
1.	manager – пользователь, который может просматривать любые рассылки, список пользователей сервиса, блокировать пользователей сервиса, отключать рассылки. Однако он не может редактировать рассылки (за исключением своих), не может управлять списком рассылок (однако может добавлять собственные рассылки), не может изменять рассылки и сообщения (за исключением своих рассылок).
2.	reg_user – пользователь, который может выполнять операции только со своими клиентами и рассылками (в т.ч. настройками и письмами).
3.	content_manager – может просматривать все посты блога, создавать, редактировать и удалять только свои посты.

Весь функционал по ограничению возможностей разных групп пользователей настроен в проекте (следует оставить поле is_staff (персонал) в состоянии False, чтобы исключить возможность пользователей вмешиваться в настройки административной панели). В качестве персонала рекомендуется регистрировать только суперпользователя (администратора), для остальных пользователей (впрочем, как и для администратора) все возможности предоставлены через их учётные записи на сайте. 

### Кеширование
1.	Блог – кеширование списка постов (blog/urls.py)
2.	Главная страница – кеширование списка постов (clients/home.html, clients/view.py, clients/services.py)


### Дополнительно
Исключительно в целях демонстрации работы в репозиторий выложены директории /media/ и /fixtures/. После проверки работы и успешной сдачи они будут удалены из GitHub. 

Команда создания фикстуры:
python -Xutf8 manage.py dumpdata <app> --indent=4 -o fixtures/<app>_data.json

Команда загрузки фикстуры в БД:
python manage.py loaddata fixtures/<app>_data.json

### Установка зависимостей
Зависимости, необходимые для работы и тестирования проекта указаны в pyproject.toml.

### P.S. 
Идея содержания сайта пришла в процессе размышлений над тем, кому и какие письма следует отправлять. Нашёл десяток известных писем, имеющих смысл и интересное содержание, а затем и тема сайта (в т.ч. содержание блога) «вылилось» из этой идеи.