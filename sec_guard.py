from flask import Flask,render_template,request,session,jsonify
from dbconnection import Db
app = Flask(__name__)
app.secret_key="123"



@app.route('/')
def hello_world():
    return render_template("LOGIN.html")

@app.route("/login",methods=["post"])
def login():
    username=request.form["t1"]
    password=request.form["t2"]
    db=Db()
    qry="select * from logindb where username='"+username+"' and password='"+password+"'"
    result=db.selectone(qry)
    if result is None:
        return 'username or password is erorr'
    else:
        if result['utype']=="admin":
            return render_template("admin_home.html")
        elif result['utype']=="subadmin":
            return render_template("subadmin_home.html")
        else:
            return "invalid user"

@app.route('/admin_view_reg_user')
def admin_view_reg_user():
    db=Db()
    qry="select * from userdb where type='user'"
    res=db.selectall(qry)
    return render_template('user1.html',data=res)
@app.route('/admin_block_users/<ulid>')
def block_users(ulid):
    db=Db()
    qry="update logindb set utype='block' where ulid='"+ulid+"'"
    db.update(qry)
    qry1="update userdb set type='block' where ulid='"+ulid+"'"
    db.update(qry1)
    return admin_view_reg_user()
@app.route('/send_notification')
def send_notification():
    return render_template("notification_add.html")

@app.route('/send_notification_post',methods=['post'])
def send_notification_post():
    db=Db()
    n1=request.form["textfield"]
    qry="insert into notificationdb(notification,date)values('"+n1+"',curdate())"
    db.insert(qry)
    return send_notification()
@app.route('/view_notification')
def view_notification():
    db=Db()
    qry = "select * from notificationdb order by nid desc"
    res=db.selectall(qry)
    return  render_template('view_notification.html',data=res)

@app.route('/delete_notification/<nid>')
def delete_notification(nid):
    db=Db()
    qry="delete from notificationdb where nid='"+nid+"'"
    db.delete(qry)
    return view_notification()
@app.route('/edit_notification/<nid>')
def edit_notification(nid):
    db=Db()
    session['nid']=nid
    qry="select * from notificationdb where nid='"+nid+"'"
    res=db.selectone(qry)
    return render_template('edit_notification.html',data=res)
@app.route('/update_notification_post',methods=['post'])
def update_notification_post():
    db=Db()
    n1=request.form["textfield"]
    nid=session['nid']
    qry="update notificationdb set notification='"+n1+"' where nid='"+nid+"'"
    db.update(qry)
    return view_notification()

@app.route('/station_registration')
def station_registration():
    return render_template('police_add.html')
@app.route('/station_registration_post',methods=['post'])
def station_registration_post():
    db=Db()
    station_name=request.form["textfield"]
    place=request.form['textfield2']
    city=request.form['textfield3']
    pin=request.form['textfield4']
    street=request.form['textfield5']
    state=request.form['textfield6' ]
    phone=request.form['textfield7']
    email=request.form['textfield9']
    latitude=request.form['textfield10']
    langitude=request.form['textfield8']
    qry="insert into logindb values(null,'"+email+"','"+phone+"','police')"
    lid=db.insert(qry)
    qry1="insert into policestationdb(stid,stlid,stationname,place,state,phone,email,pin,city,street,latitude,longitude)values(null,'"+str(lid)+"','"+station_name+"','"+place+"','"+state+"','"+phone+"','"+email+"','"+pin+"','"+city+"','"+street+"','"+latitude+"','"+longitude+"')"
    db.insert(qry1)
    return render_template('police_add.html')
@app.route('/police_view')
def police_view():
    db=Db()
    qry = "select * from policestationdb order by stid desc"
    res=db.selectall(qry)
    return  render_template('police_view.html',data=res)
@app.route('/delete_police/<stid>')
def delete_police(stid):
    db=Db()
    qry="delete from policestationdb where stid='"+stid+"'"
    db.delete(qry)
    return police_view()
@app.route('/edit_police/<stid>')
def edit_police(stid):
    db=Db()
    session['stid']=stid
    qry="select * from policestationdb where stid='"+stid+"'"
    res=db.selectone(qry)
    return render_template('police_edit.html',data=res)
