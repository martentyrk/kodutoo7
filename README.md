# kodutoo7

7nda kodutöö jaoks loodud ussimäng, mida soovime kasutada reinforcement learningu jaoks.

#Kuidas jooksutada?

Kui jooksutate programmi eraldi virtuaalkeskkonnas, siis antud kausta sisenedes ning seejärel jooksutades 
`pip install -r requirements.txt` peaks installima kõik vajalikud moodulid.

Kui kõik moodulid, mida failides kasutatakse, on ära tõmmatud, võib käivitada main.py faili ja nautida vaatepilti.

#Kirjeldus
Antud repos on 3 faili, mis väärivad tähelepanu.

snake.py paneb pygame'i mooduli abil käima antud mängu, ning seal on ka defineeritud kõik võimalikud tegevused mängus.
Näiteks  on seal toidu lisamine, mängulauajoonistamine ja liikumine.

agent.py on mudel ise, mis hakkab õppima.

main.py fail paneb kõik kokku, võtab agendi (mudeli) ning
söödab talle sisse Snake() objekti, mille peal masin õppima hakkab.

Algoritmile on meil hetkel pandud piiriks ette 50 ringi. Ehk maksimaalselt saab see treenida
50 korda läbi mängides. Valisime selle arvu kuna 13 peal hakkab ta juba üsnagi
mõistlikult mängima, kuigi arenguruumi on endiselt palju.

Masin õpib läbi selle, et me anname talle punkte toidu kätte saamise eest ning karistame, kui
uss peaks ära surema kuidagi võttes punkte maha.