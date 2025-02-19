from flask import Flask  # 导入Flask类 ，flask是包
from api import api_bp
from backStage import backStage



app = Flask(__name__)       # 创建一个flask应用程序的实例，它是整个应用程序的核心对象
app.register_blueprint(api_bp,url_prefix='/api')
app.register_blueprint(backStage)








if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)               # 默认 Debug mode: off