@app.route('/update_police_post',methods=['post'])
def update_police_post():
    db=Db()
    name=request.form["textfield"]
    place=request.form["textfield2"]
    city=request.form["textfield3"]
    pin=request.form["textfield4"]
    street=request.form["textfield5"]
    state=request.form["textfield6"]
    phone=request.form["textfield7"]
    # email=request.form["textfield9"]
    latitude=request.form["textfield10"]
    langitude=request.form["textfield8"]
    stid=session['stid']
    qry="update policestationdb set stationname='"+name+"',place='"+place+"',city='"+city+"',pin='"+pin+"',street='"+street+"',state='"+state+"',phone='"+phone+"',latitude='"+latitude+"',langitude='"+langitude+"' where stid='"+stid+"'"
    db.update(qry)
    return police_view()

@app.route('/add_vehicle')
def add_vehicle():
    return render_template("add_vehicle.html")
@app.route('/add_vehicle_post',methods=['post'])
def add_vehicle_post():
    db=Db()
    name=request.form["textfield2"]
    number=request.form["textfield3"]
    rcowner=request.form["textfield4"]
    qry="insert into vehicledb(vname,vnumber,rcowner)values('"+name+"','"+number+"','"+rcowner+"')"
    db.insert(qry)
    return add_vehicle()
@app.route('/view_vehicle')
def vehicle_view():
    db=Db()
    qry = "select * from vehicledb order by vid desc"
    res=db.selectall(qry)
    return  render_template('view_vehicle.html',data=res)
@app.route('/delete_vehicle/<vid>')
def delete_vehicle(vid):
    db=Db()
    qry="delete from vehicledb where vid='"+vid+"'"
    db.delete(qry)
    return vehicle_view()
@app.route('/edit_vehiclee/<vid>')
def edit_vehicle(vid):
    db=Db()
    session['vid']=vid
    qry="select * from vehicledb where vid='"+vid+"'"
    res=db.selectone(qry)
    return render_template('vehicle_edit.html',data=res)
@app.route('/update_vehicle_post',methods=['post'])
def update_vehicle_post():
    db=Db()
    name=request.form["textfield2"]
    number=request.form["textfield3"]
    rc=request.form["textfield4"]
    vid=session['vid']
    qry="update vehicledb set vname='"+name+"',vnumber='"+number+"',rcowner='"+rc+"' where vid='"+vid+"'"
    db.update(qry)
    return vehicle_view()

@app.route('/assign_vs')
def assign_vs():
    db=Db()
    qry = "select * from vehicledb order by vid desc"
    qry1 = "select * from policestationdb order by stid desc"
    res=db.selectall(qry)
    res1=db.selectall(qry1)
    return  render_template('assign_vehicle.html',data=res,data2=res1)
@app.route('/assign_post',methods=['post'])
def assign_vehicle_post():
    db=Db()
    vehicle=request.form["select"]
    station=request.form["select2"]
    qr="select * from assign where vid='"+vehicle+"'"
    rr=db.selectone(qr)
    if rr is None:
        qry="insert into assign(vid,stationid)values('"+vehicle+"','"+station+"')"
    else:
        qry="update assign set stationid='"+station+"' where vid='"+vehicle+"'"
    db.insert(qry)
    return assign_vs()

@app.route('/assign_view')
def assign_view():
    db=Db()
    qry = "select assign.aid,policestationdb.stationname,policestationdb.place,vehicledb.vname,vehicledb.vnumber from assign,policestationdb,vehicledb where assign.vid=vehicledb.vid and assign.stationid=policestationdb.stlid"
    res=db.selectall(qry)
    return  render_template('assign_vehicle_view.html',data=res)

@app.route('/delete_assign/<aid>')
def delete_assign(aid):
    db=Db()
    qry="delete from assign where aid='"+aid+"'"
    db.delete(qry)
    return assign_view()

@app.route('/view_feedback')
def view_feedback():
    db=Db()
    qry = "select * from feedback order by fid desc"
    res=db.selectall(qry)
    return  render_template('feedback_view1.html',data=res)

@app.route('/delete_feedback/<fid>')
def delete_feedback(fid):
    db=Db()
    qry="delete from feedback where fid='"+fid+"'"
    db.delete(qry)
    return view_feedback()

@app.route('/add_subadmin')
def add_subadmin():
    return render_template('add_subadmin1.html')
