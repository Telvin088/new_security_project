from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
from flask_mail import Mail, Message
from mysql.connector import Error as MySQLError
from flask_mysqldb import MySQL
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
import logging
import pymysql

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="new_security_auth"
    )


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'telvinngichukii@gmail.com'
app.config['MAIL_PASSWORD'] = 'pgnt fflh cyub jssn'

mail = Mail(app)


@app.route('/send-mail')
def send_mail(email, username):
    msg = Message('Subject of the Email', sender='telvinngichukii@gmail.com',
                  recipients=['davidhmainah@gmail.com'])
    msg.body = "This is the plain text body of the email"
    msg.html = "<b>This is the HTML body of the email</b>"
    mail.send(msg)
    return 'Email Sent!'


UPLOAD_FOLDER = os.path.join('website', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def truncate_words(s, num_words):
    words = s.split()
    if len(words) > num_words:
        return ' '.join(words[:num_words]) + '...'
    return s

# Register the filter with Jinja2
app.jinja_env.filters['truncate_words'] = truncate_words

@app.route('/notifications')
def notifications():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Fetch data from incident_assignments table
    cursor.execute("SELECT * FROM incident_assignments")
    incidents = cursor.fetchall()

    # Fetch detailed incident data for each incident assignment
    detailed_incidents = []
    for incident in incidents:
        incident_id = incident['incident_id']
        detailed_data = get_detailed_incident_data(incident_id)
        
        # Add data from incident_assignments to the detailed_data
        if detailed_data:
            detailed_data.update(incident)
        else:
            detailed_data = incident

        detailed_incidents.append(detailed_data)

    # Close the database connection
    cursor.close()
    conn.close()

    # Render the template with the fetched data
    return render_template('notifications.html', incidents=detailed_incidents)





def get_detailed_incident_data(incident_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Determine which table contains the incident_id
    cursor.execute("SELECT * FROM reports WHERE incident_id = %s", (incident_id,))
    report = cursor.fetchone()

    if report:
        incident_data = report
        table_name = "Violence"
    else:
        cursor.execute("SELECT * FROM theft_reports WHERE incident_id = %s", (incident_id,))
        theft_report = cursor.fetchone()
        if theft_report:
            incident_data = theft_report
            table_name = "Theft"
        else:
            cursor.execute("SELECT * FROM damages WHERE incident_id = %s", (incident_id,))
            damage_report = cursor.fetchone()
            if damage_report:
                incident_data = damage_report
                table_name = "Damages"
            else:
                incident_data = None
                table_name = None

    cursor.close()
    connection.close()

    return {
        "incident_data": incident_data,
        "table_name": table_name
    }


@app.route('/save_solved_incident', methods=['POST'])
def save_solved_incident():
    try:
        data = request.json
        print('Received data:', data)  # Check the incoming data in your Flask console/log

        # Extract data from JSON payload
        incident_id = data['incident_id']
        assign_date = data['assign_date']
        username = data['username']
        notes = data['notes']
        incident_data = data['incident_data']

        # Connect to the database
        db = get_db_connection()
        cursor = db.cursor()

        # Insert into solved_incidents table
        cursor.execute('''
            INSERT INTO solved_incidents (incident_id, assign_date, username, notes, incident_data)
            VALUES (%s, %s, %s, %s, %s)
        ''', (incident_id, assign_date, username, notes, json.dumps(incident_data)))
        db.commit()

        cursor.close()
        db.close()

        return jsonify({'status': 'success', 'message': 'Incident marked as solved and saved.'})

    except Exception as e:
        print(f"Error saving solved incident: {e}")
        return jsonify({'status': 'error', 'message': f'Error saving solved incident: {e}'}), 500





#comment
@app.route('/admin_dash', methods=['GET', 'POST'])
def admin_dash():
    if 'user_session_id' not in session:
        return redirect(url_for('login'))

    session_id = session.get('user_session_id')
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        date_time = request.form['date_time'].split(
            'T')[0]  # Extract date part only
        victim_name = request.form['victim_name']
        victim_age = request.form['victim_age']
        witness = request.form['witness']
        incident_description = request.form['incident_description']

        # Fetch username associated with the session_id from the users table
        cursor.execute(
            'SELECT username FROM users WHERE session_id = %s', (session_id,))
        user = cursor.fetchone()

        if user:
            username = user['username']

            # Insert data into the reports table
            cursor.execute(
                'INSERT INTO reports (date_time, victim_name, victim_age, witness, incident_description, username, session_id) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (date_time, victim_name, victim_age, witness,
                 incident_description, username, session_id)
            )
            db.commit()

            # Redirect to reports endpoint
            return redirect(url_for('admin_dash'))
        else:
            return 'User not found'

    try:
        # Fetch all reports data from the database (no session_id filter)
        cursor.execute(
            'SELECT *, DATE_FORMAT(date_time, "%Y-%m-%d") as date_only FROM reports')
        reports_data = cursor.fetchall()

        # Fetch all theft reports data from the database (no session_id filter)
        cursor.execute(
            'SELECT *, DATE_FORMAT(date_time, "%Y-%m-%d") as date_only FROM theft_reports')
        theft_reports_data = cursor.fetchall()

        # Get the total number of assigned incidents created (assuming incident_assignments table)
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()['COUNT(*)']

        # Get the total number of assigned incidents created (assuming incident_assignments table)
        cursor.execute('SELECT COUNT(*) FROM incident_assignments')
        total_assigned = cursor.fetchone()['COUNT(*)']

        # Get the total number of assigned incidents created (assuming incident_assignments table)
        cursor.execute('SELECT COUNT(*) FROM reports')
        total_recorder_reports = cursor.fetchone()['COUNT(*)']

        # Get the total number of assigned incidents created (assuming incident_assignments table)
        cursor.execute('SELECT COUNT(*) FROM theft_reports')
        total_theft_reports = cursor.fetchone()['COUNT(*)']

        # Get the total number of assigned incidents created (assuming incident_assignments table)
        cursor.execute('SELECT COUNT(*) FROM damages')
        total_reported_damages = cursor.fetchone()['COUNT(*)']

        fetched_total_incidents = total_recorder_reports + total_theft_reports + total_reported_damages

        # Fetch all damage reports data from the database (no session_id filter)
        cursor.execute(
            'SELECT *, DATE_FORMAT(date_time, "%Y-%m-%d") as date_only FROM damages')
        damage_reports_data = cursor.fetchall()

    except Error as e:
        print(f"Error fetching data: {e}")
        return render_template('error.html', message='Error fetching data from database.')

    finally:
        cursor.close()
        db.close()

    return render_template('admin_dash.html',
                           reports=reports_data,
                           theft_reports=theft_reports_data,
                           damage_reports=damage_reports_data,
                           total_assigned=total_assigned,
                           total_users=total_users,
                           fetched_total_incidents=fetched_total_incidents)


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'new_security_auth'
}


