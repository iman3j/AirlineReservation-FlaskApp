from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
pymysql.install_as_MySQLdb()
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'replace_with_some_secret'

# --- CONFIGURE DB ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Abc@123' 
app.config['MYSQL_DB'] = 'AirlineReservationSystem'

mysql = MySQL(app)


def fetchall(query, args=None):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query, args or ())
    rows = cur.fetchall()
    cur.close()
    return rows

def fetchone(query, args=None):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(query, args or ())
    row = cur.fetchone()
    cur.close()
    return row

def execute(query, args=None):
    cur = mysql.connection.cursor()
    cur.execute(query, args or ())
    mysql.connection.commit()
    lastrowid = cur.lastrowid
    cur.close()
    return lastrowid

# --- Routes and CRUD handlers ---
@app.route('/')
def index():
    counts = {}
    tables = ['Airports','Flights','Passengers','Tickets','Payments','Crew','Routes']
    for t in tables:
        r = fetchone(f"SELECT COUNT(*) AS cnt FROM {t}")
        counts[t] = r['cnt'] if r else 0
    return render_template('index.html', counts=counts)

# Airports
@app.route('/airports')
def airports_list():
    q = request.args.get('q')
    if q:
        rows = fetchall("SELECT * FROM Airports WHERE name LIKE %s OR city LIKE %s OR country LIKE %s OR code LIKE %s", (f"%{q}%",)*4)
    else:
        rows = fetchall("SELECT * FROM Airports")
    return render_template('airports.html', airports=rows)

@app.route('/airports/add', methods=['GET','POST'])
def airport_add():
    if request.method == 'POST':
        name = request.form['name']
        city = request.form.get('city') or None
        country = request.form.get('country') or None
        code = request.form.get('code') or None
        try:
            execute("INSERT INTO Airports(name,city,country,code) VALUES(%s,%s,%s,%s)", (name,city,country,code))
            flash('Airport added successfully','success')
            return redirect(url_for('airports_list'))
        except Exception as e:
            flash(str(e),'danger')
    return render_template('airport_form.html', airport=None)

@app.route('/airports/edit/<int:aid>', methods=['GET','POST'])
def airport_edit(aid):
    airport = fetchone('SELECT * FROM Airports WHERE airport_id=%s', (aid,))
    if request.method=='POST':
        name = request.form['name']
        city = request.form.get('city') or None
        country = request.form.get('country') or None
        code = request.form.get('code') or None
        try:
            execute('UPDATE Airports SET name=%s, city=%s, country=%s, code=%s WHERE airport_id=%s', (name,city,country,code,aid))
            flash('Airport updated','success')
            return redirect(url_for('airports_list'))
        except Exception as e:
            flash(str(e),'danger')
    return render_template('airport_form.html', airport=airport)

@app.route('/airports/delete/<int:aid>', methods=['POST'])
def airport_delete(aid):
    try:
        execute('DELETE FROM Airports WHERE airport_id=%s', (aid,))
        flash('Airport deleted','success')
    except Exception as e:
        flash(str(e),'danger')
    return redirect(url_for('airports_list'))

# Flights
@app.route('/flights')
def flights_list():
    q = request.args.get('q')
    if q:
        rows = fetchall("SELECT f.*, a1.name AS source_name, a2.name AS dest_name FROM Flights f LEFT JOIN Airports a1 ON f.source_airport_id=a1.airport_id LEFT JOIN Airports a2 ON f.dest_airport_id=a2.airport_id WHERE f.airline LIKE %s OR a1.name LIKE %s OR a2.name LIKE %s", (f"%{q}%",)*3)
    else:
        rows = fetchall('SELECT f.*, a1.name AS source_name, a2.name AS dest_name FROM Flights f LEFT JOIN Airports a1 ON f.source_airport_id=a1.airport_id LEFT JOIN Airports a2 ON f.dest_airport_id=a2.airport_id')
    airports = fetchall('SELECT * FROM Airports')
    return render_template('flights.html', flights=rows, airports=airports)

@app.route('/flights/add', methods=['GET','POST'])
def flight_add():
    airports = fetchall('SELECT * FROM Airports')
    if request.method=='POST':
        airline = request.form['airline']
        source = request.form.get('source_airport_id') or None
        dest = request.form.get('dest_airport_id') or None
        departure_time = request.form.get('departure_time') or None
        arrival_time = request.form.get('arrival_time') or None
        status = request.form.get('status') or None
        try:
            execute('INSERT INTO Flights(airline, source_airport_id, dest_airport_id, departure_time, arrival_time, status) VALUES(%s,%s,%s,%s,%s,%s)', (airline, source or None, dest or None, departure_time or None, arrival_time or None, status))
            flash('Flight added','success')
            return redirect(url_for('flights_list'))
        except Exception as e:
            flash(str(e),'danger')
    return render_template('flight_form.html', flight=None, airports=airports)

