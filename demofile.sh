
mkdir templates 
python3 scaffold.py domaine name adresse bridges:radio horses:radio bows:radio
python3 scaffold.py domaine_reseau domaine_id:references name
python3 scaffold.py appareil domaine_reseau_id:references  adresse_reseau
python3 scaffold.py user username dateofbirth country_id:references email password phone pic:file fullname
python3 scaffold.py conversation user1_id user2_id domaine_reseau_id:references message
python3 scaffold.py begin_adventure title description  pic:file
python3 scaffold.py country name
python3 scaffold.py songtrack artist_composer title
python3 scaffold.py adventurehassongtrack song_track_id:references begin_adventure_id:references
python3 scaffold.py adventure_has_user user_id:references begin_adventure_id:references
