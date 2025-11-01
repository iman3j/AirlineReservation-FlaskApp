# ✈️ Airline Reservation System (Flask Web App)

This project is a **web-based Airline Reservation System** built with **Python (Flask)**, **HTML**, **CSS**, and **MySQL**.  
It allows managing flights, passengers, routes, tickets, crew, and payments through a clean web interface.

---

## 🧠 Features
- ✅ CRUD operations for flights, passengers, tickets, payments, routes, and crew  
- ✅ MySQL database integration  
- ✅ Flash messages for user feedback  
- ✅ Clean and simple frontend using HTML & CSS  

---

## ⚙️ Technologies Used
| Layer       | Technology |
|------------|------------|
| Backend    | Python (Flask) |
| Frontend   | HTML, CSS |
| Database   | MySQL |
| IDE        | Visual Studio Code |

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
└── css/


---

## 🚀 How to Run Locally

1. **Clone the repository**
```bash
git clone https://github.com/iman3j/AirlineReservation-FlaskApp.git
cd AirlineReservationFlaskApp

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt

mysql -u root -p < airlineReservation.sql

python app.py
Open your browser at http://127.0.0.1:5000
🗄️ Database Info

Database Name: airlineReservation
Tables: Airports, Flights, Passengers, Tickets, Payments, Routes, Crew

👨‍💻 Developer
Name: Eman bin Ahmed

Education:
Bachelor’s in Statistics — Karachi University
AI & Data Science Diploma — NED University
Skills: Flask | Python | MySQL | Power BI | Machine Learning | Deep Learning | Langchain | LangGraph | NLP
Email: e3j@gmail.com
GitHub: iman3j

