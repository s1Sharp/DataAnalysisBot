# DataAnalysisBot

Installation
Clone the repository from GitHub, then create a virtual environment, and install all the dependencies.

============================================================================================
git clone https://github.com/s1Sharp/DataAnalysisBot.git
python3 -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
===========================================================================================
after those steps add value of your token after those steps 
add value of your token to environment variable with name <token>
===========================================================================================Main menu of bot

*Команды для студентов:
1)/reg - Начать регистрацию пользователя
2)/jointhecourse - поступить на курс
3)/infoaboutme - получить информацию о себе
4)/getmygrades получить оценки по предмету
5)/leavethecours - покинуть курс
6)/getmystats - получить среднюю оценку по курсу
*Команды для преподавателя:
1)/teacher - стать администратором курса
2)/liststudents - получить excel файл с списком студентов, для выставления оценок
3)/assigngrades - выставить оценки из файла пункта (2)
4)/getjurnal - получить журнал с оценками
5)/getcoursestats - получить среднюю оценку по курсу
6)getnumberofstudents - получить кол-во студентов
7)/gettop5 - получить топ 5 студентов по оценкам

