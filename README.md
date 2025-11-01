# ✈️ Airline Reservation System (Flask Web App)

This project is a web-based **Airline Reservation System** developed using **Python (Flask)**, **HTML**, **CSS**, and **MySQL**.  
It enables efficient management of flights, passengers, routes, tickets, crew, and payments — all through a clean, browser-based interface.

---

## 🧠 Features
✅ Add, view, update, and delete records (CRUD operations)  
✅ Manage flights, passengers, payments, routes, and crew  
✅ MySQL database integration for data persistence  
✅ Flash messages for user feedback  
✅ Clean and simple HTML/CSS frontend design  

---

## ⚙️ Technologies Used
| Layer | Technology |
|--------|-------------|
| **Backend** | Python (Flask Framework) |
| **Frontend** | HTML, CSS |
| **Database** | MySQL |
| **IDE** | Visual Studio Code |

---

## 📁 Project Structure

AirlineReservationFlask/
│
├── app.py
├── requirements.txt
├── airlineReservation.sql
│
├── templates/
│ ├── index.html
│ ├── flights.html
│ ├── flight_form.html
│ ├── passengers.html
│ ├── passenger_form.html
│ ├── payments.html
│ ├── payment_form.html
│ ├── routes.html
│ ├── route_form.html
│ ├── tickets.html
│ ├── ticket_form.html
│ └── crew.html
│
└── static/
├── css/


---

## 🚀 How to Run Locally
1️⃣ **Clone the repository**
```bash
git clone https://github.com/iman3j/AirlineReservation-FlaskApp.git

cd AirlineReservation-FlaskApp

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

mysql -u root -p < airlineReservation.sql

python app.py
http://127.0.0.1:5000

## 🗄️ Database Information

Database Name: airlineReservation
Tables:
Airports | Flights | Passengers | Tickets | Payments | Routes | Crew

👨‍💻 Developer

Eman bin Ahmed
🎓 Bachelor’s in Statistics — Karachi University
🎓 AI & Data Science Diploma — NED University
💻 Skills: Flask | Python | MySQL | Power BI | Machine Learning | Deep learning | Langchain | LangGraph | NLP |
iman3j📧 e3j@gmail.com
🌐 GitHub Profile


---

git add README.md
git commit -m "Added professional README file"
git push



