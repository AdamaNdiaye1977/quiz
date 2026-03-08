from flask import Flask, render_template, request, redirect, session, flash, url_for

import random

from functools import wraps

app = Flask(__name__)
app.secret_key = "geheime_schlüssel"  # In produzione usare un segreto complesso!
app.config["TEMPLATES_AUTO_RELOAD"] = True


# ----- ROUTES ---

# Dati del quiz – puoi estendere ogni categoria
quiz_data = {
    "bake-off": [
        {
            "img": "BROT WELTMEISTER CHIA",
            "code": "4034",
            "name": "BROT WELTMEISTER CHIA",
        },
        {"img": "BROT WURZEL DUNKEL", "code": "4018", "name": "BROT WURZEL DUNKEL"},
        {"img": "BURGERSTYLE CLASSIC", "code": "4481", "name": "BURGERSTYLE CLASSIC"},
        {"img": "CIABATTA", "code": "4400", "name": "CIABATTA"},
        {"img": "CREAM MOOD", "code": "4660", "name": "CREAM MOOD"},
        {
            "img": "CROISSANT NUSS-NOUGAT",
            "code": "4673",
            "name": "CROISSANT NUSS-NOUGAT",
        },
        {"img": "CROISSANT BUTTER", "code": "4672", "name": "CROISSANT BUTTER"},
        {
            "img": "CROISSANT PISTAZIENCREME",
            "code": "4466",
            "name": "CROISSANT PISTAZIENCREME",
        },
        {
            "img": "DONUT MIT KRISTALLZUCKER",
            "code": "4473",
            "name": "DONUT MIT KRISTALLZUCKER",
        },
        {
            "img": "DONUT SCHOKO MIT.STREUSEL",
            "code": "4689",
            "name": "DONUT SCHOKO MIT.STREUSEL",
        },
        {"img": "FLADENBROT MINI", "code": "4229", "name": "FLADENBROT MINI"},
        {"img": "FRANZBROETCHEN", "code": "4633", "name": "FRANZBROETCHEN"},
        {"img": "KAISERSEMMEL", "code": "4234", "name": "KAISERSEMMEL"},
        {
            "img": "KNUSPERSTANGE MIT HAEHNCHEN",
            "code": "4696",
            "name": "KNUSPERSTANGE MIT HAEHNCHEN",
        },
        {"img": "LAUGENSTANGE", "code": "505", "name": "LAUGENSTANGE"},
        {"img": "LAUGENZOPF MIT KAESE", "code": "4416", "name": "LAUGENZOPF MIT KAESE"},
        {"img": "LUETTICHER WAFFEL", "code": "4479", "name": "LUETTICHER WAFFEL"},
        {
            "img": "NEW YORK STYLE ROLL CACAO",
            "code": "4470",
            "name": "NEW YORK STYLE ROLL CACAO",
        },
        {"img": "PIZZA MARGHERITA", "code": "4636", "name": "PIZZA MARGHERITA"},
        {"img": "PIZZA SALAMI", "code": "4765", "name": "PIZZA SALAMI"},
        {"img": "Quarkbällchen", "code": "430", "name": "Quarkbällchen"},
        {"img": "SONNTAGSBROETCHEN", "code": "4225", "name": "SONNTAGSBROETCHEN"},
        {"img": "APFELDREIECK", "code": "5009", "name": "APFELDREIECK"},
        {"img": "BAGUETTE", "code": "4409", "name": "BAGUETTE"},
        {"img": "BAGUETTE ZWIEBEL", "code": "4428", "name": "BAGUETTE ZWIEBEL"},
        {"img": "BERLINER EIERLIKÖR", "code": "4691", "name": "BERLINER EIERLIKÖR"},
        {
            "img": "BERLINER LONG DRIZZLE",
            "code": "4467",
            "name": "BERLINER LONG DRIZZLE",
        },
        {"img": "BERLINER NUSS-NOUGAT", "code": "4469", "name": "BERLINER NUSS-NOUGAT"},
        {"img": "BERLINER - KRAPPEN", "code": "4706", "name": "BERLINER/KRAPPEN"},
        {"img": "BITE BERRY BOMB", "code": "4522", "name": "BITE BERRY BOMB"},
        {"img": "BREZEL LAUGE", "code": "462", "name": "BREZEL LAUGE"},
        {"img": "BROET. WALNUSS HONIG", "code": "4219", "name": "BROET. WALNUSS HONIG"},
        {
            "img": "BROETCHEN KARTOF. HEL",
            "code": "4213",
            "name": "BROETCHEN KARTOF. HEL",
        },
        {
            "img": "BROETCHEN KUERBISKERN",
            "code": "4217",
            "name": "BROETCHEN KUERBISKERN",
        },
        {"img": "BROETCHEN MEHRKORN", "code": "4204", "name": "BROETCHEN MEHRKORN"},
        {
            "img": "BROETCHEN ROSEN DINKE",
            "code": "4241",
            "name": "BROETCHEN ROSEN DINKE",
        },
        {
            "img": "BROT ROSEN KART.DUNK.",
            "code": "450",
            "name": "BROT ROSEN KART.DUNK.",
        },
        {"img": "BROT GRILL", "code": "4404", "name": "BROT GRILL"},
        {
            "img": "BROT KARTOFFELZWIEBEL",
            "code": "4044",
            "name": "BROT KARTOFFELZWIEBEL",
        },
        {"img": "BROT KRUSTEN", "code": "4032", "name": "BROT KRUSTEN"},
        {
            "img": "BROT WEIZENMISCH hell 1kg",
            "code": "4031",
            "name": "BROT WEIZENMISCH hell 1kg",
        },
        {
            "img": "BROT WEIZENMISCH 500G ST",
            "code": "4037",
            "name": "BROT WEIZENMISCH 500G ST",
        },
        {
            "img": "MUFFINS STRACCIA 360G",
            "code": "363",
            "name": "MUFFINS STRACCIA 360G",
        },
        # Aggiungi più domande...
    ],
    "gemüse": [
        {"img": "AUBERGINE 1ST LS", "code": "263", "name": "AUBERGINE 1ST LS"},
        {"img": "BLATTSPINAT 500G BT", "code": "185", "name": "BLATTSPINAT 500G BT"},
        {
            "img": "BLATTSPINAT BABY BIO 1ST FP",
            "code": "168",
            "name": "BLATTSPINAT BABY BIO 1ST FP",
        },
        {"img": "BLUMENKOHL ST", "code": "312", "name": "BLUMENKOHL ST"},
        {"img": "BOHNE BUSCH 400G PK", "code": "161", "name": "BOHNE BUSCH 400G PK"},
        {"img": "BROCCOLI 500G PK", "code": "125", "name": "BROCCOLI 500G PK"},
        {"img": "CHAMPIGNONS WEISS", "code": "272", "name": "CHAMPIGNONS WEISS"},
        {"img": "CHICOREE 500G PK", "code": "116", "name": "CHICOREE 500G PK"},
        {"img": "CHINAKOHL KG LS", "code": "112", "name": "CHINAKOHL KG LS"},
        {"img": "FENCHEL KG LS", "code": "186", "name": "FENCHEL KG LS"},
        {"img": "GURKE BIO ST", "code": "167", "name": "GURKE BIO ST"},
        {"img": "GURKE MINI 1ST LS", "code": "236", "name": "GURKE MINI 1ST LS"},
        {
            "img": "GURKE SNACK BIO 250G SL",
            "code": "311",
            "name": "GURKE SNACK BIO 250G SL",
        },
        {"img": "GURKEN S ST", "code": "101", "name": "GURKEN S ST"},
        {"img": "HOKKAIDO BIO 1KG LS", "code": "126", "name": "HOKKAIDO BIO 1KG LS"},
        {"img": "KAROTTE 2KG BT", "code": "112", "name": "KAROTTE 2KG BT"},
        {"img": "KAROTTE 1KG BT", "code": "162", "name": "KAROTTE 1KG BT"},
        {"img": "KAROTTE BIO 1KG PK", "code": "297", "name": "KAROTTE BIO 1KG PK"},
        {"img": "KAROTTE EUR 1KG LS", "code": "149", "name": "KAROTTE EUR 1KG LS"},
        {"img": "KART. BIO 1,5KG PK", "code": "154", "name": "KART. BIO 1,5KG PK"},
        {"img": "KART. SUESS. 1KG LS", "code": "198", "name": "KART. SUESS. 1KG LS"},
        {
            "img": "KARTOFFELN UNGEWASCHEN 1KG LS",
            "code": "124",
            "name": "KARTOFFELN UNGEWASCHEN 1KG LS",
        },
        {"img": "KARTOFFELN 4 KG", "code": "230", "name": "KARTOFFELN 4 KG"},
        {
            "img": "KARTOFFEL FEST PREMIUM 2,5KG NZ",
            "code": "300",
            "name": "KARTOFFEL FEST PREMIUM 2,5KG NZ",
        },
        {
            "img": "KARTOFFEL MEHLIG 2,5KG PK",
            "code": "356",
            "name": "KARTOFFEL MEHLIG 2,5KG PK",
        },
        {"img": "KNOBLAUCH 200G NZ", "code": "140", "name": "KNOBLAUCH 200G NZ"},
        {"img": "KOHLRABI ST", "code": "201", "name": "KOHLRABI ST"},
        {
            "img": "KRAEUTER BASILIKUM BIO 1ST TG",
            "code": "129",
            "name": "KRAEUTER BASILIKUM BIO 1ST TG",
        },
        {
            "img": "KRAEUTER PETERS.GL.BIO 1ST TG",
            "code": "274",
            "name": "KRAEUTER PETERS.GL.BIO 1ST TG",
        },
        {
            "img": "KRAEUTER SCHNITTLA.BIO 1ST TG",
            "code": "276",
            "name": "KRAEUTER SCHNITTLA.BIO 1ST TG",
        },
        {"img": "LAUCHZWIEBEL BD", "code": "320", "name": "LAUCHZWIEBEL BD"},
        {"img": "PAKCHOI 300G FP", "code": "139", "name": "PAKCHOI 300G FP"},
        {"img": "PAPRIKA BIO 1KG LS", "code": "177", "name": "PAPRIKA BIO 1KG LS"},
        {"img": "PAPRIKA MIX 500G PK", "code": "245", "name": "PAPRIKA MIX 500G PK"},
        {"img": "PAPRIKA ROT 500G PK", "code": "285", "name": "PAPRIKA ROT 500G PK"},
        {
            "img": "PAPRIKA ROT SPITZ 500G PK",
            "code": "293",
            "name": "PAPRIKA ROT SPITZ 500G PK",
        },
        {
            "img": "PETERSILIE KRAUS BIO 1ST TG",
            "code": "275",
            "name": "PETERSILIE KRAUS BIO 1ST TG",
        },
        {
            "img": "PILZ CHAMP. BRAUN BIO 250G SL",
            "code": "108",
            "name": "PILZ CHAMP. BRAUN BIO 250G SL",
        },
        {
            "img": "PILZ CHAMPIGNON 400G SL",
            "code": "109",
            "name": "PILZ CHAMPIGNON 400G SL",
        },
        {
            "img": "PILZ CHAMPIGNON BRAUN 400G SL",
            "code": "138",
            "name": "PILZ CHAMPIGNON BRAUN 400G SL",
        },
        {"img": "ROTE BETE 500G PK", "code": "143", "name": "ROTE BETE 500G PK"},
        {"img": "SALAT EISBERG 1ST LS", "code": "144", "name": "SALAT EISBERG 1ST LS"},
        {"img": "SALAT FELD 150G SL", "code": "257", "name": "SALAT FELD 150G SL"},
        {
            "img": "SALAT KOPF WURZEL 1ST TT",
            "code": "104",
            "name": "SALAT KOPF WURZEL 1ST TT",
        },
        {"img": "SALAT RUCOLA 125G SL", "code": "261", "name": "SALAT RUCOLA 125G SL"},
        {
            "img": "SALAT SALATRIO 1ST LS",
            "code": "187",
            "name": "SALAT SALATRIO 1ST LS",
        },
        {
            "img": "SALATHERZEN ROMA 2ST PK",
            "code": "251",
            "name": "SALATHERZEN ROMA 2ST PK",
        },
        {"img": "SELLERIE", "code": "235", "name": "SELLERIE"},
        {
            "img": "SELLERIE STAUDE BIO 1ST LS",
            "code": "137",
            "name": "SELLERIE STAUDE BIO 1ST LS",
        },
        {
            "img": "SPARGEL GRUEN 400G BD",
            "code": "163",
            "name": "SPARGEL GRUEN 400G BD",
        },
        {"img": "SPITZKOHL KG LS", "code": "203", "name": "SPITZKOHL KG LS"},
        {"img": "SUPPENGRUEN 800G PK", "code": "279", "name": "SUPPENGRUEN 800G PK"},
        {
            "img": "TOMATO CHERRY ROMA 250G SL",
            "code": "278",
            "name": "TOMATO CHERRY ROMA 250G SL",
        },
        {
            "img": "TOMATO CHERRY ROMA BIO 250G SL",
            "code": "233",
            "name": "TOMATO CHERRY ROMA BIO 250G SL",
        },
        {
            "img": "TOMATO CHERRYRISPE 500G SL",
            "code": "277",
            "name": "TOMATO CHERRYRISPE 500G SL",
        },
        {
            "img": "TOMATO CHERRYRISPE MIN 200G SL",
            "code": "249",
            "name": "TOMATO CHERRYRISPE MIN 200G SL",
        },
        {
            "img": "TOMATO COCKTAILRISPE 350G SL",
            "code": "266",
            "name": "TOMATO COCKTAILRISPE 350G SL",
        },
        {"img": "TOMATO RISPE 500G SL", "code": "222", "name": "TOMATO RISPE 500G SL"},
        {
            "img": "TOMATO RISPE BIO 500G SL",
            "code": "226",
            "name": "TOMATO RISPE BIO 500G SL",
        },
        {"img": "TOMATO ROMA 250G PK", "code": "224", "name": "TOMATO ROMA 250G PK"},
        {
            "img": "TOMATO ROMA RISPE 300G SL",
            "code": "283",
            "name": "TOMATO ROMA RISPE 300G SL",
        },
        {"img": "TOMATO SNACK MIX", "code": "246", "name": "TOMATO SNACK MIX"},
        {"img": "WEISSKOHL KG LS", "code": "323", "name": "WEISSKOHL KG LS"},
        {"img": "ZUCCHINI 1KG LS", "code": "308", "name": "ZUCCHINI 1KG LS"},
        {"img": "ZUCCHINI BIO 500G NZ", "code": "244", "name": "ZUCCHINI BIO 500G NZ"},
        {
            "img": "ZUCKERMAIS VAK. BIO 400G SL",
            "code": "176",
            "name": "ZUCKERMAIS VAK. BIO 400G SL",
        },
        {
            "img": "ZWIEBEL GEMÜSSE 750G NZ",
            "code": "191",
            "name": "ZWIEBEL GEMÜSSE 750G NZ",
        },
        {"img": "ZWIEBEL ROT 500G NZ", "code": "166", "name": "ZWIEBEL ROT 500G NZ"},
        {"img": "ZWIEBELN BIO 1KG NZ", "code": "135", "name": "ZWIEBELN BIO 1KG NZ"},
    ],
    "obs": [
        {"img": "ANANAS 1ST LS", "code": "332", "name": "ANANAS 1ST LS"},
        {"img": "APFEL GRUEN 1KG LS", "code": "114", "name": "APFEL GRUEN 1KG LS"},
        {"img": "APFEL GRUEN 1KG PK", "code": "329", "name": "APFEL GRUEN 1KG PK"},
        {
            "img": "APFEL REGIONAL ROT 2KG PK",
            "code": "265",
            "name": "APFEL REGIONAL ROT 2KG PK",
        },
        {"img": "APFEL ROT 1KG LS", "code": "110", "name": "APFEL ROT 1KG LS"},
        {"img": "APFEL ROT 2KG PK", "code": "111", "name": "APFEL ROT 2KG PK"},
        {"img": "APFEL ROT 1KG FT", "code": "170", "name": "APFEL ROT 1KG FT"},
        {
            "img": "APFEL ROT BIO 650G FE",
            "code": "237",
            "name": "APFEL ROT BIO 650G FE",
        },
        {"img": "AVOCADO 1ST LS", "code": "117", "name": "AVOCADO 1ST LS"},
        {"img": "AVOCADO BIO 250G NZ", "code": "294", "name": "AVOCADO BIO 250G NZ"},
        {
            "img": "AVOCADO PREMIUM 1ST LS",
            "code": "1020",
            "name": "AVOCADO PREMIUM 1ST LS",
        },
        {"img": "BANANE BIO 1KG LS", "code": "155", "name": "BANANE BIO 1KG LS"},
        {"img": "BANANE CHIQUITA PY", "code": "205", "name": "BANANE CHIQUITA PY"},
        {"img": "BANANE GELB 1KG LS", "code": "100", "name": "BANANE GELB 1KG LS"},
        {"img": "BIRNE 1KG PK", "code": "119", "name": "BIRNE 1KG PK"},
        {"img": "BIRNE 1KG LS", "code": "120", "name": "BIRNE 1KG LS"},
        {"img": "BIRNE NASHI 1ST LS", "code": "324", "name": "BIRNE NASHI 1ST LS"},
        {"img": "ERDBEERE 500G SL", "code": "182", "name": "ERDBEERE 500G SL"},
        {
            "img": "ERDBEERE PREMIUM 400G SL",
            "code": "303",
            "name": "ERDBEERE PREMIUM 400G SL",
        },
        {
            "img": "ERDNUESSE I.D. SCHALE 400G BT",
            "code": "360",
            "name": "ERDNUESSE I.D. SCHALE 400G BT",
        },
        {"img": "GRANATAPFEL 1ST LS", "code": "165", "name": "GRANATAPFEL 1ST LS"},
        {"img": "GRAPEFRUIT 1ST LS", "code": "183", "name": "GRAPEFRUIT 1ST LS"},
        {"img": "HEIDELBEERE 500G PK", "code": "146", "name": "HEIDELBEERE 500G PK"},
        {"img": "HEIDELBEERE 300G SL", "code": "219", "name": "HEIDELBEERE 300G SL"},
        {"img": "HEIDELBEERE 125G SL", "code": "341", "name": "HEIDELBEERE 125G SL"},
        {
            "img": "HEIDELBEEREN BIO 125G SL",
            "code": "338",
            "name": "HEIDELBEEREN BIO 125G SL",
        },
        {"img": "HIMBEERE 125G SL", "code": "309", "name": "HIMBEERE 125G SL"},
        {"img": "INGWER BIO 1KG LS", "code": "181", "name": "INGWER BIO 1KG LS"},
        {"img": "KIWI 1ST LS", "code": "256", "name": "KIWI 1ST LS"},
        {"img": "KIWI GOLD 1ST LS", "code": "142", "name": "KIWI GOLD 1ST LS"},
        {"img": "LIMETTE BIO 300G NZ", "code": "229", "name": "LIMETTE BIO 300G NZ"},
        {"img": "MANDARINE 1KG NZ", "code": "212", "name": "MANDARINE 1KG NZ"},
        {"img": "MANDARINE 750G NZ", "code": "284", "name": "MANDARINE 750G NZ"},
        {
            "img": "MANDARINE M. BLATT 1KG LS",
            "code": "248",
            "name": "MANDARINE M. BLATT 1KG LS",
        },
        {"img": "MANGO 1ST LS", "code": "169", "name": "MANGO 1ST LS"},
        {"img": "MELONE HONIG 1KG LS", "code": "333", "name": "MELONE HONIG 1KG LS"},
        {"img": "NEKTARINE 1KG LS", "code": "152", "name": "NEKTARINE 1KG LS"},
        {"img": "ORANGE 1KG LS", "code": "136", "name": "ORANGE 1KG LS"},
        {"img": "ORANGE 2KG NZ", "code": "210", "name": "ORANGE 2KG NZ"},
        {"img": "ORANGE SAFT 1,5KG NZ", "code": "132", "name": "ORANGE SAFT 1,5KG NZ"},
        {
            "img": "PAPAYA ESSREIF 1ST LS",
            "code": "327",
            "name": "PAPAYA ESSREIF 1ST LS",
        },
        {
            "img": "PASSIONSFRUCHT 1ST LS",
            "code": "326",
            "name": "PASSIONSFRUCHT 1ST LS",
        },
        {"img": "PFLAUME 500G SL", "code": "108", "name": "PFLAUME 500G SL"},
        {"img": "PHYSALIS 100G SL", "code": "241", "name": "PHYSALIS 100G SL"},
        {"img": "POMELO HONIG 1ST LS", "code": "242", "name": "POMELO HONIG 1ST LS"},
        {
            "img": "TRAUBE BLAU KERNLOS 500G SL",
            "code": "287",
            "name": "TRAUBE BLAU KERNLOS 500G SL",
        },
        {
            "img": "TRAUBE HELL KERNLOS 500G SL",
            "code": "299",
            "name": "TRAUBE HELL KERNLOS 500G SL",
        },
        {"img": "ZITRONE 1ST LS", "code": "190", "name": "ZITRONE 1ST LS"},
    ],
    "blumen": [
        {"img": "BLUMENERDE 30L BT", "code": "9292", "name": "BLUMENERDE 30L BT"},
        {"img": "BIO UNIVERSALERDE", "code": "367", "name": "BIO UNIVERSALERDE"},
        {"img": "ZINNIA FARBMIX T12", "code": "3207", "name": "ZINNIA FARBMIX T12"},
        {
            "img": "FELDNARZISSEN 30-35CM",
            "code": "4747",
            "name": "FELDNARZISSEN 30-35CM",
        },
        {"img": "MINZE TOPF 14", "code": "3366", "name": "MINZE TOPF 14"},
        {"img": "OREGANO TOPF 14", "code": "3365", "name": "OREGANO TOPF 14"},
        {
            "img": "PRIMULA ACAULIS TOPF 14",
            "code": "3253",
            "name": "PRIMULA ACAULIS TOPF 14",
        },
        {"img": "ROSMARIN TOPF 14", "code": "3361", "name": "ROSMARIN TOPF 14"},
        {"img": "SALBEI TOPF 14", "code": "1580", "name": "SALBEI TOPF 14"},
        {"img": "THYMIAN BUNT TOPF 14", "code": "3363", "name": "THYMIAN BUNT TOPF 14"},
        {
            "img": "THYMIAN GRUEN TOPF 14",
            "code": "3362",
            "name": "THYMIAN GRUEN TOPF 14",
        },
        {
            "img": "ZITRONENMELISSE TOPF 14",
            "code": "3364",
            "name": "ZITRONENMELISSE TOPF 14",
        },
        {
            "img": "ZWEIGE KIRSCHE 1ST BD",
            "code": "316",
            "name": "ZWEIGE KIRSCHE 1ST BD",
        },
        {
            "img": "ZWEIGE KORKENZIEHERWE. 1ST BD",
            "code": "321",
            "name": "ZWEIGE KORKENZIEHERWE. 1ST BD",
        },
        {
            "img": "ZWEIGE WEIDENKAETZCHEN 1ST BD",
            "code": "317",
            "name": "ZWEIGE WEIDENKAETZCHEN 1ST BD",
        },
    ],
}


