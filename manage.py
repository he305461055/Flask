import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask import request,jsonify,render_template,Response,Flask
import pymysql
import json

app = Flask(__name__)

def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'db': 'spiders',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }


#def make_shell_context():
#    return dict(app=app, db=db)
#    manager.add_command("shell",Shell(make_context=make_shell_context))
#    manager.add_command('db', MigrateCommand)
def get_data(tablename,parameter):
    datalist=[]
    connection=pymysql.connect(**config)
    with  connection.cursor() as cursor:
        sql='SELECT %s FROM %s limit 1 ' %(parameter,tablename)
        cursor.execute(sql)
        for row in cursor.fetchall():
            sss=str(row)
            #aa=json.loads(sss)
            #print(aa)
            #print(aa['url'])
            #value='\"value\":' +str(row)
            #print(value)
            datalist.append(row)
    return datalist


'''
@app.route('/api/<string:str>', methods=['GET'])
def get_task(str):
    #if request.method=='POST':
    #    print(request.form)
    #    print(request.get_data())
    #    print(request.data)
    #    return jsonify({tablename: get_data(tablename,parameter)})
    #else:
    url = request.url
    tablename = url.split('/')[-1].split('?')[0]
    parameter = url.split('?')[-1]
    return json.dumps(get_data(tablename,parameter))
    #return "%s(%s);" % (request.args.get('callback'), json.dumps(get_data(tablename,parameter)))

@app.route("/data", methods=["GET"])
def getdata():
    connection = pymysql.connect(**config)
    with  connection.cursor() as cursor:
        sql = 'SELECT url,CBD FROM meituanshop limit 10 '
        cursor.execute(sql)
        #ones = [[i[0], i[1]] for i in cursor.fetchall()]
        #for row in cursor.fetchall():
        entries=cursor.fetchall()
        return render_template('qianduan.html',entries=entries)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
'''

@app.route('/')
def hello_world():
    return render_template('test.html')

@app.route('/echarts')
def echarts():
    #data=["Android","IOS","PC","Ohter"]
    #return render_template('echarts.html',data=data)
    connection = pymysql.connect(**config)
    datalist = []
    with  connection.cursor() as cursor:
        sql = 'SELECT shopname,SUBSTRING(shopsold,3) as shopsold FROM meituanshop  WHERE shopsold<>"None" LIMIT 10'
        cursor.execute(sql)
        for row in cursor.fetchall():
            datalist.append(row)
    content = json.dumps({'data':datalist})
    resp = Response_headers(content)
    return resp


@app.errorhandler(403)
def page_not_found(error):
    content = json.dumps({"error_code": "403"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(404)
def page_not_found(error):
    content = json.dumps({"error_code": "404"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(400)
def page_not_found(error):
    content = json.dumps({"error_code": "400"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(410)
def page_not_found(error):
    content = json.dumps({"error_code": "410"})
    resp = Response_headers(content)
    return resp


@app.errorhandler(500)
def page_not_found(error):
    content = json.dumps({"error_code": "500"})
    resp = Response_headers(content)
    return resp

if __name__ == '__main__':    
    app.run(host='0.0.0.0')