@app.route('/assign_incident', methods=['POST'])
def assign_incident():
    if 'user_session_id' not in session:
        return redirect(url_for('login'))

    assign_date = request.form.get('assign-date')
    user_username = request.form.get('assign-user')
    notes = request.form.get('assign-notes')
    session_id = session.get('user_session_id')
    incident_id = request.form.get('incident_id')
    print(f"Incident ID from form: {incident_id}")

    print(f"Form data: assign_date={assign_date}, user_username={user_username}, notes={notes}, session_id={session_id}, incident_id={incident_id}")

    if not incident_id:
        return render_template('error.html', message='Incident ID is missing.')

    db = get_db_connection()
    if db is None:
        return render_template('error.html', message='Error connecting to the database.')

    cursor = db.cursor()

    try:
        # Check if the username exists in the users table before inserting
        cursor.execute(
            'SELECT id FROM users WHERE username = %s', (user_username,))
        user_id = cursor.fetchone()
        # send email to user/person assigned
        #send_email(username, email, refund)

        if not user_id:
            return render_template('error.html', message=f'User "{user_username}" not found.')

        # Insert data into incident_assignments table
        insert_query = """
            INSERT INTO incident_assignments (assign_date, username, notes, session_id, incident_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (assign_date, user_username, notes, session_id, incident_id))
        db.commit()

        # Update status in reports table
        update_reports_query = """
            UPDATE reports
            SET status = 'assigned'
            WHERE incident_id = %s AND status = 'pending'
        """
        cursor.execute(update_reports_query, (incident_id,))
        db.commit()

        # Update status in theft_reports table
        update_theft_reports_query = """
            UPDATE theft_reports
            SET status = 'assigned'
            WHERE incident_id = %s AND status = 'pending'
        """
        cursor.execute(update_theft_reports_query, (incident_id,))
        db.commit()

        # Update status in damages table
        update_damages_query = """
            UPDATE damages
            SET status = 'assigned'
            WHERE incident_id = %s AND status = 'pending'
        """
        cursor.execute(update_damages_query, (incident_id,))
        db.commit()

    except MySQLError as e:
        logging.error(f"Error inserting data: {e}")
        return render_template('error.html', message='Error saving assignment to database.')

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return redirect(url_for('manage'))



@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if 'user_session_id' not in session:
        return redirect(url_for('login'))

    session_id = session.get('user_session_id')
    db = get_db_connection()
    if db is None:
        return render_template('error.html', message='Error connecting to the database.')

    cursor = db.cursor(dictionary=True)

    try:
        # Fetch all reports data from the database (no session_id filter)
        cursor.execute(
            'SELECT *, DATE_FORMAT(date_time, "%Y-%m-%d") as date_only FROM reports')
        reports_data = cursor.fetchall()

        # Fetch all theft reports data from the database (no session_id filter)
        cursor.execute(
            'SELECT *, DATE_FORMAT(date_time, "%Y-%m-%d") as date_only FROM theft_reports')
        theft_reports_data = cursor.fetchall()

        # Fetch all damage reports data from the database (no session_id filter)
        cursor.execute(
            'SELECT *, DATE_FORMAT(date_time, "%Y-%m-%d") as date_only FROM damages')
        damage_reports_data = cursor.fetchall()

        # Get the total number of assigned incidents created (assuming incident_assignments table)
        cursor.execute('SELECT COUNT(*) FROM incident_assignments')
        total_assigned = cursor.fetchone()['COUNT(*)']


        # Fetch all users from the database
        cursor.execute('SELECT id, username FROM users')
        users_data = cursor.fetchall()

        # Get the total number of assigned incidents created (assuming incident_assignments table)
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()['COUNT(*)']

        # Get the total number of assigned incidents created (assuming incident_assignments table)
        cursor.execute('SELECT COUNT(*) FROM reports')
        total_recorder_reports = cursor.fetchone()['COUNT(*)']

        # Get the total number of assigned incidents created (assuming incident_assignments table)
        cursor.execute('SELECT COUNT(*) FROM theft_reports')
        total_theft_reports = cursor.fetchone()['COUNT(*)']

        # Get the total number of assigned incidents created (assuming incident_assignments table)
        cursor.execute('SELECT COUNT(*) FROM damages')
        total_reported_damages = cursor.fetchone()['COUNT(*)']

        fetched_total_incidents = total_recorder_reports + total_theft_reports + total_reported_damages

    except MySQLError as e:
        print(f"Error fetching data: {e}")
        return render_template('error.html', message='Error fetching data from database.')
    finally:
        cursor.close()
        db.close()

    return render_template('manage.html',
                           reports=reports_data,
                           total_users=total_users,
                           theft_reports=theft_reports_data,
                           damage_reports=damage_reports_data,
                           users=users_data,
                           total_recorder_reports=total_recorder_reports,
                           fetched_total_incidents=fetched_total_incidents,
                           total_assigned=total_assigned)


@app.route('/generate_pdf/<int:incident_id>')
def generate_pdf(incident_id):
    db = get_db_connection()
    if db is None:
        return "Error connecting to the database."

    cursor = db.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT * FROM incidents WHERE id = %s', (incident_id,))
    incident = cursor.fetchone()

    if not incident:
        return "Incident not found."

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Incident Report - ID: {incident['id']}")
    p.drawString(100, 730, f"Date: {incident['date']}")
    p.drawString(100, 710, f"Description: {incident['description']}")
    p.drawString(100, 690, f"Status: {incident['status']}")

    # Add more fields as necessary

    p.showPage()
    p.save()

    buffer.seek(0)

    cursor.close()
    db.close()

    return send_file(buffer, as_attachment=True, download_name=f"incident_{incident_id}.pdf", mimetype='application/pdf')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        # Handle form submission and save data to database
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        message = request.form['message']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO contact_messages (name, email, phone_number, message)
            VALUES (%s, %s, %s, %s)
        """, (name, email, phone_number, message))
        db.commit()
        db.close()

        # Redirect to profile page to avoid form resubmission on refresh
        return redirect(url_for('profile'))

    else:
        # Fetch all messages from the database
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM contact_messages")
            messages = cursor.fetchall()
        except Exception as e:
            print(f"Error fetching messages: {e}")
            messages = []  # Provide an empty list in case of error
        finally:
            cursor.close()
            db.close()

        # Debugging: Print messages to console
        print(messages)

        return render_template('profile.html', messages=messages)


