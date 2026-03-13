import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# ផ្ទុកទិន្នន័យបណ្តោះអាសន្ន
items = []
current_deposit = 0.0

@app.route('/')
def index():
    grand_total = sum(item['total'] for item in items)
    balance = grand_total - current_deposit
    
    # រៀបចំកាលបរិច្ឆេទជាភាសាខ្មែរ
    now = datetime.now()
    months_kh = ["", "មករា", "កុម្ភៈ", "មីនា", "មេសា", "ឧសភា", "មិថុនា", "កក្កដា", "សីហា", "កញ្ញា", "តុលា", "វិច្ឆិកា", "ធ្នូ"]
    current_date = f"{now.day} {months_kh[now.month]} {now.year}"

    return render_template('invoice.html', 
                           items=items, 
                           grand_total=grand_total, 
                           deposit=current_deposit, 
                           balance=balance, 
                           date=current_date)

@app.route('/add', methods=['POST'])
def add_item():
    global current_deposit
    name = request.form.get('name')
    qty = request.form.get('qty', type=float, default=0)
    price = request.form.get('price', type=float, default=0)
    unit = request.form.get('unit', '')
    
    # បញ្ចូលលុយកក់
    deposit_input = request.form.get('deposit', type=float)
    if deposit_input is not None:
        current_deposit = deposit_input
    
    if name:
        items.append({
            'name': name, 'qty': qty, 'unit': unit, 'price': price, 'total': qty * price
        })
    return redirect(url_for('index'))

@app.route('/clear')
def clear():
    global items, current_deposit
    items = []
    current_deposit = 0.0
    return redirect(url_for('index'))

if __name__ == '__main__':
    # កំណត់ Port ឱ្យត្រូវតាម Server របស់ Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)