import base64
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Function to perform basic arithmetic operations
def calculate(num1, num2, operation):
    if operation == 'add':
        return num1 + num2
        return num1 - num2
    elif operation == 'multiply':
        return num1 * num2
    elif operation == 'divide':
        if num2 != 0:
            return num1 / num2
        else:
            return "Error: Division by zero"
    else:
        return "Invalid operation"

# Function to hide images using base64 encoding
def hide_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
    except FileNotFoundError:
        return "Image not found"

# Route for the calculator
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = ""
    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        operation = request.form['operation']
        result = calculate(num1, num2, operation)
    
    return render_template_string('''
        <form method="post">
            <input type="number" name="num1" placeholder="Number 1" required>
            <input type="number" name="num2" placeholder="Number 2" required>
            <select name="operation">
                <option value="add">Add</option>
                <option value="subtract">Subtract</option>
                <option value="multiply">Multiply</option>
                <option value="divide">Divide</option>
            </select>
            <button type="submit">Calculate</button>
        </form>
        <h2>Result: {{ result }}</h2>
    ''', result=result)

# Route for hiding images
@app.route('/hide_image', methods=['GET', 'POST'])
def hide_image_route():
    hidden_image = ""
    if request.method == 'POST':
        image_path = request.form['image_path']
        hidden_image = hide_image(image_path)
    
    return render_template_string('''
        <form method="post">
            <input type="text" name="image_path" placeholder="Path to image" required>
            <button type="submit">Hide Image</button>
        </form>
        {% if hidden_image != "Image not found" %}
            <img src="data:image/jpeg;base64,{{ hidden_image }}" alt="Hidden Image">
        {% else %}
            <p>{{ hidden_image }}</p>
        {% endif %}
    ''', hidden_image=hidden_image)

if __name__ == '__main__':
    app.run(debug=True)