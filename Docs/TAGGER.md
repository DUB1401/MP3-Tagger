# Обработчик классификаторов
В Melon встроен специальный интерпритатор полускриптового языка, позволяющий создавать правила редактирования и распределения классификаторов контента. 

### Типы классификаторов
| **Тип**         | **Описание**                                                                                                                                                                                                            |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| _classificator_ | Общий тип и название для всех остальных типов. Указывается, когда изначальная принадлежность неизвестна.                                                                                                                |
| _genre_         | Показывает, к какой группе относится это произвдение в зависимости от тех или иных сюжетных и стилистических признаков.                                                                                                 |
| _franchise_     | Линейка продукции: литературные произведения, фильмы, телепередачи, компьютерные игры и прочее, связанная персонажами, антуражем, зачастую торговой маркой и состоящая из оригинального произведения и его производных. |
| _person_        | Указывает на наличие конкретного персонажа в данном произведении.                                                                                                                                                       |
| _tag_           | Маркер или ключевое слово, позволяющее читателям быстро определить наличие в книги тех или иных элементов.                                                                                                              |

Все правила описываются в простом текстовом файле _Configs/tagger.ini_. Расширение ***.ini** используется для частичной синтаксической подсветки и фактически не привязывает содержимое к способам разметки конфигурационных файлов.

Интерпретация происходит сверху вниз построчно, при этом выделаются следующие понятия:
1. **Правило** – строка, описывающая правило обработки классификатора. Всегда начинается с определения оного.
2. **Секция** – группа правил, находящихся между объявлением секции (заключается в квадратные скобки) и другим объявлением либо концом файла. Любая секция имеет приоритет над правилами вне секций, потому при срабатывании правила в секции остальные проверки прерываются.
3. **Директива** – определённый для секции или группы правил вне секций параметр, определяющий частично или полностью поведение операций. Всегда начинается с символа `@`.

### Пример синтаксиса
```INI
# Классификатор "Исекай" привести к нижнему регистру и определить как жанр.
* "Исекай" -low -g
# Жанр "кровососы" переименовать и определить как тег.
genre "кровососы" rename "вампиры" -t

# Секция правил для определённого источника.
[site]
# Директива: приводить все классификаторы к нижнему регистру.
@LOW
# Удалить персонажа.
person "Василий" -del
```

| **Директива** | **Описание**                                        |
|---------------|-----------------------------------------------------|
| DROP          | Сбрасывает все активные директивы.                  |
| FRANCHISES    | Определяет следующие классификаторы как франшизы.   |
| GENRES        | Определяет следующие классификаторы как жанры.      |
| IGNORE        | Игнорировать правила.                               |
| LOW           | Приводить классификаторы к нижнему регистру.        |
| PERSONS       | Определяет следующие классификаторы как персонажей. |
| TAGS          | Определяет следующие классификаторы как теги.       |
| UP            | Приводить классификаторы к верхнему регистру.       |

При обработке каждого классификатора создаётся операция, которая после всех процедур содержит следующие данные на выходе:
1. Название классификатора.
2. Тип классификатора.
3. Состояние: требуется ли удалить классификатор.
4. Состояние: было ли найдено правило для этого классификатора.

### Пример выходных данных
```JSON
{
	"name": "название жанра",
	"type": "genre",
	"delete": false,
	"rule": true
}
```

При отсутствии изменений выводятся оригинальные данные. Все поля обязательно присутствуют в каждой структуре операции.

Для получения дополнительных сведений об использовании обработчика классификаторов через CLI можно получить посредством команды `melon help tagger`.