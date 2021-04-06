# Fzu
# +F
# 更新结束


from flask import Flask
from flask import json
from flask.globals import request
from flask.json import jsonify
from flask.wrappers import Response
from werkzeug.exceptions import abort
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from math import ceil
import time
import redis

app = Flask(__name__)
app.config["SECRET_KEY"] = "dsaiwe982nzcxsa79e812dsa"


tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'state': 'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False,
        'owner':1,
        'start_time':'2019.1.1',
        'end_time':'2019.1.2'
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'state': 'Need to find a good Python tutorial on the web',
        'done': False,
        'owner':1,
        'start_time':'2019.2.1',
        'end_time':'2019.2.2'
    },
    {
        'id': 3,
        'title': 'Test_title_3',
        'state': 'Test_state_3',
        'done': False,
        'owner':1,
        'start_time':'2019.3.1',
        'end_time':'2019.3.2'
    },
    {
        'id': 4,
        'title': 'Test_title_3',
        'state': 'Test_state_33333',
        'done': False,
        'owner':1,
        'start_time':'2019.3.1',
        'end_time':'2019.3.2'
    },
    {
        'id': 5,
        'title': 'Test_title_3',
        'state': 'Tsssss333',
        'done': False,
        'owner':1,
        'start_time':'2019.3.1',
        'end_time':'2019.3.2'
    }
]

users = [
    {
        'id':0,
        'username':'0',
        'password':'0'
    },
    {
        'id':1,
        'username':'1',
        'password':'1'
    },
    {
        'id':2,
        'username':'2',
        'password':'2'
    },
    {
        'id':3,
        'username':'3',
        'password':'3'
    },
    {
        'id':4,
        'username':'4',
        'password':'4'
    },
    {
        'id':5,
        'username':'5',
        'password':'5'
    },
    {
        'id':6,
        'username':'6',
        'password':'6'
    },
    {
        'id':6,
        'username':'6',
        'password':'6'
    },
    {
        'id':7,
        'username':'7',
        'password':'7'
    },
    {
        'id':8,
        'username':'8',
        'password':'8'
    }
]

errors = [
    {
        "code":404,
        "state":"Page Not Found!"
    },
    {
        "code":401,
        "state":"401"
    },
    {
        "code":402,
        "state":"402"
    },
]

status = [
    {
        "code":1,
        "state":"Delete Successfully!"
    },
    {
        "code":2,
        "state":"Id No Found!"
    },
    {
        "code":3,
        "state":"Add Failed!"
    }
]


@app.route("/api/v1/get",methods=["GET"])
def get():
    return "addr:"+str(request.remote_addr)+"user:"+str(request.remote_user)+"1:"+str(request.args)+"  2:"+str(request.host)+"  3:"+str(request.host_url)+"  4:"+str(request.base_url)+"  5:"+str(request.full_path)+"  6:"+str(request.url_root)+"  7:"+str(request.url_rule)+"  8:"+str(request.trusted_hosts)+"  9:"+str(request.method)+"  10:"+str(request.url)+"  11:"+str(request)

#####################删除###########################
# 删除接口，返回data中带有删除的task
@app.route("/api/v1/del_task/<int:id>",methods=["DELETE"])
def del_task(id):
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=4,message="Have Not Login",data=""))
    user_id=token_result['id']


    for i in tasks :
        if i["id"]==id and i["owner"]==user_id:
            del_task = i
            tasks.remove(i)
            return jsonify(return_Feedback(status=0,message="Delete Successfully",data=del_task))
    return jsonify(return_Feedback(status=6,message="Delete Failed,Id Not Found",data=""))

# 删除所有已完成事项
@app.route("/api/v1/del_all_done",methods=["DELETE"])
def del_all_done():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=4,message="Have Not Login",data=""))
    user_id=token_result['id']

    temp_task1 = []
    for i in tasks:
        if i["done"] == True and i["owner"]==user_id:
            temp_task1.append(i)
    for j in temp_task1:
        tasks.remove(j)
    return jsonify(return_Feedback(status=0,message="Delete Successfully",data=temp_task1))

