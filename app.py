from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# BankAccount class definition
class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        self.balance -= amount
        return self.balance

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'account_created' not in session:
        session['account_created'] = False
    
    if 'balance' not in session:
        session['balance'] = 0

    if request.method == 'POST':
        if 'create_account' in request.form:
            amount = float(request.form['balance_input'])
            session['balance'] = amount
            session['account_created'] = True
            return redirect(url_for('index'))
        
        if 'deposit' in request.form:
            deposit_amount = float(request.form['deposit_amount'])
            account = BankAccount(session['balance'])
            session['balance'] = account.deposit(deposit_amount)
            return redirect(url_for('index'))

        if 'withdraw' in request.form:
            withdraw_amount = float(request.form['withdraw_amount'])
            if withdraw_amount <= session['balance']:
                account = BankAccount(session['balance'])
                session['balance'] = account.withdraw(withdraw_amount)
            return redirect(url_for('index'))

    return render_template('index.html', account_created=session['account_created'], balance=session['balance'])

if __name__ == '__main__':
    app.run(debug=True)
