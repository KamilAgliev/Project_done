# -*- coding: utf-8 -*-
"""MyEng - Телеграм бот для узучения английского языка"""

import random
import sys

import requests
from requests import post, get, delete
from telegram import ReplyKeyboardMarkup

TOKEN_FOR_TELEGRAM_BOT = "1116820230:AAHm6C00UvlPDOk-NAnT1kPgftMPuzI-CG4"
sessionStorage = {}
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CommandHandler

WORDS_FOR_LEARNING = {
    'путешествия': {
        "inception": "Одной из причин, по которой человек решает выучить или "
                     "освежить в памяти подзабытый английский язык – это необходимость в нем во время путешествий."
                     "Как известно, английский язык давно является международным."
                     " Поэтому английский для путешествий необходим хотя бы в объеме нескольких ходовых фраз."
                     " А всем изучающим английский язык более серьезно,"
                     " в туристической поездке представляется великолепная возможность попрактиковаться."
                     "Если вы проводите отпуск за границей, в какую бы вы страну не планировали отправиться,"
                     " переговоры о бронировании жилья и билетов традиционно ведутся на английском языке,"
                     " английский для путешественников так же необходим в затруднительных ситуациях в аэропорту,"
                     " в гостинице, в кафе, в незнакомом городе и т.п."
                     " Поэтому основные фразы на английском для туристов, выученные перед путешествием,"
                     " помогут вам сделать вашу поездку более приятной и комфортной.",
        "themes": [
            {"title": "Английский для туристов в дороге",
             "youtube_urls": ["https://www.youtube.com/watch?v=pgjfHxFj2_I"],
             "words": [['the check-in desk ', 'стойка регистрации'],
                       ['self check-in point ', 'место для самостоятельной регистрации'],
                       ['passport control ', 'паспортный контроль'],
                       ['customs ', 'таможня'],
                       ['immigration enquiries ', 'иммиграционный контроль'],
                       ['arrivals, arrivals hall ', 'зона прилета'],
                       ['a ticket ', 'билет'],
                       ['a boarding pass ', 'посадочный талон'],
                       ['airline enquiries ', 'справочная служба аэропорта'],
                       ['lost and found ', 'бюро находок'],
                       ['baggage drop-off ', 'зона сдачи багажа'],
                       ['baggage claim, baggage reclaim ', 'зона выдачи багажа'],
                       ['an international flight ', 'международный рейс'],
                       ['a domestic flight ', 'внутренний рейс'],
                       ['transfer ', 'трансфер'],
                       ['departures, departures hall', 'зона вылета']],
             "exsamples": [],
             "description": "",
             },
            {"title": "Английский в гостинице",
             "youtube_urls": ["https://www.youtube.com/watch?v=sQlEvZIdTms"],
             "words": [['Hello, can I reserve a room, please? ', 'Здравствуйте, могу ли я забронировать номер?'],
                       ['Can I book a room? ', 'Могу ли я забронировать номер?'],
                       ['What types of rooms are available? ', 'Какие номера свободны?'],
                       ['I’m leaving in ', '5 days. Я уезжаю через 5 дней.'],
                       ['I would like to book a single room', 'Я бы хотел зарезервировать одноместный номер'],
                       ['What’s the price for a single room?', 'Какова стоимость одноместного номера?'],
                       ['I’d like to book a room overviewing the sea/lake. ',
                        'Я бы хотел забронировать номер с видом на море/озеро.'],
                       ['I’d like full board ', '/ half-board. Я бы хотел полный пансион / полупансион.'],
                       ['May I have a late check-out? ', 'Могу ли я попросить поздний выезд?'],
                       ['Do you have a car park? ', 'У вас есть парковка?'],
                       ['Does the hotel have a gym ',
                        '/ swimming pool? В отеле есть тренажерный зал / бассейн?'],
                       ['Do you have a special menu for children? ', 'У вас есть специальное меню для детей?'],
                       ['Does the hotel have any facilities for children? ',
                        'В отеле есть развлечения (услуги) для детей?'],
                       ['Do you allow pets? ', 'Разрешаете ли вы заселяться с домашними животными?'],
                       ['Does the hotel provide airport transfer? ',
                        'Отель обеспечивает трансфер из/до аэропорта?'],
                       ['How much is the service charge and tax? ', 'Сколько стоит обслуживание и налог?'],
                       ['Is there anything cheaper? ', 'Есть что-то подешевле?'],
                       ['What is the total cost? ', 'Какова итоговая сумма к оплате?'],
                       ['smoking allowed ', 'разрешено курить'],
                       ['a rental ', 'сумма арендной платы'],
                       ['a single room ', 'комната на одного человека'],
                       ['a double room ', 'комната на двоих с общей кроватью'],
                       ['a twin room ', 'комната на двоих с раздельными кроватями'],
                       ['a crib ', 'детская кроватка'],
                       ['free parking ', 'бесплатная парковка'],
                       ['amenities ', 'удобства'],
                       ['heating ', 'отопление'],
                       ['a fireplace ', 'камин'],
                       ['a kitchen ', 'кухня'],
                       ['a fridge ', 'холодильник'],
                       ['dishes ', 'посуда'],
                       ['cutlery ', 'столовые приборы'],
                       ['a stove ', 'плита'],
                       ['an oven ', 'духовка'],
                       ['a dishwasher ', 'посудомоечная машина'],
                       ['cable TV ', 'кабельное ТВ'],
                       ['an iron ', 'утюг'],
                       ['bed linen ', 'постельное белье'],
                       ['toiletries ', 'ванные принадлежности'],
                       ['towels ', 'полотенца'],
                       ['a garden ', 'сад'],
                       ['a pool ', 'бассейн'],
                       ['pets allowed ', 'можно останавливаться с животными'],
                       ['check-in time ', 'время заезда'],
                       ['check-out time ', 'время выезда']],
             "exsamples": [],
             "description": "Оказавшись в гостинице, вам необходимо подойти на стойку"
                            " регистрации (reception) и узнать о размещении (accommodation)."
                            " Если вы бронировали жилье, скажите: Hello! I have a reservation."
                            " My surname is Ivan Ivanov. — Здравствуйте! У меня есть бронь. Меня зовут Иван Иванов."
                            "Вот ещё фразы для этого случая",
             },
            {"title": "Исследуем город",
             "youtube_urls": ["https://www.youtube.com/watch?v=cp_5Z3RUnow",
                              "https://www.youtube.com/watch?v=J6gWridhh64"],
             "words": [
                 ['a cathedral ', 'собор'],
                 ['a square ', 'площадь'],
                 ['a mosque ', 'мечеть'],
                 ['a church ', 'церковь'],
                 ['a town hall ', 'ратуша'],
                 ['a castle ', 'замок'],
                 ['a palace ', 'дворец'],
                 ['a temple ', 'храм'],
                 ['a tower ', 'башня'],
                 ['a museum ', 'музей'],
                 ['a statue ', 'статуя'],
                 ['a monument ', 'памятник'],
                 ['a sculpture ', 'скульптура'],
                 ['a park ', 'парк'],
                 ['a fountain ', 'фонтан'],
                 ['an art gallery ', 'художественная галерея'],
                 ['a ballet ', 'балет'],
                 ['an opera ', 'опера'],
                 ['a theatre ', 'театр'],
                 ['a cinema ', 'кинотеатр'],
                 ['a circus ', 'цирк'],
                 ['a zoo ', 'зоопарк'],
                 ['a stadium ', 'стадион'],
                 ['a canyon ', 'каньон'],
                 ['a cave ', 'пещера'],
                 ['beautiful ', 'красивый'],
                 ['crowded ', 'переполненный'],
                 ['packed with tourist ', 'забит туристами'],
                 ['lovely ', 'милый'],
                 ['unique ', 'уникальный'],
                 ['spectacular ', 'захватывающий'],
                 ['picturesque ', 'красочный'],
                 ['remarkable ', 'выдающийся'],
                 ['impressive ', 'впечатляющий'],
                 ['charming ', 'очаровательный'],
             ],
             "exsamples": [['Could you tell me how to get to the National museum? ',
                            'Вы не могли бы сказать мне, как добраться до национального музея?'],
                           ['How can I get to the supermarket? ', 'Как мне добраться до супермаркета?'],
                           ['Where is the nearest bus/subway station? ', 'Где находится ближайший автовокзал/метро?'],
                           ['Is there an ATM ', '/ cash machine near here? Здесь поблизости есть банкомат?'],
                           ['Where is the nearest bus stop? ', 'Где находится ближайшая автобусная остановка?'],
                           ['How can I get to Hilton Hotel? ', 'Как я могу добраться до отеля Hilton?'],
                           ['Which bus/train goes to the Blue Mosque from here? ',
                            'Какой автобус/поезд идет до Голубой мечети отсюда?'],
                           ['What is the best way to get around London? ',
                            'Какой лучший способ перемещаться по Лондону?'],
                           ['Go straight ', '(on). Идите прямо.'],
                           ['Turn left. ', 'Поверните налево.'],
                           ['Turn left at the corner. ', 'На углу поверните налево.'],
                           ['Turn right. ', 'Сверните направо.'],
                           ['Turn right at the crossroads/intersection. ', 'На перекрестке поверните направо.'],
                           ['Cross the street. ', 'Перейдите дорогу.'],
                           ['Continue along Bank Street until you see the cinema. ',
                            'Продолжайте (идти) вдоль Bank Street, пока не увидите кинотеатр.'],
                           ['Then turn left. ', 'Затем поверните налево.'],
                           ['After that take Oxford Street. ', 'После этого идите по / держитесь Oxford Street.'],
                           ['When you get to the bridge, you’ll see the National museum. ',
                            'Когда вы доберетесь до моста, вы увидите Национальный музей.'],
                           ['At the corner of the street you will see the National museum. ',
                            'На углу улицы вы увидите Национальный музей.'],
                           ['It is next to... ', 'Это рядом с...'],
                           ['The cinema is next to the park. ', 'Кинотеатр находится рядом с парком.'],
                           ['It is far from here/near hear. ', 'Это далеко/близко отсюда.'],
                           ['The bank is between... ', 'Банк находится между...'],
                           ['The railway station is between the bank and the theatre. ',
                            'Железнодорожный вокзал находится между банком и театром.'],
                           ['It is across from/opposite... ', 'Это по другую сторону / напротив...'],
                           ['The shop you are looking for is across from/opposite the church. ',
                            'Магазин, который вы ищите, находится напротив церкви.']],
             "description": "",
             },
            {"title": "Английский для туристов в ресторане",
             "youtube_urls": ["https://www.youtube.com/watch?v=ZObNbpRhpGc"],
             "words": [
                 ['I’ve booked a table. ', 'Я бронировал столик.'],
                 ['Do you have any free tables? I need a table for two. ',
                  'У вас есть свободные столики? Мне нужен столик на двоих.'],
                 ['May I sit here? ', 'Я могу сесть здесь?'],
                 ['Can I get a table by the window? ', 'Можно мне столик у окна?'],
                 ['Could we get an extra chair? ', 'Можно нам еще один стул?'],
                 ['Can I have the menu, please? ', 'Можно мне меню, пожалуйста?'],
                 ['Where can I see a list of drinks? ', 'Где я могу найти список напитков?'],
                 ['What dish can you recommend? ', 'Какое блюдо вы могли бы посоветовать?'],
                 ['What do you recommend? ', 'Что вы порекомендуете?'],
                 ['We are ready to order. ', 'Мы готовы сделать заказ.'],
                 ['I am not ready yet. ', 'Я еще не готов.'],
                 ['I would like a cup of coffee. ', 'Я бы хотел чашечку кофе.'],
                 ['A glass of water, please. ', 'Стакан воды, пожалуйста.'],
                 ['I would like the set lunch. ', 'Я бы хотел комплексный обед.'],
                 ['Can I have a steak, please? ', 'Можно мне стейк, пожалуйста?'],
                 ['What are the side dishes? ', 'Какие есть гарниры?'],
                 ['What is this dish? ', 'Что это за блюдо?'],
                 ['', 'Если у вас есть особые пожелания, используйте следующие фразы:'],
                 ['I am allergic to nuts. Does this dish contain nuts? ',
                  'У меня аллергия на орехи. Это блюдо содержит орехи?'],
                 ['I am a vegetarian. Do you have any vegetarian food? ',
                  'Я вегетарианец. У вас есть вегетарианская еда?'],
                 ['Can I get this burger without onion? ', 'Можно мне этот бургер без лука?'],
                 ['Could I change my order? I would like a salad instead of meat. ',
                  'Я могу изменить заказ? Я бы хотел салат вместо мяса.'],
                 ['I am in a hurry. How long will I have to wait for the order? ',
                  'Я спешу. Сколько мне придется ждать заказ?'],
                 ['', 'Воспользуйтесь следующими фразами, чтобы расплатиться:'],
                 ['Can I have the bill/check, please? ', 'Могу ли я получить счет?'],
                 ['Could I pay by credit card/in cash? ', 'Можно заплатить картой/наличными?'],
                 ['Could you check the bill for me, please? It does not seem right. ',
                  'Не могли бы вы проверить мой счет, пожалуйста? Кажется, в нем ошибка.'],
                 ['Is service included? ', 'Обслуживание включено в счет?'],
                 ['I am paying for everybody. ', 'Я плачу за всех.'],
                 ['Can we pay separately? ', 'Можем мы заплатить раздельно?'],
                 ['Keep the change. ', 'Сдачи не надо.'],
             ],
             "exsamples": [],
             "description": "",
             },
            {"title": "Английский для туристов в магазине",
             "youtube_urls": ["https://www.youtube.com/watch?v=t4hHFNWjtk4",
                              'https://www.youtube.com/watch?v=LLpnmrbjnjI'],
             "words": [['Where is the nearest souvenir shop / shopping mall / market? ',
                        'Где находится ближайший сувенирный магазин / торговый центр / рынок?'],
                       ['Sorry, can you help me, please? ', 'Прошу прощения, вы можете мне помочь?'],
                       ['How much is it? ', 'How much is it?'],
                       ['How much does it cost? ', 'Сколько это стоит?'],
                       ['Do you have a special offer? ', 'У вас есть специальное предложение?'],
                       ['Are there any discounts? ', 'А скидки есть?'],
                       ['Okay, I’ll take it. ', 'Хорошо, я беру/покупаю.'],
                       ['Where can I pay for it? ', 'Где я могу рассчитаться за это?'],
                       ['Can you give me a receipt? ', 'Можете выдать мне чек?'],
                       ['Where is a shop assistant? ', 'Где продавец-консультант?'],
                       ['I don’t see a price tag. ', 'Я не вижу ценник.'],
                       ['Can I pay for it by card? ', 'Я могу расплатиться за это картой?'],
                       ['I am looking for a shirt/dress/T-shirt. ', 'Я ищу рубашку/платье/футболку.'],
                       ['Do you have this suit in white? ', 'Этот костюм есть в белом цвете?'],
                       ['I would like to try it on. ', 'Я бы хотел примерить это.'],
                       ['Excuse me, where is the fitting room/changing room? ',
                        'Извините, где находится примерочная?'],
                       ['Where can I try this coat on? ', 'Где я могу примерить это пальто?'],
                       ['Do you have this jacket in S/M/L size? ',
                        'У вас есть этот пиджак/куртка в размере S/M/L?'],
                       ['Can you give me a bigger/smaller size? ',
                        'Вы не могли бы дать мне размер побольше/поменьше?'],
                       ['I need to take this dress back to the shop. ',
                        'Мне нужно вернуть это платье в магазин.'],
                       ['I would like to get a refund. ', 'Я бы хотел получить возврат.'],
                       ['I would like to change it. I have bought the wrong size. ',
                        'Я бы хотел поменять это. Я купил неправильный размер.']],
             "exsamples": [],
             "description": "",
             }],
        'conclusion': "Знание английского — огромный плюс для любого путешественника."
                      "\nВы получаете сразу несколько весомых преимуществ:"
                      "\n1) Свободное общение без разговорников, словарей, приложений для гаджетов"
                      "\n2) Уважение местных жителей: люди, владеющие английским, вызывают у иностранцев уважение"
                      "\n3) Путешествие по собственному маршруту"
                      "\n4) Выгодные покупки"
                      "\n5) Новые знакомства",
    }, 'для работы за границей': {
        "inception": "Английский язык – это не только разговорная речь."
                     " Изучая язык, мы учим не только разговорную речь,"
                     " но и деловую лексику. Business English нужен каждому человеку,"
                     " чья работа требует командировок за границу. Да что там говорить!"
                     " Без хорошего делового английского трудно продвигаться по карьерной лестнице"
                     " и получить повышение. Сегодня мы рассмотрим деловой английский для начинающих."
                     " Приведем пример специальных слов и фраз,"
                     " которые понадобятся  делово общении с партнерами по бизнесу.",
        "themes": [
            {
                "title": "Основные термины бизнеса",
                "youtube_urls": ["https://www.youtube.com/watch?v=4qPM4RspC60",
                                 "https://www.youtube.com/watch?v=caVK3vtmR6E"],
                "words": [['Buyer',
                           'покупатель'],
                          ['Seller', 'продавец'],
                          ['Dealer', 'дилер'],
                          ['Retailer', 'розничный продавец'],
                          ['Supplier', 'поставщик'],
                          ['Wholesaler', 'оптовый продавец'],
                          ['Rival', 'соперник'], ],
                'exsamples': [["Наши покупатели настолько щедрые, что мы можем продавать наши товары без наценки.",
                               "Our buyers are so general that thanks to them we can sell our products without extra charge"],
                              [
                                  "Наши дилеры были действительно вежливыми во время нашей последней встречи. Странно. В предыдущий раз некоторые из них были грубыми.",
                                  "Our dealers were really polite during our last meeting. Strange. The previous time some of them were rude"],
                              [
                                  "Кто может заработать больше денег – розничные или оптовые продавцы? Интересный вопрос, но я думаю последние имеют больше.",
                                  "Who can make more money – retailers or wholesalers? It is interesting question, but I think the last ones have more"],
                              ["Наши поставщики с разных стран, но большинство из них с Испании и Америки.",
                               "Our suppliers are from different countries, but most of them are from Spain and America"],
                              [
                                  "Оптовые продавцы не могут поставиться на свои товары слишком высокую цену. Никто не купит товар. Более того, их цена должна быть порядком ниже цены, которую ставят их конкуренты. Если нет, они не будут иметь успеха.",
                                  "The wholesalers can’t put a very high price on their goods. No one will buy it. Moreover, their price are to be much lower their rival’s price. If no, they will have no success"],
                              ["Our rivals are no more competitive. So we can be calm",
                               "Наши соперники больше не конкурентоспособные. Что ж, мы можем быть спокойными."],
                              ],
                "description": "Бизнес английский совсем не такой сложный, как многим кажется."
                               " Да, есть узкопрофильная лексика, которая действительно тяжелая для восприятия."
                               " Но есть слова, которые выучить легко и просто."
                               " Приведем некоторые примеры часто используемых слов,"
                               " которые пригодятся не только на работе, но и в жизни.",
            },
            {
                "title": "Фразы на английском, которые касаются работы производства",
                "youtube_urls": [],
                "words": [['Consumption', 'потребление'],
                          ['To operate', 'работать, управлять'],
                          ['To launch', 'запускать'],
                          ['Raw materials', 'сырье'],
                          ['Warehouse', 'склад'], ['To produce, to manufacture', 'производить'], ],
                "exsamples": [['To produce, to manufacture',
                               'производить. It is believed that luxury brands are to manufacture only high quality products => Считается, что бренды люкс-класса должны производить только высококачественную продукцию.'],
                              ['Is the amount of consumption economically dependent?',
                               'Является ли количество потребления экономически зависимым?'],
                              ['The new workers have to understand how to operate with modern machines very quickly',
                               'Новые рабочие должны очень быстро понять, как работать с современным оборудованием.'],
                              ['The factory has to launch several new products these days, but it has no resources',
                               'На днях фабрика должна запустить в производство несколько новых продуктов, но у нее нет ресурсов.'],
                              [
                                  'Our directors told us to buy only expensive raw materials. I doubt, whether it was right decision: the final price will be much more higher. That is no good',
                                  'Наши директоры сказали нам покупать только дорогое сырье. Я сомневаюсь, что это правильное решение: конечная цена будет намного выше. Это не хорошо.'],
                              [
                                  'We have a big big warehouse. That is good for us because we want to expand the production',
                                  'Мы имеем большой-большой склад. Это хорошо для нас, так как мы планируем расширить производство.'],
                              ['It is believed that luxury brands are to manufacture only high quality products',
                               'Считается, что бренды люкс-класса должны производить только высококачественную продукцию.'], ],
                "description": "",
            },
            {"title": "Лексика для маркетинга, рекламы и продаж",
             "youtube_urls": ["https://www.youtube.com/watch?v=HRLwmd51bbM"],
             "words": [['Provide services', 'предоставлять услуги.'],
                       ['Bring a product to market', 'запускать продукт на рынок'],
                       ['Outsell', 'распродать'],
                       ['Marketable', 'пользующийся спросом'],
                       ['Goods', 'товары'],
                       ['Distribution', 'распространение'],
                       ['Positioning', 'позиционирование'],
                       ['Demand for', 'спрос на'], ],
             "exsamples": [['Our company provide services in different',
                            'Наша компания предоставляет услуги в разных направлениях.'],
                           [
                               'The previous year we decided to bring a product to market. And our decision was very successful',
                               'В прошлом году мы решили запустить продукт на рынок. И наше решение было очень удачным.'],
                           [
                               'The company decided to outsell its goods and start a new production with better ones',
                               'Компания решила распродать свои товары и начать новое производство с лучшими.'],
                           [
                               'Are these products marketable? If no, we have to stop produce it',
                               'Эти товары пользуются спросом. Если нет, мы должны прекратить выпускать их.'],
                           ['These goods are so expensive! Only rich people can afford buy them!',
                            'Эти товары такие дорогие! Только богатые люди могут позволить себе купить их!'],
                           [
                               'The distribution of the goods is so slow… Our rivals are much more successful!',
                               'Распространение товара такое медленное… Наши соперники намного успешнее!'],
                           [
                               'The positioning of the product is one of the key moments in its success',
                               'Позиционирование товара – один из ключевых моментов его успеха (успешного продвижения на рынке).'],
                           ['Do we have demand for that kind of products?',
                            'У нас есть спрос на ту категорию товаров?'], ],
             "description": "",
             },
            {"title": "Финансовая тематика",
             "youtube_urls": ["https://www.youtube.com/watch?v=42iJXnHQFwg",
                              "https://www.youtube.com/watch?v=U8wflQ40FUU"],
             "words": [['Profit', 'прибыль'],
                       ['Loss', 'потери, убытки'],
                       ['A loan', 'заем'],
                       ['To owe', 'быть должным'],
                       ['To own', 'владеть'],
                       ['An interest', 'процент (по кредиту)'],
                       ['Turnover', 'оборот'],
                       ['Cash flow', 'поток денежных средств'],
                       ['Annual report', 'годовой отчет'],
                       ['Overheads', 'накладные расходы'], ],
             "exsamples": [['What is the profit of this company? Please be so kind to count in dollars',
                            'Какова прибыль этой компании? Будьте так добры посчитать в долларах.'],
                           [
                               'We had some losses the previous month. We have to analyze the situation and prevent it to happen once more',
                               'У нас были убытки на прошлом месяце. Мы должны проанализировать ситуацию и не допустить, чтобы это повторилось еще раз.'],
                           ['Borrowers can be given a loan up to 100, 000 dollars',
                            'Заемщики могут получить заем вплоть до 100,000 долларов.'],
                           ['No one likes to be owed money to a credit company',
                            'Никому не нравится быть должным кредитной компании.'],
                           ['The company own a capital of 1,000,000 dollars',
                            'Компания владеет капиталом в 1 миллион долларов.'],
                           [
                               'What is your interest due to this credit? It is rather a big one. But it becomes lower month from month',
                               'Какой у тебя процент по этому кредиту? Довольно большой. Но каждый месяц он становится меньше.'],
                           ['A turnover of the company should be no less than 1 million dollars per year',
                            'Оборот компании должен быть не менее 1 миллиона долларов в год.'],
                           [
                               'The cash flow is so rapid I’m sure we will open one more company this year. Our business is very successful',
                               'Поток денежных средств настолько быстрый, что я уверен, мы откроем еще одну компанию в этом году. Наш бизнес очень успешный.'],
                           ['The chief accountant has to provide us with the annual report',
                            'Главный бухгалтер должен предоставить нам годовой отчет.'],
                           [
                               'What concerns overheads, we stick to transparent policy. You can look at them every time you want',
                               'Что касается накладных расходов, мы придерживаемся прозрачной политики. Вы можете посмотреть их в любое время.'],
                           ],
             "description": "Финансовый английский – важный пункт для тех, чья работа связана"
                            " с бухгалтерией и финансами. Если говорить о профессии, напрямую связанной с финансами,"
                            " где вы постоянно составляете отчеты, считаете прибыль и высчитываете процентные ставки,"
                            " то специализированная лексика очень нужна"
             },
            {"title": "Полезные фразы для собеседования на английском",
             "youtube_urls": ["https://www.youtube.com/watch?v=4w0an9uJ6ig",
                              "https://www.youtube.com/watch?v=u2rhfPghv6U"],
             "words": [],
             "exsamples": [['I am good at multitasking', 'Я хорошо работаю в многозадачном режиме.'],
                           ['I perform well under pressure', 'Я хорошо справляюсь с работой в стрессовых ситуациях.'],
                           ['I should be hired because I am …', 'Я подхожу на эту должность, потому что … .'],
                           ['I have … years of experience in this field', 'У меня … лет опыта в данной среде.'],
                           ['I am a team player', 'Я командный игрок (работаю в команде).'],
                           ['I handle stress easily', 'Я легко справляюсь со стрессом.'],
                           ['I am very attentive to details', 'Я очень внимательный к деталям.'],
                           ['I have effective communication skills in English – both verbally and in writing',
                            'У меня хорошие навыки владения английским – как устным, так и письменным.'], ],
             "description": "Есть список фраз для собеседования на английском языке,"
                            " которые желательно тщательно выучить. Конечно, проходить собеседование на "
                            "иностранном языке всегда тяжело, особенно если вы хотите получить высокую должность",
             }
        ],
        'conclusion': "Business English нужен каждому успешному работнику."
                      " Чтобы вести диалог на английском, мало иметь базовые знания языка."
                      " Нужно владеть специализированной лексикой. Для телефонного разговора,"
                      " переговоров и интервью узкопрофильная лексика станет просто необходимой,"
                      " если вы хотите наладить хорошие отношения с партнерами. Особенно этот вопрос"
                      " актуален для секретаря, ведь основная его задача – отвечать на телефонные звонки"
                      " и давать исчерпывающую информацию. Любое его выражение идет от имени всей компании."
                      " Деловая обстановка требует формальности. А если вы работаете в международной компании,"
                      " которая сотрудничает с иностранными поставщиками,"
                      " то знание делового английского просто обязательно!",
    }, "разговорный": {
        "inception": "Разговорный английский - тут нет теории!"
                     "\nEдинственное что реально важно - говорить, и говорить реально много!"
                     "\nМы дадим вам пару советов для ускорения обучения говорению."
        , 'themes': [
            {
                "title": "Слушать и слышать!",
                "youtube_urls": ["https://www.youtube.com/watch?v=R8ShgEfbGiI",
                                 "https://www.youtube.com/watch?v=ygO7LVuA0PI"],
                "words": [],
                "exsamples": [],
                "description": "На начальном этапе самое главное — это как можно больше слушать."
                               " Слушать легкие тексты, проигрывать их несколько раз,"
                               " пока не будете понимать 90% всех слов. Для начинающих изучать язык,"
                               " на просторах онлайн мира вы найдете сотни детских аудиокниг (тут и моя подборка),"
                               " где лексика очень простая и понятная."
                               " Можете попробовать и аудиосказки — у меня на блоге есть подборка лучших из них."
                               " Потом можно и на песни перейти. Более того,"
                               " сейчас онлайн можно найти очень много аудиокурсов,"
                               " где буквально за месяц вы сможете обучиться основам разговорной речи."
                               " Один из таких — аудиокурс доктора Пимслера,"
                               " с которым вы можете ознакомиться на моем блоге."
                               " Вы знаете, моя мама любит путешествовать и следующая точка мира у нее — Сингапур."
                               " Так вот она понемногу начала слушать уроки Пимслера, где все очень разжевано!"
                               " Прогресс уже есть)",
            }, {
                "title": "Чтение на английском",
                "youtube_urls": ["https://www.youtube.com/watch?v=-HmSHNGYxJk",
                                 "https://www.youtube.com/watch?v=_isI7oknG8Y"],
                "words": [],
                "exsamples": [],
                "description": "Это не только увлекательное занятие, но и очень полезное:"
                               "\n1. Увеличение словарного запаса - например вы можете очень хорошо используете 100 слов,"
                               " умеете комбинировать их и состовлять предложения, но не пополняя свой словарный запас,"
                               " вы не сможете говорить свободно, так как вы находитесь в рамках этих 100 слов"
                               "\n2. Активация пассивного словарного запаса(слова, которые вы не используете) -"
                               " часто людям хватает только части своего словарного запаса и"
                               " остальная его часть начинает забываться,"
                               " здесь на помощь и приходят книги"
                               "\n3. Изучение грамматики на практике и в контексте -"
                               " вы хорошо поймете, как строить предложения,"
                               " ваша речь станет красивой и легкой для восприятия"
                               "\n4. Повышение самооценки и чувство гордости за себя - "
                               " представьте, как здорово чувствуешь себя, когда выбрал книгу на английском,"
                               " прочел ее от начала до конца и получил удовольствие не только от процесса,"
                               " но и от результата! "
                               "\nИзучение английского приносит свои плоды:"
                               " вы можете читать и понимать, обсуждать прочитанное и делиться впечатлениями"
                               " с друзьями или преподавателем."
                               " Это заставляет гордиться своими достижениями и мотивирует к дальнейшим успехам.",
            }, {
                "title": "Старый друг лучше новых двух?",
                "youtube_urls": ["https://www.youtube.com/watch?v=HNfr_qt0sLI",
                                 "https://www.youtube.com/watch?v=x9jzZ2E-lzs"],
                "words": [],
                "exsamples": [],
                "description": "Заводите новых друзей! Самый легкий способ для начинающих —"
                               " это найти в вашем городе сообщества таких же новичков, как и вы."
                               " Они наверняка встречаются где-нибудь в клубе или кафе,"
                               " чтобы практиковать разговорную речь! Это поможет вам не только научиться слушать,"
                               " но и выйти за свою зону comfort: ведь разговаривать с чужими людьми —"
                               " это невероятно страшно! Но это в любом случае лучше, чем сидеть дома и "
                               "бояться вымолвить хоть слово! Практика, практика и только практика — вот мой совет!"
                               "/get_people_to_chat - покажет пользователей(их никнеймы) телеграм,"
                               " которые тоже заинтересованы в изучении английского",
            }, {
                "title": "Переносим всю свою жизнь на английский язык!",
                "youtube_urls": [],
                "words": [],
                "exsamples": [],
                "description": "Скажу вам по секрету, это один из важнейших пунктов овладения разговорным английским!"
                               " Вы просто должны создать условия, когда вам придется говорить на языке!"
                               " Да, придется вам все-таки пожертвовать своим комфортом и привычным течением дел."
                               " Потому что с этого дня мы просим вас все ваши фильмы, шоу и сериалы СМОТРЕТЬ ТОЛЬКО на английском!"
                               " Более того, я прошу вас ДУМАТЬ на английском. Пробовали когда-нибудь?"
                               "Даже самое простое предложение из разряда «Я хочу кушать»"
                               " произносите внутри себя (а лучше вслух) на английском языке: «I am hungry».",
            },
            {
                "title": "Рекомендации для тех, кто хочет хорошо говорить на английском",
                "youtube_urls": [],
                "words": [],
                "exsamples": [],
                "description": """1. Медленный темп речи
                                \nНет ничего страшного в том, что вы говорите не так быстро, как иностранцы,
                                делаете паузы или подбираете слова. Для вас общение на английском — нечто новое,
                                к чему нужно привыкнуть. Зато если вы будете стараться чаще говорить с людими,
                                которые знают английский, то вы значительно пошатнёте пресловутый языковой барьер.
                                \n2. Грамматические ошибки
                                \nВы находитесь не на экзамене, поэтому не бойтесь ошибаться.
                                Люди, которые знают английский, все равно поймут вас,
                                даже если вы случайно пропустите вспомогательный глагол или употребите не то время.
                                Все прекрасно понимают, что английский язык для вас не является родным,
                                поэтому не будут обращать внимания на небольшие погрешности.
                                \n3. Лексические ошибки
                                \nНекоторые люди боятся запутаться в английской лексике.
                                Мы советуем ознакомиться со статьей: «Miscommunication abroad или как я ела мыло на обед».
                                Вы увидите, нет ничего страшного в путанице, всегда можно найти выход из положения и
                                объяснить другими словами, что вам нужно.
                                \n4. Акцент
                                \nНаш последний совет: сохраняйте спокойствие и имитируйте британский акцент.
                                Во многих из нас живет страх: я не смогу говорить как настоящий англичанин или американец,
                                у меня акцент, это может звучать смешно. Совершенно необоснованная фобия.
                                Во-первых, у каждого человека есть свои собственные особенности речи, интонации, произношения. 
                                Во-вторых, в любой стране есть местный вариант английского: в некоторых языках нет звука «ш»,
                                в каком-то отсутствует «ч», кому-то сложно научиться произносить сочетание th — так и
                                формируются разные акценты в английском жителей различных стран.
                                Тем не менее, это не мешает миллионам людей изучать язык, общаться и понимать друг друга.
                                Кстати, многие считают, что австралийский и канадский английский звучат еще более экзотично,
                                чем наша с вами речь.
                                \n5. Вот дополнительные ссылки по теме:
                                \n
                                https://lim-english.com/posts/izychenie-razgovornogo-angliiskogo-yazika-samostoyatelno - изучение английского самостоятельно
                                \n
                                https://habr.com/ru/post/472754/ - как заговорить на английском, рассказ блогерши.
                                """,
            },
        ],
        'conclusion': "Разговорный английский открывает дороги во многие сферы жизни."
                      "\nСтуденты находят новых друзей из разных стран мира, заключают браки с иностранцами,"
                      "\nчитают книги и статьи в оригинале,"
                      "\nсмотрят фильмы и сериалы без субтитров, пользуются зарубежными "
                      "\nприложениямя. Поэтому принято считать,"
                      "\nчто разговорный английский - самая нужная часть английского",
    }
}

