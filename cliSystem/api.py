from datetime import datetime
from flask import Blueprint,jsonify,request,Response
import time
import sql,os,json
from flask_cors import CORS


api_bp = Blueprint('api',__name__)
# resources={r"api/*":{'origins':'http://localhost:8080'},r"/static/workers/*":{"origins":'*'}}
# ,supports_credentials = True
CORS(api_bp,resoruces=r'/*')
db = sql.Mysql_Object('127.0.0.1','root','12root','cli_db')

# 查询student表中所有信息函数
def stu_list(id):
    stusql = "select * from student where student_id='{}'".format(id)
    stucount, stures = db.select_sql(stusql)
    results = []
    basedir = os.path.abspath(os.path.dirname((__file__))) # 获取项目跟路径
    for stu in stures:
        stu_data = {}
        stu_data['stuId'] = stu[0]
        stu_data['name'] = stu[1]
        stu_data['gender'] = stu[2]
        stu_data['age'] = stu[3]
        stu_data['nickName'] = stu[4]
        stu_data['pwd'] = stu[5]
        stu_data['imgFile'] = os.path.join(basedir,stu[6]) #  根据相对路径获取图片的绝对路径
        results.append(stu_data)
    return jsonify({'students': results})


# 设置学生信息接口
@api_bp.route('/students',methods=['GET','POST'])
def get_students():
    if request.method == 'POST':
        data = request.get_json()
        nick = data['nickName']
        mima = data['pwd']
        sid = data['stuId']
        updatesql = "update student set nick_name='{}',pwd='{}' where student_id='{}'".format(nick,mima,sid)
        db.excute_sql(updatesql)
        return stu_list(sid)
    elif request.method == 'GET':
        token = request.headers.get('token')
        stusql = "select * from student where student_id='{}'".format(token)
        stucount, stures = db.select_sql(stusql)
        if stucount:  # 获取就诊卡信息
            cardsql = "select * from medical_card where user_id='{}'".format(token)
            cardcount, cardres = db.select_sql(cardsql)
            card={}
            for i in cardres:
                card['cardId'] = i[0]
                card['userId'] = i[1]
                card['money'] = i[2]
            stuInfo = json.loads(stu_list(token).data.decode('utf-8'))
            data={'students':stuInfo,'card':card}
            return jsonify(data)
        else:
            return 'nothing'
    else:
        return '请求失败'

# 查看用户头像接口
@api_bp.route('/students/avatar/<imageId>.png')
def get_avatar(imageId):
    if imageId =='undefined':
        return '图片没有标识符'
    else:
        # 图片上传保存的路径
        with open('D:/Pycode/cliSystem/uploads/avatar/{}.png'.format(imageId),'rb') as f:
            image = f.read()
            resp = Response(image,mimetype="image/png")
            return resp


# 上传头像接口
@api_bp.route('/students/upAvatar',methods=['POST'])
def up_avatar():
    # 获取项目跟路径
    basedir = os.path.abspath(os.path.dirname((__file__)))
    # 获取文件
    file = request.files['avatar']
    # 将用户id作为文件名
    imageId = request.form.get('imageId')
    filename =  imageId+'.png'
    if file is None:
        return jsonify(({'error':'no image uploaded'}))

    # 存储文件
    file.save(os.path.join(basedir,'uploads\\avatar',filename))
    res = 'http://127.0.0.1:5000/api/students/avatar/{}.png?t={}'.format(imageId,time.time())
    return res


# 诊疗费用信息接口
@api_bp.route('/diagnosisFee',methods=['POST'])
def diagnosis_fee():
    data = request.get_json()
    fee_sql = "select dia_name,price from diagnosis where dia_name like '%{}%' ".format(data['value'])
    fee_count, fee_res = db.select_sql(fee_sql)
    results = []
    for fee in fee_res:
        fee_data = {}
        fee_data['dia_name'] = fee[0]
        fee_data['price'] = fee[1]
        results.append(fee_data)
    return jsonify({'dia_fee':results})


