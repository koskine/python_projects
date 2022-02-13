"""
COMP.SC.100 Projekti Hangman (graafinen käyttöliittymä)

Tekijät: Iris Matinlauri
         Iiro Koskinen

Opiskelijanumerot: H299798 (Iris)
                   H299947 (Iiro)

Sähköpostit: iris.matinlauri@tuni.fi
             iiro.koskinen@tuni.fi


Ohjelma mallintaa hirsipuupeliä, joka aloitetaan painamalla "Aloita peli"
-nappia. Pelaaja voi valita pelin vaikeusasteen: perinteinen hirttolava tarjoaa
12 arvausmahdollisuutta ennen hirteen joutumista, puu tarjoaa vain seisemän.
Peliä pelataan yksin (tai mikä jottei kaverin kanssa, molemmat tosin eivät
pääse hirteen, vaikka haluaisivat) ja arvattavat sanat arvotaan joka
kierrokselle ohjelmoijien keksimältä sanalistalta.  Pelissä painellaan
kirjainnappeja, jotka muuttuvat joko vihreiksi, jos arvaus on oikea, tai
punaisiksi, mikäli arvaus menee väärin. Samalla kuvaan joko rakentuu
hirttäjäismaisemaa tai kuvan oikealla puolella arvattavaan sanaan paljastuu
kirjaimia. Mikäli tunnelma on liian ahdistava ja/tai uhkaava, pelin voi aina
lopettaa "Pysää ny!"-napista.

Ongelmatilanteita, jotka on otettu ohjelmassa huomioon: aloitusnappia voi
painaa vain kerran, joka leikkiin lähtee, se leikin kestäköön. Vaikeusastetta
ei voi muuttaa valikosta kesken pelin, eikä jo painettuja kirjainnappeja voi
painaa uudestaan.

Tämä ohjelma tähtää kehittyneeseen versioon projektista.
"""

# Kutsutaan kaikki ohjelmassa tarvittavat kirjastot ja työkalut
from tkinter import *
from tkinter import messagebox
from re import *
import random


