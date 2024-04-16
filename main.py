import phonenumbers
import folium
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import pytz
from opencage.geocoder import OpenCageGeocode
from phonenumbers import geocoder as phonenumbers_geocoder  # Rename the import to avoid conflict
from phonenumbers import carrier
import webbrowser


def find_info():
    number = str(entry.get())
    pepnum = phonenumbers.parse(number)
    location = phonenumbers_geocoder.description_for_number(pepnum, "en")  # Use the renamed import here
    service_provider = carrier.name_for_number(pepnum, "en")
    # add abi key
    geocoder_key = ""
    geocoder_obj = OpenCageGeocode(geocoder_key)
    re = geocoder_obj.geocode(str(location))

    t = re[1]['annotations']['timezone']['name']
    state = re[1]['components']['state']
    lat = re[0]['geometry']['lat']
    lng = re[0]['geometry']['lng']
    utc_now = datetime.utcnow()
    muscat_tz = pytz.timezone(t)
    muscat_now = utc_now.replace(tzinfo=pytz.utc).astimezone(muscat_tz)

    m = folium.Map(location=[lat, lng], zoom_start=9)
    folium.Marker([lat, lng], popup=location).add_to(m)

    m.save("lo.html")
    s = (f"Current time: {muscat_now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}\ncountry: {location}\nstate: {state}\nservice "
         f"provider: {service_provider}\nLat: {lat}\nLng: {lng}")
    messagebox.showinfo(title="Numbers Info", message=s)
    webbrowser.open("lo.html")


window = Tk()
window.title("Get Num Info")
window.config(padx=50, pady=50)

label = Label(text="Enter number: ")
label.grid(row=0, column=0)

entry = Entry(width=21)
entry.grid(row=0, column=1)
entry.focus()

button = Button(width=42,text="get info", command=find_info)
button.grid(row=1, column=0, columnspan=2)


window.mainloop()