# 药品查询接口
@api_bp.route('/drugs',methods=['POST'])
def drugs():
    data = request.get_json()
    drug_sql = "select drug_name,drug_specification,drug_form,enterprise,price from drug where drug_name like '%{}%' ".format(data['value'])
    drug_count, drug_res = db.select_sql(drug_sql)
    results = []
    for drug in drug_res:
        drug_data = {}
        drug_data['name'] = drug[0]
        drug_data['specification'] = drug[1]
        drug_data['form'] = drug[2]
        drug_data['enterprise'] = drug[3]
        drug_data['price'] = drug[4]
        results.append(drug_data)
    return jsonify({'drugs': results})


# 查询医生信息方法
def doc_list(depart,key):
    if key=='keshi':
        docsql = "select doc_id,doc_name,post_title,skilled,depart from doctor where depart='{}'".format(depart)
        doccount, docres = db.select_sql(docsql)
    elif key=='id':
        docsql = "select doc_id,doc_name,post_title,skilled,depart from doctor where doc_id='{}'".format(depart)
        doccount, docres = db.select_sql(docsql)
    results = []
    for doc in docres:
        doc_data = {}
        doc_data['doc_id'] = doc[0]
        doc_data['doc_name'] = doc[1]
        doc_data['doc_post'] = doc[2]
        doc_data['doc_skill'] = doc[3]
        doc_data['depart'] = doc[4]
        results.append(doc_data)
    return jsonify({'doctors': results})


# 医生信息查询接口
@api_bp.route('/doctors', methods=['POST'])
def doctors():
    data = request.get_json()
    if data.get('depart') is not None:
        return doc_list(data['depart'],'keshi')
    elif data.get('doc_id') is not None:
        return doc_list(data['doc_id'], 'id')
    else:
        return '请求数据有误'

# 获取医生头像接口
@api_bp.route('/doctors/photo/<imageId>.png')
def get_doc_img(imageId):
    if imageId =='undefined':
        return '图片没有标识符'
    else:
        # 图片上传保存的路径
        with open('D:/Pycode/cliSystem/uploads/docImg/{}.png'.format(imageId),'rb') as f:
            image = f.read()
            resp = Response(image,mimetype="image/png")
            return resp


# 获取用户昵称方法
def get_nick(user_id):
    nicksql="select nick_name from student where student_id='{}'".format(user_id)
    nick_count,nick_res = db.select_sql(nicksql)
    return nick_res


# 查询对应医生评价方法
def sel_eval(doc_id):
    eval_sql="select doc_id,user_id,DATE_FORMAT(`eval_time`,'%Y.%m.%d'),eval_content from doc_evaluation where doc_id = '{}' order by eval_time desc".format(doc_id)
    evalcount, evalres = db.select_sql(eval_sql)
    results = []
    for eval in evalres:
        eval_data = {}
        eval_data['doc_id'] = eval[0]
        # 根据用户id获取相应昵称
        nick = get_nick(eval[1])[0][0]
        eval_data['user_nick'] = nick
        eval_data['eval_time'] = eval[2]
        eval_data['eval_con'] = eval[3]
        results.append(eval_data)
    return jsonify({'evaluations': results})


# 访问对应医生评价接口
@api_bp.route('/evaluation/select',methods=['POST'])
def get_eval():
    data = request.get_json()
    return sel_eval(data['doc_id'])


# 添加评价接口
@api_bp.route('/evaluation/add',methods=['POST'])
def add_eval():
    data = request.get_json()
    eval_sql = "insert into doc_evaluation(doc_id,user_id,eval_time,eval_content) values ('{}','{}','{}','{}');"\
        .format(data['doc_id'],data['stu_id'],data['eval_time'],data['eval_con'])
    db.excute_sql(eval_sql)
    return '添加成功'


# 获取对应医生的值班情况方法
def duty(id):
    doc_sql = "select doc_name,post_title,skilled from doctor where doc_id='{}' ".format(id)
    doc_count,doc_res = db.select_sql(doc_sql)
    results = []
    for doc in doc_res:
        doc_data = {}
        doc_data['doc_name'] = doc[0]
        doc_data['doc_post'] = doc[1]
        doc_data['doc_skill'] = doc[2]
        results.append(doc_data)
    return results


