#!/usr/bin/python
from BeautifulSoup import BeautifulSoup
import sys
import re
import urllib
import gtk
import hildon

class Wmata:
	def __init__(self):
		print "new wmata object is created"

	def stationstat(self, id):
		baseurl="http://www.wmata.com/rider_tools/pids/showpid.cfm?station_id="  
		url = baseurl + str(id)
		#s = sys.stdin.read()
		i=0
		j=0
		station = []

		f=urllib.urlopen(url)
		s=f.read()

		soup = BeautifulSoup(s)

		p = re.compile('\d+')
		h = soup.find("h2")
		stationname = h.contents[0]

		for table in soup.findAll("table"):
			for tr in table.findAll("tr"):	
				if len(tr.contents[1].contents) > 1:
					color = tr.contents[1].contents[1]['alt']
					car = tr.contents[3].contents[0]
					destination = tr.contents[5].contents[0]
					minutes = tr.contents[7].contents
					if len(minutes) > 1 : 
						minutes = tr.contents[7].contents[1].contents[0].contents[0]
					else:
						# clear the digits from \t and \n
						minutes = p.findall(minutes[0])
						minutes = minutes[0]
					station = [color, car, destination, minutes, stationname]
#					return station
					print color + " train with destination to " + destination + " will be here in " + minutes + " minute(s)"



	def stations(self, cache):	
		stations = {}
		if cache == 0:
			url="http://www.wmata.com/rail/stations.cfm"
			#s = sys.stdin.read()
			i=0
			j=0
			
			f=urllib.urlopen(url)
			s=f.read()
			
			soup = BeautifulSoup(s)
			t = soup.find("table", { "class" : "tabular"})
			for row in t.findAll("tr", { "class" : "even"}): 
				for gecici in row.findAll("a"):
					p = re.compile('\d+')
					id = p.findall(gecici["href"])
					stationid = id[0]
					stationname = gecici.next
					station = stationid, stationname
					stations[stationname] = stationid
	
		else:
			f = open('.stations', 'r')
			line = "empty"
			while line:
				line = f.readline()
				line = line.strip()
				station = line.split('|')
				if line:
					stations[station[1]] = station[0]
			
			f.close()
	

		return stations
	

#w = Wmata()
#queriedStation = w.stationstat(43)
#stations = w.stations(1)

#print queriedStation



def app_quit(widget, data=None):
	    gtk.main_quit()

def on_picker_value_changed(button, user_data=None):
    stationname = button.get_value()
    so = Wmata()
    stationlist = so.stations(1)
    stationid = stationlist[stationname]
    so.stationstat(stationid)

def main ():
    w = Wmata()
    stations = w.stations(1).keys()
    stations.sort()

    program = hildon.Program.get_instance()
    gtk.set_application_name("wmata station picker")

    window = hildon.StackableWindow()
    program.add_window(window)

    # Create a picker button
    picker_button = hildon.PickerButton(gtk.HILDON_SIZE_AUTO,
		                                            hildon.BUTTON_ARRANGEMENT_VERTICAL)

    # Set a title to the button 
    picker_button.set_title("Pick a station")

    # Create a touch selector entry
    selector = hildon.TouchSelectorEntry(text=True)
       
    # Populate the selector
    for station in stations:
	            selector.append_text(station)

    # Attach the touch selector to the picker button
    picker_button.set_selector(selector)

    # Attach callback to the "value-changed" signal
    picker_button.connect("value-changed", on_picker_value_changed)

    # Add button to main window
    window.add(picker_button)

    window.connect("destroy", app_quit)
    window.show_all()
    gtk.main()

if __name__ == "__main__":
	    main()

#print stations.keys()