# ------ Routes
# ---- willkommen --
@app.route("/willkommen", methods=["GET", "POST"])
def willkommen():
    if request.method == "POST":
        geheime_code = request.form.get("geheime_code")
        if geheime_code == "penny77":  # Codice segreto da controllare
            session["auth"] = True
            return redirect(url_for("index"))
        else:
            flash("Codice segreto errato!", "error")
    return render_template("willkommen.html")


@app.route("/logout")
def logout():
    session.clear()  # Löscht alle Sitzungsvariablen
    flash("Du wurdest erfolgreich abgemeldet.", "info")  # Bestätigungsnachricht
    return redirect(
        url_for("willkommen")
    )  # Leitet zur Willkommensseite (oder Login-Seite) weiter


@app.route("/")
def index():
    if not session.get("auth"):
        return redirect(url_for("willkommen"))
    return render_template("index.html")


# Decoratore per evitare accessi diretti

from functools import wraps


def geheimer_code_erforderlich(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("auth"):
            flash(
                "Zugriff verweigert. Bitte geben Sie den geheimen Code ein.", "warning"
            )
            return redirect(url_for("willkommen"))
        return f(*args, **kwargs)

    return wrapper


from flask import flash


@app.route("/start_quiz", methods=["POST"])
def start_quiz():
    category = request.form.get("category")

    if category not in quiz_data:
        flash("⚠️ Bitte wähle zuerst eine Kategorie aus.")
        return redirect(url_for("categories"))  # O qualunque sia la pagina di partenza

    questions_list = quiz_data[category]
    if len(questions_list) < 7:
        questions = questions_list.copy()
    else:
        questions = random.sample(questions_list, 7)

    session["questions"] = questions
    session["current_question"] = 0
    session["score"] = 0
    session["attempts"] = 0
    session["category"] = category
    session["repeat_count"] = 0

    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
@geheimer_code_erforderlich
def quiz():
    questions = session.get("questions", [])
    current_index = session.get("current_question", 0)
    score = session.get("score", 0)

    if current_index >= len(questions):
        return redirect(url_for("result"))

    question = questions[current_index]
    show_answer = False
    answer_feedback = None  # può essere "correct" o "wrong"

    if request.method == "POST":
        user_code = request.form.get("code_input", "")
        if user_code == question["code"]:
            session["score"] = score + 1
            answer_feedback = "correct"
        else:
            answer_feedback = "wrong"
        show_answer = True

    return render_template(
        "quiz.html",
        question=question,
        question_num=current_index + 1,
        show_answer=show_answer,
        answer_feedback=answer_feedback,
    )

    return render_template(
        "quiz.html",
        question=question,
        question_num=current + 1,
        show_answer=show_answer,
    )


@app.route("/next_question", methods=["POST"])
@geheimer_code_erforderlich
def next_question():
    session["current_question"] += 1
    return redirect(url_for("quiz"))


@app.route("/answer", methods=["POST"])
@geheimer_code_erforderlich
def answer():
    user_code = request.form.get("code")
    current = session.get("current_question", 0)
    questions = session.get("questions", [])

    if current >= len(questions):
        return redirect(url_for("result"))

    correct_code = questions[current]["code"]
    session["attempts"] += 1

    if user_code == correct_code:
        session["score"] += 1

    session["current_question"] = current + 1
    return redirect(url_for("quiz"))


@app.route("/handle_repeat_choice", methods=["POST"])
@geheimer_code_erforderlich
def handle_repeat_choice():
    choice = request.form.get("repeat")
    repeat_count = session.get("repeat_count", 0)
    category = session.get("category")
    questions = session.get("questions", [])

    if choice == "yes":
        # Ripete lo stesso set di domande
        session["current_question"] = 0
        session["score"] = 0
        session["repeat_count"] = repeat_count + 1
        return redirect(url_for("quiz"))
    else:
        # Nuove domande (se disponibili)
        if category in quiz_data:
            questions_list = quiz_data[category]
            if len(questions_list) < 5:
                new_questions = questions_list.copy()
            else:
                new_questions = random.sample(questions_list, 7)

            session["questions"] = new_questions
            session["current_question"] = 0
            session["score"] = 0
            session["repeat_count"] = 0
        return redirect(url_for("quiz"))


@app.route("/result")
@geheimer_code_erforderlich
def result():
    score = session.get("score", 0)
    repeat_count = session.get("repeat_count", 0)
    category = session.get("category", "")

    if repeat_count < 2:
        session["repeat_count"] = repeat_count + 1
    else:
        session["repeat_count"] = 0

    return render_template(
        "result.html", score=score, repeat_count=repeat_count, category=category
    )


@app.route("/settings")
@geheimer_code_erforderlich
def settings():
    return render_template("einstellungen.html")


@app.route("/info")
def info():
    return render_template("info.html")


# Lernen
# Dati di esempio (puoi estendere questa lista con tutti i tuoi prodotti)
category_data = {
    "bake-off": [
        {
            "img": "BROT WELTMEISTER CHIA",
            "code": "4034",
            "name": "BROT WELTMEISTER CHIA",
        },
        {"img": "BROT WURZEL DUNKEL", "code": "4018", "name": "BROT WURZEL DUNKEL"},
        {"img": "BURGERSTYLE CLASSIC", "code": "4481", "name": "BURGERSTYLE CLASSIC"},
        {"img": "CIABATTA", "code": "4400", "name": "CIABATTA"},
        {"img": "CREAM MOOD", "code": "4660", "name": "CREAM MOOD"},
        {
            "img": "CROISSANT NUSS-NOUGAT",
            "code": "4673",
            "name": "CROISSANT NUSS-NOUGAT",
        },
        {"img": "CROISSANT BUTTER", "code": "4672", "name": "CROISSANT BUTTER"},
        {
            "img": "CROISSANT PISTAZIENCREME",
            "code": "4466",
            "name": "CROISSANT PISTAZIENCREME",
        },
        {
            "img": "DONUT MIT KRISTALLZUCKER",
            "code": "4473",
            "name": "DONUT MIT KRISTALLZUCKER",
        },
        {
            "img": "DONUT SCHOKO MIT.STREUSEL",
            "code": "4689",
            "name": "DONUT SCHOKO MIT.STREUSEL",
        },
        {"img": "FLADENBROT MINI", "code": "4229", "name": "FLADENBROT MINI"},
        {"img": "FRANZBROETCHEN", "code": "4633", "name": "FRANZBROETCHEN"},
        {"img": "KAISERSEMMEL", "code": "4234", "name": "KAISERSEMMEL"},
        {
            "img": "KNUSPERSTANGE MIT HAEHNCHEN",
            "code": "4696",
            "name": "KNUSPERSTANGE MIT HAEHNCHEN",
        },
        {"img": "LAUGENSTANGE", "code": "505", "name": "LAUGENSTANGE"},
        {"img": "LAUGENZOPF MIT KAESE", "code": "4416", "name": "LAUGENZOPF MIT KAESE"},
        {"img": "LUETTICHER WAFFEL", "code": "4479", "name": "LUETTICHER WAFFEL"},
        {
            "img": "NEW YORK STYLE ROLL CACAO",
            "code": "4470",
            "name": "NEW YORK STYLE ROLL CACAO",
        },
        {"img": "PIZZA MARGHERITA", "code": "4578", "name": "PIZZA MARGHERITA"},
        {"img": "PIZZA SALAMI", "code": "4765", "name": "PIZZA SALAMI"},
        {"img": "Quarkbällchen", "code": "430", "name": "Quarkbällchen"},
        {"img": "SONNTAGSBROETCHEN", "code": "4225", "name": "SONNTAGSBROETCHEN"},
        {"img": "APFELDREIECK", "code": "5009", "name": "APFELDREIECK"},
        {"img": "BAGUETTE", "code": "4409", "name": "BAGUETTE"},
        {"img": "BAGUETTE ZWIEBEL", "code": "4428", "name": "BAGUETTE ZWIEBEL"},
        {"img": "BERLINER EIERLIKÖR", "code": "4691", "name": "BERLINER EIERLIKÖR"},
        {
            "img": "BERLINER LONG DRIZZLE",
            "code": "4467",
            "name": "BERLINER LONG DRIZZLE",
        },
        {"img": "BERLINER NUSS-NOUGAT", "code": "4469", "name": "BERLINER NUSS-NOUGAT"},
        {"img": "BERLINER - KRAPPEN", "code": "4706", "name": "BERLINER/KRAPPEN"},
        {"img": "BITE BERRY BOMB", "code": "4522", "name": "BITE BERRY BOMB"},
        {"img": "BREZEL LAUGE", "code": "462", "name": "BREZEL LAUGE"},
        {"img": "BROET. WALNUSS HONIG", "code": "4219", "name": "BROET. WALNUSS HONIG"},
        {
            "img": "BROETCHEN KARTOF. HEL",
            "code": "4213",
            "name": "BROETCHEN KARTOF. HEL",
        },
        {
            "img": "BROETCHEN KUERBISKERN",
            "code": "4217",
            "name": "BROETCHEN KUERBISKERN",
        },
        {"img": "BROETCHEN MEHRKORN", "code": "4204", "name": "BROETCHEN MEHRKORN"},
        {
            "img": "BROETCHEN ROSEN DINKE",
            "code": "4241",
            "name": "BROETCHEN ROSEN DINKE",
        },
        {
            "img": "BROT ROSEN KART.DUNK.",
            "code": "450",
            "name": "BROT ROSEN KART.DUNK.",
        },
        {"img": "BROT GRILL", "code": "4404", "name": "BROT GRILL"},
        {
            "img": "BROT KARTOFFELZWIEBEL",
            "code": "4044",
            "name": "BROT KARTOFFELZWIEBEL",
        },
        {"img": "BROT KRUSTEN", "code": "4032", "name": "BROT KRUSTEN"},
        {
            "img": "BROT WEIZENMISCH hell 1kg",
            "code": "4031",
            "name": "BROT WEIZENMISCH hell 1kg",
        },
        {
            "img": "BROT WEIZENMISCH 500G ST",
            "code": "4037",
            "name": "BROT WEIZENMISCH 500G ST",
        },
        {
            "img": "MUFFINS STRACCIA 360G",
            "code": "363",
            "name": "MUFFINS STRACCIA 360G",
        },
        # ... altri elementi ...
    ],
    "gemüse": [
        {"img": "AUBERGINE 1ST LS", "code": "263", "name": "AUBERGINE 1ST LS"},
        {"img": "BLATTSPINAT 500G BT", "code": "185", "name": "BLATTSPINAT 500G BT"},
        {
            "img": "BLATTSPINAT BABY BIO 1ST FP",
            "code": "168",
            "name": "BLATTSPINAT BABY BIO 1ST FP",
        },
        {"img": "BLUMENKOHL ST", "code": "312", "name": "BLUMENKOHL ST"},
        {"img": "BOHNE BUSCH 400G PK", "code": "161", "name": "BOHNE BUSCH 400G PK"},
        {"img": "BROCCOLI 500G PK", "code": "125", "name": "BROCCOLI 500G PK"},
        {"img": "CHAMPIGNONS WEISS", "code": "272", "name": "CHAMPIGNONS WEISS"},
        {"img": "CHICOREE 500G PK", "code": "116", "name": "CHICOREE 500G PK"},
        {"img": "CHINAKOHL KG LS", "code": "112", "name": "CHINAKOHL KG LS"},
        {"img": "FENCHEL KG LS", "code": "186", "name": "FENCHEL KG LS"},
        {"img": "GURKE BIO ST", "code": "167", "name": "GURKE BIO ST"},
        {"img": "GURKE MINI 1ST LS", "code": "236", "name": "GURKE MINI 1ST LS"},
        {
            "img": "GURKE SNACK BIO 250G SL",
            "code": "311",
            "name": "GURKE SNACK BIO 250G SL",
        },
        {"img": "GURKEN S ST", "code": "101", "name": "GURKEN S ST"},
        {"img": "HOKKAIDO BIO 1KG LS", "code": "126", "name": "HOKKAIDO BIO 1KG LS"},
        {"img": "KAROTTE 2KG BT", "code": "112", "name": "KAROTTE 2KG BT"},
        {"img": "KAROTTE 1KG BT", "code": "162", "name": "KAROTTE 1KG BT"},
        {"img": "KAROTTE BIO 1KG PK", "code": "297", "name": "KAROTTE BIO 1KG PK"},
        {"img": "KAROTTE EUR 1KG LS", "code": "149", "name": "KAROTTE EUR 1KG LS"},
        {"img": "KART. BIO 1,5KG PK", "code": "154", "name": "KART. BIO 1,5KG PK"},
        {"img": "KART. SUESS. 1KG LS", "code": "198", "name": "KART. SUESS. 1KG LS"},
        {
            "img": "KARTOFFELN UNGEWASCHEN 1KG LS",
            "code": "124",
            "name": "KARTOFFELN UNGEWASCHEN 1KG LS",
        },
        {"img": "KARTOFFELN 4 KG", "code": "230", "name": "KARTOFFELN 4 KG"},
        {
            "img": "KARTOFFEL FEST PREMIUM 2,5KG NZ",
            "code": "300",
            "name": "KARTOFFEL FEST PREMIUM 2,5KG NZ",
        },
        {
            "img": "KARTOFFEL MEHLIG 2,5KG PK",
            "code": "356",
            "name": "KARTOFFEL MEHLIG 2,5KG PK",
        },
        {"img": "KNOBLAUCH 200G NZ", "code": "140", "name": "KNOBLAUCH 200G NZ"},
        {"img": "KOHLRABI ST", "code": "201", "name": "KOHLRABI ST"},
        {
            "img": "KRAEUTER BASILIKUM BIO 1ST TG",
            "code": "129",
            "name": "KRAEUTER BASILIKUM BIO 1ST TG",
        },
        {
            "img": "KRAEUTER PETERS.GL.BIO 1ST TG",
            "code": "274",
            "name": "KRAEUTER PETERS.GL.BIO 1ST TG",
        },
        {
            "img": "KRAEUTER SCHNITTLA.BIO 1ST TG",
            "code": "276",
            "name": "KRAEUTER SCHNITTLA.BIO 1ST TG",
        },
        {"img": "LAUCHZWIEBEL BD", "code": "320", "name": "LAUCHZWIEBEL BD"},
        {"img": "PAKCHOI 300G FP", "code": "139", "name": "PAKCHOI 300G FP"},
        {"img": "PAPRIKA BIO 1KG LS", "code": "177", "name": "PAPRIKA BIO 1KG LS"},
        {"img": "PAPRIKA MIX 500G PK", "code": "245", "name": "PAPRIKA MIX 500G PK"},
        {"img": "PAPRIKA ROT 500G PK", "code": "285", "name": "PAPRIKA ROT 500G PK"},
        {
            "img": "PAPRIKA ROT SPITZ 500G PK",
            "code": "293",
            "name": "PAPRIKA ROT SPITZ 500G PK",
        },
        {
            "img": "PETERSILIE KRAUS BIO 1ST TG",
            "code": "275",
            "name": "PETERSILIE KRAUS BIO 1ST TG",
        },
        {
            "img": "PILZ CHAMP. BRAUN BIO 250G SL",
            "code": "108",
            "name": "PILZ CHAMP. BRAUN BIO 250G SL",
        },
        {
            "img": "PILZ CHAMPIGNON 400G SL",
            "code": "109",
            "name": "PILZ CHAMPIGNON 400G SL",
        },
        {
            "img": "PILZ CHAMPIGNON BRAUN 400G SL",
            "code": "138",
            "name": "PILZ CHAMPIGNON BRAUN 400G SL",
        },
        {"img": "ROTE BETE 500G PK", "code": "143", "name": "ROTE BETE 500G PK"},
        {"img": "SALAT EISBERG 1ST LS", "code": "144", "name": "SALAT EISBERG 1ST LS"},
        {"img": "SALAT FELD 150G SL", "code": "257", "name": "SALAT FELD 150G SL"},
        {
            "img": "SALAT KOPF WURZEL 1ST TT",
            "code": "104",
            "name": "SALAT KOPF WURZEL 1ST TT",
        },
        {"img": "SALAT RUCOLA 125G SL", "code": "261", "name": "SALAT RUCOLA 125G SL"},
        {
            "img": "SALAT SALATRIO 1ST LS",
            "code": "187",
            "name": "SALAT SALATRIO 1ST LS",
        },
        {
            "img": "SALATHERZEN ROMA 2ST PK",
            "code": "251",
            "name": "SALATHERZEN ROMA 2ST PK",
        },
        {"img": "SELLERIE", "code": "235", "name": "SELLERIE"},
        {
            "img": "SELLERIE STAUDE BIO 1ST LS",
            "code": "137",
            "name": "SELLERIE STAUDE BIO 1ST LS",
        },
        {
            "img": "SPARGEL GRUEN 400G BD",
            "code": "163",
            "name": "SPARGEL GRUEN 400G BD",
        },
        {"img": "SPITZKOHL KG LS", "code": "203", "name": "SPITZKOHL KG LS"},
        {"img": "SUPPENGRUEN 800G PK", "code": "279", "name": "SUPPENGRUEN 800G PK"},
        {
            "img": "TOMATO CHERRY ROMA 250G SL",
            "code": "278",
            "name": "TOMATO CHERRY ROMA 250G SL",
        },
        {
            "img": "TOMATO CHERRY ROMA BIO 250G SL",
            "code": "233",
            "name": "TOMATO CHERRY ROMA BIO 250G SL",
        },
        {
            "img": "TOMATO CHERRYRISPE 500G SL",
            "code": "277",
            "name": "TOMATO CHERRYRISPE 500G SL",
        },
        {
            "img": "TOMATO CHERRYRISPE MIN 200G SL",
            "code": "249",
            "name": "TOMATO CHERRYRISPE MIN 200G SL",
        },
        {
            "img": "TOMATO COCKTAILRISPE 350G SL",
            "code": "266",
            "name": "TOMATO COCKTAILRISPE 350G SL",
        },
        {"img": "TOMATO RISPE 500G SL", "code": "222", "name": "TOMATO RISPE 500G SL"},
        {
            "img": "TOMATO RISPE BIO 500G SL",
            "code": "226",
            "name": "TOMATO RISPE BIO 500G SL",
        },
        {"img": "TOMATO ROMA 250G PK", "code": "224", "name": "TOMATO ROMA 250G PK"},
        {
            "img": "TOMATO ROMA RISPE 300G SL",
            "code": "283",
            "name": "TOMATO ROMA RISPE 300G SL",
        },
        {"img": "TOMATO SNACK MIX", "code": "246", "name": "TOMATO SNACK MIX"},
        {"img": "WEISSKOHL KG LS", "code": "323", "name": "WEISSKOHL KG LS"},
        {"img": "ZUCCHINI 1KG LS", "code": "308", "name": "ZUCCHINI 1KG LS"},
        {"img": "ZUCCHINI BIO 500G NZ", "code": "244", "name": "ZUCCHINI BIO 500G NZ"},
        {
            "img": "ZUCKERMAIS VAK. BIO 400G SL",
            "code": "176",
            "name": "ZUCKERMAIS VAK. BIO 400G SL",
        },
        {
            "img": "ZWIEBEL GEMÜSSE 750G NZ",
            "code": "191",
            "name": "ZWIEBEL GEMÜSSE 750G NZ",
        },
        {"img": "ZWIEBEL ROT 500G NZ", "code": "166", "name": "ZWIEBEL ROT 500G NZ"},
        {"img": "ZWIEBELN BIO 1KG NZ", "code": "135", "name": "ZWIEBELN BIO 1KG NZ"},
        # ... altri elementi ...
    ],
    "obs": [
        {"img": "ANANAS 1ST LS", "code": "332", "name": "ANANAS 1ST LS"},
        {"img": "APFEL GRUEN 1KG LS", "code": "114", "name": "APFEL GRUEN 1KG LS"},
        {"img": "APFEL GRUEN 1KG PK", "code": "329", "name": "APFEL GRUEN 1KG PK"},
        {
            "img": "APFEL REGIONAL ROT 2KG PK",
            "code": "265",
            "name": "APFEL REGIONAL ROT 2KG PK",
        },
        {"img": "APFEL ROT 1KG LS", "code": "110", "name": "APFEL ROT 1KG LS"},
        {"img": "APFEL ROT 2KG PK", "code": "111", "name": "APFEL ROT 2KG PK"},
        {"img": "APFEL ROT 1KG FT", "code": "170", "name": "APFEL ROT 1KG FT"},
        {
            "img": "APFEL ROT BIO 650G FE",
            "code": "237",
            "name": "APFEL ROT BIO 650G FE",
        },
        {"img": "AVOCADO 1ST LS", "code": "117", "name": "AVOCADO 1ST LS"},
        {"img": "AVOCADO BIO 250G NZ", "code": "294", "name": "AVOCADO BIO 250G NZ"},
        {
            "img": "AVOCADO PREMIUM 1ST LS",
            "code": "1020",
            "name": "AVOCADO PREMIUM 1ST LS",
        },
        {"img": "BANANE BIO 1KG LS", "code": "155", "name": "BANANE BIO 1KG LS"},
        {"img": "BANANE CHIQUITA PY", "code": "205", "name": "BANANE CHIQUITA PY"},
        {"img": "BANANE GELB 1KG LS", "code": "100", "name": "BANANE GELB 1KG LS"},
        {"img": "BIRNE 1KG PK", "code": "119", "name": "BIRNE 1KG PK"},
        {"img": "BIRNE 1KG LS", "code": "120", "name": "BIRNE 1KG LS"},
        {"img": "BIRNE NASHI 1ST LS", "code": "324", "name": "BIRNE NASHI 1ST LS"},
        {"img": "ERDBEERE 500G SL", "code": "182", "name": "ERDBEERE 500G SL"},
        {
            "img": "ERDBEERE PREMIUM 400G SL",
            "code": "303",
            "name": "ERDBEERE PREMIUM 400G SL",
        },
        {
            "img": "ERDNUESSE I.D. SCHALE 400G BT",
            "code": "360",
            "name": "ERDNUESSE I.D. SCHALE 400G BT",
        },
        {"img": "GRANATAPFEL 1ST LS", "code": "165", "name": "GRANATAPFEL 1ST LS"},
        {"img": "GRAPEFRUIT 1ST LS", "code": "183", "name": "GRAPEFRUIT 1ST LS"},
        {"img": "HEIDELBEERE 500G PK", "code": "146", "name": "HEIDELBEERE 500G PK"},
        {"img": "HEIDELBEERE 300G SL", "code": "219", "name": "HEIDELBEERE 300G SL"},
        {"img": "HEIDELBEERE 125G SL", "code": "341", "name": "HEIDELBEERE 125G SL"},
        {
            "img": "HEIDELBEEREN BIO 125G SL",
            "code": "338",
            "name": "HEIDELBEEREN BIO 125G SL",
        },
        {"img": "HIMBEERE 125G SL", "code": "309", "name": "HIMBEERE 125G SL"},
        {"img": "INGWER BIO 1KG LS", "code": "181", "name": "INGWER BIO 1KG LS"},
        {"img": "KIWI 1ST LS", "code": "256", "name": "KIWI 1ST LS"},
        {"img": "KIWI GOLD 1ST LS", "code": "142", "name": "KIWI GOLD 1ST LS"},
        {"img": "LIMETTE BIO 300G NZ", "code": "229", "name": "LIMETTE BIO 300G NZ"},
        {"img": "MANDARINE 1KG NZ", "code": "212", "name": "MANDARINE 1KG NZ"},
        {"img": "MANDARINE 750G NZ", "code": "284", "name": "MANDARINE 750G NZ"},
        {
            "img": "MANDARINE M. BLATT 1KG LS",
            "code": "248",
            "name": "MANDARINE M. BLATT 1KG LS",
        },
        {"img": "MANGO 1ST LS", "code": "169", "name": "MANGO 1ST LS"},
        {"img": "MELONE HONIG 1KG LS", "code": "333", "name": "MELONE HONIG 1KG LS"},
        {"img": "NEKTARINE 1KG LS", "code": "152", "name": "NEKTARINE 1KG LS"},
        {"img": "ORANGE 1KG LS", "code": "136", "name": "ORANGE 1KG LS"},
        {"img": "ORANGE 2KG NZ", "code": "210", "name": "ORANGE 2KG NZ"},
        {"img": "ORANGE SAFT 1,5KG NZ", "code": "132", "name": "ORANGE SAFT 1,5KG NZ"},
        {
            "img": "PAPAYA ESSREIF 1ST LS",
            "code": "327",
            "name": "PAPAYA ESSREIF 1ST LS",
        },
        {
            "img": "PASSIONSFRUCHT 1ST LS",
            "code": "326",
            "name": "PASSIONSFRUCHT 1ST LS",
        },
        {"img": "PFLAUME 500G SL", "code": "108", "name": "PFLAUME 500G SL"},
        {"img": "PHYSALIS 100G SL", "code": "241", "name": "PHYSALIS 100G SL"},
        {"img": "POMELO HONIG 1ST LS", "code": "242", "name": "POMELO HONIG 1ST LS"},
        {
            "img": "TRAUBE BLAU KERNLOS 500G SL",
            "code": "287",
            "name": "TRAUBE BLAU KERNLOS 500G SL",
        },
        {
            "img": "TRAUBE HELL KERNLOS 500G SL",
            "code": "299",
            "name": "TRAUBE HELL KERNLOS 500G SL",
        },
        {"img": "ZITRONE 1ST LS", "code": "190", "name": "ZITRONE 1ST LS"},
        # ... altri prodotti di obs ...
    ],
    "blumen": [
        {"img": "BLUMENERDE 30L BT", "code": "9292", "name": "BLUMENERDE 30L BT"},
        {"img": "BIO UNIVERSALERDE", "code": "367", "name": "BIO UNIVERSALERDE"},
        {"img": "ZINNIA FARBMIX T12", "code": "3207", "name": "ZINNIA FARBMIX T12"},
        {
            "img": "FELDNARZISSEN 30-35CM",
            "code": "4747",
            "name": "FELDNARZISSEN 30-35CM",
        },
        {"img": "MINZE TOPF 14", "code": "3366", "name": "MINZE TOPF 14"},
        {"img": "OREGANO TOPF 14", "code": "3365", "name": "OREGANO TOPF 14"},
        {
            "img": "PRIMULA ACAULIS TOPF 14",
            "code": "3253",
            "name": "PRIMULA ACAULIS TOPF 14",
        },
        {"img": "ROSMARIN TOPF 14", "code": "3361", "name": "ROSMARIN TOPF 14"},
        {"img": "SALBEI TOPF 14", "code": "1580", "name": "SALBEI TOPF 14"},
        {"img": "THYMIAN BUNT TOPF 14", "code": "3363", "name": "THYMIAN BUNT TOPF 14"},
        {
            "img": "THYMIAN GRUEN TOPF 14",
            "code": "3362",
            "name": "THYMIAN GRUEN TOPF 14",
        },
        {
            "img": "ZITRONENMELISSE TOPF 14",
            "code": "3364",
            "name": "ZITRONENMELISSE TOPF 14",
        },
        {
            "img": "ZWEIGE KIRSCHE 1ST BD",
            "code": "316",
            "name": "ZWEIGE KIRSCHE 1ST BD",
        },
        {
            "img": "ZWEIGE KORKENZIEHERWE. 1ST BD",
            "code": "321",
            "name": "ZWEIGE KORKENZIEHERWE. 1ST BD",
        },
        {
            "img": "ZWEIGE WEIDENKAETZCHEN 1ST BD",
            "code": "317",
            "name": "ZWEIGE WEIDENKAETZCHEN 1ST BD",
        },
        # ... altri fiori ...
    ],
}


@app.route("/lernen")
def lernen():
    category = request.args.get("category")
    index = int(request.args.get("index", 0))

    if category and category in category_data:
        items = category_data[category]
        item = items[index % len(items)]  # ciclico
        return render_template("lernen.html", category=category, item=item, index=index)
    return render_template("lernen.html")

# ----- AVVIO APPLICAZIONE -----
if __name__ == "__main__":
    # Ottieni la porta dalla variabile d'ambiente PORT (fornita da Render)
    # Se non esiste, usa 5000 come fallback (per lo sviluppo locale)
    port = int(os.environ.get('PORT', 5000))
    
    # Disabilita il debug in produzione
    # host='0.0.0.0' è necessario per Render
    app.run(host='0.0.0.0', port=port, debug=False)