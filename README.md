# CFrating
统计ACM集训队成员CF rating以及每场比赛参与情况

使用Django编写

rating页显示每个账号的rating，参与场次以及最近五场的趋势

contests页显示每场比赛的参与人数以及每个人的解题数与排名

Ubuntu安装
```sh
# clone 代码
git clone https://github.com/maggch97/CFrating.git
# 安装python3以及pip3
sudo apt install python3 python3-pip
# 安装django以及bootstrap3
sudo pip3 install django django-bootstrap5
# 建立数据库
cd CFrating
python3 manage.py makemigrations
python3 manage.py migrate
# 创建管理员账户
python3 manage.py createsuperuser
# 启动服务器
python3 manage.py runserver 0:8000
# 访问 http://ip:8000/admin 填写学生信息
#启动数据获取程序，默认每两分钟更新一人信息
python3 get.py
# 地址 http://ip:8000/
```