@app.route('/add_subadmin_post',methods=['post'])
def add_subadmin_post():
    db=Db()
    name=request.form["textfield"]
    print("name=",name)

    place=request.form["textfield2"]
    print("place=",place)

    post=request.form["textfield3"]
    print("post=",post)

    pin=request.form["textfield4"]
    print("pin=",pin)

    email=request.form["textfield5"]
    print("email=",email)

    contact=request.form["textfield6"]
    print("contact=",contact)

    photo=request.files["textfield7"]
    print("photo=",photo)

    photo.save("C:\\Users\\vtmoi\\PycharmProjects\\sec_guard\\static\\subadmin_images\\"+photo.filename)
    path="/static/subadmin_images/"+photo.filename
    qry = "insert into logindb values(null,'" + email + "','" + contact + "','subadmin')"
    lid = db.insert(qry)
    qry="insert into subadmindb(name,place,post,pin,email,contact,photo,lid)values('"+name+"','"+place+"','"+post+"','"+pin+"','"+email+"','"+contact+"','"+path+"','"+str(lid)+"')"
    db.insert(qry)
    return add_subadmin()
@app.route('/view_subadmin')
def view_subadmin():
    db=Db()
    qry = "select * from subadmindb order by sbid desc"
    res=db.selectall(qry)
    return  render_template('view_subadmin.html',data=res)
@app.route('/delete_subadmin/<sbid>')
def delete_subadmin(sbid):
    db=Db()
    qry="delete from subadmindb where sbid='"+sbid+"'"
    db.delete(qry)
    return view_subadmin()
@app.route('/edit_subadmin/<sbid>')
def edit_subadmin(sbid):
    db=Db()
    session['sbid']=sbid
    qry="select * from subadmindb where sbid='"+sbid+"'"
    res=db.selectone(qry)
    return render_template('edit_subadmin.html',i=res)
@app.route('/update_subadmin_post',methods=['post'])
def update_subadmin_post():
    db=Db()
    name=request.form["textfield"]
    place=request.form["textfield2"]
    post=request.form["textfield3"]
    pin=request.form["textfield4"]
    email=request.form["textfield5"]
    contact=request.form["textfield6"]
    sbid=session['sbid']

    if 'textfield7' in request.files:

        photo = request.form["textfield7"]

        if photo.filename=='':

            qry = "update subadmindb set name='" + name + "', place='" + place + "', post='" + post + "', pin='" + pin + "',email='" + email + "',contact='" + contact + "' where sbid='" + sbid + "'"
            db.update(qry)
            return view_subadmin()
        else:

            photo.save("C:\\Users\\vtmoi\\PycharmProjects\\sec_guard\\static\\subadmin_images\\" + photo.filename)
            path = "/static/subadmin_images/" + photo.filename
            qry = "update subadmindb set name='" + name + "', place='" + place + "', post='" + post + "', pin='" + pin + "',email='" + email + "',contact='" + contact + "'photo='" + path + "' where sbid='" + sbid + "'"
            db.update(qry)
            return view_subadmin()
    else:
        qry = "update subadmindb set name='" + name + "', place='" + place + "', post='" + post + "', pin='" + pin + "',email='" + email + "',contact='" + contact + "' where sbid='" + sbid + "'"
        db.update(qry)
        return view_subadmin()

@app.route('/sbadmin_view_feedback')
def sbadmin_view_feedback():
    db=Db()
    qry = "select * from viewfeedbackdb order by fid desc"
    res=db.selectall(qry)
    return  render_template('sbview_feedback.html',data=res)
@app.route('/delete_sb_feedback/<fid>')
def delete_sb_feedback(fid):
    db=Db()
    qry="delete from viewfeedbackdb where fid='"+fid+"'"
    db.delete(qry)
    return sbadmin_view_feedback()
@app.route('/addsb_safe_point')
def add_safe_point():
    return render_template("add_safe_point.html")

@app.route('/add_safe_pointpost',methods=['post'])
def add_safe_pointpost():
    db=Db()
    place=request.form["textfield"]
    langitude=request.form["textfield3"]
    latitude=request.form["textfield4"]
    description=request.form["textfield2"]
    image=request.files["fileField"]
    image.save("C:\\Users\\vtmoi\\PycharmProjects\\sec_guard\\static\\subadmin_images\\" + image.filename)
    path = "/static/subadmin_images/" + image.filename
    qry="insert into safepoint(place,description,image,longitude,latitude)values('"+place+"','"+description+"','"+path+"','"+langitude+"','"+latitude+"')"
    db.insert(qry)
    return add_safe_point()
@app.route('/view_safepoint')
def view_safepoint():
    db=Db()
    qry = "select * from safepoint order by safeid desc"
    res=db.selectall(qry)
    return  render_template('view_safepoint.html',data=res)

