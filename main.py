from server import db, app, cursor
from flask import render_template, request, redirect, url_for
from server import Creditcards, Transactions, Users
from datetime import date, datetime
import locale, pandas

db.create_all()
db.session.commit()
locale.setlocale(locale.LC_ALL, 'en_PH.UTF-8')


@app.route("/create", methods=['GET', 'POST'])
def create():
    creditcards = Creditcards.query.all()
    transactions = Transactions.query.all()
    users = Users.query.all()
    datetoday = date.today()
    if request.method == 'POST':
        t_ccname = request.form["cardname"]
        t_date = request.form["date"]
        t_vendor = request.form["vendor"]
        t_particulars = request.form["particulars"]
        t_amount = float(request.form["amount"])
        t_expenseby = request.form["expenseby"]
        new_transaction = Transactions(cc_id=t_ccname, date=datetime.strptime(t_date, "%Y-%m-%d"),
                                       vendor=t_vendor, particulars=t_particulars,
                                       amount=t_amount, user_id=t_expenseby)
        db.session.add(new_transaction)
        db.session.commit()
    return render_template('create.html', creditcards=creditcards, datetoday=datetoday,
                           users=users,home=url_for('home'),create=url_for('create'),transactions_all=url_for('view_transactions',table='all',table_id='all',page_num=1),
                            import_transactions = url_for('import_transactions'),setup=url_for('setup'))


@app.route("/addcredit", methods=['GET', 'POST'])
def addcredit():
    creditcards = Creditcards.query.all()
    transactions = Transactions.query.all()
    users = Users.query.all()
    if request.method == 'POST':
        c_num = request.form["number"]
        c_bank = request.form["bank"]
        c_alias = request.form["alias"]
        c_type = request.form["type"]
        new_credit = Creditcards(number=c_num, bank=c_bank, alias=c_alias, type=c_type)
        db.session.add(new_credit)
        db.session.commit()
    return render_template('addcredit.html', home=url_for('home'),create=url_for('create'),transactions_all=url_for('view_transactions',table='all',table_id='all',page_num=1),
                            import_transactions = url_for('import_transactions'),setup=url_for('setup'))


