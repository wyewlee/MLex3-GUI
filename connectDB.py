from flask import Flask, render_template, request, redirect,url_for
from flask_mysqldb import MySQL
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import json
import pandas as pd
import os
import websockets
import asyncio
from flask_socketio import SocketIO, send

app = Flask(__name__)
message = ""

app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql12387086'
app.config['MYSQL_PASSWORD'] = '2QcQXFXL9C'
app.config['MYSQL_DB'] = 'sql12387086'

mysql = MySQL(app)

client = MongoClient("mongodb+srv://Licz728:Vin7282073@cluster.bhgyx.mongodb.net/sample_analytics?retryWrites=true&w=majority") #host uri
db = client.sample_analytics #Select the database
collection = db.accounts #Select the collection name

#create index route
@app.route('/', methods=['POST','GET'])
def index():
    return render_template("index.html", message = message)

@app.route('/showDB')
def pageindex():
    return render_template('connectDB.html')

@app.route('/MySql')
def databaseindex():
    cur = mysql.connection.cursor()
    cur1 = mysql.connection.cursor()

    cur.execute('''SELECT * FROM staff''')
    results = cur.fetchall()
    print('Staff table:')
    cur1.execute('''SHOW columns FROM staff''')
    results1 = cur1.fetchall()
    df = pd.DataFrame(results1)
    #print(df.iloc[:,0])
    df = df.iloc[:,0]
                
    df2 = pd.DataFrame(data=results)
    df2.columns = df
    df2.style.hide_index()
    print(df2)

    cur.execute('''SHOW TABLES''')
    results = cur.fetchall()
    print(results)

    return render_template('connectDB.html' ,column_names=df2.columns.values, row_data=list(df2.values.tolist()), zip=zip)
           

@app.route('/getSql', methods=['POST', 'GET'])
def MySql():
    if request.method == 'POST':
        print("1")
        Mysql = request.form['MySql']
        print("2")
        if Mysql == "staff":
            # to be updated
            try:
                cur = mysql.connection.cursor()
                cur1 = mysql.connection.cursor()

                cur.execute('''SELECT * FROM staff''')
                results = cur.fetchall()
                print('Staff table:')
                cur1.execute('''SHOW columns FROM staff''')
                results1 = cur1.fetchall()
                df = pd.DataFrame(results1)
                #print(df.iloc[:,0])
                df = df.iloc[:,0]
                
                df2 = pd.DataFrame(data=results)
                df2.columns = df
                df2.style.hide_index()
                print(df2)
                print("Done")
                return render_template('connectDB.html' ,column_names=df2.columns.values, row_data=list(df2.values.tolist()), zip=zip)
                
            except:
                return render_template('connectDB.html')
        elif Mysql == "student":
            # to be updated
            try:
                cur = mysql.connection.cursor()
                cur1 = mysql.connection.cursor()

                cur.execute('''SELECT * FROM student''')
                results = cur.fetchall()
                print('Student table:')
                cur1.execute('''SHOW columns FROM student''')
                results1 = cur1.fetchall()
                df = pd.DataFrame(results1)
                #print(df.iloc[:,0])
                df = df.iloc[:,0]
                
                df2 = pd.DataFrame(data=results)
                df2.columns = df
                df2.style.hide_index()
                print(df2)
                print("Done")
                return render_template('/getSql' ,column_names=df2.columns.values, row_data=list(df2.values.tolist()), zip=zip)
            except:
                return render_template('connectDB.html')
    else:
        print("fail")
        return render_template('connectDB.html')


@app.route("/", methods=['POST'])
def insert_document():
    req_data = request.get_json()
    collection.insert_one(req_data).inserted_id
    return ('', 204)

@app.route('/read')
def get():
    documents = collection.find()
    response = []
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    
    #df3=pd.read_json()
    df3=pd.read_json(json.dumps(response))
    print(df3.head(10))

    #return json.dumps(response)
    return render_template('connectDB.html' ,column_names1=df3.columns.values, row_data1=list(df3.values.tolist()), zip=zip)

if __name__ == "__main__":
    app.run(debug=True)