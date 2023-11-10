from flask import redirect, render_template, request, session
import readdb
import writedb
from app import app

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/newaccount")
def newaccount():
    return render_template("newaccount.html")

@app.route("/create", methods=["POST"])
def create():
    name = request.form["accname"]
    password = request.form["passwrd"]
    if password == None or name == None:
        return "<script>alert('Kelvoton salasana')</script><script>document.location='/newaccount'</script>"
    #Tähän sitten salasanan laatutarkastus
    #elif (len(password) < 8) or (name in password):
        #return "<script>alert('Kelvoton salasana')</script><script>document.location='/newaccount'</script>"
    writedb.add_user(name, password)
    session["username"] = name
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    name = request.form["accname"]
    password = request.form["passwrd"]    
    if readdb.confirm_user_pass(name, password):
        session["username"] = name
        return redirect("/")
    return "<script>alert('Väärä nimi tai salasana')</script><script>document.location='/account'</script>"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/personal")
def personal():
    return render_template("personal.html")

@app.route("/started")
def started():
    discussions = readdb.get_discussion_by_writer(session["username"])
    return render_template("personaldiscussions.html")

@app.route("/friendlist")
def friends():
    friendlist = readdb.get_friends_by_user(session["username"])
    return render_template("friendlist.html", friends=friendlist)

@app.route("/friendlist/send")
def friendsend():
    return render_template("friendsend.html")

@app.route("/friendlist/send/confirm", methods=["POST"])
def sendfriend():
    writedb.send_friendrequest(session["username"], request.form["friend"])
    return redirect("/friendlist")

@app.route("/friendlist/received")
def sentrequests():
    requested = readdb.get_friend_requests(session["username"])
    return render_template("requests.html", requested=requested)

@app.route("/changepass")
def changepass():
    return render_template("changepass.html")

@app.route("/changepass/confirm", methods=["POST"])
def changeconfirm():
    if readdb.confirm_user_pass(session["username"], request.form["oldpasswrd"]):
        writedb.change_user_pass(session["username"], request.form["newpasswrd"])
    return redirect("/personal")

@app.route("/rmvuser")
def removeuser():
    return render_template("rmvuser.html")

@app.route("/")
def index():
    areas = readdb.get_areas()
    return render_template("index.html", areas=areas)

@app.route("/area/<int:id>")
def area(id):
    area = readdb.get_area_by_id(id)
    discussions = readdb.get_discussions_by_area(area.names)
    discussions.reverse()
    return render_template("area.html", area=area, area_discussions=discussions)

@app.route("/area/<int:id>/newdiscussion")
def newdiscussion(id):
    return render_template("newdiscussion.html",area=id)

@app.route("/area/<int:id>/creatediscussion", methods=["POST"])
def creatediscussion(id):
    title = request.form["title"]
    message = request.form["body"]
    if title == None or message == None:
        return "<script>alert('Kenttä tyhjä')</script><script>document.location='/area/newdiscussion'</script>"
    area_name = readdb.get_area_by_id(id).names
    writedb.add_discussion(title, area_name)
    writedb.add_message(session["username"], message, title)
    return redirect("/area/"+str(id))

@app.route("/area/<int:id1>/discussion/<int:id2>")
def discussion(id1, id2):
    discussion = readdb.get_discussion_by_id(id2)
    messages = readdb.get_messages_from_discussion(discussion.names)
    return render_template("discussion.html", current_discussion=discussion, ids=[id1,id2], messages=messages)

@app.route("/area/<int:id1>/discussion/<int:id2>/newmessage", methods=["POST"])
def newmessage(id1, id2):
    message = request.form["bodyfield"]
    if message == None:
        return "<script>alert('Kenttä tyhjä')</script><script>document.location='/area'+id1+'/discussion/'+id2</script>"
    discussion_name = readdb.get_discussion_by_id(id2)
    writedb.add_message(session["username"], message, discussion_name)
    return redirect("/area/"+str(id1)+"/discussion/"+str(id2))