# import module
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date, datetime

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import users_dao, richieste_dao, aule_dao, slot_dao
 

from models import Aula, User, Richiesta, Slot

from datetime import datetime
from assegnazione_avanzata import assegna_aule_avanzato  

import assegnazione_dao  



app = Flask(__name__)

app.config['SECRET_KEY'] = 'Secret key della app'

login_manager = LoginManager()
login_manager.init_app(app)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():

  utente_form = request.form.to_dict()

  db_user = users_dao.get_user_by_email(utente_form['email'])
  print(db_user)

  if not db_user or not check_password_hash(db_user['password'], utente_form['password']):
    flash('Credenziali non valide, riprova', 'danger')
    return redirect(url_for('home'))
  else:
    new = User(id=db_user['id'],  nome=db_user['nome'], cognome=db_user['cognome'],	email=db_user['email'], password=db_user['password'])
    login_user(new, True)
    flash('Bentornato ' + db_user['nome'] + '!', 'success')

    return redirect(url_for('home'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    
    nuovo_utente_form = request.form.to_dict()

    user_in_db = users_dao.get_user_by_email(nuovo_utente_form.get('email'))

    if user_in_db:
        flash('C\'è già un utente registrato con questa email', 'danger')
        return redirect(url_for('signup'))
    else:

        #password criptata, la salvo aggiornata
        nuovo_utente_form['password'] = generate_password_hash(nuovo_utente_form.get('password'))
        
        nuovo_utente_form['nome'] = nuovo_utente_form.get('nome')
        nuovo_utente_form['cognome'] = nuovo_utente_form.get('cognome')



        success = users_dao.add_user(nuovo_utente_form)
        

        if success:
            flash('Utente creato correttamente', 'success')
            return redirect(url_for('home'))
        else:
            flash('Errore nella creazione del utente: riprova!', 'danger')

    return redirect(url_for('signup'))

@app.route('/richiesta')
@login_required
def richiesta():
    return render_template('richiesta.html')

@app.route('/richiesta', methods=['POST'])
@login_required
def richiesta_post():
    # Recupera i dati dal form
    capienza = request.form.get('capienza')
    raw_slots = request.form.getlist('slot')  # ['Lunedì_08:30-10:00', ...]
    print(raw_slots)

    # Validazione input
    if not capienza or not raw_slots:
        flash("Compilare tutti i campi richiesti!", "error")
        return redirect(url_for('richiesta'))

    try:
        capienza = int(capienza)
    except ValueError:
        flash("La capienza deve essere un numero valido.", "error")
        return redirect(url_for('richiesta'))

    # Conversione da label slot a ID slot
    slot_ids = []
    for raw in raw_slots:
        try:
            giorno, fascia = raw.split("_")
            ora_inizio, ora_fine = fascia.split("-")
            id_slot = slot_dao.get_slot_id_by_label(giorno, ora_inizio, ora_fine)
            print(giorno, fascia, ora_inizio, ora_fine, id_slot)
            if id_slot:
                slot_ids.append(str(id_slot))
        except Exception as e:
            print(f"Errore con lo slot {raw}: {e}")

    if not slot_ids:
        flash("Nessuno slot valido selezionato.", "error")
        return redirect(url_for('richiesta'))

    # Salva nel database
    richieste_dao.create_richiesta(
        idProf=current_user.id,
        capienza=capienza,
        slots=slot_ids
    )

    flash("Richiesta inserita correttamente!", "success")
    return redirect(url_for('home'))

@app.route('/myaccount')
@login_required
def myaccount():
    # Prende direttamente solo le richieste dell'utente loggato
    mie_richieste = richieste_dao.get_richieste_by_idProf(current_user.id)

     # Trasformiamo gli slot in descrizione leggibile
    richieste_con_descrizione = []
    for richiesta in mie_richieste:
        # slots è una stringa tipo "2,3,4" --> va splittata
        slot_ids = [int(s) for s in richiesta['slots'].split(',')]
        descrizione_slots = slot_dao.get_descrizione_slot_by_ids(slot_ids)
        richiesta_obj = {
            'id': richiesta['id'],
            'capienza': richiesta['capienza'],
            'slots': descrizione_slots  # qui passo la versione leggibile
        }
        richieste_con_descrizione.append(richiesta_obj)

    return render_template('myaccount.html', richieste=richieste_con_descrizione)



@app.route('/assegna_aule')
@login_required
def assegna_aule():
    # Recupera dati
    richieste_rows = richieste_dao.get_richieste()
    aule_rows = aule_dao.get_aule()
    slots_rows = slot_dao.get_all_slots()

    richieste = []
    for r in richieste_rows:
        slot_ids = [int(s) for s in r['slots'].split(',')] if r['slots'] else []
        richieste.append(Richiesta(id=r['id'], id_prof=r['idProf'], capienza_richiesta=r['capienza'], slotIds=slot_ids))

    aule = []
    for a in aule_rows:
        aule.append(Aula(id_aula=a['id'], capienza=a['capienza']))

    slots = []
    for s in slots_rows:
        slots.append(Slot(id=s['id'], giorno=s['giorno'], ora_inizio=s['ora_inizio'], ora_fine=s['ora_fine']))

    # Esegui l'assegnazione avanzata
    assegnazioni, motivazioni = assegna_aule_avanzato(richieste, aule, slots)

    # Pulisce vecchie assegnazioni
    assegnazione_dao.elimina_tutte_assegnazioni()

    # Salva nuove assegnazioni
    for id_richiesta, id_aula in assegnazioni.items():
        if id_aula:  # Solo quelle andate a buon fine
            assegnazione_dao.salva_assegnazione(id_richiesta, id_aula)

    # Prepara risultati da mostrare
    risultati = []
    for richiesta in richieste:
        risultati.append({
            'id_richiesta': richiesta.id,
            'aula_assegnata': assegnazioni.get(richiesta.id),
            'motivazione': motivazioni.get(richiesta.id)
        })

    return render_template('assegna_aule.html', risultati=risultati)

@app.route('/visualizza_assegnazioni')
@login_required
def visualizza_assegnazioni():
    # Recupera tutte le assegnazioni salvate
    assegnazioni_rows = assegnazione_dao.get_assegnazioni()
    
    risultati = []
    for row in assegnazioni_rows:
        richiesta = richieste_dao.get_richiesta_by_id(row['id_richiesta'])
        aula = aule_dao.get_aula_by_id(row['id_aula'])
        
        slot_ids = [int(s) for s in richiesta['slots'].split(',')] if richiesta and richiesta['slots'] else []
        descrizione_slots = slot_dao.get_descrizione_slot_by_ids(slot_ids) if slot_ids else "N/A"

        risultati.append({
            'professore': richiesta['idProf'] if richiesta else "?",  # oppure potremmo anche prendere nome/cognome con join
            'capienza_richiesta': richiesta['capienza'] if richiesta else "N/A",
            'aula': aula['id'] if aula else "N/A",
            'capienza_aula': aula['capienza'] if aula else "N/A",
            'slot_descrizione': descrizione_slots
        })

    return render_template('visualizza_assegnazioni.html', risultati=risultati)



if __name__ == '__main__':
    app.run(debug=True)






@login_manager.user_loader
def load_user(user_id):

    db_user = users_dao.get_user_by_id(user_id)
    if db_user is not None:
        user = User(id=db_user['id'],  nome=db_user['nome'], cognome=db_user['cognome'], email=db_user['email'],	password=db_user['password'] )
    else:
        user = None

    return user

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))