@app.route('/delete_safepoint/<safeid>')
def delete_safepoint(safeid):
    db=Db()
    qry="delete from safepoint where safeid='"+safeid+"'"
    db.delete(qry)
    return view_safepoint()
@app.route('/edit_safepoint/<safeid>')
def edit_safepoint(safeid):
    db=Db()
    session['safeid']=safeid
    qry="select * from safepoint where safeid='"+safeid+"'"
    res=db.selectone(qry)
    return render_template('edit_safepoint.html',i=res)

@app.route('/update_safepoint_post',methods=['post'])
def update_safepoint_post():
    db=Db()
    place=request.form["textfield"]
    longitude=request.form["textfield3"]
    latitude=request.form["textfield4"]
    description=request.form["textfield2"]
    safeid=session['safeid']
    if 'textfield7' in request.files:

        image = request.form["filefield"]

        if image.filename=='':

            qry = "update safepoint set place='" + place + "', langitude='" + langitude + "', latitude='" + latitude + "', description='" + description + "' where safeid='" + safeid + "'"
            db.update(qry)
            return view_safepoint()
        else:

            image.save("C:\\Users\\vtmoi\\PycharmProjects\\sec_guard\\static\\subadmin_images\\" + image.filename)
            path = "/static/subadmin_images/" + image.filename
            qry = "update safepoint set place='" + place + "', langitude='" + langitude + "', latitude='" + latitude + "', description='" + description + "' where safeid='" + safeid + "'"
            db.update(qry)
            return view_safepoint()

    qry = "update safepoint set place='" + place + "', longitude='" + longitude + "', latitude='" + latitude + "', description='" + description + "' where safeid='" + safeid + "'"
    db.update(qry)
    return view_safepoint()

@app.route('/view_dangerous_spots')
def view_dangerous_spots():

    return  render_template('view_dangerous_spots.html')

@app.route('/dangerous_spots',methods=['post'])
def dangerous_spot_post():
    db = Db()
    type=request.form['select']
    qry = "select * from dngspotdb where type='" + type + "' "

    res=db.selectall(qry)
    return render_template("view_dangerous_spots.html",data=res)

@app.route('/view_police_vehicle')
def view_police_vehicle():
    db=Db()
    qry = "select * from vehicle_location,vehicledb where vehicledb.vid=vehicle_location.vid order by locationid desc"
    res=db.selectall(qry)
    return  render_template('track_vehicle.html',data=res)

@app.route('/view_visual')
def view_visual():
    db=Db()
    qry = "select * from visualdb order by visualid desc"
    res=db.selectall(qry)
    return  render_template('view_visual.html',data=res)
@app.route("/and_login",methods=["post"])
def and_login():
    username=request.form["username"]
    password=request.form["password"]
    db=Db()
    qry="select * from logindb where username='"+username+"' and password='"+password+"'"
    result=db.selectone(qry)
    if result is None:
        return jsonify(status="no")
    else:
        if result['utype']=="police":
            return jsonify(status="ok",lid=result["lid"],type=result["utype"])
        elif result['utype']=="user":
            return jsonify(status="ok",lid=result["lid"],type=result["utype"])
        elif result['utype']=="public":
            return jsonify(status="ok")
        else:
            return jsonify(status="no")

@app.route('/and_view_emergency_request',methods=['post'])
def view_emergency_request():
    db=Db()
    qry="select requestdb.*,userdb.name,userdb.uid from requestdb,userdb where userdb.uid=requestdb.uid order by eid desc"
    res=db.selectall(qry)
    print(res)
    return jsonify(status="1",data=res)
@app.route('/and_view_compliant',methods=['post'])
def and_view_compliat():
    db=Db()
    qry="select complaintdb.*,userdb.name,userdb.ulid from complaintdb,userdb where userdb.ulid=complaintdb.ulid order by cid desc"
    res=db.selectall(qry)
    return jsonify(status="1",data=res)
@app.route('/and_replay_compliant',methods=['post'])
def and_replay_compliat():
    db=Db()
    reply=request.form['reply']
    cid=request.form['cid']
    qry="update complaintdb set reply='"+reply+"',status='replied' where cid='"+cid+"'"
    res=db.update(qry)
    return jsonify(status="ok",data=res)

@app.route('/and_add_dangerous_spot',methods=['post'])
def and_add_dangerous_spot():
    db=Db()
    place=request.form["place"]
    street=request.form["street"]
    pin=request.form["pin"]
    city=request.form["city"]
    state = request.form["state"]
    ulid = request.form["lid"]
    qry="insert into spotdb(place,street,pin,city,state,ulid)values('"+place+"','"+street+"','"+pin+"','"+city+"','"+state+"','"+ulid+"')"
    db.insert(qry)
    return jsonify(status="ok")
