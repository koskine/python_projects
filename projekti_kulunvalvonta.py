"""
COMP.SC.100 Projekti ystäväverkko

Tekijät: Iris Matinlauri
         Iiro Koskinen

Opiskelijanumerot: H299798 (Iris)
                   H299947 (Iiro)

Sähköpostit: iris.matinlauri@tuni.fi
             iiro.koskinen@tuni.fi

Ohjelma mallintaa kulkukorttien hallintaohjelmaa, jossa voi tulostaa kaikkien
korttien tiedot, vain yhden kortin tiedot, tarkistaa pääsekö kortilla tietystä
ovesta, lisätä ovikoodeja kortille ja yhdistää kahden kortin ovikoodit ilman
päällekkäisyyksiä ovikoodeissa. Tämä ohjelma on kommentoitu suomeksi, vaikka muu
koodi on englanniksi, sillä pohja oli jo aloitettu englanniksi, jolloin tätä
tyyliä emme muuta.
"""

DOORCODES = {'TC114': ['TIE'], 'TC203': ['TIE'], 'TC210': ['TIE', 'TST'],
             'TD201': ['TST'], 'TE111': [], 'TE113': [], 'TE115': [],
             'TE117': [], 'TE102': ['TIE'], 'TD203': ['TST'], 'TA666': ['X'],
             'TC103': ['TIE', 'OPET', 'SGN'], 'TC205': ['TIE', 'OPET', 'ELT'],
             'TB109': ['OPET', 'TST'], 'TB111': ['OPET', 'TST'],
             'TB103': ['OPET'], 'TB104': ['OPET'], 'TB205': ['G'],
             'SM111': [], 'SM112': [], 'SM113': [], 'SM114': [],
             'S1': ['OPET'], 'S2': ['OPET'], 'S3': ['OPET'], 'S4': ['OPET'],
             'K1705': ['OPET'], 'SB100': ['G'], 'SB202': ['G'],
             'SM220': ['ELT'], 'SM221': ['ELT'], 'SM222': ['ELT'],
             'secret_corridor_from_building_T_to_building_F': ['X', 'Y', 'Z'],
             'TA': ['G'], 'TB': ['G'], 'SA': ['G'], 'KA': ['G']}