@app.route('/my_reports')
def my_reports():
    # Check if the session ID exists
    if 'user_session_id' not in session:
        return "User is not logged in", 401  # Unauthorized

    session_id = session['user_session_id']

    # Establish the database connection
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        # Get the total number of accounts created (assuming users table)
        cursor.execute('SELECT COUNT(*) FROM users')
        total_accounts = cursor.fetchone()['COUNT(*)']

        # Get the total number of theft reports
        cursor.execute('SELECT COUNT(*) FROM theft_reports')
        total_theft_reports = cursor.fetchone()['COUNT(*)']

        # Get the total number of damages
        cursor.execute('SELECT COUNT(*) FROM damages')
        total_damages = cursor.fetchone()['COUNT(*)']

        # Combine total incidents (theft reports + damages)
        total_incidents = total_theft_reports + total_damages

        # Fetch theft reports data from the database for the active session
        cursor.execute(
            'SELECT * FROM theft_reports WHERE session_id = %s', (session_id,))
        theft_reports_data = cursor.fetchall()

        # Fetch damage reports data from the database for the active session
        cursor.execute(
            'SELECT * FROM damages WHERE session_id = %s', (session_id,))
        damage_reports_data = cursor.fetchall()

        # Fetch general reports data from the database for the active session
        cursor.execute(
            'SELECT * FROM reports WHERE session_id = %s', (session_id,))
        reports_data = cursor.fetchall()

        # Fetch incident assignments data from the database for the active session
        cursor.execute(
            'SELECT * FROM incident_assignments WHERE session_id = %s', (session_id,))
        incident_assignments_data = cursor.fetchall()

    except Exception as e:
        # Handle exceptions appropriately (logging, error pages, etc.)
        print(f"Error fetching data: {e}")
        return render_template('error.html', message='Error fetching data from database.')

    finally:
        # Close the cursor and database connection
        cursor.close()
        db.close()

    # Render the template with the fetched data
    return render_template('my_reports.html',
                           theft_reports=theft_reports_data,
                           damages=damage_reports_data,
                           reports=reports_data,
                           incident_assignments=incident_assignments_data,
                           total_accounts=total_accounts,
                           total_theft_reports=total_theft_reports,
                           total_damages=total_damages,
                           total_incidents=total_incidents)



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_session_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Handle contact message form submission
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        message = request.form['message']

        db = get_db_connection()
        cursor = db.cursor()

        try:
            # Insert contact message into the database
            cursor.execute("""
                INSERT INTO contact_messages (name, email, phone_number, message, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, phone_number, message, datetime.now()))
            db.commit()
        except Exception as e:
            print(f"Error inserting contact message: {e}")
            db.rollback()
        finally:
            cursor.close()
            db.close()

        # Redirect to avoid form resubmission on refresh
        return redirect(url_for('dashboard'))

    # Fetch data for the dashboard
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        # Get the total number of accounts created
        cursor.execute('SELECT COUNT(*) AS total_accounts FROM users')
        total_accounts = cursor.fetchone()['total_accounts']

        # Get the total number of reports posted
        cursor.execute('SELECT COUNT(*) AS total_reports FROM reports')
        total_reports = cursor.fetchone()['total_reports']

        # Get the total number of theft reports
        cursor.execute(
            'SELECT COUNT(*) AS total_theft_reports FROM theft_reports')
        total_theft_reports = cursor.fetchone()['total_theft_reports']

        # Get the total number of damages
        cursor.execute('SELECT COUNT(*) AS total_damages FROM damages')
        total_damages = cursor.fetchone()['total_damages']

        # Combine total incidents (reports, theft reports, and damages)
        total_incidents = total_reports + total_theft_reports + total_damages

        # Fetch reports data
        cursor.execute('SELECT * FROM reports')
        reports_data = cursor.fetchall()

        # Fetch theft reports data
        cursor.execute('SELECT * FROM theft_reports')
        theft_reports_data = cursor.fetchall()

        # Fetch damage reports data
        cursor.execute('SELECT * FROM damages')
        damage_reports_data = cursor.fetchall()

        # Fetch users data
        cursor.execute('SELECT id, username, session_id, email, profile_photo FROM users')
        users_data = cursor.fetchall()

        # Fetch contact messages data
        cursor.execute('SELECT * FROM contact_messages')
        contact_messages = cursor.fetchall()

        # Format the date_time field to only show the date part
        for report in reports_data + theft_reports_data + damage_reports_data:
            report['date_time'] = report['date_time'].strftime('%Y-%m-%d')

    except Exception as e:
        print(f"Error fetching data: {e}")
        return render_template('error.html', message='Error fetching data from database.')

    finally:
        cursor.close()
        db.close()

    return render_template('dashboard.html',
                           reports=reports_data,
                           theft_reports=theft_reports_data,
                           damage_reports=damage_reports_data,
                           users=users_data,
                           contact_messages=contact_messages,
                           total_accounts=total_accounts,
                           total_reports=total_reports,
                           total_theft_reports=total_theft_reports,
                           total_damages=total_damages,
                           total_incidents=total_incidents)


# Route to handle reports page
@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if 'user_session_id' not in session:
        return redirect(url_for('login'))

    session_id = session.get('user_session_id')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        date_time = request.form['date_time'].split(
            'T')[0]  # Extract date part only
        victim_name = request.form['victim_name']
        victim_age = request.form['victim_age']
        witness = request.form['witness']
        incident_description = request.form['incident_description']
        incident_id = generate_unique_id()  # Function to generate a unique ID

        # Fetch username associated with the session_id from the users table
        cursor.execute(
            'SELECT username FROM users WHERE session_id = %s', (session_id,))
        user = cursor.fetchone()

        if user:
            username = user['username']

            # Insert data into the reports table
            cursor.execute(
                'INSERT INTO reports (incident_id, date_time, victim_name, victim_age, witness, incident_description, username, session_id) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (incident_id, date_time, victim_name, victim_age,
                 witness, incident_description, username, session_id)
            )
            db.commit()

            # Redirect to reports endpoint
            return redirect(url_for('reports'))
        else:
            return 'User not found'
    else:
        try:
            # Fetch all reports data from the database (no session_id filter)
            cursor.execute(
                'SELECT *, DATE_FORMAT(date_time, "%Y-%m-%d") as date_only FROM reports')
            reports_data = cursor.fetchall()

            # Fetch all theft reports data from the database (no session_id filter)
            cursor.execute('SELECT * FROM theft_reports')
            theft_reports_data = cursor.fetchall()

            # Fetch all damage reports data from the database (no session_id filter)
            cursor.execute('SELECT * FROM damages')
            damage_reports_data = cursor.fetchall()

        except Exception as e:
            print(f"Error fetching data: {e}")
            return render_template('error.html', message='Error fetching data from database.')

        finally:
            cursor.close()
            db.close()

        return render_template('reports.html',
                               reports=reports_data,
                               theft_reports=theft_reports_data,
                               damages=damage_reports_data)


@app.route('/save_and_display_theft_report', methods=['POST'])
def save_and_display_theft_report():
    if 'user_session_id' not in session:
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        date_time = request.form['date_time']
        stolen_items = request.form['stolen_items']
        stolen_value = request.form['stolen_value']
        theft_description = request.form['theft_description']
        session_id = session.get('user_session_id')
        incident_id = generate_unique_id()  # Function to generate a unique ID

        # Fetch username associated with the session_id from the users table
        cursor.execute(
            'SELECT username FROM users WHERE session_id = %s', (session_id,))
        user = cursor.fetchone()

        if user:
            username = user['username']

            # Insert theft report data into the database
            cursor.execute(
                'INSERT INTO theft_reports (incident_id, date_time, stolen_items, stolen_value, theft_description, username, session_id) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (incident_id, date_time, stolen_items, stolen_value,
                 theft_description, username, session_id)
            )
            db.commit()

            # Fetch all theft reports from the database
            cursor.execute('SELECT * FROM theft_reports')
            theft_reports = cursor.fetchall()

            return render_template('reports.html', theft_reports=theft_reports)
        else:
            return 'User not found'

    except mysql.connector.Error as e:
        print(e)
        return 'Error saving or displaying theft report data'

    finally:
        cursor.close()
        db.close()


# Route to handle damage report form submission
@app.route('/save_damage_report', methods=['POST'])
def save_damage_report():
    if 'user_session_id' not in session:
        return redirect(url_for('login'))  # Redirect if user not logged in

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        date_time = request.form['date_time']
        items_destroyed = int(request.form['items_destroyed'])
        value_of_destroyed = float(request.form['value_of_destroyed'])
        damage_description = request.form['damage_description']
        estimated_repair = float(request.form['estimated_repair'])
        session_id = session.get('user_session_id')
        incident_id = generate_unique_id()  # Function to generate a unique ID

        # Fetch username associated with the session_id from the users table
        cursor.execute(
            'SELECT username FROM users WHERE session_id = %s', (session_id,))
        user = cursor.fetchone()

        if user:
            username = user['username']

            # Insert damage report data into the damages table
            cursor.execute(
                'INSERT INTO damages (incident_id, date_time, items_destroyed, value_of_destroyed, damage_description, estimated_repair, username, session_id) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (incident_id, date_time, items_destroyed, value_of_destroyed,
                 damage_description, estimated_repair, username, session_id)
            )
            db.commit()

            # Redirect to the dashboard or another page
            return redirect(url_for('reports'))
        else:
            return 'User not found'

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return 'Error saving damage report'

    finally:
        cursor.close()
        db.close()


def generate_unique_id():
    return str(uuid.uuid4())


@app.route('/statistics')
def statistics():
    db = get_db_connection()
    cursor = db.cursor()

    # Get the total number of accounts created
    cursor.execute('SELECT COUNT(*) FROM users')
    total_accounts = cursor.fetchone()[0]

    # Get the total number of reports posted
    cursor.execute('SELECT COUNT(*) FROM reports')
    total_reports = cursor.fetchone()[0]

    cursor.close()
    db.close()

    return render_template('base.html', total_accounts=total_accounts, total_reports=total_reports)


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hardcoded admin login
        if username == 'admin' and password == 'admin123':
            # Redirect to admin_dash.html
            return render_template('admin_dash.html')
        
        # For regular users
        db = get_db_connection()  # Implement your database connection function
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user and check_password_hash(user['password'], password):
            session['user_session_id'] = user['session_id']
            session['username'] = user['username']
            # Set other session variables as needed, e.g., profile_photo
            session['profile_photo'] = user['profile_photo']
            return redirect(url_for('dashboard'))
        
        return 'Invalid credentials'

    return render_template('signup.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return 'Passwords do not match'

        if 'profile_photo' not in request.files:
            return 'No file part'
        file = request.files['profile_photo']

        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_photo_path = os.path.join('static', 'uploads', filename)
        else:
            return 'File not allowed'

        hashed_password = generate_password_hash(password)

        # Generate a unique session ID
        session_id = str(uuid.uuid4())

        # Store the session ID in the session data
        session['user_session_id'] = session_id

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO users (username, email, profile_photo, password, session_id) VALUES (%s, %s, %s, %s, %s)',
            (username, email, profile_photo_path, hashed_password, session_id)
        )
        db.commit()
        cursor.close()
        db.close()

        session['username'] = username
        # Add this line to set profile_photo in session
        session['profile_photo'] = profile_photo_path

        return redirect(url_for('dashboard'))
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_session_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
