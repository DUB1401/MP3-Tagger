from Source.Core.SystemObjects import SystemObjects
from Source.Core.Formats import By

from dublib.Methods.Filesystem import ReadJSON

import os

class Collector:
	"""Менеджер коллекций."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def slugs(self) -> list[str]:
		"""Список алиасов в коллекции."""

		return self.__Collection

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __ReadCollection(self) -> list[str]:
		"""Читает коллекцию."""

		Collection = list()
		
		if os.path.exists(self.__Path) and not self.__SystemObjects.FORCE_MODE:
			
			with open(self.__Path, "r") as FileReader:
				Buffer = FileReader.read().split("\n")

				for Line in Buffer:
					Line = Line.strip()
					if Line: Collection.append(Line)

		elif self.__SystemObjects.FORCE_MODE:
			self.__SystemObjects.logger.info("Collection will be overwritten.")
			print("Collection will be overwritten.")

		return Collection

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, system_objects: SystemObjects, merge: bool = False):
		"""
		Менеджер коллекций.
			system_objects – коллекция системных объектов;\n
			merge – указывает, считывать ли коллекцию.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__SystemObjects = system_objects

		self.__Path = system_objects.temper.parser_temp + "/Collection.txt"
		self.__Collection = self.__ReadCollection() if merge else list()

	def append(self, slugs: str | list[str]):
		"""
		Добавляет в коллекцию список алиасов.
			slugs – алиас или список алиасов.
		"""

		if type(slugs) != list: slugs = [slugs]
		self.__Collection += slugs

	def get_local_identificators(self, identificator_type: By) -> list[int] | list[str]:
		"""
		Сканирует директорию и возвращает список идентификаторов тайтлов.
			identificator_type – тип идентификаторов в спике.
		"""
		
		ParserSettings = self.__SystemObjects.manager.parser_settings

		LocalTitles = [Entry.name for Entry in os.scandir(ParserSettings.common.titles_directory) if Entry.is_file() and Entry.name.endswith(".json")]
		Identificators = list()

		for Filename in LocalTitles:

			try:
				if identificator_type == By.Filename:
					Identificators.append(Filename[:-5])

				elif identificator_type in [By.ID, By.Slug]:
					Title = ReadJSON(f"{ParserSettings.common.titles_directory}/{Filename}") 
					Identificators.append(Title[identificator_type.value])

			except KeyError: pass

		return Identificators

	def save(self, sort: bool = False):
		"""
		Сохраняет коллекцию.
			sort – указывает, нужно ли сортировать алиасы в алфавитном порядке.
		"""

		self.__Collection = list(set(self.__Collection))
		if sort: self.__Collection = sorted(self.__Collection)

		with open(self.__Path, "w") as FileWriter:
			for Slug in self.__Collection: FileWriter.write(Slug + "\n")

	def from_local(self) -> int:
		"""Сканирует директорию тайтлов и сторит из неё коллекцию."""
		
		LocalTitles = self.get_local_identificators(By.Slug)
		TitlesCount = len(LocalTitles)
		self.__Collection += LocalTitles

		return TitlesCount