1.  Tabela `user`.

    Lista użytkowników zarejestrowanych w aplikacji.

    -   `user_id`
        identyfikator użytkownika

    -   `login`
        nazwa użytkownika, która identyfikuje użytownika

    -   `passord`
        hasło użytkownika do uwierzytelniania w systemie

2.  Tabela `gnome`.

    Lista kransoludków możliwych do znalezienia.

    -   `gnome_id
		identyfikator krasnoludka

	-   `name`
		nazwa (imię) krasnoludka

	-   `longitude`
		długość geograficzna lokacji krasnoludka

	-   `latitude`
		szerokość geograficzna lokacji krasnoludka

	-   `photo`
        zdjęcie krasnoludka

3.  Tabela `visit`

    rejestr znalezień krasnoludków.

	-   `user_id`
		identyfikator użytkownika, który znalazł krasnoludka

	-   `gnome_id`
		identyfikator znalezionego krasnoludka

	-   `photo`
		ewentualne zdjęcie znalezionego krasnoludka

	-   `visit_date`
        data i czas znalezienia krasnoludka

    .. note:: Dany użytkownik może znaleźć danego krasnoludka tylko raz!

4.  Tabela `user_comment`

    Rejestr komentarzy dotyczących krasnoludków.

    -   `gnome_id`
		identyfikator komentowanego krasnoludka

    -   `comment`
        treść komentarza

    -   `user_id`
        użytkownik komentujący krasnoludka

    -   `comment_date`
        data i czas zamieszczenie komentarza

5.  Tabela `user_level`

	-   `level_id`
        identyfikator osiągniętego poziomu

	-   `name`
		nazwa poziomu

	-   `gnome_count`
		liczba krasnloudków, którą trzeba znaleźć, aby uzyskać dany poziom

	-   `time_max`
        maksymalny czas (w dniach), w czasie których podana liczba krasnoludków
        musi zostać znaleziona, aby uzyskać dany poziom
