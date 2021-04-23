from flask import Flask, render_template, request, jsonify, make_response
import pandas as pd
from os import listdir, system,chdir,getcwd
from os.path import isfile, join, getctime, abspath
import websockets
import asyncio
#from flask_socketio import SocketIO, send

app = Flask(__name__)

message = ""
global csvFolder
global csv_path
global crawlerFolder
global homepath

assetsFolder = join("assets")
csvFolder = join("csv")
csv_path = join(assetsFolder,csvFolder)

crawlerFolder = join("crawlers")
homepath='..'

# create index route
@app.route('/', methods=['POST','GET'])
def index():
    return render_template("index.html", message = message)


@app.route('/crawler')
def crawlerindex():

    csvwlcmsg = 'Choose CSV on the left box to show contents!'
    csvList = [f for f in listdir(csv_path) if isfile(join(csv_path, f))]

    return render_template("crawler.html", csv_list = csvList, msg=csvwlcmsg)

@app.route('/getCSV')
def getCSV():

    csvList = [f for f in listdir(csv_path) if isfile(join(csv_path, f))]

    #receive csvname parameter
    csvName = request.args.get('csvName')

    #read csv
    pd.set_option('display.max_rows', None)
    df = pd.read_csv(join(csv_path, csvName))

    return render_template("crawler.html", column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip, csv_list = csvList)

##########Crawler############``
@app.route('/getCrawler', methods=['POST', 'GET'])
def crawler():
    if request.method == 'POST':
        crawler = request.form['crawler']
        sucMsg = "crawler has succesfully run! Please refresh the page to see the CSV file. CSV generated: "
        failMsg = "crawler has failed to run."
        if crawler == "TW":
            try:
                old_list = getFiles()
                chdir(crawlerFolder)
                result = system('python twitter.py')
                if result == 0:
                    print("Crawler run successful")
                    csv_list = getGeneratedCSV(old_list)
                    print(csv_list)
                    for csv in csv_list:
                        sucMsg += '<br>'+ csv
                    return jsonify({'result': sucMsg})
                else:
                    print("Run failed")
                    return jsonify({'result': failMsg})
            except:
                return jsonify({'result': failMsg})
        elif crawler == "YT":
            try:
                old_list = getFiles()
                chdir(crawlerFolder)
                result = system('python youtube.py')
                if result == 0:
                    print("Crawler run successful")
                    csv_list = getGeneratedCSV(old_list)
                    print(csv_list)
                    for csv in csv_list:
                        sucMsg += '<br>'+ csv
                    return jsonify({'result': sucMsg})
                else:
                    print("Run failed")
                    return jsonify({'result': failMsg})
            except:
                return jsonify({'result': failMsg})
        elif crawler == "FB":
            try:
                old_list = getFiles()
                facepageFolder = join('Facepager','src')
                facepagerPath = join(crawlerFolder,facepageFolder)
                chdir(facepagerPath)
                print(facepagerPath)
                result = system('python Facepager.py')
                if result == 0:
                    print("Crawler run successful")
                    csv_list = getGeneratedCSV(old_list)
                    print(csv_list)
                    for csv in csv_list:
                        sucMsg += '<br>'+ csv
                    return jsonify({'result': sucMsg})
                else:
                    print("Run failed")
                    return jsonify({'result': failMsg})
            except:
                return jsonify({'result': failMsg})
        elif crawler == "IG":
            try:
                old_list = getFiles()
                chdir(crawlerFolder)
                result = system('python igv2_deploy.py')
                if result == 0:
                    print("Crawler run successful")
                    csv_list = getGeneratedCSV(old_list)
                    print(csv_list)
                    for csv in csv_list:
                        sucMsg += '<br>'+ csv
                    return jsonify({'result': sucMsg})
                else:
                    print("Run failed")
                    return jsonify({'result': failMsg})
            except:
                return jsonify({'result': failMsg})
        elif crawler == "RD":
            # to be updated
            try:
                old_list = getFiles()
                chdir(crawlerFolder)
                result = system('python reddit.py')
                if result == 0:
                    print("Crawler run successful")
                    csv_list = getGeneratedCSV(old_list)
                    print("print test")
                    print(csv_list)
                    for csv in csv_list:
                        sucMsg += '<br>'+ csv
                    print(getcwd())
                    return jsonify({'result': sucMsg})
                else:
                    print("Run failed")
                    return jsonify({'result': failMsg})
            except:
                print("exception")
                return jsonify({'result': failMsg})
    else:
        return render_template('crawler.html')

@app.route('/getKw', methods=['POST', 'GET'])
def kw():
    if request.method == 'POST':
        kw = request.form['kwInput']
        with open(join('crawlers','input.txt'), "r") as file:
            lines = file.readlines()
            print('lines: ', end='')
            print(lines)
        lines[0] = kw +'\n'
        
        with open(join('crawlers','input.txt'), "w") as file:
            for line in lines:
                file.write(line)
        return jsonify({'result': 'Keyword entered'})
    else:
        return render_template('crawler.html')

@app.route('/getNum', methods=['POST', 'GET'])
def num():
    if request.method == 'POST':
        num = request.form['numInput']

        try:

            if eval(num)<0:
                print('Number less than 0')
                return ({'result':'Number entered failed. Please enter a valid number.'})
            else:
                with open(join('crawlers','input.txt'), "r") as file:
                    lines = file.readlines()
                    print('lines: ', end='')
                    print(lines)
                lines[1] = num +'\n'
                
                with open(join('crawlers','input.txt'), "w") as file:
                    for line in lines:
                        file.write(line)
                return ({'result':'Number entered successfully'})
        except:
            return ({'result':'Number entered failed'})
    else:
        return render_template('crawler.html')
        
@app.route('/getDir', methods=['POST', 'GET'])
def dir():
    csvwlcmsg = 'Choose CSV on the left box to show contents!'
    if request.method == 'POST':
        try:
            global csvFolder
            csvFolder = request.form["dir"]
            csvList = listdir(csvFolder)
        except:
            return render_template("crawler.html")
        
    return render_template("crawler.html", csv_list = csvList, msg=csvwlcmsg)

def getGeneratedCSV(old_list):
    chdir(homepath)
    csv_list = getFiles()
    print('oldlist: ', end='')
    print(old_list)
    generated = [file for file in csv_list if file not in old_list]
    print(generated)
    return generated   

def getFiles():
    list_of_files = listdir(csv_path)
    csv_list = []
    for file in list_of_files:
        if file.endswith('.csv'):
            csv_list.append(file)
    print('current list: ', end='')
    print(csv_list)
    return csv_list

if __name__ == "__main__":
    app.run(debug=True)