commands = {"learning_menu": ["/help - выводит список команд",
                              "/run_test - запустить тест по выбранной теме",  # на десерт
                              "/get_other_links - показать прочие полезные ссылки для изучения английского",
                              "/get_myeng_map - показать на карте мира всех пользователей бота",  #
                              "/get_people_to_chat - показывает людей(пользователей Телеграмм), с которыми можно по-переписываться на английском языке",
                              "/get_lesson - посмотреть все разделы и из темы, также в конце темы можно пройти тест",
                              "/change_aim - поменять изучаемый раздел (путешествия, для работы за границей, разговорный)",
                              "/FromEngToRUS - перевод вашего сообщения с английского на русский",  # translate
                              "/FromRusToEng - перевод вашего сообщения с русского на английский",
                              "/logout - выйти из аккаунта"],
            "lesson_menu": ["help_in_lesson",
                            "get_sections_info - пишет аннотации к каждому разделу",
                            "get_all_themes - показать все темы разделов",
                            "/FromEngToRUS - перевод вашего сообщения с английского на русский",  # translate
                            "/FromRusToEng - перевод вашего сообщения с русского на английский",
                            "return_to_cabinet - возвращает вас в личный кабинет",
                            ""], }
sections = ['путешествия', 'для работы за границей', 'разговорный']
other_links = [
    {"title": "1000 слов на английском - 80 % английского",
     "url": "https://speakenglishwell.ru/1000-slov-na-anglijskom-kotorye-nuzhno-znat-nachinayushhim/",
     },
    {
        "title": "сериал Friends",
        "url": "https://www.youtube.com/watch?v=tw_e1Lj6p5o&list=PL-e5esCcfNJ7DikPH96W-pdQGhuni-Cze",
    },
    {
        "title": "Сериалы с субтитрами",
        "url": "http://lelang.ru/english/serialy/",
    },
    {
        "title": "Аудирование",
        "url": """Ororo.tv — фильмы и сериалы на английском со встроенным переводчиком. 
                    \nShow-English — фильмы, сериалы и клипы на английском языке со встроенным переводчиком. 
                    \nHamatata — сериалы и фильмы на английском с субтитрами. Субтитры можно переводит""",
    },
    {
        "title": "Чтение",
        "url": """WordMemo — сайт дает возможность угадать смысл незнакомого слова. Отмеченные как незнакомые слова в тексте в дальнейшем переводятся не сразу, а сначала показывается контекст, в котором вы их встречали до этого.
                    \nWordsFromText — на сайте можно смотреть значение незнакомых слов прямо в тексте. Также можно сюда добавлять свои тексты, из которых сервис выловит все используемые в тексте слова и разбросает их в виде словаря.
                    \nGetParallelTranslations — сервис для чтения книг с возможностью добавлять новые слова в личный словарь.
                    \nNewsinlevels — здесь можно почитать новости с уровнями для изучающих английский.
                    \nReadTheory — сайт для развития навыков чтения.""",
    },
    {
        "title": "Грамматика",
        "url": """English03 — полный разбор известного учебника Essential Grammar in Use («красный Мёрфи»).
                    \nAlleng — подборка учебников по грамматике.
                    \nEgo4u — изучение грамматики онлайн с упражнениями, тестами и правильными ответами.
                    \nStudy — онлайн-справочник по грамматике английского языка с тестами.
                    \nMySpelling — портал для практики правописания, доступен без регистрации.
                    \nLang-8 — сайт, на котором носители могут проверить написанный вами текст (взамен нужно проверять тексты, написанные изучающими русский).
                    \nMacmillanDictionaries — формы неправильных глаголов английского языка в формате интерактивной рулетки.
                    \nIrregularVerbs — на этом сайте очень легко можно выучить английские неправильные глаголы.""",
    },
    {
        "title": "Фонетика",
        "url": """Am-En — фонетический анимированный справочник, созданный Университетом Айовы.
                    \n — транскрипция американского английского языка с доступными примерами произношениями.
                    \nForvo — база произношений, здесь доступны разные языки и разные диалекты.""",
    }, {
        "title": "Общение",
        "url": """Sharedtalk — здесь можно пообщаться с иностранцами по чату и микрофону.
                    \nInterpals — здесь можно найти много друзей по переписке со всего мира и помогать им изучать язык. Или же просить о помощи. Или же обмениваться помощью.
                    \nAmilingo — сайт, на котором можно общаться с преподавателями и носителями языка.
                    \nPenpalworld — сеть для свободного общения пользователей со всего мира. Можно выбрать страну или сразу весь мир.""",
    },
    {
        "title": "Видеоканалы",
        "url": """Krutopridumal — полезные видео по особенностям правильного произношения, улучшению словарного запаса и грамматике.
                    \nPhilochkoPhilochko — ведущий помогает русским адаптировать книжный английский (американский) к разговорному.
                    \nEnglishGermanSpanish — канал с обучающими видео рассматривает множество грамматических аспектов. Много уроков по аудированию.
                    \nDNewsChannel — новости науки от канала «Дискавери».
                    \nTwominute English — короткие двухминутные уроки, удобно и эффективно.
        """,
    },
    {
        "title": "Порталы для самостоятельного изучения",
        "url": """Englsecrets — сайт для самостоятельного изучения английского.
                    \nDuolingo — сервис для изучения иностранных языков с нуля. Программа каждого курса построена в форме «дерева достижений»: чтобы перейти на новый уровень, нужно набрать определенное количество очков, которые даются за правильные ответы.
                    \nLearnathome — самоучитель английского.
                    \nTolearnenglish — сервис для изучения английского с тестами, уроками, форумом.
                    \nStudyblue — портал для изучения различных предметов на английском языке.
                    \nLingvist — сайт скоростного изучения английского за 200 часов.
                    \nEnglish-polyglot — сайт с видеоуроками от Дмитрия Петрова.
                    \nStudy — портал для изучения языков.
                    \nEnglish-attack — метод обучения предполагает использование видео, фотографий, игр и общения с друзьями для ежедневной практики английского языка.
                    \nTurboenglish — изучение английского с нуля в игровой форме.
                    \nLingualeo — ресурс-тренажер со львенком и фрикадельками в качестве бонусов.""",
    }
]