# 删除所有已代办事项
@app.route("/api/v1/del_all_undone",methods=["DELETE"])
def del_all_undone():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=4,message="Have Not Login",data=""))
    user_id=token_result['id']


    temp_task2 = []
    for i in tasks:
        if i["done"] == False and i["owner"]==user_id:
            temp_task2.append(i)
    for j in temp_task2:
        tasks.remove(j)
    return jsonify(return_Feedback(status=0,message="Delete Successfully",data=temp_task2))
#######################删除#########################



#######################新增#########################
# 新增task接口，返回data中带有新增的task
@app.route("/api/v1/add_task",methods=["POST"])
def add_task():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=4,message="Have Not Login",data=""))
    user_id=token_result['id']


    if not request.json or not 'title' in request.json:
        return jsonify(return_Feedback(status=5,message="Not Title In Your Request",data=""))
    
    year = (time.localtime(time.time()).tm_year)
    month = (time.localtime(time.time()).tm_mon)
    day = (time.localtime(time.time()).tm_mday)
    current_time = (str)(year)+"."+(str)(month)+"."+(str)(day)    
    
    task={
        "id":tasks[-1]["id"]+1,
        "title":request.json["title"],
        'state': request.json.get("state", ""),
        "done":False,
        "owner":user_id,
        "start_time":current_time,
        "end_time":request.json.get("end_time","")
    }
    tasks.append(task)
    # print(tasks)
    return jsonify(return_Feedback(status=0,message="Add Successfully",data=task))
#######################新增#########################



#######################更改#########################
# 将1条task设为已办
@app.route("/api/v1/set_a_done/<int:id>",methods=["PUT"])
def set_a_done_(id):
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=4,message="Have Not Login",data=""))
    user_id=token_result['id']



    for i in tasks:
        if i["id"] == id and i["owner"]==user_id:
            i["done"] = True
            return jsonify(return_Feedback(status=0,message="Change Successfully",data=i))
    return jsonify(return_Feedback(status=6,message="Id Not Found",data=""))

# 将1条task设为待办
@app.route("/api/v1/set_a_undone/<int:id>",methods=["PUT"])
def set_a_undone_(id):
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=4,message="Have Not Login",data=""))
    user_id=token_result['id']



    for i in tasks:
        if i["id"] == id and i["owner"]==user_id:
            i["done"] = False
            return jsonify(return_Feedback(status=0,message="Change Successfully",data=i))
    return jsonify(return_Feedback(status=6,message="Id Not Found",data=""))

# 将所有task设为已办
@app.route("/api/v1/set_all_done",methods=["PUT"])
def set_all_done_():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=4,message="Have Not Login",data=""))
    user_id=token_result['id']



    for i in tasks:
        if i["owner"]==user_id:
            i["done"]=True
    return jsonify(return_Feedback(status=0,message="Change Successfully",data=""))

# 将所有task设为待办
@app.route("/api/v1/set_all_undone",methods=["PUT"])
def set_all_undone_():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=4,message="Have Not Login",data=""))
    user_id=token_result['id']



    for i in tasks:
        if i["owner"]==user_id:
            i["done"]=False
    return jsonify(return_Feedback(status=0,message="Change Successfully",data=""))
#######################更改#########################



#######################查找#########################
@app.route("/api/v1/display_all_tasks",methods=["GET"])
def display_tasks():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=4,message="Have Not Login",data=""))
    user_id=token_result['id']

    conn.append(user_id,"Search_All/")
    

    user_tasks=[]
    for i in tasks:
        if i["owner"]==user_id:
            user_tasks.append(i)


    length=len(user_tasks)

    if length==0:
        return jsonify(return_Feedback(status=7,message="No Data",data=""))

    peer_page=5
    max_page=ceil(length/peer_page)


    current_page=0
    if not "page" in request.args:
        current_page=1
    else:
        request_page=int(request.args["page"])
        current_page=request_page    

    if(current_page>max_page or current_page<1):
        return jsonify(return_Feedback(status=8,message="Page Out Of Index",data=""))



    low=((current_page-1)*peer_page+1)
    up=low+peer_page-1

    tasks_in_this_page=[]
    for index in range(low,up+1):
        if(index>length):
            break
        tasks_in_this_page.append(user_tasks[index-1])


    info={
        "current_page":current_page,
        "max_page":max_page,
        "peer_page":peer_page,
        "has_next?":current_page<max_page,
        "has_prev":current_page>1,
        "total_data":length
    }
    return jsonify(return_Feedback(status=0,message=info,data=tasks_in_this_page))

