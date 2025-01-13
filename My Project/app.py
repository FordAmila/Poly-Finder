import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for
import os
import uuid

app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/intersection', methods=['GET', 'POST'])
def intersection():
    graph_path = None
    explanation = None
    graph_history = []
    folder_name = None

    if request.method == 'POST':
        a1 = float(request.form['a1'])
        b1 = float(request.form['b1'])
        c1 = float(request.form['c1'])
        a2 = float(request.form['a2'])
        b2 = float(request.form['b2'])
        c2 = float(request.form['c2'])
        folder_name = request.form['folder_name']

        x = np.linspace(-10, 10, 400)
        y1 = a1 * x**2 + b1 * x + c1
        y2 = a2 * x**2 + b2 * x + c2

        plt.figure(figsize=(8, 6))
        plt.plot(x, y1, label='y = {0}x^2 + {1}x + {2}'.format(a1, b1, c1))
        plt.plot(x, y2, label='y = {0}x^2 + {1}x + {2}'.format(a2, b2, c2))
        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(0, color='black', linewidth=1)
        plt.grid(True)
        plt.legend()

        graph_folder = os.path.join('static', folder_name)
        if not os.path.exists(graph_folder):
            os.makedirs(graph_folder)
        unique_filename = f"graph_{uuid.uuid4().hex}.png"
        graph_path = os.path.join(graph_folder, unique_filename)
        plt.savefig(graph_path)

        graph_history_file = os.path.join(graph_folder, "history.txt")
        with open(graph_history_file, "a") as file:
            file.write(f"{unique_filename}\n")

        with open(graph_history_file, "r") as file:
            graph_history = file.readlines()

        poly1 = np.poly1d([a1, b1, c1])
        poly2 = np.poly1d([a2, b2, c2])
        poly_diff = poly1 - poly2
        roots = np.roots(poly_diff)
        intersection = [(r.real, poly1(r).real) for r in roots if np.isreal(r)]

        if intersection:
            explanation = ["Intersection points (x, y):"]
            for x, y in intersection:
                explanation.append("x = {:.2f}, y = {:.2f}".format(x, y))
        else:
            explanation = ["No intersection found within the given range."]

    return render_template('index.html', graph_path=graph_path, explanation=explanation, graph_history=graph_history, folder_name=folder_name)

@app.route('/quadratic_info', methods=['GET', 'POST'])
def quadratic_info():
    graph_path = None
    folder_name = None

    if request.method == 'POST':
        a = float(request.form['a'])
        b = float(request.form['b'])
        c = float(request.form['c'])
        folder_name = request.form['folder_name']

        x = np.linspace(-10, 10, 400)
        y = a * x**2 + b * x + c

        plt.figure(figsize=(8, 6))
        plt.plot(x, y, label='y = {0}x^2 + {1}x + {2}'.format(a, b, c))
        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(0, color='black', linewidth=1)
        plt.grid(True)
        plt.legend()

        graph_folder = os.path.join('static', folder_name)
        if not os.path.exists(graph_folder):
            os.makedirs(graph_folder)
        unique_filename = f"graph_{uuid.uuid4().hex}.png"
        graph_path = os.path.join(graph_folder, unique_filename)
        plt.savefig(graph_path)

    return render_template('quadratic_info.html', graph_path=graph_path, folder_name=folder_name)

if __name__ == '__main__':
    app.run(debug=True)
