import os
import sqlite3
import base64
import json

from flask import Flask, render_template, request, jsonify, redirect, url_for

import db

app = Flask(__name__)

#strona domowa serwera

@app.route('/')
def home():
    return render_template('home.html')


# @app.route('/enternew')
# def new_student():
#     return render_template('hello_30_student.html')


#lista wszystkich gnomów

@app.route('/gnomes')
def list_gnomes():
    con = sqlite3.connect(database)
    con.row_factory = sqlite3.Row
    
    cur = con.cursor()
    cur.execute("select * from gnome")
    
    rows = cur.fetchall();
    for row in rows:
        db.write_file(row[4], f'photo/{row[1]}.jpg')

    return render_template("gnomes.html",rows = rows)


#zwraca dane krasnala o podanym ID
@app.route('/gnomes/<int:gnome_id>', methods=['GET'])
def list_gnome(gnome_id):
    # Połączenie z bazą danych
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Wykonanie zapytania SQL
    cur.execute('SELECT gnome_id, name, longitude, latitude, photo FROM gnome WHERE gnome_id = ?', (gnome_id,))
    gnome = cur.fetchone()  # fetchone() zwraca jeden rekord lub None, jeśli nie znaleziono rekordu

    # Zamknięcie połączenia z bazą danych
    conn.close()

    # Sprawdzenie, czy krasnal istnieje
    if gnome:
        # Renderowanie JSON z danymi krasnala
        return jsonify({
            'name': gnome['name'],
            'gnome_id': gnome['gnome_id'],
            'longitude': gnome['longitude'],
            'latitude': gnome['latitude'],
        })
    else:
        # Zwrócenie informacji o braku krasnala
        return jsonify({'error': 'Gnome not found'}), 404


#Wyswietlenie rankingu
@app.route('/users', methods=['GET'])
def list_users():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Zapytanie SQL zliczające wizyty dla każdego użytkownika i sortujące wyniki według liczby wizyt
    cur.execute('''
        SELECT u.user_id, u.login, COUNT(v.visit_id) as visit_count
        FROM user u
        LEFT JOIN visit v ON u.user_id = v.user_id
        GROUP BY u.user_id
        ORDER BY visit_count DESC
        LIMIT 10
    ''')

    users = cur.fetchall()
    conn.close()

    user_list = []
    for user in users:
        user_list.append({
            'login': user['login'],
            'visitcount': user['visit_count']
        })

    return jsonify(user_list)


#wyswielenie danych uzytkownika o podanym id

@app.route('/users/<int:user_id>')
def get_user(user_id):
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT user_id, login, password FROM user WHERE user_id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()
    if user:
        return render_template('user_detail.html', user=user)
    else:
        return "User not found", 404

#dodanie wizyty do bazy danych
@app.route('/visit', methods=['POST'])
def add_visit():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    user_id = data.get('user_id')
    gnome_id = data.get('gnome_id')
    visit_date = data.get('visit_date')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    print([user_id, gnome_id, visit_date, latitude, longitude])
    if not all([user_id, gnome_id, visit_date, latitude, longitude]):
        return jsonify({'error': 'Missing data'}), 400

    try:
        with sqlite3.connect(database) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            # Pobierz współrzędne krasnala
            cur.execute("SELECT latitude, longitude FROM gnome WHERE gnome_id = ?", (gnome_id,))
            gnome = cur.fetchone()
            if not gnome:
                return jsonify({'error': 'Gnome not found'}), 404

            gnome_lat = gnome['latitude']
            gnome_lon = gnome['longitude']

            # Sprawdź odległość
            distance_threshold = 100 / 111000  # Przelicznik 10 metrów na stopnie
            if abs(latitude - gnome_lat) > distance_threshold or abs(longitude - gnome_lon) > distance_threshold:
                return jsonify({'error': 'You are not within 10 meters of the gnome'}), 400

            # Dodaj wizytę
            cur.execute('''
                INSERT INTO visit (user_id, gnome_id, visit_date)
                VALUES (?, ?, ?)
            ''', (user_id, gnome_id, visit_date))
            conn.commit()

            return jsonify({'message': 'Visit successfully logged'}), 201

    except sqlite3.IntegrityError:
        return jsonify({'error': 'This visit has already been logged'}), 409
    except Exception as e:
        app.logger.error(f'An error occurred: {e}')
        return jsonify({'error': 'Failed to log visit due to an internal error'}), 500

#Pobranie danych z wizyty o podanym ID
@app.route('/visit/<int:visit_id>', methods=['GET'])
def get_visit(visit_id):
    try:
        with sqlite3.connect(database) as conn:
            conn.row_factory = sqlite3.Row  # This enables column access by name
            cur = conn.cursor()
            cur.execute("SELECT * FROM visit WHERE visit_id = ?", (visit_id,))
            visit = cur.fetchone()

            if visit:
                visit_dict = dict(visit)
                # Optionally convert the photo from bytes to a string if it's stored in binary format
                return jsonify(visit_dict), 200
            else:
                return jsonify({'error': 'Visit not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Dodanie komentarza pod gnomem o danym id
@app.route('/gnomes/<int:gnome_id>/comment', methods=['POST'])
def add_comment(gnome_id):
    if not request.json or 'coment' not in request.json or 'user_id' not in request.json:
        print (request.json)
        return jsonify({'error': 'Missing comment or user_id in request'}), 400

    comment = request.json['coment']
    user_id = request.json['user_id']

    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()

        # Check if the visit exists for the given user and gnome
        cur.execute('SELECT visit_id FROM visit WHERE user_id = ? AND gnome_id = ?', (user_id, gnome_id))
        visit = cur.fetchone()

        if not visit:
            return jsonify({'error': 'No visit found for this user and gnome'}), 404

        visit_id = visit[0]

        # Insert the comment
        cur.execute('INSERT INTO user_comment (visit_id, coment, user_id) VALUES (?, ?, ?)',
                    (visit_id, comment, user_id))
        conn.commit()

        return jsonify({'message': 'Comment added successfully'}), 201

    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'This user cannot comment twice on the same visit'}), 409

    except Exception as e:
        app.logger.error(f'Error adding comment: {e}')
        return jsonify({'error': 'Failed to add comment'}), 500

    finally:
        conn.close()