class Accesscard:
    """
    This class models an access card which can be used to check
    whether a card should open a particular door or not.
    """

    def __init__(self, id, name):
        """
        Constructor, creates a new object that has no access rights.

        :param id: str, card holders personal id
        :param name: str, card holders name

        THIS METHOD IS AUTOMATICALLY TESTED, DON'T CHANGE THE NAME OR THE
        PARAMETERS!
        """

        self.__id = id
        self.__name = name

        # alustetaan lista, johon tallennetaan kulkukortin pääsykoodit
        self.__codes = []

    def info(self):
        """
        The method has no return value. It prints the information related to
        the access card in the format:
        id, name, access: a1,a2,...,aN
        for example:
        777, Thelma Teacher, access: OPET, TE113, TIE
        Note that the space characters after the commas and semicolon need to
        be as specified in the task description or the test fails.

        THIS METHOD IS AUTOMATICALLY TESTED, DON'T CHANGE THE NAME, THE
        PARAMETERS, OR THE PRINTOUT FORMAT!
        """

        # muutetaan listan esitysmuoto merkkijonoksi tulostusta varten
        as_string = ", ".join(sorted(self.__codes))
        print(f"{self.__id}, {self.__name}, access: {as_string}")

    def get_name(self):
        """
        :return: Returns the name of the accesscard holder.
        """

        return self.__name

    def get_id(self):
        """

        :return: Returns the id number of the accesscard holder.
        """
        return self.__id

    def add_access(self, new_access_code):
        """
        The method adds a new accesscode into the accesscard according to the
        rules defined in the task description.

        :param new_access_code: str, the accesscode to be added in the card.

        THIS METHOD IS AUTOMATICALLY TESTED, DON'T CHANGE THE NAME, THE
        PARAMETERS, OR THE RETURN VALUE! DON'T PRINT ANYTHING IN THE METHOD!
        """
        # Tarkistetaan onko syötetty kulkukoodi olemassa. Joudumme toteuttamaan
        # tarkistuksen myös metodin sisällä, sillä emme muuten saaneet add
        # komentoa menemään läpi automaattitesteristä, sillä se vaatii id:n
        # tarkistuksen ennen kulkukoodin tarkastusta, emmekä saaneet koodiamme
        # muutettua oikeanlaiseksi mitenkään tyylikkäämmin.
        code_found = False
        # Aluksi käydään läpi kaikki kulkualueet ja tarkistetaan
        # onko syötetty kulkukoodi yksi niistä.
        for i in DOORCODES:
            if new_access_code in DOORCODES[i]:
                code_found = True
        # Tarkistetaan myös onko syötetty kulkukoodi jokin olemassa
        # olevista ovikoodeista.
        if new_access_code in DOORCODES:
            code_found = True
        # aluksi käydään läpi löytyykö kortilta jo kulkualue, joka oikeuttaa
        # lisättäväksi tarkoitetun oven avaamiseen. Jos näin on, ei ovikoodia
        # lisätä.
        if not code_found:
            return

        try:
            for i in DOORCODES[new_access_code]:
                if i in self.__codes:
                    return

        # Keyerror except-rakenteen avulla vältetään ohjelman suorituksen
        # pysähtyminen jos annettua uutta ovikoodia ei löydy DOORCODES
        # sanakirjasta
        except KeyError:
            pass

        # jos uutta ovikoodia vastavaa kulkualuetta ei löydy kortilta,
        # tarkistetaan löytyykö uusi ovikoodi itsessään kulkukortilta.
        # Jos uutta ovikoodia tai sitä vastaavaa kulkualuetta ei löydy kortilta
        # lisätään uusi ovikoodi kortille.
        if new_access_code in self.__codes:
            return
        else:
            self.__codes.append(new_access_code)

        # Jos uusi kulkukoodi on kulkualue, poistetaan kortilta tätä
        # kulkualuetta vastaavat yksittäiset ovikoodit. Tämä toteutetaan
        # käymällä läpi DOORCODES-sanakirjaa ja poistamalla vastaantulevat
        # päällekkäisyydet.
        for i in DOORCODES:
            if new_access_code in DOORCODES[i]:
                try:
                    self.__codes.remove(i)
                except ValueError:
                    pass

    def check_access(self, door):
        """
        Checks if the accesscard allows access to a certain door.

        :param door: str, the doorcode of the door that is being accessed.
        :return: True: The door opens for this accesscard.
                 False: The door does not open for this accesscard.

        THIS METHOD IS AUTOMATICALLY TESTED, DON'T CHANGE THE NAME, THE
        PARAMETERS, OR THE RETURN VALUE! DON'T PRINT ANYTHING IN THE METHOD!
        """

        # Aluksi tarkistetaan löytyykö kortilta kulkualue, joka oikeuttaa
        # kysytyn ovikoodin käyttöön. Jos kulkualue löytyy, palautetaan True
        try:
            for i in DOORCODES[door]:
                if i in self.__codes:
                    return True

        # Kuten edellä, estetään ohjelman pysähtyminen, mikäli kysyttyä
        # ovikoodia ei ole olemassa
        except KeyError:
            pass

        # Jos kulkualuetta ei löydy, tarkistetaan löytyykö kysytty ovikoodi
        # kortilta. Paluuarvo määräytyy suoraan tämän perusteella.
        if door in self.__codes:
            return True
        else:
            return False

    def merge(self, card):
        """
        Merges the accesscodes from another accesscard to this accesscard.

        :param card: Accesscard, the accesscard whose access rights are added to this card.

        THIS METHOD IS AUTOMATICALLY TESTED, DON'T CHANGE THE NAME, THE
        PARAMETERS, OR THE RETURN VALUE! DON'T PRINT ANYTHING IN THE METHOD!
        """

        # Koska add_access metodi huolehtii, ettei korteille synny
        # päällekkäisyyksiä koodien suhteen, ei tässä kohtaa tarvitse ottaa
        # sitä huomioon.
        for i in card.__codes:
            self.add_access(i)


def read_file(filename):
    """
    Function reads the file and saves the data to two lists. One containing
    Accescard objects and the other containing the respective object's
    accesscodes

    :param filename: str, name of the file to be opened
    :return: list, containing Accescard objects
    """

    # Alustetaan lista, johon tallennetaan Accescard-olioita syötetiedostolta.
    accesscard_list = []

    # Yritetään avata tiedosto ja mikäli se onnistuu, luodaan tiedoista
    # Accesscard-olioita, ja liitetään niihin niille kuuluvat kulkukoodit.
    try:
        file = open(filename, mode="r")

        for row in file:
            parts = row.rstrip().split(";")
            codes = parts[2].split(",")
            single_accesscard = Accesscard(parts[0], parts[1])

            accesscard_list.append(single_accesscard)

            for i in codes:
                single_accesscard.add_access(i)

        file.close()

        return accesscard_list

    except OSError:
        print("Error: file cannot be read.")
        # Palautetaan arvo 1, jotta sitä voidaan käyttää ehtona ohjelman
        # toiminnan pysäyttämiseen main-funktiossa
        return 1


