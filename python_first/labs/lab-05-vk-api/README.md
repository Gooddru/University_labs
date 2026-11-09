# **Лабораторная работа №5. Работа с API ВКонтакте**

Эта работа посвящена взаимодействию с [API ВКонтакте](https://vk.com/dev/manuals).

**Замечание**: Если вы не знакомы с термином "API", то рекомендую прочитать статью: [What is an API? In English, please.](https://medium.freecodecamp.org/what-is-an-api-in-english-please-b880a3214a82)

Чтобы начать работать с API от вас требуется зарегистрировать новое приложение. Для этого зайдите на форму создания нового Standalone приложения [https://vk.com/editapp?act=create](https://vk.com/editapp?act=create) и следуйте инструкциям. Вашему приложению будет назначен идентификатор, который потребуется для выполнения работы.

Запросы к API ВКонтакте имеют следующий формат ([из документации](https://vk.com/dev/api_requests)):

[https://api.vk.com/method/METHOD\_NAME?PARAMETERS\&access\_token=ACCESS\_TOKEN\&v=V](https://api.vk.com/method/METHOD_NAME?PARAMETERS&access_token=ACCESS_TOKEN&v=V)

где:

* METHOD\_NAME \- это название метода API, к которому Вы хотите обратиться.  
* PARAMETERS \- входные параметры соответствующего метода API, последовательность пар name=value, объединенных амперсандом &.  
* ACCESSS\_TOKEN \- ключ доступа.  
* V \- используемая версия API (в настоящий момент 5.53).

Например, чтобы получить список друзей, с указанием их пола, нужно выполнить следующий запрос:

[https://api.vk.com/method/friends.get?fields=sex\&access\_token=0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5bc866455623bd560732ab\&v=5.53](https://api.vk.com/method/friends.get?fields=sex&access_token=0394a2ede332c9a13eb82e9b24631604c31df978b4e2f0fbd2c549944f9d79a5bc866455623bd560732ab&v=5.53)

**Внимание:** Токен доступа ненастоящий, поэтому этот запрос работать не будет.

Чтобы получить токен доступа вы можете воспользоваться написанным для вас скриптом access\_token.py следующим образом:

$ python access\_token.py YOUR\_CLIENT\_ID \-s friends,messages

где вместо YOUR\_CLIENT\_ID необходимо подставить идентификатор вашего приложения.

После выполнения команды откроется новая вкладка браузера, из адресной строки которого вам необходимо скопировать токен доступа.


**Внимание:** На этом этапе вы можете повторить ранее представленный пример запроса, чтобы убедиться, что вы делаете все верно.

Далее приведено содержимое файла access\_token.py:

import webbrowser  
import argparse

def get\_access\_token(client\_id, scope):  
    assert isinstance(client\_id, int), 'clinet\_id must be positive integer'  
    assert isinstance(scope, str), 'scope must be string'  
    assert client\_id \> 0, 'clinet\_id must be positive integer'  
    url \= """\\  
    [https://oauth.vk.com/authorize?client\_id={client\_id}&\\](https://oauth.vk.com/authorize?client_id={client_id}&\\)  
    redirect\_uri=[https://oauth.vk.com/blank.hmtl&\\](https://oauth.vk.com/blank.hmtl&/)  
    scope={scope}&\\  
    \&response\_type=token&\\  
    display=page\\  
    """.replace(" ", "").format(client\_id=client\_id, scope=scope)  
    webbrowser.open\_new\_tab(url)

if \_\_name\_\_ \== "\_\_main\_\_":  
    parser \= argparse.ArgumentParser()  
    parser.add\_argument("client\_id", help="Application Id", type=int)  
    parser.add\_argument("-s",  
                        dest="scope",  
                        help="Permissions bit mask",  
                        type=str,  
                        default="",  
                        required=False)  
    args \= parser.parse\_args()  
    get\_access\_token(args.client\_id, args.scope)

**Задание №1**. Требуется написать функцию прогнозирования возраста пользователя по возрасту его друзей.

def get\_friends(user\_id, fields):  
    """ Returns a list of user IDs or detailed information about a user's friends """  
    assert isinstance(user\_id, int), "user\_id must be positive integer"  
    assert isinstance(fields, str), "fields must be string"  
    assert user\_id \> 0, "user\_id must be positive integer"  
    \# PUT YOUR CODE HERE  
    pass

Для выполнения этого задания нужно получить список всех друзей для указанного пользователя, отфильтровать тех у кого возраст не указан или указаны только день и месяц рождения.

Для выполнения запросов к API мы будем использовать библиотеку [requests](http://docs.python-requests.org/en/master/):

$ pip install requests

Список пользователей можно получить с помощью метода [friends.get](https://vk.com/dev/friends.get). Ниже приведен пример обращения к этому методу для получения списка всех друзей указанного пользователя:

domain \= "[https://api.vk.com/method](https://api.vk.com/method)"  
access\_token \= \# PUT YOUR ACCESS TOKEN HERE  
user\_id \= \# PUT USER ID HERE

query\_params \= {  
    'domain' : domain,  
    'access\_token': access\_token,  
    'user\_id': user\_id,  
    'fields': 'sex'  
}

query \= "{domain}/friends.get?access\_token={access\_token}\&user\_id={user\_id}\&fields={fields}\&v=5.53".format(\*\*query\_params)  
response \= requests.get(query)

Функция requests.get выполняет [GET запрос](https://ru.wikipedia.org/wiki/HTTP#GET) и возвращает объект Response, который представляет собой ответ сервера на посланный нами запрос.

Объект Response имеет множество атрибутов:

\>\>\> response.\<tab\>  
response.apparent\_encoding      response.history                response.raise\_for\_status  
response.close                  response.is\_permanent\_redirect  response.raw  
response.connection             response.is\_redirect            response.reason  
response.content                response.iter\_content           response.request  
response.cookies                response.iter\_lines             response.status\_code  
response.elapsed                response.json                   response.text  
response.encoding               response.links                  response.url  
response.headers                response.ok

Нас будет интересовать только метод response.json, который возвращает [JSON](https://ru.wikipedia.org/wiki/JSON) объект:

\>\>\> response.json()  
{'response': {'count': 136,  
              'items': \[{'first\_name': 'Drake',  
                         'id': 1234567,  
                         'last\_name': 'Wayne',  
                         'online': 0,  
                         'sex': 1},  
                        {'first\_name': 'Gracie'  
                         'id': 7654321,  
                         'last\_name': 'Habbard',  
                         'online': 0,  
                         'sex': 0},  
                         ...  
\>\>\> response.json()\['response'\]\['count'\]  
136  
\>\>\> response.json()\['response'\]\['items'\]\[0\]\['first\_name'\]  
'Drake'

Поле count содержит число записей, а items список словарей с информацией по каждому пользователю.

Выполняя запросы мы не можем быть уверены, что не возникнет ошибок. Возможны различные ситуации, например:

* есть неполадки в сети;  
* удаленный сервер по какой-то причине не может обработать запрос;  
* мы слишком долго ждем ответ от сервера.

В таких случаях необходимо попробовать повторить запрос. При этом повторные запросы желательно посылать не через константные промежутки времени, а по алгоритму экспоненциальной задержки.

Описание алгоритма с примерами можно найти в статье [Exponential Backoff или как «не завалить сервер»](https://habrahabr.ru/post/227225/). Почитать про обработку исключений при работе с библиотекой requests можно [тут](https://khashtamov.com/ru/python-requests/).

Напишите функцию get(), которая будет выполнять GET-запрос к указанному адресу, а при необходимости повторять запрос указанное число раз по алгоритму экспоненциальной задержки:

def get(url, params={}, timeout=5, max\_retries=5, backoff\_factor=0.3):  
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос  
    :param params: параметры запроса  
    :param timeout: максимальное время ожидания ответа от сервера  
    :param max\_retries: максимальное число повторных запросов  
    :param backoff\_factor: коэффициент экспоненциального нарастания задержки  
    """  
    \# PUT YOUR CODE HERE  
    pass

\>\>\> get("[https://httpbin.org/get](https://httpbin.org/get)")  
\>\>\> \<Response \[200\]\>

\>\>\> get("[https://httpbin.org/delay/2](https://httpbin.org/delay/2)", timeout=1)  
ReadTimeout: HTTPSConnectionPool(host='httpbin.org', port=443): Read timed out. (read timeout=1)

\>\>\> get("[https://httpbin.org/status/500](https://httpbin.org/status/500)")  
HTTPError: 500 Server Error: INTERNAL SERVER ERROR for url: [https://httpbin.org/status/](https://httpbin.org/status/)500

\>\>\> get("[https://noname.com](https://noname.com/)", timeout=1)  
ConnectionError: HTTPSConnectionPool(host='[noname.com](http://noname.com/)', port=443): Max retries exceeded with url: /

На текущий момент вы должны заполнить тело функции get\_friends так, чтобы она возвращала список друзей для указанного пользователя. Аргумент fields представляет из себя строку, в которой через запятую указываются какие поля необходимо получить по каждому пользователю.

Теперь мы можем написать функцию age\_predict для "наивного" прогнозирования возраста пользователя с идентификатором user\_id (под "наивным" прогнозированием подразумевается вычисление среднего арифметического или медианы):

def age\_predict(user\_id):  
    """  
    \>\>\> age\_predict(???)  
    ???  
    """  
    assert isinstance(user\_id, int), "user\_id must be positive integer"  
    assert user\_id \> 0, "user\_id must be positive integer"  
    \# PUT YOUR CODE HERE  
    pass

**Замечание:** Так как дата рождения пользователя может быть не указана или указаны только день и месяц, то для обработки таких ситуаций вы можете использовать конструкцию try...except, где except будет содержать только pass.

**Задание №2:** Требуется написать функцию, которая бы выводила график частоты переписки с указанным пользователем.

Давайте начнем с того, что получим всю или часть переписки с указанным пользователем. Для этого вам потребуется реализовать метод API [messages.getHistory](https://vk.com/dev/messages.getHistory) по аналогии с тем, как вы реализовывали получение списка друзей пользователя:

def messages\_get\_history(user\_id, offset=0, count=20):  
    assert isinstance(user\_id, int), "user\_id must be positive integer"  
    assert user\_id \> 0, "user\_id must be positive integer"  
    assert isinstance(offset, int), "offset must be positive integer"  
    assert offset \>= 0, "user\_id must be positive integer"  
    assert count \>= 0, "user\_id must be positive integer"  
    \# PUT YOUR CODE HERE  
    pass

**Замечание:** В реализации функции messages\_get\_history нужно учитывать, что API ВКонтакте устанавливает ограничение на число запросов в одну секунду (на сегодняшний день это три запроса). Число сообщений, которое вы можете получить за одно запрос \- 200\.

Далее приведен пример использования функции messages\_get\_history:

\>\>\> user\_id \= \# PUT USER ID HERE  
\>\>\> history \= messages\_get\_history(user\_id)  
\>\>\> from pprint import pprint as pp  
\>\>\> message \= history\['response'\]\['items'\]\[0\]  
\>\>\> pp(message)  
{'body': 'Это текст сообщения.',  
 'date': 1474811631,  
 'from\_id': USER\_ID\_HERE,  
 'id': 168989,  
 'out': 0,  
 'read\_state': 1,  
 'user\_id': USER\_ID\_HERE}

Каждое сообщение содержит следующие поля:

* body \- текст сообщения;  
* date \- дата отправки сообщения в формате [unixtime](https://ru.wikipedia.org/wiki/UNIX-%D0%B2%D1%80%D0%B5%D0%BC%D1%8F);  
* from\_id \- идентификатор автора сообщения;  
* id \- идентификатор сообщения;  
* out \- тип сообщения (0 — полученное, 1 — отправленное, не возвращается для пересланных сообщений);  
* read\_state \- статус сообщения (0 — не прочитано, 1 — прочитано, не возвращается для пересланных сообщений);  
* user\_id \- идентификатор пользователя, в диалоге с которым находится сообщение.

Нас интересует поле date, которое представляет дату отправки сообщения в формате unixtime. Чтобы изменить формат даты представления можно воспользоваться функцией strftime из модуля datetime:

\>\>\> from datetime import datetime  
\>\>\> date \= datetime.fromtimestamp(message\['date'\]).strftime("%Y-%m-%d")  
'2016-09-25'

Формат представления указывается в виде [строки форматирования](https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior), например, %Y-%m-%d \- год, месяц и день, соответственно.

На данный момент вашей задачей является написать функцию count\_dates\_from\_messages, которая возвращает два списка: список дат и список частоты каждой даты, а принимает список сообщений:

def count\_dates\_from\_messages(messages):  
    \#PUT YOUR CODE HERE  
    pass

**Замечание:** При большом количестве сообщений вы их можете разбить по неделям или месяцам.

Далее мы воспользуемся сервисом [Plot.ly](https://plot.ly/), который предоставляет API для рисования графиков. Запрос содержит информацию о точках, которые нужно отобразить на графике. Вам нужно зарегистрироваться и получить ключ доступа (API KEY). Для более простого взаимодействия с Plot.ly мы воспользуемся готовым модулем (существуют решения и для других языков):

$ pip3 install plotly

Перед началом его использования нужно провести предварительную [настройку](https://plot.ly/python/getting-started/), указав ключ доступа и имя пользователя:

import plotly  
plotly.tools.set\_credentials\_file(username='YOUR\_USER\_NAME', api\_key='YOUR\_API\_KEY')

Ниже приведен пример построения графика, где переменная x содержит даты, а y \- количество сообщений в этот день:

import plotly.plotly as py  
import plotly.graph\_objs as go

from datetime import datetime  
x \= \[datetime(year=2016, month=09, day=23),  
     datetime(year=2016, month=09, day=24),  
     datetime(year=2016, month=09, day=25)\]

data \= \[go.Scatter(x=x,y=\[142, 50, 8\])\]  
py.iplot(data)

Созданный график вы можете найти в своем [профиле](https://plot.ly/organize/home):


**Задание №3**: Требуется написать функцию get\_network(), которая для указанного списка пользователей users\_ids строит граф и представляет его либо в виде матрицы смежности (as\_edgelist=False), либо в виде списка ребер (as\_edgelist=True). В полученном графе необходимо выделить сообщества и визуализировать результат.

def get\_network(users\_ids, as\_edgelist=True):  
    """ Building a friend graph for an arbitrary list of users """  
    \# PUT YOUR CODE HERE  
    pass

Поиск сообществ на графе (community detection) является хорошо изученной задачей, а ряд наиболее известных алгоритмов реализован в библиотеке igraph.

$ pip install python-igraph  
$ pip install numpy  
$ pip install cairocffi  
$ brew install cairo    \# Только для MacOS X. Для других ОС см. [https://www.cairographics.org/download/](https://www.cairographics.org/download/)

from igraph import Graph, plot  
import numpy as np

vertices \= \[i for i in range(7)\]  
edges \= \[  
    (0,2),(0,1),(0,3),  
    (1,0),(1,2),(1,3),  
    (2,0),(2,1),(2,3),(2,4),  
    (3,0),(3,1),(3,2),  
    (4,5),(4,6),  
    (5,4),(5,6),  
    (6,4),(6,5)  
\]

g \= Graph(vertex\_attrs={"label":vertices},  
    edges=edges, directed=False)

N \= len(vertices)  
visual\_style \= {}  
visual\_style\["layout"\] \= g.layout\_fruchterman\_reingold(  
    maxiter=1000,  
    area=N\*\*3,  
    repulserad=N\*\*3)

plot(g, \*\*visual\_style)

g.simplify(multiple=True, loops=True)

communities \= g.community\_edge\_betweenness(directed=False)  
clusters \= communities.as\_clustering()  
print(clusters)

Clustering with 7 elements and 2 clusters  
\[0\] 0, 1, 2, 3  
\[1\] 4, 5, 6

pal \= igraph.drawing.colors.ClusterColoringPalette(len(clusters))  
g.vs\['color'\] \= pal.get\_many(clusters.membership)
