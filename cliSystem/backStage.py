from flask import Blueprint,request,redirect,url_for,render_template  # 导入Flask类 ，flask是包
import sql,json,base64



backStage = Blueprint('bs', __name__)
db = sql.Mysql_Object('127.0.0.1','root','12root','cli_db')

@backStage.route('/')
def index():
    return redirect('login')

@backStage.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        userrole = request.form.get('role')
        if username and password and userrole != '2':
            usersql = 'select doc_id,pwd,role from doctor where doc_id='+username
            usercount,userres = db.select_sql(usersql)
            if usercount == 0:
                return render_template('login.html', message='用户不存在')
            else:
                if username == userres[0][0] and password == userres[0][1]:
                    username_bytes = username.encode('utf-8')  # 将字符串转换为bytes类型
                    encoded_username = base64.b64encode(username_bytes)  # 对bytes类型进行base64编码
                    if userrole == '0' and userrole==userres[0][2]:
                        return redirect(url_for('bs.admin',userId=encoded_username))
                    elif userrole == '1' and userrole==userres[0][2]:
                        return redirect(url_for('bs.doctor',userId=encoded_username))
                    else:
                        return render_template('login.html', message='身份错误')
                else:
                    return render_template('login.html',message='密码错误')
        return render_template('login.html')
    return render_template('login.html')


@backStage.route('/doctor/?<userId>')
def doctor(userId):
    decoded_userId_bytes = base64.b64decode(userId)
    decoded_userId = decoded_userId_bytes.decode('utf-8')
    return render_template('doctor.html',userId=decoded_userId)


@backStage.route('/admin',methods=['GET','POST'])
def admin():
    # 左侧导航栏点击事件的数据库操作
    if request.method == 'POST':
        info = request.json.get('object')
        page = int(request.json.get('page',0))
        if info == 'stu':
            stusql = 'select student_id,full_name,gender,age,nick_name from student'
            stucount, stures = db.select_sql(stusql)
            return json.dumps(stures)
        elif info == 'doc':
            if page:
                offset = (page - 1) * 10
                docsql = "select doc_id,depart_id,depart,doc_name,gender,post_title,skilled from doctor where role='1' limit {},10".format(offset)
                doccount, docres = db.select_sql(docsql)
            else:
                docsql = "select doc_id,depart_id,depart,doc_name,gender,post_title,skilled from doctor where role='1'"
                doccount, docres = db.select_sql(docsql)
            doctor={
                "doctorcount":doccount,
                "doctors":docres
            }
            return json.dumps(doctor)
        elif info == 'drug':
            if page:
                # 计算出SQL语句中的OFFSET值
                offset = (page-1)*6
                # 使用SQL查询数据
                drugsql = 'select * from drug limit {},6'.format(offset)
                drugcount, drugres = db.select_sql(drugsql)
            else:
                drugsql = 'select * from drug'
                drugcount, drugres = db.select_sql(drugsql)
            drug={
                "drugcount":drugcount,
                "drugs":drugres
            }
            return json.dumps(drug)
    elif request.method=='GET':
        # 获取登录界面传来的账号
        userId = request.args.get('userId')
        decoded_userId_bytes = base64.b64decode(userId)
        decoded_userId = decoded_userId_bytes.decode('utf-8')
        return render_template('admin.html', userId=decoded_userId)
    return render_template('admin.html')
