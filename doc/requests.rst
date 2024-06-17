``URL`` - bazowy adres serwera

1.  Podaj listę użytkowników.

    Zwraca wykaz nazw wszystkich użytkowników z liczbami znalezionych przez nich krasnali.

    -   adres: ``URL/users``
    -   parametry (payload): brak
    -   dane zwracane (JSON)::

            {"users": [
                {
                 "user_id": integer,
                 "name": string,
                 "found": integer
                },
                {
                 "user_id":
                 ...}
                ]
            }

2.  Podaj listę krasnali:

    Zwraca wykaz nazw wszystkich krasnali z ich współrzędnymi i zdjęciami.

    -   adres: ``URL/gnomes``
    -   parametry (payload): brak
    -   dane zwracane (JSON)::

            {"gnomes": [
                {
                 "gnome_id": integer,
                 "name": string,
                 "longitude": float,
                 "latitude": float,
                 "photo": string base64 encoded
                },
                {
                 "gnome_id":
                 ...}
                ]
            }

3.  Zarejestruj znalezienie krasnala:

    Rejestruje znalezienie krasnala przez daego użytkownika.

    -   adres: ``URL/visit``
    -   parametry (payload)::

            {
             "user_id": integer,
             "gnome_id": integer,
             "photo": string base64 encoded
            }

        Jako moment znalezienia krasnala, przyjmowany jest aktualny czas.

    -   dane zwracane (JSON): brak

4.  Dodaj komentarz do krasnala:

    Rejestruje dodanie komentarza do krasnala.

    -   adres: ``URL/comment``
    -   parametry (payload)::

            {
             "user_id": integer,
             "gnome_id": integer,
             "comment": string
            }

        Jako moment dodanie komentarza, przyjmowany jest aktualny czas.

    -   dane zwracane (JSON): brak

5.  Podaj komentarze krasnala.

    Zwraca wszystkie komentarze dotyczące danego krasnala.

    -   adres: ``URL/gnome_comments``
    -   parametry (payload)::

            {
             "gnome_id": integer
            }

    -   dane zwracane (JSON)::

            {"comments": [
                {
                 "user_id": integer,
                 "comment": string,
                 "datetime": ISO 8601 formatted string
                },
                {
                 "user_id": integer,
                 ...}
                ]
            }

6.  Wylosuj krasnala.

    Zwraca krasnala do znalezienia dzisiaj.

    -   adres: ``URL/draw``
    -   parametry (payload)::

            {
             "user_id": integer
            }

    -   dane zwracane (JSON)::

            {
             "gnome_id": integer
            }
