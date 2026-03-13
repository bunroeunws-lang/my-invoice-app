from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# បញ្ជីទំនិញបណ្តោះអាសន្ន
items = []
# បង្កើត Variable សកលសម្រាប់រក្សាតម្លៃលុយកក់
current_deposit = 0.0

@app.route('/')
def index():
    grand_total = sum(item['total'] for item in items)
    balance = grand_total - current_deposit
    
    now = datetime.now()
    # កែសម្រួលឆ្នាំឱ្យត្រឹមត្រូវ (2026)
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
    qty = request.form.get('qty', type=int, default=0)
    price = request.form.get('price', type=float, default=0.0)
    unit = request.form.get('unit', '')
    
    # ទទួលយកតម្លៃលុយកក់ថ្មី ប្រសិនបើអ្នកប្រើបញ្ចូល
    deposit_input = request.form.get('deposit', type=float)
    if deposit_input is not None:
        current_deposit = deposit_input
    
    if name: # បន្ថែមទំនិញតែពេលមានឈ្មោះ
        items.append({
            'name': name,
            'qty': qty,
            'unit': unit,
            'price': price,
            'total': qty * price
        })
    return redirect(url_for('index'))
@app.route('/clear')
def clear_data():
    global items, current_deposit
    items = []            # លុបទិន្នន័យទំនិញទាំងអស់ក្នុងបញ្ជី
    current_deposit = 0.0 # កំណត់លុយកក់ឲ្យមកនៅ ០ វិញ
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)