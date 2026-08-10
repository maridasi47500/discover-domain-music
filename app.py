from flask import Flask, render_template, request, session
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_domaine", methods=["GET","POST"])
def add_one_domaine():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into domaine (name,adresse,bridges,horses,bows) values (:name,:adresse,:bridges,:horses,:bows)",hey)
        user = query_db('select * from domaine')

        return render_template("domaineform.html", domaines=user, one_user=one_user, the_title="add new domaine")


    user = query_db('select * from domaine')
    one_user = query_db("select * from domaine limit 1", one=True)
    return render_template("domaineform.html", domaines=user, one_user=one_user, the_title="add new domaine")

@app.route("/add_one_domaine_reseau", methods=["GET","POST"])
def add_one_domaine_reseau():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesdomaine= query_db("select * from domaine")

        one_user = query_db("insert into domaine_reseau (domaine_id,name) values (:domaine_id,:name)",hey)
        user = query_db('select * from domaine_reseau')

        return render_template("domaine_reseauform.html", domaine_reseaus=user, one_user=one_user, the_title="add new domaine_reseau", touslesdomaine=touslesdomaine)


    touslesdomaine= query_db("select * from domaine")

    user = query_db('select * from domaine_reseau')
    one_user = query_db("select * from domaine_reseau limit 1", one=True)
    return render_template("domaine_reseauform.html", domaine_reseaus=user, one_user=one_user, the_title="add new domaine_reseau", touslesdomaine=touslesdomaine)

@app.route("/add_one_appareil", methods=["GET","POST"])
def add_one_appareil():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesdomaine_reseau= query_db("select * from domaine_reseau")

        one_user = query_db("insert into appareil (domaine_reseau_id,adresse_reseau) values (:domaine_reseau_id,:adresse_reseau)",hey)
        user = query_db('select * from appareil')

        return render_template("appareilform.html", appareils=user, one_user=one_user, the_title="add new appareil", touslesdomaine_reseau=touslesdomaine_reseau)


    touslesdomaine_reseau= query_db("select * from domaine_reseau")

    user = query_db('select * from appareil')
    one_user = query_db("select * from appareil limit 1", one=True)
    return render_template("appareilform.html", appareils=user, one_user=one_user, the_title="add new appareil", touslesdomaine_reseau=touslesdomaine_reseau)

@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (username,dateofbirth,country_id,email,password,phone,pic,fullname) values (:username,:dateofbirth,:country_id,:email,:password,:phone,:pic,:fullname)",hey)
        user = query_db('select * from user')

        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','dateofbirth','country_id','email','password','phone','pic','fullname']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','dateofbirth','country_id','email','password','phone','pic','fullname']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','dateofbirth','country_id','email','password','phone','pic','fullname']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_conversation", methods=["GET","POST"])
def add_one_conversation():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesdomaine_reseau= query_db("select * from domaine_reseau")

        one_user = query_db("insert into conversation (user1_id,user2_id,domaine_reseau_id,message) values (:user1_id,:user2_id,:domaine_reseau_id,:message)",hey)
        user = query_db('select * from conversation')

        return render_template("conversationform.html", conversations=user, one_user=one_user, the_title="add new conversation", touslesdomaine_reseau=touslesdomaine_reseau)


    touslesdomaine_reseau= query_db("select * from domaine_reseau")

    user = query_db('select * from conversation')
    one_user = query_db("select * from conversation limit 1", one=True)
    return render_template("conversationform.html", conversations=user, one_user=one_user, the_title="add new conversation", touslesdomaine_reseau=touslesdomaine_reseau)

@app.route("/add_one_begin_adventure", methods=["GET","POST"])
def add_one_begin_adventure():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename


        one_user = query_db("insert into begin_adventure (title,description,pic) values (:title,:description,:pic)",hey)
        user = query_db('select * from begin_adventure')

        return render_template("begin_adventureform.html", begin_adventures=user, one_user=one_user, the_title="add new begin_adventure")


    user = query_db('select * from begin_adventure')
    one_user = query_db("select * from begin_adventure limit 1", one=True)
    return render_template("begin_adventureform.html", begin_adventures=user, one_user=one_user, the_title="add new begin_adventure")

@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey)
        user = query_db('select * from country')

        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_songtrack", methods=["GET","POST"])
def add_one_songtrack():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into songtrack (artist_composer,title) values (:artist_composer,:title)",hey)
        user = query_db('select * from songtrack')

        return render_template("songtrackform.html", songtracks=user, one_user=one_user, the_title="add new songtrack")


    user = query_db('select * from songtrack')
    one_user = query_db("select * from songtrack limit 1", one=True)
    return render_template("songtrackform.html", songtracks=user, one_user=one_user, the_title="add new songtrack")

@app.route("/add_one_adventurehassongtrack", methods=["GET","POST"])
def add_one_adventurehassongtrack():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslessong_track= query_db("select * from song_track")

        touslesbegin_adventure= query_db("select * from begin_adventure")

        one_user = query_db("insert into adventurehassongtrack (song_track_id,begin_adventure_id) values (:song_track_id,:begin_adventure_id)",hey)
        user = query_db('select * from adventurehassongtrack')

        return render_template("adventurehassongtrackform.html", adventurehassongtracks=user, one_user=one_user, the_title="add new adventurehassongtrack", touslessong_track=touslessong_track, touslesbegin_adventure=touslesbegin_adventure)


    touslessong_track= query_db("select * from song_track")

    touslesbegin_adventure= query_db("select * from begin_adventure")

    user = query_db('select * from adventurehassongtrack')
    one_user = query_db("select * from adventurehassongtrack limit 1", one=True)
    return render_template("adventurehassongtrackform.html", adventurehassongtracks=user, one_user=one_user, the_title="add new adventurehassongtrack", touslessong_track=touslessong_track, touslesbegin_adventure=touslesbegin_adventure)

@app.route("/add_one_adventure_has_user", methods=["GET","POST"])
def add_one_adventure_has_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        touslesbegin_adventure= query_db("select * from begin_adventure")

        one_user = query_db("insert into adventure_has_user (user_id,begin_adventure_id) values (:user_id,:begin_adventure_id)",hey)
        user = query_db('select * from adventure_has_user')

        return render_template("adventure_has_userform.html", adventure_has_users=user, one_user=one_user, the_title="add new adventure_has_user", touslesuser=touslesuser, touslesbegin_adventure=touslesbegin_adventure)


    touslesuser= query_db("select * from user")

    touslesbegin_adventure= query_db("select * from begin_adventure")

    user = query_db('select * from adventure_has_user')
    one_user = query_db("select * from adventure_has_user limit 1", one=True)
    return render_template("adventure_has_userform.html", adventure_has_users=user, one_user=one_user, the_title="add new adventure_has_user", touslesuser=touslesuser, touslesbegin_adventure=touslesbegin_adventure)