FLASK_SERVER = "http://localhost:5000"
reply_keyboard = [["1000 слов на английском - 80 % английского"],
                  ["сериал Friends"],
                  ["Сериалы с субтитрами"],
                  ["Аудирование"],
                  ["Чтение"],
                  ["Грамматика"],
                  ["Фонетика"],
                  ["Общение"],
                  ["Видеоканалы"],
                  ["Порталы для самостоятельного изучения"],
                  ["назад"]]
other_links_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
reply_keyboard = [["Английский для туристов в дороге"],
                  ["Английский в гостинице"],
                  ["Исследуем город"],
                  ["Английский для туристов в ресторане"],
                  ["Английский для туристов в магазине"],
                  ["Основные термины бизнеса"],
                  ["Фразы на английском, которые касаются работы производства"],
                  ["Лексика для маркетинга, рекламы и продаж"],
                  ["Финансовая тематика"],
                  ["Полезные фразы для собеседования на английском"],
                  ["Слушать и слышать!"],
                  ["Чтение на английском"],
                  ["Старый друг лучше новых двух?"],
                  ["Переносим всю свою жизнь на английский язык!"],
                  ["Рекомендации для тех, кто хочет хорошо говорить на английском"],
                  ['назад']]
themes_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
reply_keyboard = [['начать тест'],
                  ['назад'],
                  ["Английский для туристов в дороге"],
                  ["Английский в гостинице"],
                  ["Исследуем город"],
                  ["Английский для туристов в ресторане"],
                  ["Английский для туристов в магазине"],
                  ["Основные термины бизнеса"],
                  ["Фразы на английском, которые касаются работы производства"],
                  ["Лексика для маркетинга, рекламы и продаж"],
                  ["Финансовая тематика"],
                  ["Полезные фразы для собеседования на английском"],
                  ["Слушать и слышать!"],
                  ["Чтение на английском"],
                  ["Старый друг лучше новых двух?"],
                  ["Переносим всю свою жизнь на английский язык!"],
                  ["Рекомендации для тех, кто хочет хорошо говорить на английском"]
                  ]
