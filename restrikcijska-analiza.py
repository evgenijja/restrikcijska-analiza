import os, subprocess, sys
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from model import *

organizem = Organizem()

def razrezi():
    organizem.dna, organizem.encim = vhod1.get(), vhod2.get()
    organizem.doloci_dolzino_rezov()
    izhod1.configure(text='Dobimo: {}!'.format(organizem.razrezan))

def primerjaj_v(): #v za vmesnik
    organizem.dna, organizem.encim = vhod1.get(), vhod2.get()
    organizem.doloci_dolzino_rezov()
    organizem.primerjaj(vhod3.get())
    izhod2.configure(text='Zgoraj dobimo {}, torej {}'.format(organizem.razrezan, organizem.ujemanje))

def razrez_z_vec_encimi_v():
    organizem.dna = vhod4.get()
    encimi = vhod5.get()
    organizem.razrez_z_vec_encimi(encimi)
    izhod3.configure(text='Razrezi po vrsti: {}'.format(organizem.razrezan))

def razrez_z_datotekami_v():
    organizem.dna = vhod6.get()
    encimi_d = vhod7.get()
    try:
        organizem.razrez_z_datotekami(encimi_d)
        if sys.platform == 'win32':
            os.startfile('Dolzine.txt')
        elif sys.platform == 'darwin':
            subprocess.call(['open', 'Dolzine.txt'])
        else:
            subprocess.call(['xdg-open', 'Dolzine.txt'])
    except FileNotFoundError:
        messagebox.showerror(title='Napaka', message='Datoteke ni bilo mogoče najti!')

def vec_primerjav_v():
    organizem.dna = vhod8.get()
    eksperiment_d = vhod9.get()
    try:
        organizem.vec_primerjav(eksperiment_d)
        if organizem.ujemanje == ':(':
            messagebox.showerror(title='Napaka', message='Preveri ali si v datoteke zapisal podatke na pravilen način (za vsako DNA zaporedje v svojo vrsto po vrsti zapiši reze za posamezen encim in jih loči s presledkom), ter preveri, da primerjaš isto število zaporedij z istim številom encimov')
        else:
            izhod5.configure(text='Približno ujemanje po vrsti:\n {}'.format(organizem.ujemanje))
    except FileNotFoundError:
        messagebox.showerror(title='Napaka', message='Datoteke ni bilo mogoče najti!')

okno = tk.Tk()
okno.title('Restrikcijska analiza')

levo = tk.Frame(okno)
desno = tk.Frame(okno)
levo.grid(row=0, column=0)
desno.grid(row=0, column=1)


#levo
naslov1 = tk.Label(levo, text='Restrikcijska analiza enega NDA zaporedja\n z enim encimom', font=('arial', 9, 'bold'))
oznaka1 = tk.Label(levo, text='vpiši dna zaporedje')
oznaka2 = tk.Label(levo, text='vpiši zaporedje pri katerem reže encim\n (mesto reza označi z "/")')
vhod1 = tk.Entry(levo)
vhod2 = tk.Entry(levo)
izhod1 = tk.Label(levo, text='Dobimo:')

naslov1.grid(row=0, column=0)
oznaka1.grid(row=1, column=0)
oznaka2.grid(row=2, column=0)
vhod1.grid(row=1, column=1)
vhod2.grid(row=2, column=1)
izhod1.grid(row=4, column=0)
tk.Button(levo, text='razreži', command=razrezi).grid(row=3, column=0)

oznaka3 = tk.Label(levo, text='vpiši razrez, ki si ga določil eksperimentalno')
vhod3 = tk.Entry(levo)
izhod2 = tk.Label(levo, text='Dobimo:')                     

oznaka3.grid(row=5, column=0)
vhod3.grid(row=5, column=1)
izhod2.grid(row=7, column=0)
tk.Button(levo, text='preveri ujemanje', command=primerjaj_v).grid(row=6, column=0)
presledek1 = tk.Label(levo, text='\n').grid(row=8, column=0)

#levo

naslov2 = tk.Label(levo, text='Restrikcijska analiza enega \nDNA zaporedja z več encimi', font=('arial', 9, 'bold'))
oznaka4 = tk.Label(levo, text='vpiši dna zaporedje')
oznaka5 = tk.Label(levo, text='po vrsti vpiši zaporedja pri katerih režejo\n encimi, loči jih z vejico')
vhod4 = tk.Entry(levo)
vhod5 = tk.Entry(levo)
izhod3 = tk.Label(levo, text='Razrezi po vrsti:')

naslov2.grid(row=9, column=0)
oznaka4.grid(row=10, column=0) 
oznaka5.grid(row=11, column=0)
vhod4.grid(row=10, column=1)
vhod5.grid(row=11, column=1)
izhod3.grid(row=13, column=0)
tk.Button(levo, text='razreži', command=razrez_z_vec_encimi_v).grid(row=12, column=0)
presledek2 = tk.Label(levo, text=' \n ').grid(row=14, column=0)

#desno

naslov3 = tk.Label(desno, text='Restrikcijska analiza več DNA zaporedij\n z več encimi s pomočjo datotek', font=('arial', 9, 'bold')) 
oznaka6 = tk.Label(desno, text='vpiši ime datoteke z dna zaporedji\n (primer: dna.txt)')
oznaka7 = tk.Label(desno, text='vpiši ime datoteke z zaporedji za encime')
vhod6 = tk.Entry(desno)
vhod7 = tk.Entry(desno)

naslov3.grid(row=0, column=0)
oznaka6.grid(row=1, column=0)
oznaka7.grid(row=2, column=0)
vhod6.grid(row=1, column=1)
vhod7.grid(row=2, column=1)
tk.Button(desno, text='razreži vse', command=razrez_z_datotekami_v).grid(row=3, column=0)

oznaka8 = tk.Label(desno, text='vpiši ime datoteke s pričakovanimi rezultati')
oznaka9 = tk.Label(desno, text='vpiši ime datoteke z rezultati,\n določenimi eksperimentalno')
vhod8 = tk.Entry(desno)
vhod9 = tk.Entry(desno)
izhod5 = tk.Label(desno, text='Približno ujemanje po vrsti:')

oznaka8.grid(row=5, column=0)
oznaka9.grid(row=6, column=0)
vhod9.grid(row=6, column=1)
vhod8.grid(row=5, column=1)
izhod5.grid(row=8, column=0)
tk.Button(desno, text='primerjaj vse', command=vec_primerjav_v).grid(row=7, column=0)

okno.mainloop()
