# Melon
**Melon** – это модульный парсер манги и новелл, способный записывать всю информацию о тайтлах в JSON, записывать её, запрашивать обновления и собирать контент в удобный для ознакомления формат.

Проект приветствует добавление парсеров сторонними разработчиками. Для создана и поддерживается в актуальном состоянии подробная документация:
* [Поддерживаемые ресурсы](Docs/PARSERS.md)
* [Разработка парсера](Docs/DEVELOPMENT.md)
* [Настройка логов](Docs/LOGGER.md)
* [Форматы описательных файлов](Docs/Examples)

## Порядок установки и использования
1. Скачать и распаковать последний релиз.
2. Убедиться в доступности на вашем устройстве Python версии не старше **3.10**.
3. Открыть каталог со скриптом в терминале: можно воспользоваться командой `cd` или встроенными возможностями файлового менеджера.
4. Создать виртуальное окружение Python.
```
python -m venv .venv
```
5. Активировать вирутальное окружение. 
```
# Для Windows.
.venv\Scripts\activate.bat

# Для Linux или MacOS.
source .venv/bin/activate
```
6. Установить зависимости.
```
pip install -r requirements.txt
```
7. Произвести настройку путём редактирования файла _Settings.json_.
8. В вирутальном окружении указать для выполнения интерпретатором файл `main.py`, передать ему необходимые параметры и запустить.

# Консольные команды
___
```
list
```
Выводит список установленных парсеров, их целевые ресурсы, а также версии.
___
```
parse [TARGET*] [FLAGS] [KEYS]
```
Проводит парсинг тайтла с указанным алиасом и скачивает его обложки. В случае, если описательный файл уже существует, дополнит его новыми данными. 

**Описание позиций:**
* **TARGET** – задаёт цель для парсинга. Обязательная позиция.
	* Аргумент – алиас тайтла для парсинга.
	* Флаги:
		* _**-collection**_ – указывает, что список тайтлов для парсинга необходимо взять из файла _Collection.txt_;
		* _**-local**_ – указывает для парсинга все описательные файлы в директории хранения.
		
**Список специфических флагов:**
* _**-f**_ – включает перезапись уже загруженных обложек и существующих JSON файлов.

**Список специфических ключей:**
* _**--from**_ – указывает алиас тайтла, с момента обнаружения которого в коллекции тайтлов необходимо начать парсинг.
___
```
repair [FILENAME*] [TARGET*]
```
Заново получает сведения о содержимом конкретной главы и заносит их в уже существующий описательный файл.

**Описание позиций:**
* **FILENAME** – имя описательного файла. Обязательная позиция.
	* Аргумент – имя файла в директории хранения. Можно указывать как с расширением, так и без него.
* **TARGET** – цель для получения новых данных. Обязательная позиция.
	* Ключи:
		* _**--chapter**_ – указывает ID главы.

_Copyright © DUB1401. 2022-2024._