#wyswietlenie wszystkich komentarzy pod gnomem o danym id
@app.route('/gnomes/<int:gnome_id>/comments', methods=['GET'])
def get_gnome_comments(gnome_id):
    try:
        comments = db.get_comments(database, gnome_id)
        formatted_comments = [{'login': comment['login'], 'comment': comment['comment']} for comment in comments]
        return jsonify(formatted_comments), 200
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve comments: {e}'}), 500

#rejestracja uzytkownika, dodanie go do bazy
@app.route('/register', methods=['POST'])
def create_user():
    try:
        data = request.json
        if not data or 'login' not in data or 'password' not in data:
            return jsonify({'error': 'Missing login or password in request'}), 400

        login = data['login']
        password = data['password']

        # Create user
        db.create_user(database, login, password)

        return jsonify({'message': 'User created successfully'}), 201
    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'User already exists'}), 409
    except Exception as e:
        app.logger.error(f'Error creating user: {e}')
        return jsonify({'error': 'Failed to create user'}), 500


#Logowanie, sprawdzenie czy dana kombinacja loginu i hasla isnieje w bazie
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data or 'login' not in data or 'password' not in data:
            return jsonify({'error': 'Missing login or password in request'}), 400

        login = data['login']
        password = data['password']

        # Verify user
        if db.verify_user(database, login, password):
            user_id = db.get_user_id(database, login)
            return jsonify({'message': 'Login successful', 'userId': user_id}), 200
        else:
            return jsonify({'error': 'Invalid login or password'}), 401
    except Exception as e:
        app.logger.error(f'Error during login: {e}')
        return jsonify({'error': 'Failed to login'}), 500



#zwrocenie zliczonych wizyt dla jednego uzytkownika
@app.route('/users/<int:user_id>/visits', methods=['GET'])
def get_user_visits(user_id):
    try:
        visits, count = db.get_user_visits(database, user_id)
        return jsonify({'visits': visits, 'count': count}), 200
    except Exception as e:
        app.logger.error(f'Error fetching visits for user {user_id}: {e}')
        return jsonify({'error': f'Failed to fetch visits for user {user_id}'}), 500


#wszystkie mozliwe osiagniecia
@app.route('/achievements')
def list_achievements():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute('SELECT * FROM user_level')
    achievements = cur.fetchall()
    conn.close()

    return render_template('achievements.html', achievements=achievements)


#Wyswietlenie osiagniec uzytkownika o danym ID
@app.route('/users/<int:user_id>/achievements', methods=['GET'])
def user_achievements(user_id):
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Sprawdź, czy użytkownik istnieje
    cur.execute('SELECT login FROM user WHERE user_id = ?', (user_id,))
    user = cur.fetchone()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_login = user['login']

    # Pobierz liczbę wizyt (odwiedzonych krasnali) przez użytkownika
    cur.execute('SELECT COUNT(DISTINCT gnome_id) as gnome_count FROM visit WHERE user_id = ?', (user_id,))
    user_gnome_count = cur.fetchone()['gnome_count']

    # Pobierz wszystkie osiągnięcia
    cur.execute('SELECT * FROM user_level')
    all_achievements = cur.fetchall()

    # Sprawdź, które osiągnięcia użytkownik zdobył
    user_achievements = []
    for achievement in all_achievements:
        if user_gnome_count >= achievement['gnome_count']:
            user_achievements.append({
                'name': achievement['name'],
                'gnome_count': achievement['gnome_count'],
            })

    conn.close()

    if user_achievements:
        return jsonify({
            'user_login': user_login,
            'achievements': user_achievements
        })
    else:
        return jsonify({'achievements': 'Użytkownik nie zdobył osiągnięć'})

#Losuje gnoma i zwraca jego id, po czym przechodzi na strone gnoma o tym id i zwraca informacje o nim
@app.route('/users/<int:user_id>/draw_gnome', methods=['GET'])
def draw_gnome_for_user(user_id):
    drawn_gnome = db.draw_gnome(database, user_id)

    if drawn_gnome:
        return redirect(url_for('list_gnome', gnome_id=drawn_gnome))
    else:
        return jsonify({'error': 'No gnome to draw for this user or user not found'}), 404

if __name__ == '__main__':
    database = '../instance/pokegnome.sqlite3'
    app.run(host='0.0.0.0', port=5000, debug=True)  # Use 0.0.0.0 to accept connections from all IP addresses
    app.run(debug = True)
