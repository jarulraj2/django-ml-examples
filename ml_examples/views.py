from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.cluster import KMeans
from collections import Counter

def home_view(request):
    return render(request, 'ml_examples/home.html')


def supervised_view(request):
    data = {
        'monthly_usage_gb': [50, 10, 30, 80, 5, 60, 20, 90],
        'num_complaints': [1, 5, 0, 0, 3, 2, 1, 0],
        'late_payments': [0, 1, 0, 0, 2, 0, 1, 0],
        'tenure_months': [12, 3, 8, 24, 2, 18, 6, 30],
        'churn': [0, 1, 0, 0, 1, 0, 1, 0]
    }
    df = pd.DataFrame(data)

    X = df[['monthly_usage_gb', 'num_complaints', 'late_payments', 'tenure_months']]
    y = df['churn']

    model = LogisticRegression(max_iter=200)
    model.fit(X, y)

    default_input = {
        'monthly_usage_gb': 40,
        'num_complaints': 1,
        'late_payments': 0,
        'tenure_months': 10,
    }

    prediction = None
    probability = None

    if request.method == 'POST':
        monthly_usage_gb = float(request.POST.get('monthly_usage_gb'))
        num_complaints = int(request.POST.get('num_complaints'))
        late_payments = int(request.POST.get('late_payments'))
        tenure_months = int(request.POST.get('tenure_months'))

        user_data = np.array([[monthly_usage_gb, num_complaints, late_payments, tenure_months]])
        pred = model.predict(user_data)[0]
        prob = model.predict_proba(user_data)[0][1]

        prediction = "Churn Likely" if pred == 1 else "No Churn"
        probability = round(prob * 100, 2)

        default_input = {
            'monthly_usage_gb': monthly_usage_gb,
            'num_complaints': num_complaints,
            'late_payments': late_payments,
            'tenure_months': tenure_months,
        }

    # Convert dataframe to HTML table (Bootstrap classes)
    table_html = df.to_html(classes="table table-striped table-bordered", index=False)

    return render(request, 'ml_examples/supervised.html', {
        'default_input': default_input,
        'prediction': prediction,
        'probability': probability,
        'training_data_table': table_html,
    })


def unsupervised_view(request):
    data = np.array([
        [50, 700, 12, 1],
        [10, 200, 3, 5],
        [30, 400, 8, 0],
        [80, 1000, 24, 0],
        [5, 150, 2, 3],
        [60, 850, 18, 2],
        [20, 300, 6, 1],
        [90, 1100, 30, 0]
    ])

    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(data)
    labels = kmeans.labels_

    customers = [{'id': i + 1, 'segment': labels[i]} for i in range(len(labels))]
    segment_counts = dict(Counter(labels))

    return render(request, 'ml_examples/unsupervised.html', {
        'customers': customers,
        'segment_labels': list(segment_counts.keys()),
        'segment_counts': list(segment_counts.values())
    })


def reinforcement_view(request):
    states = [0, 1, 2]  # bandwidth allocated
    actions = [0, 1, 2]  # next allocation
    Q = np.zeros((len(states), len(actions)))
    alpha = 0.1  # learning rate
    gamma = 0.9  # discount factor
    epsilon = 0.2  # exploration rate

    def reward(state):
        if state == 2:
            return 10
        elif state == 1:
            return 5
        else:
            return -10

    for episode in range(1000):
        state = np.random.choice(states)
        if np.random.rand() < epsilon:
            action = np.random.choice(actions)
        else:
            action = np.argmax(Q[state])
        r = reward(action)
        Q[state, action] = Q[state, action] + alpha * (r + gamma * np.max(Q[action]) - Q[state, action])

    q_table = Q.tolist()

    return render(request, 'ml_examples/reinforcement.html', {
        'q_table': q_table
    })
