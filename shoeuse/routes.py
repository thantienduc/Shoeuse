import random
from flask import render_template, url_for, flash, redirect, request
from shoeuse import app, mysql
from shoeuse.forms import LoginForm, RegistrationForm, UndateAccount, PaymentForm
from datetime import datetime

user_is_authenticated = False
current_id = 1
current_user = ''
insert_ammount = 0.0
def set_true(username):
    global user_is_authenticated
    global current_user
    current_user = username
    user_is_authenticated = True
def increase_current_id():
    global current_id
    current_id+=1
def set_insert_amount(amount):
    global insert_ammount
    insert_ammount =amount
def set_authenticated_false():
    global user_is_authenticated
    user_is_authenticated = False
def set_username_null():
    global current_user
    current_user = ''

@app.route("/")
@app.route("/home")
def home():
    cur =mysql.connection.cursor()
    cur.execute("SELECT * FROM SHOE")
    mysql.connection.commit()
    shoes = cur.fetchall()
    cur.close()
    print(user_is_authenticated)
    return render_template('home.html', title='home', shoes = shoes, is_authenticated = user_is_authenticated)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        fname = form.FName.data
        lname = form.LName.data
        mname = form.MName.data
        bdate = datetime.strptime(form.BDate.data, '%Y-%m-%d').date()
        email = form.email.data
        address = form.Address.data
        phone = form.Phone.data
        password = form.password.data
        clientid = fname[0]+lname[0]+str(current_id)
        increase_current_id()
        loginid = username[0]+username[len(username)-1] +str(current_id)
        cur = mysql.connection.cursor()
        try:
            #client = """ INSERT INTO Client VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""%(clientid,fname,mname,lname,bdate,email,address,phone)
            #login_db = """ INSERT INTO LogIn VALUES(%s,%s,%s,%s) """%('',username,password,clientid)
            cur.execute(" INSERT INTO Client VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(clientid,fname,mname,lname,bdate,email,address,phone))
            mysql.connection.commit()
            cur.execute(" INSERT INTO LogIn VALUES(%s,%s,%s,%s) ",(loginid,username,password,clientid))
            mysql.connection.commit()
            cur.close()
            flash(f'Account created successfully! You are now available to login', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'please check your information','danger')
            print(e)
            return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form, is_authenticated = user_is_authenticated)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("SELECT Username, Password FROM LogIn WHERE Username = %s",(form.username.data,))
        user = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        if user and user[0][1] == form.password.data:
            set_true(user[0][0])
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/home')
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form, is_authenticated=user_is_authenticated)

@app.route("/logout")
def logout():
    set_authenticated_false()
    set_username_null()
    print(user_is_authenticated)
    return redirect(url_for('home'))

@app.route("/shoe/<shoe_id>")
def shoe(shoe_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM SHOE WHERE ShoeID =%s",(shoe_id,))
    mysql.connection.commit()
    shoe = cur.fetchall()
    cur.close()
    return render_template("shoe.html", title = shoe[0][1],shoe = shoe[0], is_authenticated = user_is_authenticated)

@app.route("/shoe/<shoe_id>/place_order")
def place_order(shoe_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM SHOE WHERE ShoeID = %s",(shoe_id,))
    mysql.connection.commit()
    shoe = cur.fetchall()
    cur.execute("SELECT ClientID FROM LogIn WHERE Username = %s ", (current_user,))
    mysql.connection.commit()
    user = cur.fetchall()
    increase_current_id()
    order_id = "ORD" + str(current_id)
    cur.execute("INSERT INTO PLACE_ORDER VALUES (%s,%s,%s,%s,%s)",(order_id,shoe[0][2]+" "+shoe[0][3],1,user[0][0],shoe[0][5]))
    mysql.connection.commit()
    cur.execute("SELECT * FROM SHOE")
    mysql.connection.commit()
    shoes = cur.fetchall()
    cur.close()
    flash('Place order succesfully!', 'success')
    return render_template('home.html', title='home', shoes = shoes, is_authenticated = user_is_authenticated)

@app.route("/account", methods=['GET', 'POST'])
def account():
    form = UndateAccount()
    if form.validate_on_submit():
        fname = form.FName.data
        mname = form.MName.data
        lname = form.LName.data
        address = form.Address.data
        phone = form.Phone.data
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT ClientID FROM LogIn WHERE Username= %s",(current_user,))
            mysql.connection.commit()
            clientid = cur.fetchall()
            cur.execute("UPDATE Client SET FName =%s, MName=%s, LName=%s,Address=%s,PhoneNumber=%s WHERE ClientID=%s",
                        (fname,mname,lname,address,phone,clientid[0][0]))
            mysql.connection.commit()
            cur.close()
            flash(f'Your account have been updated successfully!','success')
            return redirect(url_for('account'))
        except Exception as e:
            flash(f'something went wrong','danger')
            return redirect(url_for('account'))
    return render_template('account.html', title = 'Update Account', form =form, is_authenticated = user_is_authenticated)

@app.route("/payment", methods=['GET', 'POST'])
def payment():
    form = PaymentForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM LogIn WHERE Username = %s", (current_user,))
    mysql.connection.commit()
    user = cur.fetchall()
    cur.execute("SELECT * FROM PLACE_ORDER WHERE ClientID = %s", (user[0][3],))
    mysql.connection.commit()
    orders = cur.fetchall()
    shoes = []
    for order in orders:
        cur.execute("SELECT * FROM SHOE WHERE ProdID =%s",(order[4],))
        mysql.connection.commit()
        shoes.append(cur.fetchall()[0])
    if shoes:
        amount = round(random.uniform(50.00, 150.00),2)
    else: 
        amount = 0.0
    set_insert_amount(amount)
    if form.validate_on_submit():
        method = form.Method.data
        discount = form.Discount.data
        if not discount: 
            discount = 0.0
        for order in orders:
            payid = "Pay"+str(current_id)
            increase_current_id()
            cur.execute("INSERT INTO PAYMENT VALUES(%s,%s,%s,%s,%s)",(payid,insert_ammount,method,discount,order[0]))
            mysql.connection.commit()
        cur.execute("SELECT * FROM SHOE")
        mysql.connection.commit()
        shoes = cur.fetchall()
        cur.close()
        flash(f'Payment have been made successfully!', 'success')
        return render_template('home.html', title='home', shoes = shoes, is_authenticated = user_is_authenticated)
    return render_template("payment.html", shoes = shoes, amount = amount, form = form, is_authenticated = user_is_authenticated)

@app.route("/payment/<pro_id>/delete", methods= ['GET','POST'])
def delete(pro_id):
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM PLACE_ORDER WHERE ProdID =%s",(pro_id,))
    mysql.connection.commit()
    form = PaymentForm()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM LogIn WHERE Username = %s", (current_user,))
    mysql.connection.commit()
    user = cur.fetchall()
    cur.execute("SELECT * FROM PLACE_ORDER WHERE ClientID = %s", (user[0][3],))
    mysql.connection.commit()
    orders = cur.fetchall()
    shoes = []
    for order in orders:
        cur.execute("SELECT * FROM SHOE WHERE ProdID =%s",(order[4],))
        mysql.connection.commit()
        shoes.append(cur.fetchall()[0])
    cur.close()
    if shoes:
        amount = round(random.uniform(50.00, 150.00),2)
    else: 
        amount = 0.0
    set_insert_amount(amount)
    flash('Delete successfully!', 'success')
    return render_template("payment.html", shoes = shoes, amount = insert_ammount, form = form, is_authenticated = user_is_authenticated)