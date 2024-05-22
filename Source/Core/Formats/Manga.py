from Source.Core.Objects import Objects

from dublib.Methods import ReadJSON, WriteJSON

import enum
import os

#==========================================================================================#
# >>>>> ОПРЕДЕЛЕНИЯ <<<<< #
#==========================================================================================#

FORMAT_NAME = "melon-manga"

#==========================================================================================#
# >>>>> ДОПОЛНИТЕЛЬНЫЕ СТРУКТУРЫ ДАННЫХ <<<<< #
#==========================================================================================#

class BaseStructs:
	"""Контейнер базовых структур описательных файлов."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА ТОЛЬКО ДЛЯ ЧТЕНИЯ <<<<< #
	#==========================================================================================#

	@property
	def manga(self) -> dict:
		"""Базовая структура описательного файла манги."""

		return self.__MANGA_STRUCT

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Контейнер базовых структур описательных файлов."""

		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Базовая структура описательного тайтла манги.
		self.__MANGA_STRUCT = {
			"format": FORMAT_NAME,
			"site": None,
			"id": None,
			"slug": None,

			"ru_name": None,
			"en_name": None,
			"another_names": [],
			"covers": [],

			"authors": [],
			"publication_year": None,
			"description": None,
			"age_limit": None,
			
			"genres": [],
			"tags": [],
			"franchises": [],
			
			"type": None,
			"status": None,
			"is_licensed": None,
			
			"branches": [],
			"content": {} 
		}

class Statuses(enum.Enum):
	"""Определения статусов манги."""

	announced = "announced"
	ongoing = "ongoing"
	completed = "completed"
	dropped = "dropped"

class Types(enum.Enum):
	"""Определения типов манги."""

	manga = "manga"
	manhwa = "manhwa"
	manhua = "manhua"
	oel = "oel"
	western_comic = "western_comic"
	ru_comic = "ru_comic"

#==========================================================================================#
# >>>>> ОСНОВНОЙ КЛАСС <<<<< #
#==========================================================================================#