@app.route("/api/v1/display_all_done_tasks",methods=["GET"])
def display_done_tasks():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=4,message="Have Not Login",data=""))
    user_id=token_result['id']

    conn.append(user_id,"Search_All_Done/")

    user_tasks=[]
    for i in tasks:
        if i["owner"]==user_id and i["done"]==True:
            user_tasks.append(i)



    length=len(user_tasks)
    
    if length==0:
        return jsonify(return_Feedback(status=7,message="No Data",data=""))
        

    peer_page=5
    max_page=ceil(length/peer_page)


    current_page=0
    if not "page" in request.args:
        current_page=1
    else:
        request_page=int(request.args["page"])
        current_page=request_page    

    if(current_page>max_page or current_page<1):
        return jsonify(return_Feedback(status=8,message="Page Out Of Index",data=""))



    low=((current_page-1)*peer_page+1)
    up=low+peer_page-1

    tasks_in_this_page=[]
    for index in range(low,up+1):
        if(index>length):
            break
        tasks_in_this_page.append(user_tasks[index-1])


    info={
        "current_page":current_page,
        "max_page":max_page,
        "peer_page":peer_page,
        "has_next?":current_page<max_page,
        "has_prev":current_page>1,
        "total_data":length
    }
    return jsonify(return_Feedback(status=0,message=info,data=tasks_in_this_page))

@app.route("/api/v1/display_all_undone_tasks",methods=["GET"])
def display_undone_tasks():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=4,message="Have Not Login",data=""))
    user_id=token_result['id']

    conn.append(user_id,"Search_All_Undone/")

    user_tasks=[]
    for i in tasks:
        if i["owner"]==user_id and i["done"]==False:
            user_tasks.append(i)


    length=len(user_tasks)
 
    if length==0:
        return jsonify(return_Feedback(status=7,message="No Data",data=""))
 
    peer_page=5
    max_page=ceil(length/peer_page)


    current_page=0
    if not "page" in request.args:
        current_page=1
    else:
        request_page=int(request.args["page"])
        current_page=request_page    

    if(current_page>max_page or current_page<1):
        return jsonify(return_Feedback(status=8,message="Page Out Of Index",data=""))



    low=((current_page-1)*peer_page+1)
    up=low+peer_page-1

    tasks_in_this_page=[]
    for index in range(low,up+1):
        if(index>length):
            break
        tasks_in_this_page.append(user_tasks[index-1])


    info={
        "current_page":current_page,
        "max_page":max_page,
        "peer_page":peer_page,
        "has_next?":current_page<max_page,
        "has_prev":current_page>1,
        "total_data":length
    }
    return jsonify(return_Feedback(status=0,message=info,data=tasks_in_this_page))

@app.route("/api/v1/search_task/query",methods=["GET"])
def search_task():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=4,message="Have Not Login",data=""))
    user_id=token_result['id']

    conn.append(user_id,"Search_By_Query/")

    args_dict=request.args.to_dict()
    keys_list = list(args_dict.keys())


    user_tasks=[]
    for i in tasks:
        if (i["owner"] == user_id) and query(task=i, keys_list=keys_list, args_dict=args_dict):
            user_tasks.append(i)
    if len(user_tasks)==0:
        return jsonify(return_Feedback(status=7,message="No Data",data=""))
    else:
        # 分页
        length=len(user_tasks)
        peer_page=5
        max_page=ceil(length/peer_page)


        current_page=0
        if not "page" in request.args:
            current_page=1
        else:
            request_page=int(request.args["page"])
            current_page=request_page    

        if(current_page>max_page or current_page<1):
            return jsonify(return_Feedback(status=8,message="Page Out Of Index",data=""))



        low=((current_page-1)*peer_page+1)
        up=low+peer_page-1

        tasks_in_this_page=[]
        for index in range(low,up+1):
            if(index>length):
                break
            tasks_in_this_page.append(user_tasks[index-1])


        info={
            "current_page":current_page,
            "max_page":max_page,
            "peer_page":peer_page,
            "has_next?":current_page<max_page,
            "has_prev":current_page>1,
            "total_data":length
        }
        return jsonify(return_Feedback(status=0,message=info,data=tasks_in_this_page))

