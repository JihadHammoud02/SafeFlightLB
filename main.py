from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle
from bs4 import BeautifulSoup
import requests
from datetime import date
from time import strftime



class dates:
    act = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
           7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

    def __init__(self, jours, mois, annee):
        self.jours = jours
        self.mois = mois
        self.annee = annee

    def __str__(self):
        d = str(self.annee)+'-'+str(self.mois)+'-'+str(self.jours)
        return d

    def __repr__(self):
        d = str(self.annee)+'-'+str(self.mois)+'-'+str(self.jours)
        return d

    def bissextile(self):
        if self.annee % 4 == 0:
            if self.annee % 100 == 0:
                if self.annee % 400 == 0:
                    return True
            else:
                return True
        else:
            return False

    def incrementer(self, d2):
        d2 = dates(self.jours, self.mois, self.annee)
        if self.mois not in [2, 12]:
            if self.jours < dates.act[self.mois]:
                d2.jours = self.jours+1
            else:
                d2.jours = 1
                d2.mois+self.mois+1
        else:
            if self.mois == 2:
                if self.bissextile() == True:
                    if self.jours < dates.act[2]+1:
                        d2.jours = self.jours+1
                    else:
                        d2.jours = 1
                        d2.mois = 3
                else:
                    if self.jours < dates.act[2]:
                        d2.jours = self.jours+1
                    else:
                        d2.jours = 1
                        d2.mois = 3
            else:
                if self.mois == 12:
                    if self.jours < 31:
                        d2.jours = self.jours+1
                    else:
                        d2.jours = 1
                        d2.mois = 1
                        d2.annee = self.annee+1
        return d2


class Flights:
    def __init__(self, flight_liste):
        self.flight_liste = flight_liste

    def sorting(self):
        date2 = date.today()
        jours = date2.day
        mois = date2.month
        annee = date2.year
        tmr = None
        aftmr = None
        tdy = dates(jours, mois, annee)
        tmr = tdy.incrementer(tmr)
        aftmr = tmr.incrementer(aftmr)
        flights_dict = {}

        if str(tdy) in self.flight_liste:
            trips = []
            flag = True
            i = 0
            while i < len(self.flight_liste) and flag == True:
                if self.flight_liste[i] == str(tmr):
                    flag = False
                else:
                    trips.append(self.flight_liste[i])
                    self.flight_liste.remove(self.flight_liste[i])
            trips.remove(str(tdy))
            flights_dict[str(tdy)] = trips

        if str(tmr) in self.flight_liste:
            trips = []
            flag = True
            i = 0

            while i < len(self.flight_liste) and flag == True:
                if self.flight_liste[i] == str(aftmr):
                    flag = False
                else:
                    trips.append(self.flight_liste[i])
                    self.flight_liste.remove(self.flight_liste[i])
            trips.remove(str(tmr))
            flights_dict[str(tmr)] = trips

        if str(aftmr) in self.flight_liste:
            trips = []
            flag = True
            i = 0

            while i < len(self.flight_liste) and flag == True:
                if self.flight_liste[i] == str(aftmr):
                    flag = False
                else:
                    trips.append(self.flight_liste[i])

            trips.remove(str(aftmr))
            flights_dict[str(aftmr)] = trips
        return flights_dict

    def get_flights(self, n):

        dict = self.sorting()
        flight_num = ''
        rtime = ''
        city = ''
        country = ''
        counter = ''
        status = ''
        datse = ''

        for k in dict:
            x = 0
            while x < len(dict[k]):
                if dict[k][x] == n:
                    datse = k
                    flight_num = dict[k][x]
                    rtime = dict[k][x-1]
                    city = dict[k][x+1]
                    country = dict[k][x+2]
                    counter = dict[k][x+4]
                    status = dict[k][x+5]
                x = x+1
            if counter == '':
                counter = '--'
            if status == '':

                status = '--'

            cds = [flight_num, datse, rtime, city, country, counter, status]
        if city == '':

            raise IndexError

        return cds


class covid:
    def __init__(self, html_covid, cov_ordering):
        self.cl = cov_ordering
        self.co = html_covid

    def get(self):
        op = []
        for i in self.cl:
            op.append(i)
        soup23 = BeautifulSoup(self.co, 'lxml')
        new_case = soup23.find('li', class_='news_li')
        sw = new_case.text.split(' ')
        new_cas = sw[0]
        new_death = sw[4]
        if new_death[0] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
            new_death = '--'
        if new_cas[0] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
            new_cas = '--'
        return {'Tcases': op[0], 'Tdeaths': op[1], 'Tactive': op[2], 'new cases': new_cas, 'new deaths': new_death}

    def country_fixer(country):
        country = country.lower()
        i = 0
        while i < len(country):
            if country[i] == ' ':
                country = country[0:i]+'-'+country[i+1:len(country)]
            i = i+1
        if country == 'united-kingdom':
            country = 'uk' 
        else:
            if country == 'russian-federation':
                country = 'russia'
            else:
                if country == 'uae':
                    country = 'united-arab-emirates'
                else:
                    if country=='irak':
                        country='iraq'
        return country