themes_markup_beg_test = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
reply_keyboard = [['путешествия'],
                  ['для работы за границей'],
                  ['разговорный'],
                  ["путешествия, для работы за границей"],
                  ["путешествия, разговорный"],
                  ["для работы за границей, разговорный"],
                  ["путешествия, для работы за границей, разговорный"]]
aims_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


class RegisterForm:
    stages = [
        "Введите своё имя",
        "Введите свою фамилию",
        "Введите ваш email",
        "Придумайте пароль от аккаунта",
        "Повторите пароль от аккаунта",
        "Введите свой возраст",
        "Введите ваш адрес проживания",
        "Какова ваша цель изучения английского?"
        "\n(путешествия, для работы за границей, разговорный)"
        "\nМожете выбрать несколько, вводите их через запятую(,)."
    ]

    def __init__(self):
        self.surname = ""
        self.name = ""
        self.email = ""
        self.password = ""
        self.password_again = ""
        self.age = -1
        self.address = ""
        self.telegram_name = ""
        self.aim = ""


def register(update, context):
    mes = update.message.text.strip()
    user_id = update.message.from_user.id
    res = get(f"{FLASK_SERVER}/api/users/{user_id}").json()
    if res["message"] == 'ok':
        update.message.reply_text("У вас уже есть аккаунт!")
        sessionStorage[user_id]["login_stage"] = 0
        return login(update, context)
    else:
        if user_id not in sessionStorage.keys():
            form = RegisterForm()
            sessionStorage[user_id] = {
                "register_stage": 0,
                "reg_form": form,
            }
            update.message.reply_text("Hello, я - телеграм бот Myeng."
                                      "\nЗдесь вы можете изучать английский по разделам,"
                                      "\nсмотреть полезную информацию на разным темам,"
                                      "\nувидеть интересные ссылки для изучения анлийского,"
                                      "\nзнания тут закрепляються с помощью разных тестов по словам темы."
                                      "\nТакже у меня есть встроенный переводчик, который доступен в любой момент!"
                                      "\nИзучать английский интресно и весело! Вперед!")
            update.message.reply_text("Для начала вам нужно зарегистрироваться",
                                      reply_keyboard=ReplyKeyboardMarkup([], one_time_keyboard=True))
    stage = sessionStorage[user_id]['register_stage']
    if stage != len(RegisterForm.stages):
        if stage != 0:
            if stage == 1:
                sessionStorage[user_id]["reg_form"].name = mes
            if stage == 2:
                sessionStorage[user_id]["reg_form"].surname = mes
            if stage == 3:
                if "@" not in mes:
                    update.message.reply_text("email должен содержать символ '@' !")
                    return 1
                sessionStorage[user_id]["reg_form"].email = mes
            if stage == 4:
                if len(mes) < 8:
                    update.message.reply_text("Пароль должен состоять \n "
                                              "как минимум из 8 символом")
                    return 1
                sessionStorage[user_id]["reg_form"].password = mes
            if stage == 5:
                if mes != sessionStorage[user_id]["reg_form"].password:
                    update.message.reply_text("Пароли должны совпадать!")
                    return 1
                sessionStorage[user_id]["reg_form"].password_again = mes
            if stage == 6:
                sessionStorage[user_id]["reg_form"].age = int(mes)
            if stage == 7:
                sessionStorage[user_id]["reg_form"].address = mes
        if stage == 7:
            update.message.reply_text(RegisterForm.stages[stage], reply_markup=aims_markup)
        else:
            update.message.reply_text(RegisterForm.stages[stage])
        sessionStorage[user_id]['register_stage'] += 1
        return 1
    sessionStorage[user_id]["reg_form"].aim = ""
    for section in mes.lower().split(','):
        section = section.lower().strip()
        if len(section) == 0:
            continue
        if section not in ['путешествия', 'для работы за границей', 'разговорный']:
            update.message.reply_text(
                "Выберите цели из предложенных! (путешествия, для работы за границей, разговорный)."
                "\nЕсли целей много, то вводите их через запятую(,)")
            return 1
        else:
            sessionStorage[user_id]["reg_form"].aim += section + ','
    sessionStorage[user_id]['reg_form'].aim = sessionStorage[user_id]['reg_form'].aim[:-1]
    data = sessionStorage[user_id]["reg_form"]
    a = True
    nick = None
    try:
        nick = update.message.from_user.username
    except Exception:
        a = False
    if a:
        res = post(f'{FLASK_SERVER}/api/users', json={
            'id': user_id,
            'name': data.name,
            'surname': data.surname,
            'email': data.email,
            'password': data.password,
            'address': data.address,
            'age': data.age,
            'aim': data.aim,
            'telegram_name': nick,
        }).json()
    else:
        res = post(f'{FLASK_SERVER}/api/users', json={
            'id': user_id,
            'name': data.name,
            'surname': data.surname,
            'email': data.email,
            'password': data.password,
            'address': data.address,
            'age': data.age,
            'aim': data.aim,
            'telegram_name': "",
        }).json()
    print(res)
    sessionStorage[user_id]["login_stage"] = 0
    update.message.reply_text("Вы успешно зарегистрированы!")
    return learning(update, context)


