# Django ML Examples

This is a sample Django project demonstrating basic Machine Learning concepts through small web apps.  
It includes examples for Supervised, Unsupervised, and Reinforcement Learning with interactive UI built using Bootstrap and Chart.js.

---

## Features

- Supervised Learning: Logistic Regression for customer churn prediction  
- Unsupervised Learning: KMeans clustering for customer segmentation  
- Reinforcement Learning: Q-learning example for bandwidth allocation  
- Simple, clean UI with Bootstrap  
- Interactive charts with Chart.js  

---

## Installation

**1. Clone the repo:**

git clone https://github.com/jarulraj2/django-ml-examples.git
cd django-ml-examples
Create a virtual environment and activate it:
python -m venv env
source env/bin/activate      # Linux/macOS
env\Scripts\activate         # Windows

**Install dependencies:**
pip install -r requirements.txt

**Run migrations:**
python manage.py migrate

**Start the server:**
python manage.py runserver
Open http://127.0.0.1:8000/ in your browser.