def show_flights():
    try:
        def clock():
            time_upd = strftime('%H:%M:%S')
            clock_show['text'] = time_upd
            clock_show.after(1000, clock)

        def close():
            mainwindow.destroy()

        def open_covidus():
            cov_ordering = covid_ord(infos)
            c = covid(html_covid, cov_ordering)
            frame_covid = ttk.Frame(frame1, padding=(20, 18))

            def raissing():
                frame2.place_forget()
                frame_covid.place(x=230, y=50)

            def raisee():
                frame_covid.place_forget()
                frame2.place(x=220, y=50)
                covid_button.place(x=640, y=360)
                back_button.place_forget()
            title_name = ttk.Label(frame_covid, text='COVID19 Insights in ' +
                                   str(flight_info[4]), font=("Helvetica", "10", 'bold'))
            title_name.grid(row=1, column=1, columnspan=2, pady=10, padx=10)
            total_cases_txt = ttk.Label(
                frame_covid, text='Total Cases:', font=("Helvetica", "10", 'bold'))
            total_cases_txt.grid(row=2, column=1, pady=10, padx=10)
            total_death_txt = ttk.Label(
                frame_covid, text='Total Deaths:', font=("Helvetica", "10", 'bold'))
            total_death_txt.grid(row=3, column=1, pady=10, padx=10)
            total_recov_txt = ttk.Label(
                frame_covid, text='Total cases Recovered:', font=("Helvetica", "10", 'bold'))
            total_recov_txt.grid(row=4, column=1, pady=10, padx=10)
            total_cases_ans = ttk.Label(
                frame_covid, font=("Helvetica", "10", 'bold'),foreground='red')
            total_cases_ans.grid(row=2, column=2, pady=10, padx=10)
            total_death_ans = ttk.Label(
                frame_covid, font=("Helvetica", "10", 'bold'),foreground='red')
            total_death_ans.grid(row=3, column=2, pady=10, padx=10)
            total_recov_ans = ttk.Label(
                frame_covid, font=("Helvetica", "10", 'bold'),foreground='green')
            total_recov_ans.grid(row=4, column=2, pady=10, padx=10)
            new_cases_txt = ttk.Label(
                frame_covid, text='New Cases:', font=("Helvetica", "10", 'bold'))
            new_cases_txt.grid(row=5, column=1, pady=10, padx=10)
            new_deaths_txt = ttk.Label(
                frame_covid, text='New Deaths:', font=("Helvetica", "10", 'bold'))
            new_deaths_txt.grid(row=6, column=1, pady=10, padx=10)
            new_cases_ans = ttk.Label(
                frame_covid, font=("Helvetica", "10", 'bold'),foreground='red')
            new_cases_ans.grid(row=5, column=2, pady=10, padx=10)
            new_deaths_ans = ttk.Label(
                frame_covid, font=("Helvetica", "10", 'bold'),foreground='red')
            new_deaths_ans.grid(row=6, column=2, pady=10, padx=10)
            empty1 = ttk.Label(frame_covid, font=("Helvetica", "10", 'bold'))
            empty1.grid(row=7, column=1, pady=10, padx=10, columnspan=2)
            back_button = ttk.Button(frame1, text='Back', command=raisee)
            back_button.place(x=640, y=360)
            total_cases_ans['text'] = c.get()['Tcases']
            total_death_ans['text'] = c.get()['Tdeaths']
            total_recov_ans['text'] = c.get()['Tactive']
            new_cases_ans['text'] = c.get()['new cases']
            new_deaths_ans['text'] = c.get()['new deaths']
            covid_button.place_forget()
            raissing()

        flight_liste = flights_ordering(flight_text)
        flighty = Flights(flight_liste)
        flight_info = flighty.get_flights(fd.get())
        second_window = Toplevel(mainwindow)
        second_window.title('SafeFlightLB')
        second_window.resizable(False, False)
        second_window.geometry('750x400')
        second_window.iconbitmap('planeicon.ico')
        frame1 = ttk.Frame(second_window)
        frame1.grid()
        bg2_image = PhotoImage(file='bg10_.png')
        bg2 = ttk.Label(frame1, image=bg2_image)
        bg2.pack(expand=True)
        frame2 = ttk.Frame(frame1, relief=RIDGE, padding=(20, 18))
        frame2.place(x=220, y=50)
        mainwindow.state('iconic')

        flight_number_text = ttk.Label(
            frame2, text='Flight Number:', font=("Helvetica", "10", 'bold'), anchor=W)
        flight_number_text.grid(row=1, column=1, pady=10, padx=10)
        date_text = ttk.Label(frame2, text='Date:', font=(
            "Helvetica", "10", 'bold'), anchor=W)
        date_text.grid(row=2, column=1, pady=10, padx=10)
        time_text = ttk.Label(frame2, text='Departure Time:', font=(
            "Helvetica", "10", 'bold'), anchor=W)
        time_text.grid(row=3, column=1, pady=10, padx=10)
        country_text = ttk.Label(frame2, text='Country:', font=(
            "Helvetica", "10", 'bold'), anchor=W)
        country_text.grid(row=4, column=1, pady=10, padx=10)
        city_text = ttk.Label(frame2, text='City:', font=(
            "Helvetica", "10", 'bold'), anchor=W)
        city_text.grid(row=5, column=1, pady=10, padx=10)
        counter_text = ttk.Label(frame2, text='Counter Number:', font=(
            "Helvetica", "10", 'bold'), anchor=W)
        counter_text.grid(row=6, column=1, pady=10, padx=10)
        status_text = ttk.Label(frame2, text='Current Status:', font=(
            "Helvetica", "10", 'bold'), anchor=W)
        status_text.grid(row=7, column=1, pady=10, padx=10)
        flight_number_ans = ttk.Label(
            frame2, text=flight_info[0], font=("Helvetica", "10", 'bold'))
        flight_number_ans.grid(row=1, column=2, pady=10, padx=10)
        date_ans = ttk.Label(
            frame2, text=flight_info[1], font=("Helvetica", "10", 'bold'))
        date_ans.grid(row=2, column=2, pady=10, padx=10)
        time_ans = ttk.Label(
            frame2, text=flight_info[2], font=("Helvetica", "10", 'bold'),foreground='red')
        time_ans.grid(row=3, column=2, pady=10, padx=10)
        country_ans = ttk.Label(
            frame2, text=flight_info[4], font=("Helvetica", "10", 'bold'))
        country_ans.grid(row=4, column=2, pady=10, padx=10)
        city_ans = ttk.Label(
            frame2, text=flight_info[3], font=("Helvetica", "10", 'bold'))
        city_ans.grid(row=5, column=2, pady=10, padx=10)
        counter_ans = ttk.Label(
            frame2, text=flight_info[5], font=("Helvetica", "10", 'bold'),foreground='red')
        counter_ans.grid(row=6, column=2, pady=10, padx=10)
        status_ans = ttk.Label(
            frame2, text=flight_info[6], font=("Helvetica", "10", 'bold'),foreground='red')
        status_ans.grid(row=7, column=2, pady=10, padx=10)

        covid_button = ttk.Button(
            frame1, text='COVID19 INFO', command=open_covidus)
        covid_button.place(x=640, y=360)
        quit_button = ttk.Button(frame1, text='Quit', command=close)
        quit_button.place(x=50, y=360)

        clock_show = ttk.Label(frame1, text='', font=(
            "Helvetica", "20", 'bold'), background='#bad5f1', foreground='Black')
        clock_show.place(x=600, y=5)
        clock()

        url = 'https://www.worldometers.info/coronavirus/country/' + \
            str(covid.country_fixer((flight_info[4])))+'/'
        html_covid = requests.get(url).text
        soup = BeautifulSoup(html_covid, 'lxml')
        infos = soup.find_all('div', class_='maincounter-number')

        def covid_ord(infos):
            f = []
            for i in infos:
                sr = i.text
                f.append(sr.strip())
            return f
        second_window.mainloop()

    except IndexError:
        def stopp():
            msg['text'] = ''
        msg['text'] = 'Please Insert a Valid Flight Number'
        mainwindow.after(2000, stopp)



