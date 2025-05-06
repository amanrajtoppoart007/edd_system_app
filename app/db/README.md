# EDD Technologies Repair System

A console-based, object-oriented Python application designed to streamline repair operations for a technical service center. This system supports key roles like administrators, technicians, and customers, and handles the full repair lifecycle—from booking and job assignment to technician assessment and customer notifications.

---

## 🚀 Features

- Customer login and repair booking (registered or walk-in)
- Administrator-controlled technician creation and job allocation
- Technician login and job assessment
- Equipment registration and tracking
- Job costing and status updates
- Spare parts supplier management
- Role-specific command-line menus
- Basic customer notification system
- Unit testing for key modules

---

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Database**: SQLite3 (via Python’s `sqlite3` module)
- **Architecture**: MVC (Model-View-Controller)
- **Version Control**: Git

---

## 📁 Project Structure

edd-technologies/
├── database/
│ └── database.py
├── models/
│ ├── administrator.py
│ ├── technician.py
│ ├── customer.py
│ ├── equipment.py
│ ├── job.py
│ ├── supplier.py
├── controller/
│ └── app_controller.py
├── tests/
│ └── test_cases.py
├── main.py
└── README.md

---

## 🧰 Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/edd-technologies.git
cd edd-technologies

2. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install any required packages (if needed):

pip install -r requirements.txt

---

## ▶️ Running the app
Run the main interface:

python main.py

Tests are located in the tests/ directory and can be executed with:

python tests/test_cases.py

---

🐞 Known Issues
No GUI (not required at this stage)
Customer promotions/notifications not persisted
Basic notification system (printed only)

---

🧠 Future Enhancements
Persistent notification system
Web or GUI interface
Advanced customer loyalty & promotions
Technician performance tracking
Integration with external supplier APIs

---

📜 License
This project is open source and available under the MIT License.

---

👨‍💻 Author
Developed by [Your Name]
For academic or demonstration purposes.

---