def login(update, context):
    mes = update.message.text.strip()
    user_id = update.message.from_user.id
    if sessionStorage[user_id]['login_stage'] == 0:
        update.message.reply_text("Введите пароль от вашего аккаунта")
        sessionStorage[user_id]['login_stage'] += 1
        return 2
    else:
        given_password = mes
        res = get(f"{FLASK_SERVER}/api/users/{user_id}").json()
        if res['message'] == "ok":
            if res['user_data']['password'] == given_password:
                sessionStorage[user_id]['login_stage'] = 0
                return learning(update, context)
            else:
                update.message.reply_text(
                    "Введены неправильные данные, введите ещё раз")
                return 2
        else:
            update.message.reply_text(
                "Введены неправильные данные, проверьте пароль и введите ещё раз")
            return 2


def start(update, context):
    update.message.reply_text("Я работаю!")
    user_id = update.message.from_user.id
    res = get(f"{FLASK_SERVER}/api/users/{user_id}").json()
    if res["message"] == 'ok':
        update.message.reply_text(
            "У вас уже есть аккаунт, \n"
            "для продолжения авторизуйтесь", reply_keyboard=ReplyKeyboardMarkup([], one_time_keyboard=True))
        if user_id not in sessionStorage.keys():
            sessionStorage[user_id] = {
                'login_stage': 0,
                'conv_stage': 0
            }
        return login(update, context)
    else:
        return register(update, context)


def learning(update, context):
    user_id = update.message.from_user.id
    update.message.reply_text("Вы в личном кабинете,"
                              "\nЧтобы узнать все команды наберите /help")
    sessionStorage[user_id]['conv_stage'] = 3
    return 3


def logout(update, context):
    update.message.reply_text("Вы вышли из аккаунта, чтобы начать работу выполните команду /start")
    return ConversationHandler.END


def learning_help(update, context):
    text = """"""
    for com in commands['learning_menu']:
        text += com + '\n'
    update.message.reply_text(text)
    return 3