class Manga:
	"""Объектное представление манги."""

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __GenerateBranchesInfo(self):
		"""Генерирует информацию о ветвях."""

		# Список описаний ветвей.
		Branches = dict()

		# Для каждой ветви.
		for BranchID in self.__Manga["content"].keys():
			# Если ветвь ещё не описана, создать для неё структуру.
			if BranchID not in Branches.keys(): Branches[BranchID] = {
				"id": int(BranchID),
				"chapters-count": len(self.__Manga["content"][BranchID])
			}

		# Запись данных.
		self.__Manga["branches"] = list(Branches.values())

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#
	
	def __init__(self):
		"""Объектное представление манги."""
		
		#---> Генерация динамических свойств.
		#==========================================================================================#
		# Структура описательного файла манги.
		self.__Manga = BaseStructs().manga

	def amend(self, amending_method: any, message: str):
		"""
		Дополняет содержимое подробной информацией.
			amending_method – указатель на метод из парсера для дополнения;
			message – сообщение для внутреннего обработчика.
		"""

		# Дополнение содержимого.
		self.__Manga["content"] = amending_method(self.__Manga["content"], message)

	def download_covers(self):
		"""
		Скачивает обложки
			output_dir – директория хранения.
		"""

		pass

	def merge(self, output_dir: str, filename: str, system_objects: Objects):
		"""
		Объединяет данные описательного файла и текущей структуры данных.
			output_dir – директория хранения;
			filename – имя файла;
			system_objects – коллекция системных объектов.
		"""

		# Если локальный файл существует.
		if os.path.exists(f"{output_dir}/{filename}.json"):
			# Чтение описательного файла.
			LocalManga = ReadJSON(f"{output_dir}/{filename}.json")
			# Локальные данные содержимого.
			LocalContent = dict()
			# Количество глав, для которых выполнено слияние.
			MergedChaptersCount = 0

			# Для каждой ветви.
			for BranchID in LocalManga["content"]:
				# Для каждого элемента записать информацию о содержимом.
				for Chapter in LocalManga["content"][BranchID]: LocalContent[Chapter["id"]] = Chapter["slides"]
				
			# Для каждой ветви.
			for BranchID in self.__Manga["content"]:
		
				# Для каждой главы.
				for ChapterIndex in range(len(self.__Manga["content"][BranchID])):
				
					# Если для главы с таким ID найдено локальное содержимое.
					if self.__Manga["content"][BranchID][ChapterIndex]["id"] in LocalContent.keys():
						# Запись информации о содержимом.
						self.__Manga["content"][BranchID][ChapterIndex]["slides"] = LocalContent[self.__Manga["content"][BranchID][ChapterIndex]["id"]]
						# Инкремент количества глав, для которых выполнено слияние.
						MergedChaptersCount += 1

			# Запись в лог информации: количество глав, для которых выполнено слияние.
			system_objects.logger.merged_chapters_count(MergedChaptersCount)

	def save(self, output_dir: str, filename: str):
		"""
		Сохраняет данные манги в описательный файл.
			output_dir – директория хранения;
			filename – имя файла.
		"""

		# Сохранение описательного файла.
		WriteJSON(f"{output_dir}/{filename}.json", self.__Manga)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ УСТАНОВКИ СВОЙСТВ <<<<< #
	#==========================================================================================#

	def set_site(self, site: str):
		"""
		Задаёт домен источника.
			site – домен сайта.
		"""

		self.__Manga["site"] = site

	def set_id(self, id: int):
		"""
		Задаёт целочисленный идентификатор манги.
			id – идентификатор.
		"""

		self.__Manga["id"] = id

	def set_slug(self, slug: str):
		"""
		Задаёт алиас манги.
			slug – алиас.
		"""

		self.__Manga["slug"] = slug

	def set_ru_name(self, ru_name: str | None):
		"""
		Задаёт главное название манги на русском.
			ru_name – название на русском.
		"""

		self.__Manga["ru_name"] = ru_name

	def set_en_name(self, en_name: str | None):
		"""
		Задаёт главное название манги на английском.
			en_name – название на английском.
		"""

		self.__Manga["en_name"] = en_name

	def set_another_names(self, another_names: list[str]):
		"""
		Задаёт список альтернативных названий на любых языках.
			another_names – список названий.
		"""

		self.__Manga["another_names"] = another_names

	def set_covers(self, covers: list[dict]):
		"""
		Задаёт список описаний обложек.
			covers – список названий.
		"""

		self.__Manga["covers"] = covers

	def set_authors(self, authors: list[str]):
		"""
		Задаёт список авторов.
			covers – список авторов.
		"""

		self.__Manga["authors"] = authors

	def set_publication_year(self, publication_year: int | None):
		"""
		Задаёт год публикации манги.
			publication_year – год.
		"""

		self.__Manga["publication_year"] = publication_year

	def set_description(self, description: str | None):
		"""
		Задаёт описание манги.
			description – описание.
		"""

		self.__Manga["description"] = description

	def set_age_limit(self, age_limit: int | None):
		"""
		Задаёт возрастной рейтинг.
			age_limit – возрастной рейтинг.
		"""

		self.__Manga["age_limit"] = age_limit

	def set_genres(self, genres: list[str]):
		"""
		Задаёт список жанров.
			genres – список жанров.
		"""

		self.__Manga["genres"] = genres

	def set_tags(self, tags: list[str]):
		"""
		Задаёт список тегов.
			tags – список тегов.
		"""

		self.__Manga["tags"] = tags

	def set_franchises(self, franchises: list[str]):
		"""
		Задаёт список франшиз.
			franchises – список франшиз.
		"""

		self.__Manga["franchises"] = franchises

	def set_type(self, type: Types | None):
		"""
		Задаёт типп манги.
			type – тип.
		"""

		# Если передан тип.
		if type:
			# Установка типа.
			self.__Manga["type"] = type.value

		else:
			# Обнуление типа.
			self.__Manga["type"] = None

	def set_status(self, status: Statuses | None):
		"""
		Задаёт статус манги.
			status – статус.
		"""

		# Если передан статус.
		if status:
			# Установка статуса.
			self.__Manga["status"] = status.value

		else:
			# Обнуление статуса.
			self.__Manga["status"] = None
		
	def set_is_licensed(self, is_licensed: bool | None):
		"""
		Задаёт статус лицензирования манги.
			is_licensed – статус лицензирования.
		"""

		self.__Manga["is_licensed"] = is_licensed

	def set_content(self, content: dict):
		"""
		Задаёт содержимое манги.
			content – словарь ветвей с содержимым.
		"""

		# Запись содержимого.
		self.__Manga["content"] = content
		# Вычисление данных ветвей.
		self.__GenerateBranchesInfo()