@app.route("/api/v1/history",methods=["GET"])
def history():
    token_result = judge_token(request.headers)
    if token_result == False:
        return jsonify(return_Feedback(status=4,message="Have Not Login",data=""))
    user_id=token_result['id']

    try:
        temp_list = conn.get(name=(str)(user_id)).split('/')
    except:
        return jsonify(return_Feedback(status=9,message="No History",data=""))
    # print(temp_list)
    print(len(temp_list))

    list_length = len(temp_list)

    historys = []

    aString = ""

    # 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14

    if list_length>11:
        for i in range(list_length-11, list_length-1):
            historys.append(temp_list[i])
            aString+=temp_list[i]+"/"
            conn.set(1,aString)
        historys.reverse()
    else:
        for i in range(list_length-2,-1, -1):
            historys.append(temp_list[i])
        
    return jsonify(return_Feedback(status=0, message="Search Successfully",data=historys))

def query(task,keys_list,args_dict):
    for i in keys_list:
        if (str)(task[i])!=args_dict[i]:
            return False
    return True
#######################查找#########################



#######################注册#########################
@app.route("/api/v1/user/regist",methods=["POST"])
def regist():
    if not request.json or not "username" in request.json or not "password" in request.json:
        return jsonify(return_Feedback(status=1,message="Regist Form Error",data=""))
    user_id = users[-1]['id']+1
    user_username = request.json['username']
    user_password = request.json['password']

    user = {
        'id' : user_id,
        'username' : user_username,
        'password' : user_password
    }

    users.append(user)
    return jsonify(return_Feedback(status=0,message="Regist Successfully",data=user))
#######################注册#########################



#######################登录#########################
# 登录接口
@app.route("/api/v1/user/login",methods=["POST"])
def login():
    print(request.json)
    if not request.json or not "username" in request.json or not "password" in request.json:# 格式错误
        return jsonify(return_Feedback(status=2,message="Form Error",data=""))
    for i in users:# 遍历用户列表
        if i["username"] == request.json["username"] and i["password"] == request.json["password"]:
            return jsonify(return_Feedback(status=0,message="Login Successfully",data={"user":request.json,"token":get_token(user_id=i["id"],user_name=i["username"],user_pwd=i["password"])})) # 认证成功
    return jsonify(return_Feedback(status=3,message="Username Or Password Error",data=""))# 没有这个用户
    
# 返回token
def get_token(user_id,user_name,user_pwd):
    s = Serializer(secret_key=app.config["SECRET_KEY"],expires_in=3600)
    token = s.dumps({"id":user_id,"username":user_name,"password":user_pwd}).decode("ascii")
    return token

# 验证token
def judge_token(headers):
    try:
        token = headers["token"]
        s = Serializer(app.config["SECRET_KEY"],1800)
        token_result = s.loads(token)
        return token_result
    except:
        return False
#######################登录#########################




@app.errorhandler(404)
def nofound(error):
    return jsonify(errors[0])

def return_Feedback(status,message,data):
    Feedback = {
        "status"  : 0,
        "message" :" ",
        "data"    : " "
    }
    Feedback["status"]=status
    Feedback["message"]=message
    Feedback["data"]=data
    return Feedback

if __name__=="__main__":
    conn=redis.Redis(host='127.0.0.1',port=6379,db=1,decode_responses=True)
    app.run(debug=1)