def get_other_links(update, context):
    user_id = update.message.from_user.id
    mes = update.message.text.strip()
    if mes == 'назад':
        sessionStorage[user_id]['get_links_stage'] = 0
        return learning(update, context)
    if 'get_links_stage' not in sessionStorage[user_id].keys():
        sessionStorage[user_id]['get_links_stage'] = 0
    titles_mes = "Что вы хотите посмотреть? (введите строго нужный текст) " \
                 "\nЧтобы завершить просмотр ссылок введите 'назад'"
    if sessionStorage[user_id]['get_links_stage'] == 0:
        for link in other_links:
            titles_mes += "\n" + link['title']
        sessionStorage[user_id]['get_links_stage'] = 1
        update.message.reply_text(titles_mes, reply_markup=other_links_markup)
        return 4
    else:
        for link in other_links:
            if link['title'] == mes:
                update.message.reply_text(f"""Вот ваш запрос на {link['title']}: 
                                            \n{link['url']}
                                            \nВведите ещё одну тему или напишите 'назад' для выхода в личный кабинет""",
                                          reply_markup=other_links_markup)
                return 4
    update.message("Пожалуйста введите правильные данные!")
    return 4


def get_people_to_chat(update, context):
    res = get(f"{FLASK_SERVER}/api/users").json()
    text = "Вот люди, с которыми с ты можешь пообщаться." \
           "\nНайди их по никнейму, добавив в начало поиска '@'"
    leng = len(res['users'])
    for user in res['users']:
        if user['id'] == update.message.from_user.id:
            leng -= 1
            continue
        if user['telegram_name'] is None or len(user['telegram_name']) == 0:
            leng -= 1
    if leng > 0:
        cnt = 1
        for i in range(leng):
            if res['users'][i]['id'] != update.message.from_user.id and len(res['users'][i]['telegram_name']):
                text += '\n' + str(cnt) + '. ' + res['users'][i]['telegram_name']
                cnt += 1
    else:
        text = "Извините, но пока у вас нет людей для переписки, \n" \
               "скорее всего у них нет никнейма, поэтому бот не может их найти"
    update.message.reply_text(text)


def get_section_info(update, context):
    user_id = update.message.from_user.id
    curr_section = 1
    text = "Вот информация о разделах, которые вы изучаете." \
           "\nВы можете изменить свои цели изучения в личном кабинете."
    aim = sessionStorage[user_id]['user_data']['aim'].split(',')
    for section in aim:
        text += f"\n{curr_section}. {section[0].upper()}{section[1:]}." \
            f"\n\nНемного предисловия к разделу:" \
            f"\n{WORDS_FOR_LEARNING[section]['inception']}" \
            f"\n\nВот обобщение о разделе: " \
            f"\n{WORDS_FOR_LEARNING[section]['conclusion']}"
        curr_section += 1
        text += '\n'
    text += '\nПолностью прочитайте выше сказанное, вы больше не увидите эту информацию'
    text = text.strip()
    update.message.reply_text(text)


def get_lesson(update, context):
    user_id = update.message.from_user.id
    mes = update.message.text.strip()

    if 'lesson_stage' not in sessionStorage[user_id].keys():
        sessionStorage[user_id]['lesson_stage'] = 0
        sessionStorage[user_id]['test_stage'] = -1
        sessionStorage[user_id]['section_info_checked'] = 0
        sessionStorage[user_id]['user_data'] = get(f"{FLASK_SERVER}/api/users/{user_id}").json()['user_data']
        if sessionStorage[user_id]['user_data']['aim'][-1] == ',':
            sessionStorage[user_id]['user_data']['aim'] = sessionStorage[user_id]['user_data']['aim'][:-1]

    aim = sessionStorage[user_id]['user_data']['aim'].split(',')
    if sessionStorage[user_id]['lesson_stage'] == 0:
        update.message.reply_text("Вы зашли в раздел занятий."
                                  "\nЗдесь отключены некоторые функции, ведь они будут только отвлекать вас"
                                  "\nТакже можете написать /help_in_lesson, чтобы узнать все команды")
        # показать все темы, предоставить выбор
        if sessionStorage[user_id]['section_info_checked'] == 0:
            get_section_info(update, context)
            sessionStorage[user_id]['section_info_checked'] = 1
        get_all_themes(update, context)
        update.message.reply_text("Чтобы увидеть информацию по какой-либо теме, напишите её.(строго как в сообщении)"
                                  "\nВы также можете написать 'назад' для возвращения в личный кабинет",
                                  reply_markup=themes_markup)
        sessionStorage[user_id]['lesson_stage'] += 1
    elif sessionStorage[user_id]['lesson_stage'] == 1:
        if mes.lower() == 'начать тест':
            if sessionStorage[user_id]['curr_section'] == 'разговорный':
                update.message.reply_text(
                    "Это разговорный раздел, здесь нет тестов!\nЧтобы увидеть информацию по какой-либо теме, напишите её.(строго как в сообщении)"
                    "\nВы также можете написать 'назад' для возвращения в личный кабинет",
                    reply_markup=themes_markup)
                get_all_themes(update, context)
            update.message.reply_text("Сейчас мы зададим вам несколько вопросов,"
                                      " а вы будете на них отвечать")
            sessionStorage[user_id]['test'] = get_test(user_id)
            sessionStorage[user_id]['anss_given'] = []
            update.message.reply_text(sessionStorage[user_id]['test'][0][0],
                                      reply_markup=ReplyKeyboardMarkup([['завершить тест']], one_time_keyboard=True))
            sessionStorage[user_id]['test_stage'] = 1
            sessionStorage[user_id]['conv_stage'] = 5
            return 5
        if sessionStorage[user_id]['test_stage'] != -1:
            if mes == 'завершить тест':
                sessionStorage[user_id]['test_stage'] += 1
                text = f"Вот результаты теста: \n"
                score = 0
                test = sessionStorage[user_id]['test']
                for ans_id in range(len(sessionStorage[user_id]['anss_given'])):
                    ans = sessionStorage[user_id]['anss_given'][ans_id].lower().strip()
                    text += '\n' + str(ans_id + 1) + '. ' + test[ans_id][0]
                    text += f"\nВаш ответ: {ans}"
                    if ans == test[ans_id][1].lower().strip():
                        text += '\nПравильно ✓'
                        score += 1
                    else:
                        text += '\nНеправильно ❌'
                        text += f"\nВот правильный ответ: {test[ans_id][1]}"
                text = f"Тест закончен, ваш результат: {str(score)} из" \
                           f" {len(sessionStorage[user_id]['anss_given'])}\n" + text
                update.message.reply_text(text)
                sessionStorage[user_id]['test_stage'] = -1
                update.message.reply_text("Введите 'начать тест', чтобы пройти ещё один тест",
                                          "\nВведите 'назад', чтобы попасть в личный кабинет",
                                          "\nВведите название любой темы, из выше перечисленных,"
                                          " чтобы увидеть её содержание и продолжить обучение",
                                          reply_markup=themes_markup_beg_test)
                return 5
            if sessionStorage[user_id]['test_stage'] == len(sessionStorage[user_id]['test']):
                sessionStorage[user_id]['anss_given'].append(mes.lower().strip())
                sessionStorage[user_id]['test_stage'] += 1
                text = f"Вот результаты теста: \n"
                score = 0
                test = sessionStorage[user_id]['test']
                for ans_id in range(len(sessionStorage[user_id]['anss_given'])):
                    ans = sessionStorage[user_id]['anss_given'][ans_id].lower().strip()
                    text += '\n' + str(ans_id + 1) + '. ' + test[ans_id][0]
                    text += f"\nВаш ответ: {ans}"
                    if ans == test[ans_id][1].lower().strip():
                        text += '\nПравильно ✓'
                        score += 1
                    else:
                        text += '\nНеправильно ❌'
                        text += f"\nВот правильный ответ: {test[ans_id][1]}"
                text = f"Тест закончен, ваш результат: {str(score)} из" \
                           f" {len(sessionStorage[user_id]['anss_given'])}\n" + text
                update.message.reply_text(text)
                sessionStorage[user_id]['test_stage'] = -1
                update.message.reply_text("Введите 'начать тест', чтобы пройти ещё один тест"
                                          "\nВведите название любой темы, из выше перечисленных,"
                                          " чтобы увидеть её содержание и продолжить обучение"
                                          "\nВведите 'назад', чтобы попасть в личный кабинет",
                                          reply_markup=themes_markup_beg_test)
                return 5
            update.message.reply_text(sessionStorage[user_id]['test'][sessionStorage[user_id]['test_stage']][0],
                                      reply_markup=ReplyKeyboardMarkup([['завершить тест']], one_time_keyboard=True))
            sessionStorage[user_id]['anss_given'].append(mes.lower().strip())
            sessionStorage[user_id]['test_stage'] += 1
            sessionStorage[user_id]['conv_stage'] = 5
            return 5
        if mes.lower() == 'назад':
            sessionStorage[user_id]['lesson_stage'] = 0
            sessionStorage[user_id]['test_stage'] = -1
            sessionStorage[user_id]['section_info_checked'] = 0
            sessionStorage[user_id]['user_data'] = get(f"{FLASK_SERVER}/api/users/{user_id}").json()['user_data']
            if sessionStorage[user_id]['user_data']['aim'][-1] == ',':
                sessionStorage[user_id]['user_data']['aim'] = sessionStorage[user_id]['user_data']['aim'][:-1]

            return learning(update, context)

        sections = aim
        lesson = None
        curr_section = None
        for section in sections:
            if lesson is not None:
                break
            for les in WORDS_FOR_LEARNING[section]['themes']:
                if les['title'] == mes:
                    lesson = les
                    curr_section = section
                    sessionStorage[user_id]['curr_section'] = curr_section
                    sessionStorage[user_id]['curr_lesson'] = lesson
                    break
        if lesson is None:
            update.message.reply_text("Введите существующую тему!"
                                      "\nСкорее всего вы не можете посмотреть эту тему,"
                                      "\nтак противоречит вашей цели изучения анлийского."
                                      "\nВы можете изменить свою цель изучения в личном кабинете при помощи команды"
                                      "/change_aim", reply_markup=themes_markup_beg_test)
            get_all_themes(update, context)
            return 5
        lesson_text = f"Вот ваш урок. " \
            f"\n1. Оглавление: {lesson['title']}"
        if len(lesson['youtube_urls']) != 0:
            mnozh = 'a'
            if len(lesson['youtube_urls']) > 1:
                mnozh = 'и'
            lesson_text += f"\n\nВот ссылк{mnozh} на видео по данной тематике:"
            for url in lesson['youtube_urls']:
                lesson_text += f"\n{url}"
        if len(lesson['words']):
            lesson_text += "\n\nВот слова по теме:"
            for word in lesson['words']:
                lesson_text += f'\n{word[0]} - {word[1]}'
        if len(lesson['exsamples']):
            lesson_text += "\n\nВот примеры, где используются слова из темы в контексте:"
            for exsample in lesson['exsamples']:
                lesson_text += f'\n{exsample[0]} -> \n{exsample[1]}'
        if len(lesson['description']):
            lesson_text += f"\n\nДополнительная информация:" \
                f"\n{lesson['description']}"
        lesson_text += '\n\nНе пугайтесь большого объёма информации, потратьте столько времени,' \
                       ' сколько нужно, чтобы овладеть темой.' \
                       "\n\nВведите 'назад', чтобы вернуть в личный кабинет" \
                       "\nВведите 'начать тест', чтобы начать тестирование по словам этой темы" \
                       '\nНапишите название любой темы их предложенных, чтобы увидеть информацию о ней'
        update.message.reply_text(lesson_text, reply_markup=themes_markup_beg_test)
    sessionStorage[user_id]['conv_stage'] = 5
    return 5