@app.route('/flights/edit/<int:fid>', methods=['GET','POST'])
def flight_edit(fid):
    flight = fetchone('SELECT * FROM Flights WHERE flight_id=%s', (fid,))
    airports = fetchall('SELECT * FROM Airports')
    if request.method=='POST':
        airline = request.form['airline']
        source = request.form.get('source_airport_id') or None
        dest = request.form.get('dest_airport_id') or None
        departure_time = request.form.get('departure_time') or None
        arrival_time = request.form.get('arrival_time') or None
        status = request.form.get('status') or None
        try:
            execute('UPDATE Flights SET airline=%s, source_airport_id=%s, dest_airport_id=%s, departure_time=%s, arrival_time=%s, status=%s WHERE flight_id=%s', (airline, source or None, dest or None, departure_time or None, arrival_time or None, status, fid))
            flash('Flight updated','success')
            return redirect(url_for('flights_list'))
        except Exception as e:
            flash(str(e),'danger')
    return render_template('flight_form.html', flight=flight, airports=airports)

@app.route('/flights/delete/<int:fid>', methods=['POST'])
def flight_delete(fid):
    try:
        execute('DELETE FROM Flights WHERE flight_id=%s', (fid,))
        flash('Flight deleted','success')
    except Exception as e:
        flash(str(e),'danger')
    return redirect(url_for('flights_list'))

# Passengers
@app.route('/passengers')
def passengers_list():
    q = request.args.get('q')
    if q:
        rows = fetchall("SELECT * FROM Passengers WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s OR passport_no LIKE %s", (f"%{q}%",)*4)
    else:
        rows = fetchall('SELECT * FROM Passengers')
    return render_template('passengers.html', passengers=rows)

@app.route('/passengers/add', methods=['GET','POST'])
def passenger_add():
    if request.method=='POST':
        name = request.form['name']
        email = request.form.get('email') or None
        phone = request.form.get('phone') or None
        passport_no = request.form.get('passport_no') or None
        loyalty_points = request.form.get('loyalty_points') or 0
        try:
            execute('INSERT INTO Passengers(name,email,phone,passport_no,loyalty_points) VALUES(%s,%s,%s,%s,%s)', (name,email,phone,passport_no,loyalty_points))
            flash('Passenger added','success')
            return redirect(url_for('passengers_list'))
        except Exception as e:
            flash(str(e),'danger')
    return render_template('passenger_form.html', passenger=None)

@app.route('/passengers/edit/<int:pid>', methods=['GET','POST'])
def passenger_edit(pid):
    passenger = fetchone('SELECT * FROM Passengers WHERE passenger_id=%s', (pid,))
    if request.method=='POST':
        name = request.form['name']
        email = request.form.get('email') or None
        phone = request.form.get('phone') or None
        passport_no = request.form.get('passport_no') or None
        loyalty_points = request.form.get('loyalty_points') or 0
        try:
            execute('UPDATE Passengers SET name=%s, email=%s, phone=%s, passport_no=%s, loyalty_points=%s WHERE passenger_id=%s', (name,email,phone,passport_no,loyalty_points,pid))
            flash('Passenger updated','success')
            return redirect(url_for('passengers_list'))
        except Exception as e:
            flash(str(e),'danger')
    return render_template('passenger_form.html', passenger=passenger)

@app.route('/passengers/delete/<int:pid>', methods=['POST'])
def passenger_delete(pid):
    try:
        execute('DELETE FROM Passengers WHERE passenger_id=%s', (pid,))
        flash('Passenger deleted','success')
    except Exception as e:
        flash(str(e),'danger')
    return redirect(url_for('passengers_list'))

# Tickets
@app.route('/tickets')
def tickets_list():
    q = request.args.get('q')
    if q:
        rows = fetchall("SELECT t.*, p.name AS passenger_name, f.airline AS flight_airline FROM Tickets t LEFT JOIN Passengers p ON t.passenger_id=p.passenger_id LEFT JOIN Flights f ON t.flight_id=f.flight_id WHERE p.name LIKE %s OR f.airline LIKE %s OR t.seat_no LIKE %s", (f"%{q}%",)*3)
    else:
        rows = fetchall('SELECT t.*, p.name AS passenger_name, f.airline AS flight_airline FROM Tickets t LEFT JOIN Passengers p ON t.passenger_id=p.passenger_id LEFT JOIN Flights f ON t.flight_id=f.flight_id')
    flights = fetchall('SELECT * FROM Flights')
    passengers = fetchall('SELECT * FROM Passengers')
    return render_template('tickets.html', tickets=rows, flights=flights, passengers=passengers)

