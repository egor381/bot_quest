**Тайны леса**

**«Тайны леса»** — это увлекательная игра, которую можно запустить прямо в Telegram, нажимая на кнопки, ты решаешь судьбу героя. Это отличный 
способ провести время и насладиться захватывающим геймплеем. В этой игре вам предстоит путешествовать по загадочному 
лесу, разгадывать его тайны.

**Особенности игры**

Красочное оформление: игра выполнена в ярких и сочных тонах, что делает её визуально привлекательной и интересной.
Простое управление.
«Тайны леса» — это отличный способ провести время, развить свою реакцию и логическое мышление.
*«/start»* и начните своё приключение в загадочном лесу!

**Описание проекта**

Игра реализована в виде Telegram-бота, написанного на языке Python.

_Основные файлы проекта:_  
_main.py_ - в нем находится всё взаимодействие с пользователем.  
_quests.py_ - в этом файле реализовано управление интерактивными вопросами и ответами, сохранение и загрузка состояния игры и обработчик ответов пользователя.

_Хранение данных:_  
Данные игры хранятся в двух json файлах и папке media.
_storage.json_ - хранение состояния прохождения игры пользователем.
_quest.json_ - хранится описание всех уровней игры, объяснения на все случаи проигрыша и сообщение, которое выводится при начале прохождения квеста.
_media_ - папка содержащая все файлы с изображениями, иллюстрации местонахождения персонажа.

_Сценарий игры:_  
Сценарий игры построен на основе схемы, представленной ниже.
![Схема уровней игры](схема_тайного_леса.png)
