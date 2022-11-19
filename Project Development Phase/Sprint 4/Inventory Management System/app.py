import ibm_db
from flask import Flask, redirect, render_template, request, session, url_for
from markupsafe import escape

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=815fa4db-dc03-4c70-869a-a9cc13f33084.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30367;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=txg49604;PWD=krAF2h7MrxBxNuk3",'','')

app = Flask(__name__)
app.secret_key='a'


@app.route('/')
def homepage():
  return render_template('index.html')

@app.route('/register')
def register():
  return render_template('register.html')
@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/header')
def header():
    return render_template('header.html')

@app.route('/home')
def home():
  global userid
  msg = session['username']
  userid=session['id']
  msg = 'Welcome'+" "+session['username']+"!!"
  results = []

  sql ="SELECT CATEGORY, COUNT(CATEGORY) AS count FROM INVENTORY WHERE USERID = ? GROUP BY CATEGORY;"
  stmt = ibm_db.prepare(conn, sql)
  ibm_db.bind_param(stmt,1,userid)
  ibm_db.execute(stmt)
  dictionary = ibm_db.fetch_both(stmt)
  print(dictionary)
  while dictionary != False:
    # print ("The Name is : ",  dictionary)
    results.append(dictionary)
    dictionary = ibm_db.fetch_both(stmt)
  print(results[0]["CATEGORY"])

  data=[0,0,0,0,0,0]
  for result in results:
        if(result["CATEGORY"] == "books"):
          data[0] = result["COUNT"]
        elif(result["CATEGORY"] == "cosmetics"):
          data[1] = result["COUNT"]
        elif(result["CATEGORY"] == "electronicitems"):
          data[2] = result["COUNT"]
        elif(result["CATEGORY"] == "food"):
          data[3] = result["COUNT"]
        elif(result["CATEGORY"] == "furniture"):
          data[4] = result["COUNT"]
        elif(result["CATEGORY"] == "miscellaneous"):
          data[5] = result["COUNT"]
  print(data)
  return render_template('home.html', msg = msg, results = data)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/addInventory')
def addInventory():
    return render_template('addInventory.html')




@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
  if request.method == 'POST':

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    password= request.form['password']

    sql = "SELECT * FROM USERS WHERE NAME =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('login.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO USERS (Name,email,phone,password) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email )
      ibm_db.bind_param(prep_stmt, 3, phone)
      ibm_db.bind_param(prep_stmt, 4, password)
      ibm_db.execute(prep_stmt)
    
    return render_template('login.html', msg="Registered successfuly..")






@app.route('/signin', methods =['GET', 'POST'])
def signIn():
    global userid
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        sql ="SELECT * FROM USERS WHERE  email = ? AND password = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)

        if account:
            session['loggedin'] = True
            session['id'] = account['USERID']
            userid=account['USERID']
            session['username']=account['NAME']

            session["name"] = request.form.get("name")

            session['username'] = account['NAME']
            msg = 'Welcome'+" "+session['username']+"!!"
            results = []

            sql ="SELECT CATEGORY, COUNT(CATEGORY) AS count FROM INVENTORY WHERE USERID = ? GROUP BY CATEGORY;"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt,1,userid)
            ibm_db.execute(stmt)
            dictionary = ibm_db.fetch_both(stmt)
            print(dictionary)
            while dictionary != False:
              # print ("The Name is : ",  dictionary)
              results.append(dictionary)
              dictionary = ibm_db.fetch_both(stmt)
            print(results[0]["CATEGORY"])

            data=[0,0,0,0,0,0]
            for result in results:
                  if(result["CATEGORY"] == "books"):
                    data[0] = result["COUNT"]
                  elif(result["CATEGORY"] == "cosmetics"):
                    data[1] = result["COUNT"]
                  elif(result["CATEGORY"] == "electronicitems"):
                    data[2] = result["COUNT"]
                  elif(result["CATEGORY"] == "food"):
                    data[3] = result["COUNT"]
                  elif(result["CATEGORY"] == "furniture"):
                    data[4] = result["COUNT"]
                  elif(result["CATEGORY"] == "miscellaneous"):
                    data[5] = result["COUNT"]
            print(data)
            return render_template('home.html', msg = msg, results = data)
        else:
            msg = 'Incorrect username / password !'
        return render_template('login.html', msg = msg, results = data)