mainwindow = Tk()
mainwindow.geometry('600x300')
mainwindow.title('SafeFlightLB')
mainwindow.resizable(False, False)
frame0 = ttk.Frame(mainwindow)
mainwindow.iconbitmap('planeicon.ico')
frame0.pack()
bg_image = PhotoImage(file='bg2.png')
bg = ttk.Label(frame0, image=bg_image)
ms2g = ttk.Label(frame0, text='', foreground='red',
                    background='#effeff', font=("Helvetica", "10", 'bold'))
ms2g.place(x=200, y=140)
bg.pack()
try:
    url = 'http://www.beirutairport.gov.lb/_flight.php?action=&srch=&type=dprtr'
    html_text = requests.get(url, cookies={'BeirutRHIAirport_lang': 'en'}).text
    soup = BeautifulSoup(html_text, 'lxml')
    flight_text = soup.find_all('td')


    def flights_ordering(flight):
        f = []
        for i in flight:
            sr = i.text
            f.append(sr.strip())
        return f


    fd = StringVar()
    flight_number_label = ttk.Label(frame0, text='Enter a Valid Flight Number ',
                                    background='#e9feff', font=("Helvetica", "12", 'bold'))
    flight_number_label.place(x=189, y=140)
    flight_number_enter = ttk.Entry(frame0, width=20, textvariable=fd)
    flight_number_enter.place(x=410, y=137)
    flight_number_search = ttk.Button(frame0, text='Search', command=show_flights)
    flight_number_search.place(x=305, y=210)
    style = ThemedStyle(mainwindow).set_theme('yaru')
    msg = ttk.Label(frame0, text='', foreground='red',
                    background='#effeff', font=("Helvetica", "10", 'bold'))
    msg.place(x=235, y=265)
except:
    ms2g['text']='Make Sure You Are Connected To The Internet'


mainwindow.mainloop()