# 访问值班医生接口
@api_bp.route('/doctor/duty',methods=['POST'])
def get_duty():
    data = request.get_json()
    duty_sql = "select * from on_duty where doc_id='{}'".format(data['doc_id'])
    duty_count,duty_res = db.select_sql(duty_sql)
    doc_info = duty(data['doc_id'])
    results = []
    for dutys in duty_res:
        duty_data = {}
        duty_data['duty_id'] = dutys[0]
        duty_data['doc_id'] = dutys[1]
        duty_data['doc_name'] = doc_info[0]['doc_name']
        duty_data['doc_post'] = doc_info[0]['doc_post']
        duty_data['doc_skill'] = doc_info[0]['doc_skill']
        duty_data['duty_time'] = dutys[2]
        duty_data['duty_period'] = dutys[3]
        duty_data['duty_price'] = dutys[4]
        duty_data['reg_quantity'] = dutys[5]
        results.append(duty_data)
    return jsonify({'dutys': results})


# 修改挂号数量
@api_bp.route('/doctor/regcount',methods=['POST'])
def change_regcount():
    data = request.get_json()
    reg_money_sql = "select price from on_duty where id='{}'".format(data['regid'])
    regcount, regres = db.select_sql(reg_money_sql)
    if data['Regist']:
        reg_count_sql = "update on_duty set register_quantity='{}' where id='{}'".format((data['count']-1),data['regid'])
        db.excute_sql(reg_count_sql)
        money = data['cardMoney'] - regres[0][0]
        cardsql ="update medical_card set money='{}' where card_id='{}'".format(money,data['cardId'])
        db.excute_sql(cardsql)

    else:
        updatesql = "update on_duty set register_quantity='{}' where id='{}'".format((data['count']+1), data['regid'])
        db.excute_sql(updatesql)
        money = data['cardMoney'] + regres[0][0]
        cardsql = "update medical_card set money='{}' where card_id='{}'".format(money,data['cardId'])
        db.excute_sql(cardsql)
    return jsonify({'cardMoney':money})


# 插入/删除挂号记录接口
@api_bp.route('/doctor/regcord',methods=['POST'])
def update_record():
    data = request.get_json()
    if data['isReg']:
        gmt_time = datetime.strptime(data['duty_time'],'%a, %d %b %Y %H:%M:%S %Z')
        reg_time = gmt_time.strftime('%Y-%m-%d')
        insert_sql = "insert into reg_record(reg_id,user_id,doc_id,duty_time,duty_period,price) values({},'{}','{}','{}','{}',{})"\
            .format(data['reg_id'],data['user_id'],data['doc_id'],reg_time,data['duty_period'],data['price'])
        db.excute_sql(insert_sql)
        return '成功添加挂号'
    else:
        del_sql = "delete from reg_record where reg_id='{}'".format(data['reg_id'])
        db.excute_sql(del_sql)
        return '成功删除挂号'


# 查询挂号记录接口
@api_bp.route('/doctor/getrecord',methods=['POST'])
def get_record():
    data = request.get_json()
    get_sql = "select reg_id,doc_id,duty_time,duty_period from reg_record where user_id='{}'".format(data['user_id'])
    count,res = db.select_sql(get_sql)
    results = []
    if count:
        for record in res:
            record_data = {}
            record_data['reg_id'] = record[0]
            doc_sql = "select doc_name from doctor where doc_id='{}'".format(record[1])
            count, doc_name = db.select_sql(doc_sql)
            record_data['doc_id'] = record[1]
            record_data['doc_name']=doc_name[0][0]
            record_data['duty_time'] = record[2]
            record_data['duty_period'] = record[3]
            results.append(record_data)
        return jsonify({'records': results})
    else:
        return jsonify({'records': 'none'})


# 医院概况接口
@api_bp.route('/introduce')
def get_introduce():
    with open('D:/Pycode/cliSystem/static/introduce.json','r',encoding='utf-8') as f:
        intro = json.load(f)
        return jsonify(intro)

# 浏览器解决请求跨域问题
# @api_bp.after_request
# def add_cors(resp):
#     resp.headers['Access-Control-Allow-Origin']='*'
#     resp.headers['Access-Control-Allow-Methods']='GET,POST,PUT,DELETE,OPTIONS'
#     resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
#     return resp