@app.route("/adduser", methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        user_name = request.form["name"]
        new_user = Users(name=user_name)
        db.session.add(new_user)
        db.session.commit()
    return render_template('adduser.html', home=url_for('home'),create=url_for('create'),transactions_all=url_for('view_transactions',table='all',table_id='all',page_num=1),
                            import_transactions = url_for('import_transactions'),setup=url_for('setup'))


@app.route("/transactions/<table>/<table_id>/<page_num>", methods=['GET'])
def view_transactions(table, table_id,page_num):
    transactions = Transactions.query.all()
    creditcards = Creditcards.query.all()
    users = Users.query.all()
    page_num=int(page_num)
    cur_page=page_num * 10
    prev_page = cur_page - 10
    if table == 'all' and table_id == 'all':
        transactions = Transactions.query.order_by(Transactions.date.desc()).all()
    elif table == 'cc':
        transactions = Transactions.query.filter_by(cc_id=table_id).order_by(Transactions.date.desc()).all()
    elif table == 'user':
        transactions = Transactions.query.filter_by(user_id=table_id).order_by(Transactions.date.desc()).all()

    return render_template('transactions.html', home=url_for('home'),create=url_for('create'),transactions_all=url_for('view_transactions',table='all',table_id='all',page_num=1),
                            import_transactions = url_for('import_transactions'),setup=url_for('setup'), creditcards=creditcards, page_num = page_num, cur_page=cur_page,prev_page=prev_page,
                           financial=locale.currency, users=users, prev = url_for('view_transactions',table=table,table_id=table_id,page_num=page_num-1),next = url_for('view_transactions',table=table,table_id=table_id,page_num=page_num+1),
                           len=len,all=url_for('view_transactions',table=table,table_id=table_id,page_num=0),transactions=transactions,update_transaction=url_for)

@app.route("/import", methods=['GET','POST'])
def import_transactions():
    if request.method == 'POST':
        f = request.files['import']
        filename='import.csv'
        f.save(filename)
        return redirect(url_for('process_import',filename=filename))

    return render_template('import.html', home=url_for('home'),create=url_for('create'),transactions_all=url_for('view_transactions',table='all',table_id='all',page_num=1),
                            import_transactions = url_for('import_transactions'),setup=url_for('setup'))

@app.route("/process-import/<filename>", methods=['GET','POST'])
def process_import(filename):
    creditcards = Creditcards.query.all()
    transactions = Transactions.query.all()
    users = Users.query.all()
    csv = pandas.read_csv(filename)
    csv_file = csv.to_dict(orient='records')
    num_import = len(csv_file)
    if request.method == 'POST':
        for num in range(num_import):
            t_ccname = request.form[f"cardname{num}"]
            t_date = request.form[f"date{num}"]
            t_vendor = request.form[f"vendor{num}"]
            t_particulars = request.form[f"particulars{num}"]
            t_amount = float(request.form[f"amount{num}"])
            t_expenseby = request.form[f"expenseby{num}"]
            new_transaction = Transactions(cc_id=t_ccname, date=datetime.strptime(t_date, "%Y-%m-%d"),
                                            vendor=t_vendor, particulars=t_particulars,
                                            amount=t_amount, user_id=t_expenseby)
            db.session.add(new_transaction)
            db.session.commit()           
    return render_template('process_import.html',home=url_for('home'),csv_import=csv_file,creditcards=creditcards,transactions=transactions,users=users,enumerate=enumerate)

@app.route("/update/<t_id>",methods=['GET','POST'])
def update_transaction(t_id):
    transaction = Transactions.query.filter_by(id=int(t_id)).first()
    creditcards = Creditcards.query.all()
    users = Users.query.all()
    if request.method == 'POST':
        if request.form["submit"] == 'UPDATE':
            transaction.cc_id = request.form[f"cardname"]
            transaction.date = datetime.strptime(request.form[f"date"],"%Y-%m-%d")
            transaction.vendor= request.form[f"vendor"]
            transaction.particulars = request.form[f"particulars"]
            transaction.amount = float(request.form[f"amount"])
            transaction.user_id = request.form[f"expenseby"]
            db.session.commit()
            return redirect(url_for('view_transactions',table='all',table_id='all',page_num=0))
        elif request.form["submit"] == 'DELETE':
            db.session.delete(transaction)
            db.session.commit()
            return redirect(url_for('view_transactions',table='all',table_id='all',page_num=0))
         

    return render_template('update.html',transaction=transaction, creditcards=creditcards, users=users,home=url_for('home'),create=url_for('create'),transactions_all=url_for('view_transactions',table='all',table_id='all',page_num=1),
                            import_transactions = url_for('import_transactions'),setup=url_for('setup'))

@app.route("/setup")
def setup():
    return render_template('setup.html', home=url_for('home'),create=url_for('create'),transactions_all=url_for('view_transactions',table='all',table_id='all',page_num=1),
                            import_transactions = url_for('import_transactions'),setup=url_for('setup'),adduser=url_for('adduser'),addcredit=url_for('addcredit'))

@app.route("/")
def home():
    creditcards = Creditcards.query.all()
    transactions = Transactions.query.all()
    users = Users.query.all()

    def calc_totalbalance():
        total_balance = 0
        for transaction in transactions:
            total_balance += transaction.amount
        return total_balance

    def calc_balance(type, type_id):
        balance = 0
        if type == "cc":
            query = Transactions.query.filter_by(cc_id=type_id).all()
        elif type == "user":
            query = Transactions.query.filter_by(user_id=type_id).all()
        for amount in query:
            balance += amount.amount
        return balance

    def view_transactions(id, sort):
        if sort == 'desc':
            query = Transactions.query.filter_by(user_id=id).order_by(Transactions.date.desc())
        else:
            query = Transactions.query.filter_by(user_id=id).all()
        return query

    return render_template('index.html', creditcards=creditcards, home=url_for('home'),create=url_for('create'),transactions_all=url_for('view_transactions',table='all',table_id='all',page_num=1),
                            import_transactions = url_for('import_transactions'),setup=url_for('setup'),
                            financial=locale.currency, total_balance=calc_totalbalance,
                           calc_balance=calc_balance, users=users, view_transactions=view_transactions,len=len, addcredit=url_for('addcredit'),adduser=url_for('adduser'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