def get_all_themes(update, context):
    user_id = update.message.from_user.id
    text = "Вот темы на выбор:"
    sections = sessionStorage[user_id]['user_data']['aim'].split(',')
    c = 1
    for section in sections:
        cnt = 1
        text += f"\n{str(c)}. {section.title()}"
        for lesson in WORDS_FOR_LEARNING[section]['themes']:
            text += f"\n\t{str(c)}.{str(cnt)} {lesson['title']}"
            cnt += 1
        c += 1
    text = text.strip()
    update.message.reply_text(text)


def help_in_lesson(update, context):
    text = """"""
    for com in commands['lesson_menu']:
        text += com + '\n'
    update.message.reply_text(text)
    return 5


def change_aim(update, context):
    user_id = update.message.from_user.id
    mes = update.message.text.strip().lower()
    user_data = get(f"{FLASK_SERVER}/api/users/{user_id}").json()['user_data']
    if 'change_aim_stage' not in sessionStorage[user_id].keys():
        sessionStorage[user_id]['change_aim_stage'] = 0
    if sessionStorage[user_id]['change_aim_stage'] == 0:
        text = f'Выберите цели изучения английского\n(путешествия, для работы за границей, разговорный),' \
            f'\nесли их несколько, то вводите через запятую(,)'
        update.message.reply_text(text, reply_markup=aims_markup)
        sessionStorage[user_id]['change_aim_stage'] += 1
        return 6
    else:
        sections = ""
        for section in mes.lower().strip().split(','):
            section = section.lower().strip()
            if len(section) == 0:
                continue
            if section not in ['путешествия', 'для работы за границей', 'разговорный']:
                update.message.reply_text(
                    "Выберите цели из предложенных! (путешествия, для работы за границей, разговорный)."
                    "\nЕсли целей много, то вводите их через пробел", reply_markup=aims_markup)
                return 6
            else:
                sections += section + ','
        sections = sections[:-1]
        deliting = delete(f"{FLASK_SERVER}/api/users/{user_id}").json()
        print(deliting)
        res = post(f'{FLASK_SERVER}/api/users', json={
            'id': user_id,
            'name': user_data['name'],
            'surname': user_data['surname'],
            'email': user_data['email'],
            'password': user_data['password'],
            'address': user_data['address'],
            'age': user_data['age'],
            'aim': sections,
            'telegram_name': update.message.from_user.username,
        }).json()
        print(res)
        update.message.reply_text("Ваши разделы изучения успешно обновлёны!")
        sessionStorage[user_id]['change_aim_stage'] = 0
        sessionStorage[user_id]['user_data']['aim'] = sections
        if 'lesson_stage' in sessionStorage[user_id].keys():
            sessionStorage[user_id]['lesson_stage'] = 0
        return learning(update, context)


def get_test(user_id):
    section = sessionStorage[user_id]['curr_section']
    theme = sessionStorage[user_id]['curr_lesson']['title']
    res = get(f"{FLASK_SERVER}/api/tests/{theme}/{user_id}").json()
    if 'error' in res:
        words = []
        for les in WORDS_FOR_LEARNING[section]['themes']:
            if les['title'] == theme:
                words = les['words']
                break
        sam = random.sample(words, k=min(len(words), random.randint(5, 10)))
        test = []
        if 'curr_q_id' not in sessionStorage.keys():
            sessionStorage["curr_q_id"] = 1
        questions = ""
        passed_users = str(user_id)
        curr_q_id = sessionStorage['curr_q_id']
        for i in range(len(sam)):
            en, ru = sam[i]
            q = random.randint(0, 1)
            text, ans = "", ""
            if q:
                text = en + '\n' + "Как сказать это на русском?"
                ans = ru
            else:
                text = ru + '\n' + "Как сказать это на английском?"
                ans = en
            test.append([text, ans])
            from requests import post
            ques_adding = post(f"{FLASK_SERVER}/api/questions", json={
                "id": curr_q_id,
                "text": text,
                "ans": ans,
                "theme": theme,
            }).json()
            print(ques_adding)
            questions += str(curr_q_id) + ','
            curr_q_id += 1
        questions = questions[:-1]
        from requests import post
        test_adding = post(f"{FLASK_SERVER}/api/tests", json={
            "theme": theme,
            "questions": questions,
            "passed_users": passed_users,
        }).json()
        sessionStorage['curr_q_id'] = curr_q_id
        return test
    else:
        test = []
        for question_id in res['test']['questions'].split(','):
            ques = get(f"{FLASK_SERVER}/api/questions/{question_id}").json()['question']
            text = ques['text']
            ans = ques['ans']
            test.append([text, ans])
        return test


