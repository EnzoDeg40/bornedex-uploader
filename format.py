from datetime import datetime
import html

def relative_date(date_str):
    date_format = "%Y-%m-%d %H:%M:%S"
    date = datetime.strptime(date_str, date_format)
    date_actuelle = datetime.now()
    difference = date_actuelle - date
    if difference.days == 0:
        if difference.seconds < 60:
            return "Il y a quelques secondes"
        elif difference.seconds < 3600:
            minutes = difference.seconds // 60
            return f"Il y a {minutes} minute{'s' if minutes > 1 else ''}"
        else:
            heures = difference.seconds // 3600
            return f"Il y a {heures} heure{'s' if heures > 1 else ''}"
    elif difference.days == 1:
        return "Il y a 1 jour"
    elif difference.days < 7:
        return f"Il y a {difference.days} jours"
    elif difference.days < 30:
        semaines = difference.days // 7
        return f"Il y a {semaines} semaine{'s' if semaines > 1 else ''}"
    elif difference.days < 365:
        mois = difference.days // 30
        return f"Il y a {mois} mois"
    else:
        ans = difference.days // 365
        return f"Il y a {ans} an{'s' if ans > 1 else ''}"

def is_valid_borne(bool):
    return "✔️" if bool else "❌"

def map_link(x, y):
    if x is not None and y is not None:
        return f"<a href='https://www.openstreetmap.org/?mlat={x}&mlon={y}'>🗺️</a>"
    else:
        return ""

def wiki_link(wiki):
    if wiki is not None:
        return f"<a href='{html.escape(wiki)}'>📙</a>"
    else:
        return ""

if __name__ == "__main__":
    date_str = "2024-02-25 20:52:27"
    resultat = relative_date(date_str)
    print(resultat)