@app.route('/tickets/add', methods=['GET','POST'])
def ticket_add():
    flights = fetchall('SELECT * FROM Flights')
    passengers = fetchall('SELECT * FROM Passengers')
    if request.method=='POST':
        flight_id = request.form.get('flight_id') or None
        passenger_id = request.form.get('passenger_id') or None
        seat_no = request.form.get('seat_no') or None
        klass = request.form.get('class') or None
        price = request.form.get('price') or None
        booking_date = request.form.get('booking_date') or None
        status = request.form.get('status') or None
        try:
            execute('INSERT INTO Tickets(flight_id, passenger_id, seat_no, class, price, booking_date, status) VALUES(%s,%s,%s,%s,%s,%s,%s)', (flight_id, passenger_id, seat_no, klass, price, booking_date, status))
            flash('Ticket added','success')
            return redirect(url_for('tickets_list'))
        except Exception as e:
            flash(str(e),'danger')
    return render_template('ticket_form.html', ticket=None, flights=flights, passengers=passengers)

@app.route('/tickets/edit/<int:tid>', methods=['GET','POST'])
def ticket_edit(tid):
    ticket = fetchone('SELECT * FROM Tickets WHERE ticket_id=%s', (tid,))
    flights = fetchall('SELECT * FROM Flights')
    passengers = fetchall('SELECT * FROM Passengers')
    if request.method=='POST':
        flight_id = request.form.get('flight_id') or None
        passenger_id = request.form.get('passenger_id') or None
        seat_no = request.form.get('seat_no') or None
        klass = request.form.get('class') or None
        price = request.form.get('price') or None
        booking_date = request.form.get('booking_date') or None
        status = request.form.get('status') or None
        try:
            execute('UPDATE Tickets SET flight_id=%s, passenger_id=%s, seat_no=%s, class=%s, price=%s, booking_date=%s, status=%s WHERE ticket_id=%s', (flight_id, passenger_id, seat_no, klass, price, booking_date, status, tid))
            flash('Ticket updated','success')
            return redirect(url_for('tickets_list'))
        except Exception as e:
            flash(str(e),'danger')
    return render_template('ticket_form.html', ticket=ticket, flights=flights, passengers=passengers)

@app.route('/tickets/delete/<int:tid>', methods=['POST'])
def ticket_delete(tid):
    try:
        execute('DELETE FROM Tickets WHERE ticket_id=%s', (tid,))
        flash('Ticket deleted','success')
    except Exception as e:
        flash(str(e),'danger')
    return redirect(url_for('tickets_list'))

# Payments
@app.route('/payments')
def payments_list():
    rows = fetchall('SELECT p.*, t.seat_no AS ticket_seat, t.status AS ticket_status FROM Payments p LEFT JOIN Tickets t ON p.ticket_id=t.ticket_id')
    tickets = fetchall('SELECT * FROM Tickets')
    return render_template('payments.html', payments=rows, tickets=tickets)

@app.route('/payments/add', methods=['GET','POST'])
def payment_add():
    tickets = fetchall('SELECT * FROM Tickets')
    if request.method=='POST':
        ticket_id = request.form.get('ticket_id') or None
        amount = request.form.get('amount') or None
        method = request.form.get('method') or None
        status = request.form.get('status') or None
        try:
            execute('INSERT INTO Payments(ticket_id, amount, method, status) VALUES(%s,%s,%s,%s)', (ticket_id, amount, method, status))
            flash('Payment added','success')
            return redirect(url_for('payments_list'))
        except Exception as e:
            flash(str(e),'danger')
    return render_template('payment_form.html', payment=None, tickets=tickets)

@app.route('/payments/edit/<int:pid>', methods=['GET','POST'])
def payment_edit(pid):
    payment = fetchone('SELECT * FROM Payments WHERE payment_id=%s', (pid,))
    tickets = fetchall('SELECT * FROM Tickets')
    if request.method=='POST':
        ticket_id = request.form.get('ticket_id') or None
        amount = request.form.get('amount') or None
        method = request.form.get('method') or None
        status = request.form.get('status') or None
        try:
            execute('UPDATE Payments SET ticket_id=%s, amount=%s, method=%s, status=%s WHERE payment_id=%s', (ticket_id, amount, method, status, pid))
            flash('Payment updated','success')
            return redirect(url_for('payments_list'))
        except Exception as e:
            flash(str(e),'danger')
    return render_template('payment_form.html', payment=payment, tickets=tickets)