def get_myeng_map(update, context):
    users = get(f"{FLASK_SERVER}/api/users").json()['users']
    marks = ""
    for user in users:
        request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode" \
            f"={user['address']}&format=json"
        response = requests.get(request)
        if not response:
            continue
        else:
            json_response = response.json()
            if len(json_response["response"]["GeoObjectCollection"][
                       "featureMember"]) == 0:
                continue
            toponym = \
                json_response["response"]["GeoObjectCollection"][
                    "featureMember"][
                    0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            longitude, latitude = toponym_coodrinates.split()
            metka = f'{longitude},{latitude},pm'
            metka += 'wt'
            metka += 's' + '~'
            marks += metka
    Zend = ""
    if len(users) == 1:
        Zend = "&z=2"
    static_api_request = f"http://static-maps.yandex.ru/1.x/?" \
                             f"l=map&apikey=40d1649f-0493-4b70-98ba-98533de7710b&pt={marks[:-1]}" + Zend
    context.bot.send_photo(
        update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        static_api_request,
        caption=f"Вот пользователи телеграм бота MyEng на карте!"
        f"\n(возможно некоторых мы найти не смогли!)"
    )


def stop_translating(update, context):
    user_id = update.message.from_user.id
    if sessionStorage[user_id]['conv_stage'] == 3:
        return learning(update, context)
    else:
        update.message.reply_text("Вы снова в разделе занятий")
        return 5


def switch_to_from_en_to_ru(update, context):
    update.message.reply_text("Введите что нибудь для перевода c английского на русский",
                              reply_markup=ReplyKeyboardMarkup([['назад']], one_time_keyboard=True))
    return 9


def switch_to_from_ru_to_en(update, context):
    update.message.reply_text("Введите что нибудь для перевода с русского на английский",
                              reply_markup=ReplyKeyboardMarkup([['назад']], one_time_keyboard=True))
    return 8


def from_en_to_ru(update, context):
    eng_text = update.message.text.strip()
    if eng_text == 'назад':
        return stop_translating(update, context)
    token = "trnsl.1.1.20200402T145548Z.67d1c0ace063d508.c80570c74bd2edadb651ce9a4fea5da1190d2ee7"
    url_trans = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    trans_option = {'key': token, 'lang': 'en-ru', 'text': eng_text}
    webRequest = requests.get(url_trans, params=trans_option)
    response = eval(webRequest.text)
    update.message.reply_text(
        "Вот ваш перевод: \n" + response['text'][0] + ""
                                                      "\nЧтобы вернуться в личный кабинет напишите 'назад' "
                                                      "\nИначе, напишете что-нибудь для перевода на русский",
        reply_markup=ReplyKeyboardMarkup([['назад']], one_time_keyboard=True))


def return_to_cabinet(update, context):
    return learning(update, context)


def from_ru_to_en(update, context):
    ru_text = update.message.text.strip()
    if ru_text == 'назад':
        return stop_translating(update, context)
    token = "trnsl.1.1.20200402T145548Z.67d1c0ace063d508.c80570c74bd2edadb651ce9a4fea5da1190d2ee7"
    url_trans = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    trans_option = {'key': token, 'lang': 'ru-en', 'text': ru_text}
    webRequest = requests.get(url_trans, params=trans_option)
    response = eval(webRequest.text)
    update.message.reply_text(
        "Вот ваш перевод: \n" + response['text'][0] + "\nЧтобы вернуться в личный кабинет напишите 'назад'"
                                                      "\nИначе, введите что-нибудь для перевода с русского на английский"
        , reply_markup=ReplyKeyboardMarkup([['назад']], one_time_keyboard=True))


def run_test(update, context):
    user_id = update.message.from_user.id
    mes = update.message.text.strip()
    if mes.lower() == 'назад':
        sessionStorage[user_id]['test_stage'] = -1
        sessionStorage[user_id]['section_info_checked'] = 0
        sessionStorage[user_id]['user_data'] = get(f"{FLASK_SERVER}/api/users/{user_id}").json()['user_data']
        if sessionStorage[user_id]['user_data']['aim'][-1] == ',':
            sessionStorage[user_id]['user_data']['aim'] = sessionStorage[user_id]['user_data']['aim'][:-1]
        return learning(update, context)
    if mes.lower() == 'завершить тест':
        sessionStorage[user_id]['test_stage'] += 1
        text = f"Вот результаты теста: \n"
        score = 0
        test = sessionStorage[user_id]['test']
        for ans_id in range(len(sessionStorage[user_id]['anss_given'])):
            ans = sessionStorage[user_id]['anss_given'][ans_id].lower().strip()
            text += '\n' + str(ans_id + 1) + '. ' + test[ans_id][0]
            text += f"\nВаш ответ: {ans}"
            if ans == test[ans_id][1].lower().strip():
                text += '\nПравильно ✓'
                score += 1
            else:
                text += '\nНеправильно ❌'
                text += f"\nВот правильный ответ: {test[ans_id][1]}"
        text = f"Тест закончен, ваш результат: {str(score)} из" \
                   f" {len(sessionStorage[user_id]['anss_given'])}\n" + text
        update.message.reply_text(text)
        sessionStorage[user_id]['test_stage'] = -1
        update.message.reply_text("Введите 'начать тест', чтобы пройти ещё один тест"
                                  "\nВведите 'назад' для перехода в личный кабинет",
                                  reply_markup=ReplyKeyboardMarkup([['начать тест'], ['назад']],
                                                                   one_time_keyboard=True))
        return 10
    if 'test_stage' not in sessionStorage[user_id].keys():
        sessionStorage[user_id]['test_stage'] = -1
        sessionStorage[user_id]['user_data'] = get(f"{FLASK_SERVER}/api/users/{user_id}").json()['user_data']
        if sessionStorage[user_id]['user_data']['aim'][-1] == ',':
            sessionStorage[user_id]['user_data']['aim'] = sessionStorage[user_id]['user_data']['aim'][:-1]

    aim = sessionStorage[user_id]['user_data']['aim'].split(',')
    if sessionStorage[user_id]['test_stage'] == -1:
        # показать все темы, предоставить выбор
        get_all_themes(update, context)
        update.message.reply_text("Чтобы начать тест по какой-либо теме, напишите её."
                                  "\n(строго как в сообщении)"
                                  "\nВы также можете написать 'назад' для возвращения в личный кабинет",
                                  reply_markup=themes_markup)
        sessionStorage[user_id]['anss_given'] = []
        sessionStorage[user_id]['test_stage'] += 1

        return 10
    elif sessionStorage[user_id]['test_stage'] == 0:
        from data.english_data import WORDS_FOR_LEARNING
        theme = mes.strip()
        found = 0
        sessionStorage[user_id]['curr_lesson'] = None
        for section in aim:
            if found:
                break
            for lesson in WORDS_FOR_LEARNING[section]['themes']:
                if lesson['title'] == theme:
                    sessionStorage[user_id]['curr_section'] = section
                    sessionStorage[user_id]['curr_lesson'] = lesson
                    found = 1
                    break
        if sessionStorage[user_id]['curr_lesson'] is None:
            update.message.reply_text("Введите пожалуйста существующую тему!", reply_markup=themes_markup)
            return 10
        if sessionStorage[user_id]['curr_section'] == 'разговорный':
            update.message.reply_text("Это тема раздела 'разговоный',"
                                      " поэтому здесь нет слов для теста", reply_markup=themes_markup_beg_test)
            return 10
        update.message.reply_text("Сейчас мы зададим вам несколько вопросов,"
                                  " а вы будете на них отвечать. \n Пожалуйста подождите пока сгенерируеться тест")
        sessionStorage[user_id]['test'] = get_test(user_id)
        sessionStorage[user_id]['anss_given'] = []
        update.message.reply_text(sessionStorage[user_id]['test'][0][0],
                                  reply_markup=ReplyKeyboardMarkup([['завершить тест']], one_time_keyboard=True))
        sessionStorage[user_id]['test_stage'] = 1
        return 10
    else:
        if sessionStorage[user_id]['test_stage'] == len(sessionStorage[user_id]['test']):
            sessionStorage[user_id]['anss_given'].append(mes.lower().strip())
            sessionStorage[user_id]['test_stage'] += 1
            text = f"Вот результаты теста: \n"
            score = 0
            test = sessionStorage[user_id]['test']
            for ans_id in range(len(sessionStorage[user_id]['anss_given'])):
                ans = sessionStorage[user_id]['anss_given'][ans_id].lower().strip()
                text += '\n' + str(ans_id + 1) + '. ' + test[ans_id][0]
                text += f"\nВаш ответ: {ans}"
                if ans == test[ans_id][1].lower().strip():
                    text += '\nПравильно ✓'
                    score += 1
                else:
                    text += '\nНеправильно ❌'
                    text += f"\nВот правильный ответ: {test[ans_id][1]}"
            text = f"Тест закончен, ваш результат: {str(score)} из" \
                       f" {len(sessionStorage[user_id]['anss_given'])}\n" + text
            update.message.reply_text(text)
            sessionStorage[user_id]['test_stage'] = -1
            update.message.reply_text("Введите 'начать тест', чтобы пройти ещё один тест"
                                      "\nВведите 'назад' для перехода в личный кабинет",
                                      reply_markup=ReplyKeyboardMarkup([['начать тест'], ['назад']],
                                                                       one_time_keyboard=True))
            return 10
        else:
            update.message.reply_text(sessionStorage[user_id]['test'][sessionStorage[user_id]['test_stage']][0],
                                      reply_markup=ReplyKeyboardMarkup([['завершить тест']], one_time_keyboard=True))
            sessionStorage[user_id]['anss_given'].append(mes.lower().strip())
            sessionStorage[user_id]['test_stage'] += 1
            return 10


def stop_test(update, context):
    user_id = update.message.from_user.id
    text = f"Вот результаты теста: \n"
    score = 0
    test = sessionStorage[user_id]['test']
    if len(sessionStorage[user_id]['anss_given']) == 0:
        text = ""
    for ans_id in range(len(sessionStorage[user_id]['anss_given'])):
        ans = sessionStorage[user_id]['anss_given'][ans_id].lower().strip()
        text += '\n' + str(ans_id + 1) + '. ' + test[ans_id][0]
        text += f"\nВаш ответ: {ans}"
        if ans == test[ans_id][1].lower().strip():
            text += '\nПравильно ✓'
            score += 1
        else:
            text += '\nНеправильно ❌'
            text += f"\nВот правильный ответ: {test[ans_id][1]}"
    text = f"Тест закончен, ваш результат: {str(score)} из" \
               f" {len(sessionStorage[user_id]['anss_given'])}\n" + text
    update.message.reply_text(text)
    sessionStorage[user_id]['test_stage'] = -1
    update.message.reply_text("Введите 'начать тест', чтобы пройти ещё один тест"
                              "\nВведите название любой темы, из выше перечисленных,"
                              " чтобы увидеть её содержание и продолжить обучение"
                              "\nВведите 'назад' для перехода в личный кабинет"
                              "\nВведите 'завершить тест', что бы досрочно завершить тест",
                              reply_markup=themes_markup_beg_test)
    return 10


def unauthed(update, context):
    update.message.reply_text("Вы не авторизованы, чтобы начать работу выполните команду /start")


if __name__ == "__main__":
    flask_server = sys.argv[1]
    if flask_server[-1] == '/':
        flask_server = flask_server[:-1]
    print(f"Flask Server url was given: {flask_server}")
    FLASK_SERVER = flask_server
    # REQUEST_KWARGS = {
    #     'proxy_url': 'socks5://localhost:9150',  # Адрес прокси сервера
    # }
    # updater = Updater(TOKEN_FOR_TELEGRAM_BOT, use_context=True, request_kwargs=REQUEST_KWARGS)
    updater = Updater(TOKEN_FOR_TELEGRAM_BOT, use_context=True)
    dp = updater.dispatcher
    print("connected to bot")
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        fallbacks=[CommandHandler('logout', logout)],
        states={
            # регистрация
            1: [MessageHandler(Filters.text, register)],
            # авторизация
            2: [MessageHandler(Filters.text, login)],
            # пользователь в MYENG
            3: [CommandHandler("logout", logout),
                CommandHandler("get_other_links", get_other_links),
                CommandHandler("get_people_to_chat", get_people_to_chat),
                CommandHandler("get_myeng_map", get_myeng_map),
                CommandHandler("help", learning_help),
                CommandHandler("get_lesson", get_lesson),
                CommandHandler("change_aim", change_aim),
                CommandHandler("FromEngToRUS", switch_to_from_en_to_ru),
                CommandHandler("FromRusToEng", switch_to_from_ru_to_en),
                CommandHandler("run_test", run_test),
                MessageHandler(Filters.text, learning)],
            4: [MessageHandler(Filters.text, get_other_links)],  # other links
            5: [CommandHandler("get_people_to_chat", get_people_to_chat),
                CommandHandler('help_in_lesson', help_in_lesson),
                CommandHandler("return_to_cabinet", return_to_cabinet),
                MessageHandler(Filters.text, get_lesson)],  # lesson
            6: [MessageHandler(Filters.text, change_aim)],  # aim changing
            8: [CommandHandler("FromEngToRUS", switch_to_from_en_to_ru),
                CommandHandler("FromRusToEng", switch_to_from_ru_to_en),
                MessageHandler(Filters.text, from_ru_to_en)],  # translate from ru to en
            9: [CommandHandler("FromEngToRUS", switch_to_from_en_to_ru),
                CommandHandler("FromRusToEng", switch_to_from_ru_to_en),
                MessageHandler(Filters.text, from_en_to_ru)],  # translate from en to ru
            10: [MessageHandler(Filters.text, run_test), CommandHandler("stop_test", stop_test)]
        }
    )
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text, unauthed))
    updater.start_polling()
    updater.idle()
