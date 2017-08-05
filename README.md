# flask-web
flask web pro

### 开发环境

**在开发环境启用virtualenv**

安装virtualenv: pip install virtualenv, linux环境增加sudo权限

安装成功后，启动virtualenv环境：

```cmd

cd flask-web
virtualenv venv
. venv/bin/activate             #windows环境使用 venv\scripts\activate
pip install Flask               #安装过后可不执行
pip install pymongo             #安装过后可不执行
pip install Flask-Markdown      #安装过后可不执行
pip install Flask-Misaka        #安装过后可不执行
```

退出virtualenv环境使用：
```
deactivate
```

### mac下启动mongodb

```
cd /Users/caojian02/mongodb
mongodb/bin/mongod --dbpath ./db/data --logpath ./db/log/mongodb.log --logappend &
mongodb/bin/mongod --dbpath ./db/data --logpath ./db/log/mongodb.log &
```

### 启动app
```
python src/main.py
```
