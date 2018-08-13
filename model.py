#encim lahko reže pri več zaporedjih; če je zaporedje zanj npr. AG/RT pomeni,
#da reže vsakič, ko se pojavita zaporedji AGAT in AGGT saj R pomeni A ali G.
#Spodnji slovar zajema vse spremenljivke, ki se lahko pojavijo in katere
#nukleotide predstavljajo.
slovar = {
'R': ['A', 'G'], 'Y': ['C', 'T'], 'B': ['C', 'G', 'T'],
'D': ['A', 'G', 'T'], 'K': ['G', 'T'], 'M': ['A', 'C'],
'H': ['A', 'C', 'T'], 'V': ['A', 'C', 'G'], 'S':['G', 'C'],
'W': ['A', 'T'], 'N': ['A', 'C', 'G', 'T']
    }

#Spodnjo funkcijo uporabim pri funkciji primerjaj in je definirana posebej, da
#lahko hitro spremenim 'prostor ujemanja.' Trenutno se številki ujemata, če se
#razlikujeta za manj kot 20. Vecjo razliko uporabim v primeru, da se število
#nukleotidov v eksperimentalnem vzorcu močno razlikuje od pričakovanega vzorca.
#To pomeni da vzorec ni homogen.
def manjsa_razlika(prvo, drugo):
    return prvo >= drugo - 10 and prvo <= drugo + 10

def vecja_razlika(prvo, drugo):
    return prvo >= drugo - 50 and prvo <= drugo + 50

################################################################################

#DNA podajamo kot niz brez presledkov, encim pa podamo z zaporedjem pri
#katerem reže, pri čemer s '/' označimo mesto, kjer reže encim.

class Organizem:

    def __inti__(self, dna, encim):
        self.dna = dna
        self.encim = encim
        self.razrezan = ''
        self.ujemanje = ''
        
    def doloci_dolzino_rezov(self):
        '''Funkcija 'razreže' DNA (kot jo razreže encim) in vrne dolžine nastalih rezov.'''
        zap_dna, zap_encim = self.dna, self.encim 
        zap_dna, zap_encim = zap_dna.upper(), zap_encim.upper()
        vsa_zaporedja_za_encim = [] 
        for nukleotid in zap_encim:
            if nukleotid in slovar:
                for element in slovar[nukleotid]:
                    vsa_zaporedja_za_encim.append(zap_encim.replace(nukleotid, element))
        if vsa_zaporedja_za_encim == []:
            vsa_zaporedja_za_encim = [zap_encim]
        for zaporedje in vsa_zaporedja_za_encim:
            if zaporedje.replace('/', '') in zap_dna:
                zap_dna = zap_dna.replace(zaporedje.replace('/', ''), zaporedje) 
        seznam_dolzin = []
        for element in zap_dna.split('/'):
            seznam_dolzin.append(len(element))    
        koncen_seznam = ''
        for element in seznam_dolzin:
            koncen_seznam += str(element) + '/'
        self.razrezan = koncen_seznam[:-1]

#Razrezani zaporedji 'se ujemata' v dveh primerih, če se posamezne številke v
#razrezu razlikujejo za manj kot 20. 
    def primerjaj(self, eksperiment):
        '''Dolžino rezov, ki jo določimo eksperimentalno primerja s tem kar vrne funkcija doloci_dolzino_rezov in na koncu vrne: 'se ujemata', 'se ne ujemata' ali 'vzorec ni homogen' '''
        pricakovano = self.razrezan
        eksperiment_s, pricakovano_s = str(eksperiment).split('/'), str(pricakovano).split('/')
        #najprej pogledam, če eksperimentalni vzorec ni homogen, torej ali je veliko daljši od pričakovanega 
        e, p = 0, 0 #to bosta vsoti nukleotidov v vzorcih, ki jih primerjamo
        for stevilka in eksperiment_s:
            e += int(stevilka)
        for stevilka in pricakovano_s:
            p += int(stevilka)
        if not vecja_razlika(e, p):
            self.ujemanje = 'vzorec ni homogen'
        else:
            self.ujemanje = ''
        if self.ujemanje == '':
            if len(eksperiment_s) != len(pricakovano_s):
                self.ujemanje = 'se ne ujemata'
            else:
                stevec = 0
                for eksp in eksperiment_s:
                    if manjsa_razlika(int(eksp), int(pricakovano_s[eksperiment_s.index(eksp)])) == True: 
                        stevec += 1
                if stevec == len(eksperiment_s):
                    self.ujemanje = 'se ujemata'
                else:
                    self.ujemanje = 'se ne ujemata'

    def razrez_z_vec_encimi(self, encimi):
        '''Vzame zaporedje DNA in več encimov in vrne dolžine rezov po vrsti za vsak encim'''
        zap_dna = self.dna
        zap_dna, encimi = zap_dna.upper(), encimi.upper()
        encimi = encimi.split(',')
        seznam_rezov = []
        for encim in encimi:
            encim = encim.replace(',', '').replace(' ', '')
            self.encim = encim
            self.doloci_dolzino_rezov()
            seznam_rezov.append(self.razrezan)
        koncen_rezultat = ''
        for element in seznam_rezov:
            koncen_rezultat += str(element) + ', '
        self.razrezan = koncen_rezultat[:-2]

    def razrez_z_datotekami(self, encimi_d): #oznaka _d označuje da gre za datoteko
        dna_d = self.dna
        encimi = open(encimi_d)
        dna = open(dna_d)
        with open('Dolzine.txt', 'w') as dolzine: #ustvarim novo datoteko
            encimi_str = ''
            for encim in encimi: #ti koraki so potrebni zaradi načina zapisa encimov v datoteki
                if ':' in encim:
                    encim = encim[encim.index(':') + 1:]
                if '\n' in encim:
                    encim = encim.replace('\n', '')
                encimi_str += encim[1:] + ','
            for zaporedje in dna:
                if ':' in zaporedje:
                    zaporedje = zaporedje[zaporedje.index(':') + 2:]
                if zaporedje != '\n': 
                    if zaporedje[-1] == '\n':
                        zaporedje = zaporedje[:-1]
                    self.dna = zaporedje
                    self.razrez_z_vec_encimi(encimi_str[:-1])
                    for razrez in self.razrezan.split(','):
                        dolzine.write(razrez)
                    dolzine.write('\n')
            dolzine.close()