def main():
    # Luetaan lähdetiedosto
    cards = read_file("accessinfo.txt")

    # Edellä mainittu ohjelman pysäyttämisehto.
    if cards == 1:
        return

    while True:
            line = input("command> ")

            if line == "":
                break

            strings = line.split()
            command = strings[0]

            if command == "list" and len(strings) == 1:
                # Alustetaan lista, johon tallennetaan korttien id-numerot.
                # Tämän listan avulla saamme tulostuksen toteutettua
                # aakkosjärjestyksessä
                print_list = []
                # Lisätään kaikkien cards-listasta löytyvien Accescard-
                # olioiden id-numerot listaan
                for i in cards:
                    print_list.append(i.get_id())
                # Käydään kahdella sisäisellä loopilla läpi sekä id-numerot,
                # että niitä vastaavat oliot
                for j in sorted(print_list):
                    for i in cards:
                        if i.get_id() == j:
                            # Hyödynnetään yksittäisten rivien tulostuksessa
                            # metodia info.
                            i.info()

            elif command == "info" and len(strings) == 2:
                card_id = strings[1]
                # Käytetään apumuuttuja id_foundia annetun id-numeron olemassa
                # olon tutkimiseen.
                id_found = False
                # Käydään läpi cards-listalta löytyvät oliot. Jos jonkin olion
                # id-numero on sama kuin käyttäjän syöttämä numero, tulostetaan
                # tähän olioon liittyvät tiedot
                for i in cards:
                    if i.get_id() == card_id:
                        i.info()
                        id_found = True

                if not id_found:
                    print("Error: unknown id.")

            elif command == "access" and len(strings) == 3:
                card_id = strings[1]
                door_id = strings[2]

                # Hyödynnetään jälleen apumuuttujaa syötetyn id-numeron
                # olemassa olon selvittämiseen
                id_found = False
                for i in cards:
                    if i.get_id() == card_id:
                        id_found = True
                        # Jos id-numero ja ovikoodi ovat valideja, tarkistetaan
                        # onko tällä kortinhaltijalla oikeus kulkea kyseisestä
                        # ovesta.
                        if i.check_access(door_id):
                            print(f"Card {i.get_id()} ( {i.get_name()} ) has "
                                  f"access to door {door_id}")
                        # Tarkistetaan vielä, onko käyttäjän syöttämä ovikoodi
                        # validi. Tämä on hieman hölmö väli tarkistaa ovikoodi
                        # mutta emme päässeet automaattitesteristä läpi, kun
                        # tarkastus oli aikaisemmin, sillä olimme toteuttaneet
                        # sen jo ennen id-numeron tarkastusta
                        elif door_id not in DOORCODES:
                            print("Error: unknown doorcode.")
                            break
                        else:
                            print(f"Card {i.get_id()} ( {i.get_name()} ) has "
                                  f"no access to door {door_id}")
                if not id_found:
                    print("Error: unknown id.")
                    continue



            elif command == "add" and len(strings) == 3:
                card_id = strings[1]
                access_code = strings[2]



                # Tarkistetaan myös id-numeron oikeellisuus, jälleen samaa
                # apumuuttujaa hyödyntäen, kuin edellisessä command-ehdossa.
                id_found = False

                # Jos molemmat syötteet ovat valideja lisätään syötetty
                # kulkukoodi kortille
                for i in cards:
                    if i.get_id() == card_id:
                        i.add_access(access_code)
                        id_found = True
                if not id_found:
                    print("Error: unknown id.")
                    continue

                # Seuraavaksi tarkistetaan syötetyn kulkukoodin olemassa olo,
                # jälleen apumuuttujaa hyödyntäen
                code_found = False
                # Aluksi käydään läpi kaikki kulkualueet ja tarkistetaan
                # onko syötetty kulkukoodi yksi niistä.
                for i in DOORCODES:
                    if access_code in DOORCODES[i]:
                        code_found = True
                # Tarkistetaan myös onko syötetty kulkukoodi jokin olemassa
                # olevista ovikoodeista.
                if access_code in DOORCODES:
                    code_found = True

                if not code_found:
                    print("Error: unknown accesscode.")

            elif command == "merge" and len(strings) == 3:
                card_id_to = strings[1]
                card_id_from = strings[2]
                # Tarkistetaan molempien syötettyjen id-numeroiden oikeellisuus
                # jo tutuksi tulleiden apumuuttujien avulla.
                first_id_found = False
                second_id_found = False

                # Jos molemmat id-numerot ovat valideja suoritetaan korttien
                # yhdentäminen.
                for i in cards:
                    if i.get_id() == card_id_to:
                        first_id_found = True
                        for j in cards:
                            if j.get_id() == card_id_from:
                                i.merge(j)
                                second_id_found = True
                if not first_id_found or not second_id_found:
                    print("Error: unknown id.")

            elif command == "quit":
                print("Bye!")
                return

            else:
                print("Error: unknown command.")


if __name__ == "__main__":
    main()