@app.route('/payments/delete/<int:pid>', methods=['POST'])
def payment_delete(pid):
    try:
        execute('DELETE FROM Payments WHERE payment_id=%s', (pid,))
        flash('Payment deleted','success')
    except Exception as e:
        flash(str(e),'danger')
    return redirect(url_for('payments_list'))

# Crew
@app.route('/crew')
def crew_list():
    rows = fetchall('SELECT c.*, f.airline AS flight_airline FROM Crew c LEFT JOIN Flights f ON c.assigned_flight_id=f.flight_id')
    flights = fetchall('SELECT * FROM Flights')
    return render_template('crew.html', crew=rows, flights=flights)

@app.route('/crew/add', methods=['GET','POST'])
def crew_add():
    flights = fetchall('SELECT * FROM Flights')
    if request.method=='POST':
        name = request.form.get('name')
        role = request.form.get('role')
        assigned = request.form.get('assigned_flight_id') or None
        try:
            execute('INSERT INTO Crew(name, role, assigned_flight_id) VALUES(%s,%s,%s)', (name, role, assigned))
            flash('Crew added','success')
            return redirect(url_for('crew_list'))
        except Exception as e:
            flash(str(e),'danger')
    return render_template('crew_form.html', member=None, flights=flights)

@app.route('/crew/edit/<int:cid>', methods=['GET','POST'])
def crew_edit(cid):
    member = fetchone('SELECT * FROM Crew WHERE crew_id=%s', (cid,))
    flights = fetchall('SELECT * FROM Flights')
    if request.method=='POST':
        name = request.form.get('name')
        role = request.form.get('role')
        assigned = request.form.get('assigned_flight_id') or None
        try:
            execute('UPDATE Crew SET name=%s, role=%s, assigned_flight_id=%s WHERE crew_id=%s', (name, role, assigned, cid))
            flash('Crew updated','success')
            return redirect(url_for('crew_list'))
        except Exception as e:
            flash(str(e),'danger')
    return render_template('crew_form.html', member=member, flights=flights)

@app.route('/crew/delete/<int:cid>', methods=['POST'])
def crew_delete(cid):
    try:
        execute('DELETE FROM Crew WHERE crew_id=%s', (cid,))
        flash('Crew deleted','success')
    except Exception as e:
        flash(str(e),'danger')
    return redirect(url_for('crew_list'))

# Routes
@app.route('/routes')
def routes_list():
    rows = fetchall('SELECT r.*, f.airline AS flight_airline FROM Routes r LEFT JOIN Flights f ON r.flight_id=f.flight_id')
    flights = fetchall('SELECT * FROM Flights')
    return render_template('routes.html', routes=rows, flights=flights)

@app.route('/routes/add', methods=['GET','POST'])
def route_add():
    flights = fetchall('SELECT * FROM Flights')
    if request.method=='POST':
        flight_id = request.form.get('flight_id') or None
        distance_km = request.form.get('distance_km') or None
        duration_minutes = request.form.get('duration_minutes') or None
        try:
            execute('INSERT INTO Routes(flight_id, distance_km, duration_minutes) VALUES(%s,%s,%s)', (flight_id, distance_km, duration_minutes))
            flash('Route added','success')
            return redirect(url_for('routes_list'))
        except Exception as e:
            flash(str(e),'danger')
    return render_template('route_form.html', route=None, flights=flights)

@app.route('/routes/edit/<int:rid>', methods=['GET','POST'])
def route_edit(rid):
    route = fetchone('SELECT * FROM Routes WHERE route_id=%s', (rid,))
    flights = fetchall('SELECT * FROM Flights')
    if request.method=='POST':
        flight_id = request.form.get('flight_id') or None
        distance_km = request.form.get('distance_km') or None
        duration_minutes = request.form.get('duration_minutes') or None
        try:
            execute('UPDATE Routes SET flight_id=%s, distance_km=%s, duration_minutes=%s WHERE route_id=%s', (flight_id, distance_km, duration_minutes, rid))
            flash('Route updated','success')
            return redirect(url_for('routes_list'))
        except Exception as e:
            flash(str(e),'danger')
    return render_template('route_form.html', route=route, flights=flights)

@app.route('/routes/delete/<int:rid>', methods=['POST'])
def route_delete(rid):
    try:
        execute('DELETE FROM Routes WHERE route_id=%s', (rid,))
        flash('Route deleted','success')
    except Exception as e:
        flash(str(e),'danger')
    return redirect(url_for('routes_list'))

if __name__ == '__main__':
    app.run(debug=True)