#Funkcija je uporabna kadar imamo datoteki s pričakovanimi rezultati in
#rezultati, ki smo jih dobili eksperimentalno, pri čemer morata biti enako
#formulirani. Primerjava je smiselna, če primerjamo enako število DNA zaporedij
#in enako število encimov. 
    def vec_primerjav(self, eksperiment_d): 
        '''Vzame datoteko z rezultati eksperimentov in datoteko s pricakovanimi dolzinami (ki jo dobimo z zgornjimi funkcijami) - na konc vrne 'se ujema' al pa 'se ne ujema' '''
        pricakovano_d = self.dna
        eksp = open(eksperiment_d)
        pricak = open(pricakovano_d)
        koncen_rezultat = ''
        eksperimentalno, pricakovano = [], []
        for vrstica_e in eksp:
            eksperimentalno.append(vrstica_e.split(' '))
        for vrstica_p in pricak:
            pricakovano.append(vrstica_p.split(' '))
        if len(eksperimentalno) != len(pricakovano): 
            koncen_rezultat = ':( ' 
        else: 
            for i in range(len(eksperimentalno)): 
                if len(eksperimentalno[i]) != len(pricakovano[i]): 
                    koncen_rezultat += ':(' 
                else:
                    vmesen_rezultat = ''
                    for k in range(len(eksperimentalno[i])): 
                        pricakovano[i][k], eksperimentalno[i][k] = pricakovano[i][k].replace('\n', ''), eksperimentalno[i][k].replace('\n', '')
                        self.razrezan = pricakovano[i][k]
                        self.primerjaj(eksperimentalno[i][k])
                        vmesen_rezultat += self.ujemanje + ', '
                    if vmesen_rezultat == '': #v primeru da je druga datoteka prazna
                        koncen_rezultat += 'se ne ujemata' + '\n'
                    else:
                        vmesen_rezultat = vmesen_rezultat[:-2].split(',')
                        stevec = 0
                        for rezultat in vmesen_rezultat:
                            rezultat = rezultat.replace(' ', '')
                            if rezultat == 'seujemata':
                                stevec += 1
                        if stevec == len(vmesen_rezultat):
                            koncen_rezultat += 'se ujemata' + '\n'
                        else:
                            if ' vzorec ni homogen' in vmesen_rezultat:
                                koncen_rezultat += 'vzorec ni homogen' + '\n'
                            else:
                                koncen_rezultat += 'se ne ujemata' + '\n'
        if ':(' in koncen_rezultat:
            self.ujemanje = ':('
        else:
            self.ujemanje = koncen_rezultat[:-1]

#Dobljeno datoteko Dolzine.txt lahko npr. primerjamo z datotekama Dolzine-eksp-N.txt
#in Dolzine-eksp-P.txt
#V datoteki Dolzine-eksp-N.txt v tretji vrstici manjka zadnji rezultat zato
#program vrne obvestilo o napaki.
#V Datoteki Dolzine-eksp-P.txt pa so v prvih dveh vrsticah nekoliko spremenjene
#številke - posledično nekje pride do ujemanja in drugje ne.

            
 
