from django import forms

class ResumeForm(forms.Form):
    example_resume = """Name: Arulraj J
Email: arulraj@example.com
Phone: 9876543210
Job Role: Python Developer
Skills: Python, Django, REST API, Machine Learning, HTML, CSS, JavaScript, SQL
Worked as a Software Engineer at Jio from 2021 to 2023
B.Tech in Computer Science from Anna University in 2020
B.C.A in Computer Science from Anna University in 2013
Smart Attendance System using Face Recognition with Python and OpenCV
E-commerce Website using Django and Stripe Payment Gateway
Certificates:  
Python for Everybody–University of Michigan  
Advanced Django Development–LearnBay  
Machine Learning Specialization–Coursera
"""

    experience_text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 15}),
        label="Paste Resume Text",
        initial=example_resume
    )

    template_choice = forms.ChoiceField(
        choices=[
            ("template1", "Template 1"),
            ("template2", "Template 2"),
            ("template3", "Template 3"),
            ("template4", "Template 4"),
            ("template5", "Template 5"),
        ],
        label="Choose Resume Template"
    )