class Hangman:
    """"
    Luokka toteuttaa graafisella käyttöliittymällä hirsipuupelin.
    """

    def __init__(self):
        """
        Luodaan ohjelmassa myöhemmin käytettäviä listoja ja muuttujia sekä heti
        alussa näkyviin tarvittavat käyttöliittymän komponentit.
        """

        self.__mainwindow = Tk()
        self.__mainwindow["bg"]="lavender"
        # Muokataan ikkunan kokoa sopivan kokoiseksi, kun näytöllä on vain
        # muutama nappi ja tekstikenttä
        self.__mainwindow.geometry("150x75")

        # Lista, joka sisältää suomalaisen näppäimistön kirjaimet.
        self.__alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                           "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                           "u", "v", "w", "x", "y", "z", "å", "ä" ,"ö"]

        # Lista, joka sisältää vaiheittaiset kuvat hirttolavan rakentumisesta.
        self.__gallow_images = ["gallow_1.png", "gallow_2.png", "gallow_3.png",
                                "gallow_4.png", "gallow_5.png", "gallow_6.png",
                                "gallow_7.png", "gallow_8.png", "gallow_9.png",
                                "gallow_10.png", "gallow_11.png",
                                "gallow_12.png", "gallow_13.png"]

        # Lista, joka sisältää vaiheittaiset kuvat puun hirttäjäismaisemasta.
        self.__tree_images = ["tree_1.png", "tree_2.png", "tree_3.png"
                              , "tree_4.png", "tree_5.png", "tree_6.png"
                              , "tree_7.png", "tree_8.png"]

        # Lista, joka sisältää ohjelmoijien keksimät arvattavissa olevat sanat.
        self.__single_player_words = \
            ["suihkuturbiinimoottori", "loisteputkivalaisin", "tasauspyörästö",
             "matalajännitekytkentä", "mascarponevaahto", "lavatanssituokio",
             "pyyhkäisyelektronimikroskooppi", "tetrabutyyliammoniumfluoridi",
             "merikoski", "metallityöstökoneistaja", "toteemipaalu",
             "kynsilakanpoistoaine", "ydinjäteongelma", "liukuovikauppa",
             "moniviljamuro", "kalibroida", "räjähdysherkkä","gondolihissi",
             "tunturijäkälä", "asiantuntijatehtävä", "nopeusvalvontakamera",
             "foliohattu", "salaliittoteoria", "kukkahattutäti",
             "tiedustelupalvelu", "toimeentulotukihakemus", "vyöhyketerapia",
             "poppamies", "lintuinfluenssa", "savukkeensytytin",
             "perustuslakivaliokunta", "legitimiteetti", "tiedustelupalvelu",
             "maksuhäiriömerkintä", "asuntovaunu", "velkajärjestely",
             "sana", "kaksikerrosbussi", "tuholaistorjuntayksikkö",
             "saippuakauppias"]

        # Luodaan ja sijoitetaan ohjelman suorittamisen pysäyttävä nappi.
        self.__stop_button = Button(self.__mainwindow, text="Pysää ny!",
                                    bg="papaya whip", fg="purple1",
                                    command=self.stop_program)
        self.__stop_button.grid(row=0, column=15)

        # Luodaan ja sijoitetaan otsikkotekstikenttä.
        self.__hangman_label = Label(self.__mainwindow, text="HIRSIPUU-PELI",
                                     bg="papaya whip", fg="gray1")
        self.__hangman_label.grid(row=0, column=0)

        # Luodaan ja sijoitetaan pelin aloitusnappi.
        self.__begin_button = Button(self.__mainwindow, text="Aloita peli",
                                     bg="papaya whip", fg="purple1",
                                     command=self.begin_game)
        self.__begin_button.grid(row=3, column=0)

        # Alustetaan apumuuttujat kuvien vaihtumiselle ja arvattavan sanan
        # paljastumiselle.
        self.__photo_index = 0
        self.__correct_letters = 0


    def create_keyboard(self):
        """
        Metodi toteuttaa näppäimistön muodostamisen, kun peli on aloitettu
        ja vaikeusaste valittu.
        """

        # Alustetaan ja sijoitetaan jokaista kirjainta vastaava nappi
        self.__button_a = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("a"))
        self.__button_a.grid(row=7, column=2)

        self.__button_b = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("b"))
        self.__button_b.grid(row=7, column=4)

        self.__button_c = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("c"))
        self.__button_c.grid(row=7, column=6)

        self.__button_d = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("d"))
        self.__button_d.grid(row=7, column=8)

        self.__button_e = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("e"))
        self.__button_e.grid(row=7, column=10)

        self.__button_f = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("f"))
        self.__button_f.grid(row=7, column=12)

        self.__button_g = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("g"))
        self.__button_g.grid(row=8, column=2)

        self.__button_h = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("h"))
        self.__button_h.grid(row=8, column=4)

        self.__button_i = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("i"))
        self.__button_i.grid(row=8, column=6)

        self.__button_j = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("j"))
        self.__button_j.grid(row=8, column=8)

        self.__button_k = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("k"))
        self.__button_k.grid(row=8, column=10)

        self.__button_l = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("l"))
        self.__button_l.grid(row=8, column=12)

        self.__button_m = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("m"))
        self.__button_m.grid(row=9, column=2)

        self.__button_n = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("n"))
        self.__button_n.grid(row=9, column=4)

        self.__button_o = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("o"))
        self.__button_o.grid(row=9, column=6)

        self.__button_p = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("p"))
        self.__button_p.grid(row=9, column=8)

        self.__button_q = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("q"))
        self.__button_q.grid(row=9, column=10)

        self.__button_r = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("r"))
        self.__button_r.grid(row=9, column=12)

        self.__button_s = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("s"))
        self.__button_s.grid(row=10, column=2)

        self.__button_t = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("t"))
        self.__button_t.grid(row=10, column=4)

        self.__button_u = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("u"))
        self.__button_u.grid(row=10, column=6)

        self.__button_v = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("v"))
        self.__button_v.grid(row=10, column=8)

        self.__button_w = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("w"))
        self.__button_w.grid(row=10, column=10)

        self.__button_x = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("x"))
        self.__button_x.grid(row=10, column=12)

        self.__button_y = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("y"))
        self.__button_y.grid(row=11, column=2)

        self.__button_z = Button(self.__mainwindow, bg="papaya whip",
                                 fg="gray1", command=lambda: self.clicked("z"))
        self.__button_z.grid(row=11, column=4)

        # å = ao
        self.__button_ao = Button(self.__mainwindow, bg="papaya whip",
                                  fg="gray1", command=lambda: self.clicked("å"))
        self.__button_ao.grid(row=11, column=6)

        # ä = aa
        self.__button_aa = Button(self.__mainwindow, bg="papaya whip",
                                  fg="gray1", command=lambda: self.clicked("ä"))
        self.__button_aa.grid(row=11, column=8)

        # ö = oo
        self.__button_oo = Button(self.__mainwindow, bg="papaya whip",
                                  fg="gray1", command=lambda: self.clicked("ö"))
        self.__button_oo.grid(row=11, column=10)

        # Luodaan lista kirjainnapeista, jotta oikea kirjain voidaan
        # seuraavaksi sijoittaa vastaavaan nappiin ja myöhemmin
        # tarkistaa, mitä kirjainnappia on painettu.
        self.__alphabet_buttons = \
            [self.__button_a, self.__button_b, self.__button_c,
             self.__button_d, self.__button_e, self.__button_f,
             self.__button_g, self.__button_h, self.__button_i,
             self.__button_j, self.__button_k, self.__button_l,
             self.__button_m, self.__button_n, self.__button_o,
             self.__button_p, self.__button_q, self.__button_r,
             self.__button_s, self.__button_t, self.__button_u,
             self.__button_v, self.__button_w, self.__button_x,
             self.__button_y, self.__button_z, self.__button_ao,
             self.__button_aa, self.__button_oo]

        # Sijoitetaan kirjaimet oikeisiin nappeihin ja silmämääräisesti :D
        # välilyöntejä lisäämällä tasataan näppäinten kokoeroja.
        for i, j in zip(self.__alphabet,self.__alphabet_buttons):
            key = i
            if i in ["m", "w"]:
                j.config(text=f"  {i} ")
            elif i in ["i", "j"]:
                j.config(text=f"   {i}  ")
            elif i in ["s", "t", "y", "f", "l"]:
                j.config(text=f"   {i}  ")
            else:
                j.config(text=f"  {i}  ")


    def start_program(self):
        """
        Tämä metodi aloittaa ohjelman suorittamisen.
        """

        self.__mainwindow.mainloop()


    def stop_program(self):
        """
        Tämä metodi päättää ohjelman suorittamisen
        """

        self.__mainwindow.destroy()


    def begin_game(self):
        """
        Tämä metodi käynnistää pelin, tuo vaikeustason valinnan näkyville,
        deaktivoi aloitusnapin ja arpoo pelaajalle arvattavan sanan.
        """

        # Suurennetaan ikkunaa siten, että vaikeustason valinnat mahtuvat
        # näkymään
        self.__mainwindow.geometry("300x125")

        self.choose_difficulty()
        self.__begin_button.config(state=DISABLED)
        self.__word_to_be_guessed = random.choice(self.__single_player_words)


    def choose_difficulty(self):
        """
        Tämä metodi suorittaa vaikeustason valinnan käyttäjän valinnan
        perusteella ja pelin suorittaminen jatkuu joko hirttolavan tai puun
        kuvilla.
        """

        var = IntVar()
        # Helpomman (hirttolava) vaikeusasteen valitsimen luominen ja
        # sijoittaminen.
        self.__difficulty_easy = \
            Radiobutton(self.__mainwindow,
                        text="hirttolava - saatat selvitä elossa",
                        bg="lavender", fg="purple1", variable=var, value=1,
                        command=lambda:self.game(self.__gallow_images))
        self.__difficulty_easy.grid(row=8, column=0)

        # Vaikeamman vaikeusasteen (puu) valitsimen luominen ja sijoittaminen.
        self.__difficulty_hard = \
            Radiobutton(self.__mainwindow,
                        text="puu - todennäköisesti kohtaat loppusi",
                        bg="lavender", fg="purple1", variable=var, value=2,
                        command=lambda:self.game(self.__tree_images))
        self.__difficulty_hard.grid(row=9, column=0)


    def game(self, difficulty):
        """
        Tämä metodi jatkaa pelin suorittamista valinnan jälkeen. Näppäimistö,
        onnentoivotus, jatko-ohje ja aloituskuva tuodaan näkyviin, vaikeustason
        valitsimet deaktivoidaan sekä kuvan viereen tuodaan näkyviin arvattava
        sana piilotettuna.

        :param difficulty: list, kuvaa kumman vaikeusasteen kuvia pelin
        suorittamisessa käytetään
        """
        
        # Koska arvattavien sanojen pituus vaihtelee, on järkevintä palauttaa
        # ikkunan koko dynaamiseksi.
        self.__mainwindow.geometry("")
        # Otetaan näppäimistö näkyviin.
        self.create_keyboard()

        # Deaktivoidaan vaikeustason valitsimet.
        self.__difficulty_easy.config(state=DISABLED)
        self.__difficulty_hard.config(state=DISABLED)

        # Otetaan aloituskuva valitusta vaikeusasteesta näkyviin.
        self.__photo = PhotoImage(file=difficulty[0])
        self.__photo_label = Label(self.__mainwindow, image=self.__photo)
        self.__photo_label.grid(row=7, column=14, rowspan=5, columnspan=3)

        # Luodaan ja sijoitetaan onnentoivotus ja jatko-ohje peliin.
        self.__luck_label = Label(self.__mainwindow,
                                  text="May the odds be ever in your favor",
                                  bg="papaya whip", fg="purple1")
        self.__luck_label.grid(row=10, column=0)

        self.__begin_label = Label(self.__mainwindow,
                                   text="Arvauksia kehiin",
                                   bg="papaya whip", fg="purple1")
        self.__begin_label.grid(row=11, column=0)

        # Luodaan piilotettu versio arvattavasta sanasta aloituskuvan viereen.
        # Listaa hyödyntämällä saadaan sanan kirjaimet sijoitettua gridiin
        # helposti peräkkäin.
        answer = self.__word_to_be_guessed
        self.__answer_labels = []
        for i in range(0, len(answer)):
            self.__answer_labels.append(Label(self.__mainwindow, text="    ",
                                       bg="papaya whip", fg="gray1",
                                       relief=RAISED, borderwidth=1))
            self.__answer_labels[i].grid(row=9, column=17+i)


    def clicked(self, letter):
        """
        Tämä metodi tarkastelee, mitä nappia on painettu ja onko näin arvattua
        kirjainta arvattavassa sanassa sekä muuttaa napin ominaisuuksia tämän
        tarkastelun perusteella.

        :param letter: str, yksittäinen kirjain, jonka napin painamista
        tarkastellaan
        """

        # Painettu nappi löytyy samalla indeksillä kirjain- sekä kirjainnappi-
        # listalta ja täten identifioituu.
        button = self.__alphabet_buttons[self.__alphabet.index(letter)]

        # Jos arvattu kirjain on arvattavassa sanassa, kirjaimen nappi
        # deaktivoidaan, sen väri muutetaan vihreäksi ja tämä kirjain tulee
        # näkyville kuvan vieressä olevaan piilotettuun sanaan
        # oikealle paikalle/paikoille.
        if letter in self.__word_to_be_guessed:
            button.config(bg="green yellow", state=DISABLED)
            matches = finditer(letter, self.__word_to_be_guessed)
            matches_positions = [match.start() for match in matches]
            for i in matches_positions:
                self.__answer_labels[i].config(text=" "+letter+" ")
            # Jos arvaukset menevät arvausten sallitussa rajassa oikein, eli
            # oikeita kirjaimia on paljastunut sanassa olevien kirjaimien määrä
            # ,pelaaja voittaa ja tämä ilmoitetaan pop-up-ikkunassa, johon
            # reagoiminen päättää ohjelman suorittamisen.
            factor = self.__word_to_be_guessed.count(letter)
            self.__correct_letters += factor
            if self.__correct_letters == len(self.__word_to_be_guessed):
                messagebox.showinfo(title=None, message="Voitit pelin!")
                self.__mainwindow.destroy()

        # Jos arvattu kirjain ei ole arvattavassa sanassa, kirjaimen nappi
        # deaktivoidaan ja sen väri muutetaan punaiseksi. Jokaisen väärän
        # arvauksen myötä hirttomaisema edistyy ja kuolema lähenee.
        else:
            button.config(bg="red", state=DISABLED)
            self.__photo_index += 1
            # Hirttomaiseman edistyminen hirttolavalla.
            if self.__photo["file"] in self.__gallow_images:
                self.__photo = PhotoImage(file=self.__gallow_images[self.__photo_index])
                self.__photo_label.config(image=self.__photo)
                # Mikäli vääriä arvauksia tulee yhteensä 12 eli kuvalistalta
                # on esitetty jo 12 kuvaa, uusi väärä arvaus päättää pelin.
                if self.__photo_index > 11:
                    messagebox.showinfo(title=None,
                                        message=f"Hävisit pelin!\nSana oli "
                                                f"{self.__word_to_be_guessed}")
                    self.__mainwindow.destroy()
            # Hirttomaiseman edistyminen puussa.
            else:
                self.__photo = PhotoImage(file=self.__tree_images[self.__photo_index])
                self.__photo_label.config(image=self.__photo)
                # Mikäli vääriä arvauksia tulee yhteensä seitsemän eli
                # kuvalistalta on jo esitetty seitsemän kuvaa, uusi väärä
                # arvaus päättää pelin.
                if self.__photo_index > 6:
                    messagebox.showinfo(title=None,
                                        message=f"Hävisit pelin!\nSana oli "
                                                f"{self.__word_to_be_guessed}")
                    self.__mainwindow.destroy()


def main():

    # Aloitetaan graafisen käyttöliittymän esittäminen.
    ui = Hangman()
    ui.start_program()

if __name__ == '__main__':
    main()