@app.route('/and_verify_dngs_spot',methods=['post'])
def and_verify_dngs_spot():
    db=Db()
    qry = "select * from spotdb order by sid"
    res=db.selectall(qry)
    return  jsonify(status="ok",data=res)
@app.route('/and_set_emergency_no',methods=['post'])
def and_set_emergency_no():
    db=Db()
    no=request.form["number"]
    lid=request.form["lid"]
    qry="insert into emergencydb(number,lid)values('"+no+"','"+lid+"')"
    db.insert(qry)
    return jsonify(status="1")
@app.route('/and_request_emergency',methods=['post'])
def and_request_emergency():
    db=Db()
    no=request.form["request"]
    uid=request.form["lid"]
    qry="insert into requestdb(request,replay,uid,date)values('"+no+"','pending','"+uid+"',curdate())"
    db.insert(qry)
    return jsonify(status="1")
@app.route('/and_view_safe_point',methods=['post'])
def and_view_safe_point():
    db=Db()
    qry="select * from safepoint order by safeid desc"
    res=db.selectall(qry)
    return jsonify(status="1",data=res)
@app.route('/and_view_dang_spot',methods=['post'])
def and_view_dang_spot():
    db=Db()
    qry="select * from spotdb "
    res=db.selectall(qry)
    return jsonify(status="1",data=res)
@app.route('/and_search_place',methods=['post'])
def and_view_search_place():
    db=Db()
    a=request.form['place']
    qry="select * from spotdb where place like '"+a+"%' "
    res=db.selectall(qry)
    return jsonify(status="ok",data=res)
@app.route('/and_add_dangerous_spot_user',methods=['post'])
def and_add_dangerous_spot_user():
    db=Db()
    place=request.form["place"]
    street=request.form["street"]
    pin=request.form["pin"]
    city=request.form["city"]
    state = request.form["state"]
    qry="insert into spotdb(place,street,pin,city,state)values('"+place+"','"+street+"','"+pin+"','"+city+"','"+state+"')"
    db.insert(qry)
    return jsonify(status="ok")
@app.route('/emergency_call_to_usr',methods=['post'])
def emergency_call_usr():
    db=Db()
    qry="select * from emergencydb order by id desc"
    res=db.selectall(qry)
    return jsonify(status="1",data=res)
@app.route('/emergency_call_to_pl',methods=['post'])
def emergency_call_to_pl():
    db=Db()
    qry="select stationname,place,phone,state,stlid from policestationdb "
    res=db.selectall(qry)
    return jsonify(status="1",data=res)
@app.route('/and_post_complaint',methods=['post'])
def and_post_complaint():
    db=Db()
    no=request.form["complaint"]
    ulid=request.form["lid"]
    qry="insert into complaintdb(complaint,ulid,reply,status,date)values('"+no+"','"+ulid+"','pending','pending',curdate())"
    db.insert(qry)
    return jsonify(status="ok")
@app.route('/and_view_notification',methods=['post'])
def and_view_notification():
    db=Db()
    qry="select * from notificationdb order by nid desc"
    res=db.selectall(qry)
    return jsonify(status="1",data=res)
@app.route('/and_user_view_pl',methods=['post'])
def and_user_view_pl():
    db=Db()
    qry="select * from policestationdb order by stid desc"
    res=db.selectall(qry)
    return jsonify(status="1",data=res)

#

# @app.route('/and_dangerous_spots',methods=['post'])
# def and_dangerous_spot_post():
#     db = Db()
#     type=request.form['select']
#
#     qry = "select * from dngspotdb where type='" + type + "' "
#
#     res=db.selectall(qry)
#     return jsonify(status="ok",data=res)

