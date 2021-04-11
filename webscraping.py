import urllib
from bs4 import BeautifulSoup
import requests

# Web sistemako pdfak deskargatzeko

# Hasierako aldagaiak

# Erabiltzailearen izena
user = "JON BARBERO AYARZAGUENA"
cookie = ''
eskaera_kopurua = 1
# Web sistemako egelako uria
irakasgaiaren_uria = "https://egela.ehu.eus/course/view.php?id=42336"


def Postmetodoa(uria, edukia, goiburuak):
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.request('POST', uria, data=edukia_encoded, headers=goiburuak, allow_redirects=False)

    return erantzuna


def Getmetodoa(uria, goiburuak):
    erantzuna = requests.request('GET', uria, headers=goiburuak, allow_redirects=False)

    return erantzuna


def eskaera(uria, metodo, datuak):
    global eskaera_kopurua

    print("\n\n ->" + str(eskaera_kopurua) + '.ESKAERA' + "<-")
    eskaera_kopurua += 1
    print('\n Metodoa: ' + metodo)
    print("URIa: " + uria)
    if len(datuak) > 0:
        print("Datuak")
        for datua in datuak:
            print(datua + ": " + datuak[datua])


def erantzunaeman(erantzuna):
    global user
    deskribapena = erantzuna.reason
    kodea = erantzuna.status_code
    print("\n ERANTZUNA")
    print("Status: " + str(kodea) + " " + deskribapena)
    print("Goiburuak")
    for goiburua in erantzuna.headers:
        print(goiburua + ": " + erantzuna.headers[goiburua])
    if erantzuna.status_code == 200 and user in str(erantzuna.content):
        edukia = erantzuna.content
        print("Edukia")
        print(edukia)


# Orain kautotu metodo garrantzitsua implementatu dut

def kautotuegelan():

    global cookie
    global user
    kautotutadago = False
    datuak = ""
    goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': '0', "Cookie": cookie}
    uria = "https://egela.ehu.eus"

    uria, goiburuak = prozesatuesk(uria, datuak, goiburuak)

    uria, goiburuak = prozesatuesk(uria, datuak, goiburuak)

    while not kautotutadago:
        eskaera(uria, 'POST', datuak)
        erantzuna = Postmetodoa(uria, datuak, goiburuak)
        erantzunaeman(erantzuna)
        kautotutadago = (erantzuna.status_code == 200 and user in str(erantzuna.content))
        if erantzuna.status_code == 303:
            uria = erantzuna.headers['Location']
            print("Location : " + uria)
        if "Set-Cookie" in erantzuna.headers:
            cookie = erantzuna.headers["Set-Cookie"].split(';')[0]
            goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': str(len(datuak)), "Cookie": cookie}
            print("Cookie : " + cookie)
            datuak = ""
        if erantzuna.status_code == 200 and "eGela UPV/EHU: Sartu gunean" in str(erantzuna.content):
            print("\n eGela UPV/EHU: Sartu gunean")
            print("\nErabiltzaile-izena (LDAP Zenbakia)")
            erabiltzailea = input()
            print("Pasahitza")
            pasahitza = input()
            datuak = {'username': erabiltzailea, 'password': pasahitza}
            print("SARTU Idatzi")
            input()


def prozesatuesk(uria, datuak, goiburuak):
    eskaera(uria, 'GET', datuak)
    erantzuna = Getmetodoa(uria, goiburuak)
    erantzunaeman(erantzuna)
    if erantzuna.status_code == 303:
        uria = erantzuna.headers['Location']
        print("Location : " + uria)
    if "Set-Cookie" in erantzuna.headers:
        cookie = erantzuna.headers["Set-Cookie"].split(';')[0]
        print("Cookie : " + cookie)
        goiburuak["Cookie"] = cookie
    return uria, goiburuak


def irakasgaiawb():
    # Kasu honetan Web sistemako irakasgaia izango da

    global irakasgaiaren_uria
    uria = irakasgaiaren_uria
    datuak = ""
    goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': '0', "Cookie": cookie}
    eskaera(uria, 'GET', datuak)
    erantzuna = Getmetodoa(uria, goiburuak)
    # erantzunaeman(erantzuna)
    soup = BeautifulSoup(erantzuna.content, "html.parser")
    print("\n Web Sistemak irakasgaian sartu zara!")
    print("\n Pdf-ak deskargatzeko eman ENTER")
    input()
    deskargatuPDF(soup, goiburuak)


def deskargatuPDF(soup, goiburuak):
    pdf_list = soup.find_all('div', {"class": "activityinstance"})
    for pdf in pdf_list:
        if pdf.find("img", {"src": "https://egela.ehu.eus/theme/image.php/fordson/core/1611567512/f/pdf"}):
            print("\n")
            uria = str(pdf).split("onclick=\"window.open('")[1].split("\'")[0].replace("amp;", "")
            erantzuna = Getmetodoa(uria, goiburuak)
            uriapdfdago = erantzuna.headers['Location']
            erantzuna = Getmetodoa(uriapdfdago, goiburuak)
            izenapdfa = uriapdfdago.split("mod_resource/content/")[1].split("/")[1].replace("%20", "_")
            print("Deskargatzen " + izenapdfa + " ...")
            pdfa = erantzuna.content
            print(uria)
            # pdfgorde karpetaren barruan deskargatuko dira pdf-ak
            file = open("./pdfgorde/" + izenapdfa, "wb")
            file.write(pdfa)
            file.close()
            print("Deskargatuta " + izenapdfa)

    print("\n\n Amaituta, pdf guztiak ongi jaitsi dira!")
    print("\n -->pdfgorde karpetan dituzu orain pdf-ak<--")


if __name__ == "__main__":
    # Main metodoa
    kautotuegelan()
    irakasgaiawb()
