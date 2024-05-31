#--------------------------------- Get URL --------------------------------#
import pyrebase
import datetime as dt
import smtplib
config = {
    
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
today_date = dt.datetime.now().strftime("%d%m%y")

filepath1 = f"41XNAWHLOM{today_date}.h5";
filepath2 = f"41XNAWHLOM{today_date}.h5";
filepath3 = f"41XNAWHLOM{today_date}.h5";
filepath4 = f"41XNAWHLOM{today_date}.h5";
filepath5 = f"41XNAWHLOM{today_date}.h5";
filepath6 = f"41XNAWHLOM{today_date}.h5";

downloadurl1 = storage.child(filepath1).get_url(None)
downloadurl2= storage.child(filepath2).get_url(None)
downloadurl3= storage.child(filepath3).get_url(None)
downloadurl4 = storage.child(filepath4).get_url(None)
downloadurl5 = storage.child(filepath5).get_url(None)
downloadurl6 = storage.child(filepath6).get_url(None)

print("URL Sudah Didapatkan")


#---------------------------------- Send Email ----------------------------------#
db = firebase.database()

# Mendapatkan data dari Firebase Realtime Database
# Mendapatkan data dari Firebase Realtime Database
data = db.child("Subscriber").get()

# Mendefinisikan array untuk setiap opsi dataselect
emails_BaliStrait = []
emails_BadungStrait = []
emails_LombokStrait = []
emails_AlasStrait = []
emails_Sumbawa = []
emails_SumbawaFloresStrait = []

# Melooping melalui setiap entri data dan menyusunnya ke dalam array yang sesuai
for entry in data.each():
    data_dict = entry.val()
    data_dict["id"] = entry.key()
    email = data_dict.get("email", "")
    dataselect = data_dict.get("dataselect", "")
    
    # Memeriksa nilai dataselect dan menambahkan email ke array yang sesuai
    if dataselect == "Bali Strait":
        emails_BaliStrait.append(email)
    elif dataselect == "Badung Strait":
        emails_BadungStrait.append(email)
    elif dataselect == "Lombok Strait":
        emails_LombokStrait.append(email)
    elif dataselect == "Alas Strait":
        emails_AlasStrait.append(email)
    elif dataselect == "Sumbawa":
        emails_Sumbawa.append(email)
    elif dataselect == "Sumbawa-Flores Strait":
        emails_SumbawaFloresStrait.append(email)



sender = 's100team@nawhproject.com'
email_lists = {
    "Bali Strait": emails_BaliStrait,
    "Badung Strait": emails_BadungStrait,
    "Lombok Strait": emails_LombokStrait,
    "Alas Strait": emails_AlasStrait,
    "Sumbawa": emails_Sumbawa,
    "Sumbawa-Flores Strait": emails_SumbawaFloresStrait
}
messages = {
    "Bali Strait": "",
    "Badung Strait": "",
    "Lombok Strait": downloadurl1,
    "Alas Strait": "",
    "Sumbawa": "",
    "Sumbawa-Flores Strait": ""
}



receivers = emails_LombokStrait

message = f"""\
Subject: [NAWH S100 Project] - Your SWH Data Update
To: {", ".join(receivers)}
From: {sender}


Your data is up to date!

Please be advised that the requested data has been updated in accordance with your request. The SWH prediction data for seven days from today is now available.

URL: {downloadurl1}

Please contact us via WhatsApp or email if you require assistance.

Thank you,


--------------------------
NAWH S100 Project
nawhproject.com
WhatsApp : +6281220095662
Email : s100team@nawhproject.com
"""

with smtplib.SMTP("bulk.smtp.mailtrap.io", 587) as server:
    server.starttls()
    server.login("")
    for receiver in receivers:
        server.sendmail(sender, receiver, message)

print("email sent")