@app.route('/add', methods =['GET', 'POST'])
def add():
    global id
    if request.method=='POST':
      date=request.form['date']
      name=request.form['itemName']
      quantity=request.form['itemQuantity']
      rate=request.form['itemRate']
      total = int(quantity) * int(rate)
      category=request.form['itemCategory']
      id= session['id']
      print(id)
      insert_sql = "INSERT INTO INVENTORY (USERID, DATE, NAME, CATEGORY, QUANTITY, RATE, TOTAL) VALUES (?,?,?,?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, id)
      ibm_db.bind_param(prep_stmt, 2, date)
      ibm_db.bind_param(prep_stmt, 3, name)
      ibm_db.bind_param(prep_stmt, 4, category)
      ibm_db.bind_param(prep_stmt, 5, quantity)
      ibm_db.bind_param(prep_stmt, 6, rate)
      ibm_db.bind_param(prep_stmt, 7, total)
      ibm_db.execute(prep_stmt)

    return render_template('history.html', msg="Data saved successfuly..")

@app.route('/history')
def history():
  print(session['username'])
  students = []
  sql = "SELECT * FROM INVENTORY"
  stmt = ibm_db.exec_immediate(conn, sql)
  dictionary = ibm_db.fetch_both(stmt)
  print(dictionary)
  while dictionary != False:
    # print ("The Name is : ",  dictionary)
    students.append(dictionary)
    dictionary = ibm_db.fetch_both(stmt)

  if students:
    return render_template("history.html", students = students)


@app.route('/reports')
def reports():
  global userid
  msg = session['username']
  userid= session['id']
  msg = 'Welcome'+" "+session['username']+"!!"
  results = []

  sql ="SELECT CATEGORY, COUNT(CATEGORY) AS count FROM INVENTORY WHERE USERID = ? GROUP BY CATEGORY;"
  stmt = ibm_db.prepare(conn, sql)
  ibm_db.bind_param(stmt,1,userid)
  ibm_db.execute(stmt)
  dictionary = ibm_db.fetch_both(stmt)
  print(dictionary)
  while dictionary != False:
    # print ("The Name is : ",  dictionary)
    results.append(dictionary)
    dictionary = ibm_db.fetch_both(stmt)
  print(results[0]["CATEGORY"])

  data=[0,0,0,0,0,0]
  for result in results:
        if(result["CATEGORY"] == "books"):
          data[0] = result["COUNT"]
        elif(result["CATEGORY"] == "cosmetics"):
          data[1] = result["COUNT"]
        elif(result["CATEGORY"] == "electronicitems"):
          data[2] = result["COUNT"]
        elif(result["CATEGORY"] == "food"):
          data[3] = result["COUNT"]
        elif(result["CATEGORY"] == "furniture"):
          data[4] = result["COUNT"]
        elif(result["CATEGORY"] == "miscellaneous"):
          data[5] = result["COUNT"]
  print(data)
  
  category = [[],[],[],[],[],[]]
  dummy = []
  sql ="SELECT NAME, CATEGORY FROM INVENTORY WHERE USERID = ?"
  stmt = ibm_db.prepare(conn, sql)
  ibm_db.bind_param(stmt,1,userid)
  ibm_db.execute(stmt)
  dictionary = ibm_db.fetch_both(stmt)
  print(dictionary)
  while dictionary != False:
    # print ("The Name is : ",  dictionary)
    dummy.append(dictionary)
    dictionary = ibm_db.fetch_both(stmt)
  
  
  for result in dummy:
    if(result["CATEGORY"] == "books"):
      category[0].append(result["NAME"])
    elif(result["CATEGORY"] == "cosmetics"):
      category[1].append(result["NAME"])
    elif(result["CATEGORY"] == "electronicitems"):
      category[2].append(result["NAME"])
    elif(result["CATEGORY"] == "food"):
      category[3].append(result["NAME"])
    elif(result["CATEGORY"] == "furniture"):
      category[4].append(result["NAME"])
    elif(result["CATEGORY"] == "miscellaneous"):
      category[5].append(result["NAME"])

  print(category)
  total = sum(data)
  print(total)

  return render_template('reports.html', msg = msg, results = data, total = total, category = category)

@app.route('/logout')
def logout():
  session.pop('loggedin', None)
  session.pop('id', None)
  session.pop('username', None)
  return render_template('register.html')

if __name__ =='__main__':
    app.run(host='0.0.0.0',debug=True)