###########
PokeGnomeGO
###########

Kierunek: CBE

Przedmiot: Aplikacje mobilne

Grupa: Wtorek 17:05 TP

Tytuł projektu: Aplikacja PokeGnomeGO

Skład grupy projektowej:

-   Emilia Cyprych
-   Paulina Kołodziejczyk
-   Monika Śliwowska

**************
Temat projektu
**************

Tematem projektu jest napisanie aplikacji na urządzenia mobilne z systemem Android, która będzie umożliwiała oznaczanie wrocławskich krasnali, jakich zdjęcia zrobił użytkownik.
"Złapany" w ten sposób krasnal będzie oznaczony na mapie miasta, a jego zdjęcie dostępne w aplikacji użytkownika.

Aplikacja będzie nazywać się "PokeGnomeGO" i każdego dnia użytkownik będzie mógł dzięki potrząsaniu telefonem wylosować krasnala.
Zadaniem użytkownika będzie dotarcie do wskazanej lokalizacji oraz zrobienie zdjęcia krasnala.
Losowanie będzie odbywać się metodą "bez oddawania" - jeśli użytkownik wypełni zadanie, nie wylosuje ponownie już zdobytego krasnala. 

Koniec gry ma miejsce, kiedy użytkownik zrobi zdjęcia wszystkim krasnalom w bazie danych.

*************
Cele projektu
*************

Stworzenie aplikacji mobilnej o nazwie "PokeGnomeGO" na urządzenia z systemem Android.
Użytkownicy codziennie będą mogli wylosować zadanie odwiedzenia konkretnego, jeszcze nie zdobytego przez nich krasnala.
Ich celem będzie odwiedzenie wszystkich lokalizacji krasnali naniesionych na mapę Wrocławia.

Odwiedzone lokalizacje z krasnalami będą przypięte na mapie miasta pinezkami.
Po kliknięciu na konkretną pinezkę, użytkownik będzie mógł zobaczyć zdjęcie, które tam zrobił.

Stworzenie interfejsu graficznego, który pozwoli na komfortowe użytkowanie aplikacji.

Stworzenie dokumentacji technicznej zawierającej opis kodu użytego do napisania aplikacji oraz bazy danych, a także skrót procesu tworzenia projektu.

Plan przewiduje zakończenie pracy nad aplikacją oraz jej dokumentacją techniczną do terminu ósmych zajęć.

*******************
Stos technologiczny
*******************

Front-end
=========

-   aplikacja dla urządzeń mobilnych napisana w języku Kotlin. 
-   biblioteki do komunikacji aplikacji z Google Maps
-   użycie Edytora układu Android Studio do stworzenia interface’u użytkownika
-   użycie CameraX do robienia zdjęć przez użytkownika

Back-end
========

-   serwer napisany w języku Python
-   użycie frameworka Flask do zapewnienia funkcjonalności serwera
-   baza danych MySQL/MariaDB
-   PHPMyAdmin do podglądu bazy danych
-   biblioteka mySQL-connector do komunikacji z bazą danych
-   Docker do konteneryzacji serwera projektu

Schemat
=======

Elementy projektu:

-   aplikacja moblina skomunikowana z serwerem Flask
-   serwer Flask pośredniczący przy komunikacji aplikacji z bazą danych MySQL/MariaDB i obsługujący zapytania RESTful API
-   baza danych MySQL/MariaDB skomunikowana z serwerem Flask
  

.. include:: schemat.txt
   :literal:

.. uml::

    @startuml

    package "Serwer" {
        [Flask] - [MySQL]
        [Flask] ..> HTTP
    }

    [Aplikacja] ..> HTTP

    @enduml

Rys 1. Schemat działania aplikacji

Narzędzia
=========

-   Docker do konteneryzacji usług
-   Github do komunikacji i wspólnej pracy nad projektem
-   Paint do tworzenia grafik
-   Android Studio – IDE do tworzenia front-endu w języku Kotlin
-   PyCharm – IDE do tworzenia back-endu w języku Python

***********
Baza danych
***********

Na podstawie dokumentacji projektowej można zbudować schemat bazy danych dla aplikacji mobilnej "PokeGnomeGO".

.. include:: database.rst

***********************************
Opis strategii serializacji zasobów
***********************************

Serializacja zasobów dla aplikacji "PokeGnomeGO" dotycząca wymiany danych między aplikacją mobilną a serwerem będzie opierać się na:

-   RESTful API: 

    -   komunikacja między klientem a serwerem odbywająca się za pomocą API RESTful, które używa standardowego formatu JSON do przesyłania danych. 


-   biblioteki do serializacji/deserializacji:

    -   dla Kotlin: Gson lub Moshi, które umożliwiają łatwą serializację obiektów Kotlin do formatu JSON i odwrotnie.

    -   dla Python: biblioteka Flask-JSON lub Marshmallow, które umożliwiają łatwą serializację odpowiedzi serwera do JSON.

***************************************
Komunikacja między aplikacją i serwerem
***************************************

Komunikacja jest realizowana poprzez wysyłanie żądań na ustalone adresy.
Wynik przetwarzania żądania jest zwracany statusem (z ew. danymi).

.. include:: requests.rst