#
# @app.route("/viw_chat_msg", methods=['post'])
# def viw_chat_msg():
#     print("uuuuuuuuuuuuuu")
#     toid = request.form["toid"]
#     fid = request.form["fid"]
#     lmid = request.form["lastmsgid"]
#
#     ty = request.form["ty"]
#     print("ty.........")
#
#     qry = "select from_id,msg,date,msg_id from chat where msg_id>'" + str(lmid) + "' AND ((to_id='" + str(toid) + "' and  from_id='" + str(fid) + "' ) or (to_id='" + str(fid) + "' and from_id='" + str(toid) + "' )  )  order by msg_id asc"
#     print(qry)
#     db=Db()
#     res=db.selectall(qry)
#     print(res)
#     return jsonify(status="ok", users=res)
#
# @app.route('/chat_msg_send', methods=['POST'])
# def chat_msg_send():
#     print("uuu")
#     fid = request.form['fid']
#
#     msg = request.form['msg']
#     tid = request.form['toid']
#     ty = request.form['ty']
#     print("jkkjkjk")
#
#     qry = "insert into chat(from_id,msg,date,time,to_id,type)values('" + str(fid) + "','" + msg + "',curdate(),curtime(),'" + str(tid) + "','" + ty + "')"
#     print(qry)
#     db=Db()
#     db.insert(qry)
#     return jsonify(status='ok')
# @app.route('/station_registration_post',methods=['post'])
# def station_registration_post():
#     db=Db()
#     station_name=request.form["textfield"]
#     place=request.form['textfield2']
#     city=request.form['textfield3']
#     pin=request.form['textfield4']
#     street=request.form['textfield5']
#     state=request.form['textfield6' ]
#     phone=request.form['textfield7']
#     email=request.form['textfield9']
#     latitude=request.form['textfield10']
#     langitude=request.form['textfield8']
#     qry="insert into logindb values(null,'"+email+"','"+phone+"','police')"
#     lid=db.insert(qry)
#     qry1="insert into policestationdb(stid,stlid,stationname,place,state,phone,email,pin,city,street,latitude,longitude)values(null,'"+str(lid)+"','"+station_name+"','"+place+"','"+state+"','"+phone+"','"+email+"','"+pin+"','"+city+"','"+street+"','"+latitude+"','"+longitude+"')"
#     db.insert(qry1)
#     return render_template('police_add.html')


@app.route('/in_message2', methods=['POST'])
def message():
    db=Db()
    fr_id = request.form["fid"]
    to_id = request.form["toid"]
    message = request.form["msg"]
    query7 = "insert into chat(from_id,msg,date,time,to_id,type) values ('" + fr_id + "','" + message + "',curdate(),curtime(),'" + to_id + "' ,null)"

    print(query7);
    res=db.insert(query7)
    return jsonify(status='send')


@app.route('/view_message2', methods=['POST'])
def msg():
    db=Db()
    fid = request.form["fid"]
    toid = request.form["toid"]
    lmid = request.form['lastmsgid'];
    query="select from_id,msg,date,msg_id from chat where msg_id>'" + str(lmid) + "' AND ((to_id='" + str(toid) + "' and  from_id='" + str(fid) + "' ) or (to_id='" + str(fid) + "' and from_id='" + str(toid) + "' )  )  order by msg_id asc"
    res=db.selectall(query)
    print(query)
    return jsonify(status='ok', res1=res)


@app.route('/public_user_registration',methods=['post'])
def and_user_registration():
    db=Db()
    name=request.form['name']
    gender=request.form['gender']
    dob=request.form['dob']
    email=request.form['email' ]
    phone=request.form['phone']
    pin=request.form['pin']
    place=request.form['place']
    city=request.form['city']
    state=request.form['state']
    image = request.form["image"]
    passwrd=request.form["password"]
    import time
    import base64
    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)
    a = base64.b64decode(image)
    fh = open("static/user_images/" + timestr + ".jpg", "wb")
    path = "/static/user_images/" + timestr + ".jpg"
    fh.write(a)
    fh.close()
    qry = "insert into logindb values(null,'" + email + "','" + passwrd + "','user')"
    lid = db.insert(qry)
    qry1="insert into userdb(uid,ulid,name,gender,dob,email,phone,pin,place,city,state,latitude,image)values(null,'"+str(lid)+"','"+name+"','"+gender+"','"+dob+"','"+email+"','"+phone+"','"+pin+"','"+place+"','"+city+"','"+state+"','"+path+"')"
    db.insert(qry1)
    return jsonify(status="ok")
@app.route('/view_dangs_spot_public')
def view_dangs_spot_public():
    db=Db()
    qry = "select * from safepoint order by safeid desc"
    res=db.selectall(qry)
    return  render_template('view_safepoint.html',data=res)

@app.route('/view_pl_info')
def view_pl_info():
    db=Db()
    qry = "select * from policestationdb order by stid desc"
    res=db.selectall(qry)
    return  render_template('view_safepoint.html',data=res)

    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
