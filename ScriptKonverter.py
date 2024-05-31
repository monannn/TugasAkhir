import openmeteo_requests
import requests_cache
import pandas as pd
import datetime as dt
from retry_requests import retry
from datetime import datetime, timedelta
import h5py
import os
import numpy as np
import pyrebase

#----------------------------Connect Firebase----------------------------#
config = {
    
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
today_date = dt.datetime.now().strftime("%d%m%y")

#----------------------------------Get Data Script--------------------------------------#

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://marine-api.open-meteo.com/v1/marine"

# Define latitude and longitude pairs
locations = [
    {"latitude": -8, "longitude": 115},
    {"latitude": -8, "longitude": 115.25},
    {"latitude": -8, "longitude": 115.5},
    {"latitude": -8, "longitude": 115.75},
    {"latitude": -8, "longitude": 116},
    {"latitude": -8, "longitude": 116.25},
    {"latitude": -8, "longitude": 116.5},
    {"latitude": -8.25, "longitude": 115},
    {"latitude": -8.25, "longitude": 115.25},
    {"latitude": -8.25, "longitude": 115.5},
    {"latitude": -8.25, "longitude": 115.75},
    {"latitude": -8.25, "longitude": 116},
    {"latitude": -8.25, "longitude": 116.25},
    {"latitude": -8.25, "longitude": 116.5},
    {"latitude": -8.5, "longitude": 115},
    {"latitude": -8.5, "longitude": 115.25},
    {"latitude": -8.5, "longitude": 115.5},
    {"latitude": -8.5, "longitude": 115.75},
    {"latitude": -8.5, "longitude": 116},
    {"latitude": -8.5, "longitude": 116.25},
    {"latitude": -8.5, "longitude": 116.5},
    {"latitude": -8.75, "longitude": 115},
    {"latitude": -8.75, "longitude": 115.25},
    {"latitude": -8.75, "longitude": 115.5},
    {"latitude": -8.75, "longitude": 115.75},
    {"latitude": -8.75, "longitude": 116},
    {"latitude": -8.75, "longitude": 116.25},
    {"latitude": -8.75, "longitude": 116.5},
    {"latitude": -9, "longitude": 115},
    {"latitude": -9, "longitude": 115.25},
    {"latitude": -9, "longitude": 115.5},
    {"latitude": -9, "longitude": 115.75},
    {"latitude": -9, "longitude": 116},
    {"latitude": -9, "longitude": 116.25},
    {"latitude": -9, "longitude": 116.5},
    
    # Add more locations here
]

# Initialize list to store results for all locations
all_results = []

for location in locations:
    params = {
        "latitude": [location["latitude"]],
        "longitude": [location["longitude"]],
        "current": "wave_height",
        "hourly": "wave_height",
        "forecast_days": 7
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_wave_height = hourly.Variables(0).ValuesAsNumpy()

    # Create DataFrame for hourly data
    hourly_data = {
        "Time": pd.to_datetime(hourly.Time(), unit="s", utc=True),
        "wave_height": hourly_wave_height
    }

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    # Now let's divide the wave heights into intervals of 6 hours each
    interval_length = 6  # 6 hours
    num_intervals = len(hourly_dataframe) // interval_length

    # Calculate the average wave height for each interval
    average_wave_heights = []
    start_timestamps = []
    end_timestamps = []

    # Mendapatkan tanggal saat ini
    current_date = datetime.now().date()

    # Membuat objek datetime dengan waktu 00:00
    start_date = datetime.combine(current_date, datetime.min.time())

    for i in range(num_intervals):
        start_idx = i * interval_length
        end_idx = min((i + 1) * interval_length, len(hourly_dataframe))  # Ensure not to exceed the length of the dataframe
        interval_wave_heights = hourly_dataframe["wave_height"][start_idx:end_idx]
        average_wave_height = interval_wave_heights.mean()
        average_wave_heights.append(average_wave_height)

        # Calculate start and end timestamps
        start_time = start_date + timedelta(hours=i*interval_length)
        end_time = start_date + timedelta(hours=(i+1)*interval_length)
        start_timestamps.append(start_time)
        end_timestamps.append(end_time)

    # Create dataset dictionary for this location
    location_dataset = {
        'dateTimeStart': start_timestamps,
        'dateTimeEnd': end_timestamps,
        'Wave Height': average_wave_heights,
    }

    # Append the results for this location to all_results list
    all_results.append((location["latitude"], location["longitude"], pd.DataFrame(location_dataset)))

# Save each result separately
for i, result in enumerate(all_results):
    latitude, longitude, df = result
    # Mengubah format timestamp menjadi ddmmyyyy
    df['dateTimeStart'] = df['dateTimeStart'].dt.strftime('%d%m%Y %H:%M:%S')
    df['dateTimeEnd'] = df['dateTimeEnd'].dt.strftime('%d%m%Y %H:%M:%S')
    df.to_csv(f"D:\WEB Capstone\S100Converter\separated35_{i+1}.csv", index=False)

print("Wave Data Telah Didapatkan")

#----------------------------------CSVRaster Script-------------------------------------#
# Reading CSV
df1 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_1.csv")
df2 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_2.csv")
df3 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_3.csv")
df4 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_4.csv")
df5 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_5.csv")
df6 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_6.csv")
df7 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_7.csv")
df8 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_8.csv")
df9 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_9.csv")
df10 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_10.csv")
df11 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_11.csv")
df12 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_12.csv")
df13 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_13.csv")
df14 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_14.csv")
df15 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_15.csv")
df16 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_16.csv")
df17 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_17.csv")
df18 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_18.csv")
df19 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_19.csv")
df20 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_20.csv")
df21 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_21.csv")
df22 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_22.csv")
df23 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_23.csv")
df24 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_24.csv")
df25 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_25.csv")
df26 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_26.csv")
df27 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_27.csv")
df28 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_28.csv")
df29 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_29.csv")
df30 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_30.csv")
df31 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_31.csv")
df32 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_32.csv")
df33 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_33.csv")
df34 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_34.csv")
df35 = pd.read_csv("D:/WEB Capstone/S100Converter/separated35_35.csv")

# Ambil nilai yang diperlukan
whc = 0
poh = 0
# [Raster][Timestep]
# Timestep 1
ts1 = df1.iloc[0,0]
te1 = df1.iloc[0,1]
#waveHeight
r11 = df1.iloc[0,2]
r21 = df2.iloc[0,2]
r31 = df3.iloc[0,2]
r41 = df4.iloc[0,2]
r51 = df5.iloc[0,2]
r61 = df6.iloc[0,2]
r71 = df7.iloc[0,2]
r81 = df8.iloc[0,2]
r91 = df9.iloc[0,2]
r101 = df10.iloc[0,2]
r111 = df11.iloc[0,2]
r121 = df12.iloc[0,2]
r131 = df13.iloc[0,2]
r141 = df14.iloc[0,2]
r151 = df15.iloc[0,2]
r161 = df16.iloc[0,2]
r171 = df17.iloc[0,2]
r181 = df18.iloc[0,2]
r191 = df19.iloc[0,2]
r201 = df20.iloc[0,2]
r211 = df21.iloc[0,2]
r221 = df22.iloc[0,2]
r231 = df23.iloc[0,2]
r241 = df24.iloc[0,2]
r251 = df25.iloc[0,2]
r261 = df26.iloc[0,2]
r271 = df27.iloc[0,2]
r281 = df28.iloc[0,2]
r291 = df29.iloc[0,2]
r301 = df30.iloc[0,2]
r311 = df31.iloc[0,2]
r321 = df32.iloc[0,2]
r331 = df33.iloc[0,2]
r341 = df34.iloc[0,2]
r351 = df35.iloc[0,2]

# Timestep 2
ts2 = df1.iloc[1,0]
te2 = df1.iloc[1,1]
#waveHeight
r12 = df1.iloc[1,2]
r22 = df2.iloc[1,2]
r32 = df3.iloc[1,2]
r42 = df4.iloc[1,2]
r52 = df5.iloc[1,2]
r62 = df6.iloc[1,2]
r72 = df7.iloc[1,2]
r82 = df8.iloc[1,2]
r92 = df9.iloc[1,2]
r102 = df10.iloc[1,2]
r112 = df11.iloc[1,2]
r122 = df12.iloc[1,2]
r132 = df13.iloc[1,2]
r142 = df14.iloc[1,2]
r152 = df15.iloc[1,2]
r162 = df16.iloc[1,2]
r172 = df17.iloc[1,2]
r182 = df18.iloc[1,2]
r192 = df19.iloc[1,2]
r202 = df20.iloc[1,2]
r212 = df21.iloc[1,2]
r222 = df22.iloc[1,2]
r232 = df23.iloc[1,2]
r242 = df24.iloc[1,2]
r252 = df25.iloc[1,2]
r262 = df26.iloc[1,2]
r272 = df27.iloc[1,2]
r282 = df28.iloc[1,2]
r292 = df29.iloc[1,2]
r302 = df30.iloc[1,2]
r312 = df31.iloc[1,2]
r322 = df32.iloc[1,2]
r332 = df33.iloc[1,2]
r342 = df34.iloc[1,2]
r352 = df35.iloc[1,2]

# Timestep 3
ts3 = df1.iloc[2,0]
te3 = df1.iloc[2,1]
#waveHeight
r13 = df1.iloc[2,2]
r23 = df2.iloc[2,2]
r33 = df3.iloc[2,2]
r43 = df4.iloc[2,2]
r53 = df5.iloc[2,2]
r63 = df6.iloc[2,2]
r73 = df7.iloc[2,2]
r83 = df8.iloc[2,2]
r93 = df9.iloc[2,2]
r103 = df10.iloc[2,2]
r113 = df11.iloc[2,2]
r123 = df12.iloc[2,2]
r133 = df13.iloc[2,2]
r143 = df14.iloc[2,2]
r153 = df15.iloc[2,2]
r163 = df16.iloc[2,2]
r173 = df17.iloc[2,2]
r183 = df18.iloc[2,2]
r193 = df19.iloc[2,2]
r203 = df20.iloc[2,2]
r213 = df21.iloc[2,2]
r223 = df22.iloc[2,2]
r233 = df23.iloc[2,2]
r243 = df24.iloc[2,2]
r253 = df25.iloc[2,2]
r263 = df26.iloc[2,2]
r273 = df27.iloc[2,2]
r283 = df28.iloc[2,2]
r293 = df29.iloc[2,2]
r303 = df30.iloc[2,2]
r313 = df31.iloc[2,2]
r323 = df32.iloc[2,2]
r333 = df33.iloc[2,2]
r343 = df34.iloc[2,2]
r353 = df35.iloc[2,2]

# Timestep 4
ts4 = df1.iloc[3,0]
te4 = df1.iloc[3,1]
#waveHeight
r14 = df1.iloc[3,2]
r24 = df2.iloc[3,2]
r34 = df3.iloc[3,2]
r44 = df4.iloc[3,2]
r54 = df5.iloc[3,2]
r64 = df6.iloc[3,2]
r74 = df7.iloc[3,2]
r84 = df8.iloc[3,2]
r94 = df9.iloc[3,2]
r104 = df10.iloc[3,2]
r114 = df11.iloc[3,2]
r124 = df12.iloc[3,2]
r134 = df13.iloc[3,2]
r144 = df14.iloc[3,2]
r154 = df15.iloc[3,2]
r164 = df16.iloc[3,2]
r174 = df17.iloc[3,2]
r184 = df18.iloc[3,2]
r194 = df19.iloc[3,2]
r204 = df20.iloc[3,2]
r214 = df21.iloc[3,2]
r224 = df22.iloc[3,2]
r234 = df23.iloc[3,2]
r244 = df24.iloc[3,2]
r254 = df25.iloc[3,2]
r264 = df26.iloc[3,2]
r274 = df27.iloc[3,2]
r284 = df28.iloc[3,2]
r294 = df29.iloc[3,2]
r304 = df30.iloc[3,2]
r314 = df31.iloc[3,2]
r324 = df32.iloc[3,2]
r334 = df33.iloc[3,2]
r344 = df34.iloc[3,2]
r354 = df35.iloc[3,2]

# Timestep 5
ts5 = df1.iloc[4,0]
te5 = df1.iloc[4,1]
#waveHeight
r15 = df1.iloc[4,2]
r25 = df2.iloc[4,2]
r35 = df3.iloc[4,2]
r45 = df4.iloc[4,2]
r55 = df5.iloc[4,2]
r65 = df6.iloc[4,2]
r75 = df7.iloc[4,2]
r85 = df8.iloc[4,2]
r95 = df9.iloc[4,2]
r105 = df10.iloc[4,2]
r115 = df11.iloc[4,2]
r125 = df12.iloc[4,2]
r135 = df13.iloc[4,2]
r145 = df14.iloc[4,2]
r155 = df15.iloc[4,2]
r165 = df16.iloc[4,2]
r175 = df17.iloc[4,2]
r185 = df18.iloc[4,2]
r195 = df19.iloc[4,2]
r205 = df20.iloc[4,2]
r215 = df21.iloc[4,2]
r225 = df22.iloc[4,2]
r235 = df23.iloc[4,2]
r245 = df24.iloc[4,2]
r255 = df25.iloc[4,2]
r265 = df26.iloc[4,2]
r275 = df27.iloc[4,2]
r285 = df28.iloc[4,2]
r295 = df29.iloc[4,2]
r305 = df30.iloc[4,2]
r315 = df31.iloc[4,2]
r325 = df32.iloc[4,2]
r335 = df33.iloc[4,2]
r345 = df34.iloc[4,2]
r355 = df35.iloc[4,2]

# Timestep 6
ts6 = df1.iloc[5,0]
te6 = df1.iloc[5,1]
#waveHeight
r16 = df1.iloc[5,2]
r26 = df2.iloc[5,2]
r36 = df3.iloc[5,2]
r46 = df4.iloc[5,2]
r56 = df5.iloc[5,2]
r66 = df6.iloc[5,2]
r76 = df7.iloc[5,2]
r86 = df8.iloc[5,2]
r96 = df9.iloc[5,2]
r106 = df10.iloc[5,2]
r116 = df11.iloc[5,2]
r126 = df12.iloc[5,2]
r136 = df13.iloc[5,2]
r146 = df14.iloc[5,2]
r156 = df15.iloc[5,2]
r166 = df16.iloc[5,2]
r176 = df17.iloc[5,2]
r186 = df18.iloc[5,2]
r196 = df19.iloc[5,2]
r206 = df20.iloc[5,2]
r216 = df21.iloc[5,2]
r226 = df22.iloc[5,2]
r236 = df23.iloc[5,2]
r246 = df24.iloc[5,2]
r256 = df25.iloc[5,2]
r266 = df26.iloc[5,2]
r276 = df27.iloc[5,2]
r286 = df28.iloc[5,2]
r296 = df29.iloc[5,2]
r306 = df30.iloc[5,2]
r316 = df31.iloc[5,2]
r326 = df32.iloc[5,2]
r336 = df33.iloc[5,2]
r346 = df34.iloc[5,2]
r356 = df35.iloc[5,2]

# Timestep 7
ts7 = df1.iloc[6,0]
te7 = df1.iloc[6,1]
#waveHeight
r17 = df1.iloc[6,2]
r27 = df2.iloc[6,2]
r37 = df3.iloc[6,2]
r47 = df4.iloc[6,2]
r57 = df5.iloc[6,2]
r67 = df6.iloc[6,2]
r77 = df7.iloc[6,2]
r87 = df8.iloc[6,2]
r97 = df9.iloc[6,2]
r107 = df10.iloc[6,2]
r117 = df11.iloc[6,2]
r127 = df12.iloc[6,2]
r137 = df13.iloc[6,2]
r147 = df14.iloc[6,2]
r157 = df15.iloc[6,2]
r167 = df16.iloc[6,2]
r177 = df17.iloc[6,2]
r187 = df18.iloc[6,2]
r197 = df19.iloc[6,2]
r207 = df20.iloc[6,2]
r217 = df21.iloc[6,2]
r227 = df22.iloc[6,2]
r237 = df23.iloc[6,2]
r247 = df24.iloc[6,2]
r257 = df25.iloc[6,2]
r267 = df26.iloc[6,2]
r277 = df27.iloc[6,2]
r287 = df28.iloc[6,2]
r297 = df29.iloc[6,2]
r307 = df30.iloc[6,2]
r317 = df31.iloc[6,2]
r327 = df32.iloc[6,2]
r337 = df33.iloc[6,2]
r347 = df34.iloc[6,2]
r357 = df35.iloc[6,2]

# Timestep 8
ts8 = df1.iloc[7,0]
te8 = df1.iloc[7,1]
#waveHeight
r18 = df1.iloc[7,2]
r28 = df2.iloc[7,2]
r38 = df3.iloc[7,2]
r48 = df4.iloc[7,2]
r58 = df5.iloc[7,2]
r68 = df6.iloc[7,2]
r78 = df7.iloc[7,2]
r88 = df8.iloc[7,2]
r98 = df9.iloc[7,2]
r108 = df10.iloc[7,2]
r118 = df11.iloc[7,2]
r128 = df12.iloc[7,2]
r138 = df13.iloc[7,2]
r148 = df14.iloc[7,2]
r158 = df15.iloc[7,2]
r168 = df16.iloc[7,2]
r178 = df17.iloc[7,2]
r188 = df18.iloc[7,2]
r198 = df19.iloc[7,2]
r208 = df20.iloc[7,2]
r218 = df21.iloc[7,2]
r228 = df22.iloc[7,2]
r238 = df23.iloc[7,2]
r248 = df24.iloc[7,2]
r258 = df25.iloc[7,2]
r268 = df26.iloc[7,2]
r278 = df27.iloc[7,2]
r288 = df28.iloc[7,2]
r298 = df29.iloc[7,2]
r308 = df30.iloc[7,2]
r318 = df31.iloc[7,2]
r328 = df32.iloc[7,2]
r338 = df33.iloc[7,2]
r348 = df34.iloc[7,2]
r358 = df35.iloc[7,2]

# Timestep 9
ts9 = df1.iloc[8,0]
te9 = df1.iloc[8,1]
#waveHeight
r19 = df1.iloc[8,2]
r29 = df2.iloc[8,2]
r39 = df3.iloc[8,2]
r49 = df4.iloc[8,2]
r59 = df5.iloc[8,2]
r69 = df6.iloc[8,2]
r79 = df7.iloc[8,2]
r89 = df8.iloc[8,2]
r99 = df9.iloc[8,2]
r109 = df10.iloc[8,2]
r119 = df11.iloc[8,2]
r129 = df12.iloc[8,2]
r139 = df13.iloc[8,2]
r149 = df14.iloc[8,2]
r159 = df15.iloc[8,2]
r169 = df16.iloc[8,2]
r179 = df17.iloc[8,2]
r189 = df18.iloc[8,2]
r199 = df19.iloc[8,2]
r209 = df20.iloc[8,2]
r219 = df21.iloc[8,2]
r229 = df22.iloc[8,2]
r239 = df23.iloc[8,2]
r249 = df24.iloc[8,2]
r259 = df25.iloc[8,2]
r269 = df26.iloc[8,2]
r279 = df27.iloc[8,2]
r289 = df28.iloc[8,2]
r299 = df29.iloc[8,2]
r309 = df30.iloc[8,2]
r319 = df31.iloc[8,2]
r329 = df32.iloc[8,2]
r339 = df33.iloc[8,2]
r349 = df34.iloc[8,2]
r359 = df35.iloc[8,2]

# Timestep 10
ts10 = df1.iloc[9,0]
te10 = df1.iloc[9,1]
#waveHeight
r110 = df1.iloc[9,2]
r210 = df2.iloc[9,2]
r310 = df3.iloc[9,2]
r410 = df4.iloc[9,2]
r510 = df5.iloc[9,2]
r610 = df6.iloc[9,2]
r710 = df7.iloc[9,2]
r810 = df8.iloc[9,2]
r910 = df9.iloc[9,2]
r1010 = df10.iloc[9,2]
r1110 = df11.iloc[9,2]
r1210 = df12.iloc[9,2]
r1310 = df13.iloc[9,2]
r1410 = df14.iloc[9,2]
r1510 = df15.iloc[9,2]
r1610 = df16.iloc[9,2]
r1710 = df17.iloc[9,2]
r1810 = df18.iloc[9,2]
r1910 = df19.iloc[9,2]
r2010 = df20.iloc[9,2]
r2110 = df21.iloc[9,2]
r2210 = df22.iloc[9,2]
r2310 = df23.iloc[9,2]
r2410 = df24.iloc[9,2]
r2510 = df25.iloc[9,2]
r2610 = df26.iloc[9,2]
r2710 = df27.iloc[9,2]
r2810 = df28.iloc[9,2]
r2910 = df29.iloc[9,2]
r3010 = df30.iloc[9,2]
r3110 = df31.iloc[9,2]
r3210 = df32.iloc[9,2]
r3310 = df33.iloc[9,2]
r3410 = df34.iloc[9,2]
r3510 = df35.iloc[9,2]

# Timestep 11
ts11 = df1.iloc[10,0]
te11 = df1.iloc[10,1]
#waveHeight
r111 = df1.iloc[10,2]
r211 = df2.iloc[10,2]
r311 = df3.iloc[10,2]
r411 = df4.iloc[10,2]
r511 = df5.iloc[10,2]
r611 = df6.iloc[10,2]
r711 = df7.iloc[10,2]
r811 = df8.iloc[10,2]
r911 = df9.iloc[10,2]
r1011 = df10.iloc[10,2]
r1111 = df11.iloc[10,2]
r1211 = df12.iloc[10,2]
r1311 = df13.iloc[10,2]
r1411 = df14.iloc[10,2]
r1511 = df15.iloc[10,2]
r1611 = df16.iloc[10,2]
r1711 = df17.iloc[10,2]
r1811 = df18.iloc[10,2]
r1911 = df19.iloc[10,2]
r2011 = df20.iloc[10,2]
r2111 = df21.iloc[10,2]
r2211 = df22.iloc[10,2]
r2311 = df23.iloc[10,2]
r2411 = df24.iloc[10,2]
r2511 = df25.iloc[10,2]
r2611 = df26.iloc[10,2]
r2711 = df27.iloc[10,2]
r2811 = df28.iloc[10,2]
r2911 = df29.iloc[10,2]
r3011 = df30.iloc[10,2]
r3111 = df31.iloc[10,2]
r3211 = df32.iloc[10,2]
r3311 = df33.iloc[10,2]
r3411 = df34.iloc[10,2]
r3511 = df35.iloc[10,2]

# Timestep 12
ts12 = df1.iloc[11,0]
te12 = df1.iloc[11,1]
#waveHeight
r112 = df1.iloc[11,2]
r212 = df2.iloc[11,2]
r312 = df3.iloc[11,2]
r412 = df4.iloc[11,2]
r512 = df5.iloc[11,2]
r612 = df6.iloc[11,2]
r712 = df7.iloc[11,2]
r812 = df8.iloc[11,2]
r912 = df9.iloc[11,2]
r1012 = df10.iloc[11,2]
r1112 = df11.iloc[11,2]
r1212 = df12.iloc[11,2]
r1312 = df13.iloc[11,2]
r1412 = df14.iloc[11,2]
r1512 = df15.iloc[11,2]
r1612 = df16.iloc[11,2]
r1712 = df17.iloc[11,2]
r1812 = df18.iloc[11,2]
r1912 = df19.iloc[11,2]
r2012 = df20.iloc[11,2]
r2112 = df21.iloc[11,2]
r2212 = df22.iloc[11,2]
r2312 = df23.iloc[11,2]
r2412 = df24.iloc[11,2]
r2512 = df25.iloc[11,2]
r2612 = df26.iloc[11,2]
r2712 = df27.iloc[11,2]
r2812 = df28.iloc[11,2]
r2912 = df29.iloc[11,2]
r3012 = df30.iloc[11,2]
r3112 = df31.iloc[11,2]
r3212 = df32.iloc[11,2]
r3312 = df33.iloc[11,2]
r3412 = df34.iloc[11,2]
r3512 = df35.iloc[11,2]

# Timestep 13
ts13 = df1.iloc[12,0]
te13 = df1.iloc[12,1]
#waveHeight
r113 = df1.iloc[12,2]
r213 = df2.iloc[12,2]
r313 = df3.iloc[12,2]
r413 = df4.iloc[12,2]
r513 = df5.iloc[12,2]
r613 = df6.iloc[12,2]
r713 = df7.iloc[12,2]
r813 = df8.iloc[12,2]
r913 = df9.iloc[12,2]
r1013 = df10.iloc[12,2]
r1113 = df11.iloc[12,2]
r1213 = df12.iloc[12,2]
r1313 = df13.iloc[12,2]
r1413 = df14.iloc[12,2]
r1513 = df15.iloc[12,2]
r1613 = df16.iloc[12,2]
r1713 = df17.iloc[12,2]
r1813 = df18.iloc[12,2]
r1913 = df19.iloc[12,2]
r2013 = df20.iloc[12,2]
r2113 = df21.iloc[12,2]
r2213 = df22.iloc[12,2]
r2313 = df23.iloc[12,2]
r2413 = df24.iloc[12,2]
r2513 = df25.iloc[12,2]
r2613 = df26.iloc[12,2]
r2713 = df27.iloc[12,2]
r2813 = df28.iloc[12,2]
r2913 = df29.iloc[12,2]
r3013 = df30.iloc[12,2]
r3113 = df31.iloc[12,2]
r3213 = df32.iloc[12,2]
r3313 = df33.iloc[12,2]
r3413 = df34.iloc[12,2]
r3513 = df35.iloc[12,2]

# Timestep 14
ts14 = df1.iloc[13,0]
te14 = df1.iloc[13,1]
#waveHeight
r114 = df1.iloc[13,2]
r214 = df2.iloc[13,2]
r314 = df3.iloc[13,2]
r414 = df4.iloc[13,2]
r514 = df5.iloc[13,2]
r614 = df6.iloc[13,2]
r714 = df7.iloc[13,2]
r814 = df8.iloc[13,2]
r914 = df9.iloc[13,2]
r1014 = df10.iloc[13,2]
r1114 = df11.iloc[13,2]
r1214 = df12.iloc[13,2]
r1314 = df13.iloc[13,2]
r1414 = df14.iloc[13,2]
r1514 = df15.iloc[13,2]
r1614 = df16.iloc[13,2]
r1714 = df17.iloc[13,2]
r1814 = df18.iloc[13,2]
r1914 = df19.iloc[13,2]
r2014 = df20.iloc[13,2]
r2114 = df21.iloc[13,2]
r2214 = df22.iloc[13,2]
r2314 = df23.iloc[13,2]
r2414 = df24.iloc[13,2]
r2514 = df25.iloc[13,2]
r2614 = df26.iloc[13,2]
r2714 = df27.iloc[13,2]
r2814 = df28.iloc[13,2]
r2914 = df29.iloc[13,2]
r3014 = df30.iloc[13,2]
r3114 = df31.iloc[13,2]
r3214 = df32.iloc[13,2]
r3314 = df33.iloc[13,2]
r3414 = df34.iloc[13,2]
r3514 = df35.iloc[13,2]

# Timestep 15
ts15 = df1.iloc[14,0]
te15 = df1.iloc[14,1]
#waveHeight
r115 = df1.iloc[14,2]
r215 = df2.iloc[14,2]
r315 = df3.iloc[14,2]
r415 = df4.iloc[14,2]
r515 = df5.iloc[14,2]
r615 = df6.iloc[14,2]
r715 = df7.iloc[14,2]
r815 = df8.iloc[14,2]
r915 = df9.iloc[14,2]
r1015 = df10.iloc[14,2]
r1115 = df11.iloc[14,2]
r1215 = df12.iloc[14,2]
r1315 = df13.iloc[14,2]
r1415 = df14.iloc[14,2]
r1515 = df15.iloc[14,2]
r1615 = df16.iloc[14,2]
r1715 = df17.iloc[14,2]
r1815 = df18.iloc[14,2]
r1915 = df19.iloc[14,2]
r2015 = df20.iloc[14,2]
r2115 = df21.iloc[14,2]
r2215 = df22.iloc[14,2]
r2315 = df23.iloc[14,2]
r2415 = df24.iloc[14,2]
r2515 = df25.iloc[14,2]
r2615 = df26.iloc[14,2]
r2715 = df27.iloc[14,2]
r2815 = df28.iloc[14,2]
r2915 = df29.iloc[14,2]
r3015 = df30.iloc[14,2]
r3115 = df31.iloc[14,2]
r3215 = df32.iloc[14,2]
r3315 = df33.iloc[14,2]
r3415 = df34.iloc[14,2]
r3515 = df35.iloc[14,2]

# Timestep 16
ts16 = df1.iloc[15,0]
te16 = df1.iloc[15,1]
#waveHeight
r116 = df1.iloc[15,2]
r216 = df2.iloc[15,2]
r316 = df3.iloc[15,2]
r416 = df4.iloc[15,2]
r516 = df5.iloc[15,2]
r616 = df6.iloc[15,2]
r716 = df7.iloc[15,2]
r816 = df8.iloc[15,2]
r916 = df9.iloc[15,2]
r1016 = df10.iloc[15,2]
r1116 = df11.iloc[15,2]
r1216 = df12.iloc[15,2]
r1316 = df13.iloc[15,2]
r1416 = df14.iloc[15,2]
r1516 = df15.iloc[15,2]
r1616 = df16.iloc[15,2]
r1716 = df17.iloc[15,2]
r1816 = df18.iloc[15,2]
r1916 = df19.iloc[15,2]
r2016 = df20.iloc[15,2]
r2116 = df21.iloc[15,2]
r2216 = df22.iloc[15,2]
r2316 = df23.iloc[15,2]
r2416 = df24.iloc[15,2]
r2516 = df25.iloc[15,2]
r2616 = df26.iloc[15,2]
r2716 = df27.iloc[15,2]
r2816 = df28.iloc[15,2]
r2916 = df29.iloc[15,2]
r3016 = df30.iloc[15,2]
r3116 = df31.iloc[15,2]
r3216 = df32.iloc[15,2]
r3316 = df33.iloc[15,2]
r3416 = df34.iloc[15,2]
r3516 = df35.iloc[15,2]

# Timestep 17
ts17 = df1.iloc[16,0]
te17 = df1.iloc[16,1]
#waveHeight
r117 = df1.iloc[16,2]
r217 = df2.iloc[16,2]
r317 = df3.iloc[16,2]
r417 = df4.iloc[16,2]
r517 = df5.iloc[16,2]
r617 = df6.iloc[16,2]
r717 = df7.iloc[16,2]
r817 = df8.iloc[16,2]
r917 = df9.iloc[16,2]
r1017 = df10.iloc[16,2]
r1117 = df11.iloc[16,2]
r1217 = df12.iloc[16,2]
r1317 = df13.iloc[16,2]
r1417 = df14.iloc[16,2]
r1517 = df15.iloc[16,2]
r1617 = df16.iloc[16,2]
r1717 = df17.iloc[16,2]
r1817 = df18.iloc[16,2]
r1917 = df19.iloc[16,2]
r2017 = df20.iloc[16,2]
r2117 = df21.iloc[16,2]
r2217 = df22.iloc[16,2]
r2317 = df23.iloc[16,2]
r2417 = df24.iloc[16,2]
r2517 = df25.iloc[16,2]
r2617 = df26.iloc[16,2]
r2717 = df27.iloc[16,2]
r2817 = df28.iloc[16,2]
r2917 = df29.iloc[16,2]
r3017 = df30.iloc[16,2]
r3117 = df31.iloc[16,2]
r3217 = df32.iloc[16,2]
r3317 = df33.iloc[16,2]
r3417 = df34.iloc[16,2]
r3517 = df35.iloc[16,2]

# Timestep 18
ts18 = df1.iloc[17,0]
te18 = df1.iloc[17,1]
#waveHeight
r118 = df1.iloc[17,2]
r218 = df2.iloc[17,2]
r318 = df3.iloc[17,2]
r418 = df4.iloc[17,2]
r518 = df5.iloc[17,2]
r618 = df6.iloc[17,2]
r718 = df7.iloc[17,2]
r818 = df8.iloc[17,2]
r918 = df9.iloc[17,2]
r1018 = df10.iloc[17,2]
r1118 = df11.iloc[17,2]
r1218 = df12.iloc[17,2]
r1318 = df13.iloc[17,2]
r1418 = df14.iloc[17,2]
r1518 = df15.iloc[17,2]
r1618 = df16.iloc[17,2]
r1718 = df17.iloc[17,2]
r1818 = df18.iloc[17,2]
r1918 = df19.iloc[17,2]
r2018 = df20.iloc[17,2]
r2118 = df21.iloc[17,2]
r2218 = df22.iloc[17,2]
r2318 = df23.iloc[17,2]
r2418 = df24.iloc[17,2]
r2518 = df25.iloc[17,2]
r2618 = df26.iloc[17,2]
r2718 = df27.iloc[17,2]
r2818 = df28.iloc[17,2]
r2918 = df29.iloc[17,2]
r3018 = df30.iloc[17,2]
r3118 = df31.iloc[17,2]
r3218 = df32.iloc[17,2]
r3318 = df33.iloc[17,2]
r3418 = df34.iloc[17,2]
r3518 = df35.iloc[17,2]

# Timestep 19
ts19 = df1.iloc[18,0]
te19 = df1.iloc[18,1]
#waveHeight
r119 = df1.iloc[18,2]
r219 = df2.iloc[18,2]
r319 = df3.iloc[18,2]
r419 = df4.iloc[18,2]
r519 = df5.iloc[18,2]
r619 = df6.iloc[18,2]
r719 = df7.iloc[18,2]
r819 = df8.iloc[18,2]
r919 = df9.iloc[18,2]
r1019 = df10.iloc[18,2]
r1119 = df11.iloc[18,2]
r1219 = df12.iloc[18,2]
r1319 = df13.iloc[18,2]
r1419 = df14.iloc[18,2]
r1519 = df15.iloc[18,2]
r1619 = df16.iloc[18,2]
r1719 = df17.iloc[18,2]
r1819 = df18.iloc[18,2]
r1919 = df19.iloc[18,2]
r2019 = df20.iloc[18,2]
r2119 = df21.iloc[18,2]
r2219 = df22.iloc[18,2]
r2319 = df23.iloc[18,2]
r2419 = df24.iloc[18,2]
r2519 = df25.iloc[18,2]
r2619 = df26.iloc[18,2]
r2719 = df27.iloc[18,2]
r2819 = df28.iloc[18,2]
r2919 = df29.iloc[18,2]
r3019 = df30.iloc[18,2]
r3119 = df31.iloc[18,2]
r3219 = df32.iloc[18,2]
r3319 = df33.iloc[18,2]
r3419 = df34.iloc[18,2]
r3519 = df35.iloc[18,2]

# Timestep 20
ts20 = df1.iloc[19,0]
te20 = df1.iloc[19,1]
#waveHeight
r120 = df1.iloc[19,2]
r220 = df2.iloc[19,2]
r320 = df3.iloc[19,2]
r420 = df4.iloc[19,2]
r520 = df5.iloc[19,2]
r620 = df6.iloc[19,2]
r720 = df7.iloc[19,2]
r820 = df8.iloc[19,2]
r920 = df9.iloc[19,2]
r1020 = df10.iloc[19,2]
r1120 = df11.iloc[19,2]
r1220 = df12.iloc[19,2]
r1320 = df13.iloc[19,2]
r1420 = df14.iloc[19,2]
r1520 = df15.iloc[19,2]
r1620 = df16.iloc[19,2]
r1720 = df17.iloc[19,2]
r1820 = df18.iloc[19,2]
r1920 = df19.iloc[19,2]
r2020 = df20.iloc[19,2]
r2120 = df21.iloc[19,2]
r2220 = df22.iloc[19,2]
r2320 = df23.iloc[19,2]
r2420 = df24.iloc[19,2]
r2520 = df25.iloc[19,2]
r2620 = df26.iloc[19,2]
r2720 = df27.iloc[19,2]
r2820 = df28.iloc[19,2]
r2920 = df29.iloc[19,2]
r3020 = df30.iloc[19,2]
r3120 = df31.iloc[19,2]
r3220 = df32.iloc[19,2]
r3320 = df33.iloc[19,2]
r3420 = df34.iloc[19,2]
r3520 = df35.iloc[19,2]

# Timestep 21
ts21 = df1.iloc[20,0]
te21 = df1.iloc[20,1]
#waveHeight
r121 = df1.iloc[20,2]
r221 = df2.iloc[20,2]
r321 = df3.iloc[20,2]
r421 = df4.iloc[20,2]
r521 = df5.iloc[20,2]
r621 = df6.iloc[20,2]
r721 = df7.iloc[20,2]
r821 = df8.iloc[20,2]
r921 = df9.iloc[20,2]
r1021 = df10.iloc[20,2]
r1121 = df11.iloc[20,2]
r1221 = df12.iloc[20,2]
r1321 = df13.iloc[20,2]
r1421 = df14.iloc[20,2]
r1521 = df15.iloc[20,2]
r1621 = df16.iloc[20,2]
r1721 = df17.iloc[20,2]
r1821 = df18.iloc[20,2]
r1921 = df19.iloc[20,2]
r2021 = df20.iloc[20,2]
r2121 = df21.iloc[20,2]
r2221 = df22.iloc[20,2]
r2321 = df23.iloc[20,2]
r2421 = df24.iloc[20,2]
r2521 = df25.iloc[20,2]
r2621 = df26.iloc[20,2]
r2721 = df27.iloc[20,2]
r2821 = df28.iloc[20,2]
r2921 = df29.iloc[20,2]
r3021 = df30.iloc[20,2]
r3121 = df31.iloc[20,2]
r3221 = df32.iloc[20,2]
r3321 = df33.iloc[20,2]
r3421 = df34.iloc[20,2]
r3521 = df35.iloc[20,2]

# Timestep 22
ts22 = df1.iloc[21,0]
te22 = df1.iloc[21,1]
#waveHeight
r122 = df1.iloc[21,2]
r222 = df2.iloc[21,2]
r322 = df3.iloc[21,2]
r422 = df4.iloc[21,2]
r522 = df5.iloc[21,2]
r622 = df6.iloc[21,2]
r722 = df7.iloc[21,2]
r822 = df8.iloc[21,2]
r922 = df9.iloc[21,2]
r1022 = df10.iloc[21,2]
r1122 = df11.iloc[21,2]
r1222 = df12.iloc[21,2]
r1322 = df13.iloc[21,2]
r1422 = df14.iloc[21,2]
r1522 = df15.iloc[21,2]
r1622 = df16.iloc[21,2]
r1722 = df17.iloc[21,2]
r1822 = df18.iloc[21,2]
r1922 = df19.iloc[21,2]
r2022 = df20.iloc[21,2]
r2122 = df21.iloc[21,2]
r2222 = df22.iloc[21,2]
r2322 = df23.iloc[21,2]
r2422 = df24.iloc[21,2]
r2522 = df25.iloc[21,2]
r2622 = df26.iloc[21,2]
r2722 = df27.iloc[21,2]
r2822 = df28.iloc[21,2]
r2922 = df29.iloc[21,2]
r3022 = df30.iloc[21,2]
r3122 = df31.iloc[21,2]
r3222 = df32.iloc[21,2]
r3322 = df33.iloc[21,2]
r3422 = df34.iloc[21,2]
r3522 = df35.iloc[21,2]

# Timestep 23
ts23 = df1.iloc[22,0]
te23 = df1.iloc[22,1]
#waveHeight
r123 = df1.iloc[22,2]
r223 = df2.iloc[22,2]
r323 = df3.iloc[22,2]
r423 = df4.iloc[22,2]
r523 = df5.iloc[22,2]
r623 = df6.iloc[22,2]
r723 = df7.iloc[22,2]
r823 = df8.iloc[22,2]
r923 = df9.iloc[22,2]
r1023 = df10.iloc[22,2]
r1123 = df11.iloc[22,2]
r1223 = df12.iloc[22,2]
r1323 = df13.iloc[22,2]
r1423 = df14.iloc[22,2]
r1523 = df15.iloc[22,2]
r1623 = df16.iloc[22,2]
r1723 = df17.iloc[22,2]
r1823 = df18.iloc[22,2]
r1923 = df19.iloc[22,2]
r2023 = df20.iloc[22,2]
r2123 = df21.iloc[22,2]
r2223 = df22.iloc[22,2]
r2323 = df23.iloc[22,2]
r2423 = df24.iloc[22,2]
r2523 = df25.iloc[22,2]
r2623 = df26.iloc[22,2]
r2723 = df27.iloc[22,2]
r2823 = df28.iloc[22,2]
r2923 = df29.iloc[22,2]
r3023 = df30.iloc[22,2]
r3123 = df31.iloc[22,2]
r3223 = df32.iloc[22,2]
r3323 = df33.iloc[22,2]
r3423 = df34.iloc[22,2]
r3523 = df35.iloc[22,2]

# Timestep 24
ts24 = df1.iloc[23,0]
te24 = df1.iloc[23,1]
#waveHeight
r124 = df1.iloc[23,2]
r224 = df2.iloc[23,2]
r324 = df3.iloc[23,2]
r424 = df4.iloc[23,2]
r524 = df5.iloc[23,2]
r624 = df6.iloc[23,2]
r724 = df7.iloc[23,2]
r824 = df8.iloc[23,2]
r924 = df9.iloc[23,2]
r1024 = df10.iloc[23,2]
r1124 = df11.iloc[23,2]
r1224 = df12.iloc[23,2]
r1324 = df13.iloc[23,2]
r1424 = df14.iloc[23,2]
r1524 = df15.iloc[23,2]
r1624 = df16.iloc[23,2]
r1724 = df17.iloc[23,2]
r1824 = df18.iloc[23,2]
r1924 = df19.iloc[23,2]
r2024 = df20.iloc[23,2]
r2124 = df21.iloc[23,2]
r2224 = df22.iloc[23,2]
r2324 = df23.iloc[23,2]
r2424 = df24.iloc[23,2]
r2524 = df25.iloc[23,2]
r2624 = df26.iloc[23,2]
r2724 = df27.iloc[23,2]
r2824 = df28.iloc[23,2]
r2924 = df29.iloc[23,2]
r3024 = df30.iloc[23,2]
r3124 = df31.iloc[23,2]
r3224 = df32.iloc[23,2]
r3324 = df33.iloc[23,2]
r3424 = df34.iloc[23,2]
r3524 = df35.iloc[23,2]

# Timestep 25
ts25 = df1.iloc[24,0]
te25 = df1.iloc[24,1]
#waveHeight
r125 = df1.iloc[24,2]
r225 = df2.iloc[24,2]
r325 = df3.iloc[24,2]
r425 = df4.iloc[24,2]
r525 = df5.iloc[24,2]
r625 = df6.iloc[24,2]
r725 = df7.iloc[24,2]
r825 = df8.iloc[24,2]
r925 = df9.iloc[24,2]
r1025 = df10.iloc[24,2]
r1125 = df11.iloc[24,2]
r1225 = df12.iloc[24,2]
r1325 = df13.iloc[24,2]
r1425 = df14.iloc[24,2]
r1525 = df15.iloc[24,2]
r1625 = df16.iloc[24,2]
r1725 = df17.iloc[24,2]
r1825 = df18.iloc[24,2]
r1925 = df19.iloc[24,2]
r2025 = df20.iloc[24,2]
r2125 = df21.iloc[24,2]
r2225 = df22.iloc[24,2]
r2325 = df23.iloc[24,2]
r2425 = df24.iloc[24,2]
r2525 = df25.iloc[24,2]
r2625 = df26.iloc[24,2]
r2725 = df27.iloc[24,2]
r2825 = df28.iloc[24,2]
r2925 = df29.iloc[24,2]
r3025 = df30.iloc[24,2]
r3125 = df31.iloc[24,2]
r3225 = df32.iloc[24,2]
r3325 = df33.iloc[24,2]
r3425 = df34.iloc[24,2]
r3525 = df35.iloc[24,2]

# Timestep 26
ts26 = df1.iloc[25,0]
te26 = df1.iloc[25,1]
#waveHeight
r126 = df1.iloc[25,2]
r226 = df2.iloc[25,2]
r326 = df3.iloc[25,2]
r426 = df4.iloc[25,2]
r526 = df5.iloc[25,2]
r626 = df6.iloc[25,2]
r726 = df7.iloc[25,2]
r826 = df8.iloc[25,2]
r926 = df9.iloc[25,2]
r1026 = df10.iloc[25,2]
r1126 = df11.iloc[25,2]
r1226 = df12.iloc[25,2]
r1326 = df13.iloc[25,2]
r1426 = df14.iloc[25,2]
r1526 = df15.iloc[25,2]
r1626 = df16.iloc[25,2]
r1726 = df17.iloc[25,2]
r1826 = df18.iloc[25,2]
r1926 = df19.iloc[25,2]
r2026 = df20.iloc[25,2]
r2126 = df21.iloc[25,2]
r2226 = df22.iloc[25,2]
r2326 = df23.iloc[25,2]
r2426 = df24.iloc[25,2]
r2526 = df25.iloc[25,2]
r2626 = df26.iloc[25,2]
r2726 = df27.iloc[25,2]
r2826 = df28.iloc[25,2]
r2926 = df29.iloc[25,2]
r3026 = df30.iloc[25,2]
r3126 = df31.iloc[25,2]
r3226 = df32.iloc[25,2]
r3326 = df33.iloc[25,2]
r3426 = df34.iloc[25,2]
r3526 = df35.iloc[25,2]

# Timestep 27
ts27 = df1.iloc[26,0]
te27 = df1.iloc[26,1]
#waveHeight
r127 = df1.iloc[26,2]
r227 = df2.iloc[26,2]
r327 = df3.iloc[26,2]
r427 = df4.iloc[26,2]
r527 = df5.iloc[26,2]
r627 = df6.iloc[26,2]
r727 = df7.iloc[26,2]
r827 = df8.iloc[26,2]
r927 = df9.iloc[26,2]
r1027 = df10.iloc[26,2]
r1127 = df11.iloc[26,2]
r1227 = df12.iloc[26,2]
r1327 = df13.iloc[26,2]
r1427 = df14.iloc[26,2]
r1527 = df15.iloc[26,2]
r1627 = df16.iloc[26,2]
r1727 = df17.iloc[26,2]
r1827 = df18.iloc[26,2]
r1927 = df19.iloc[26,2]
r2027 = df20.iloc[26,2]
r2127 = df21.iloc[26,2]
r2227 = df22.iloc[26,2]
r2327 = df23.iloc[26,2]
r2427 = df24.iloc[26,2]
r2527 = df25.iloc[26,2]
r2627 = df26.iloc[26,2]
r2727 = df27.iloc[26,2]
r2827 = df28.iloc[26,2]
r2927 = df29.iloc[26,2]
r3027 = df30.iloc[26,2]
r3127 = df31.iloc[26,2]
r3227 = df32.iloc[26,2]
r3327 = df33.iloc[26,2]
r3427 = df34.iloc[26,2]
r3527 = df35.iloc[26,2]

# Timestep 28
ts28 = df1.iloc[27,0]
te28 = df1.iloc[27,1]
#waveHeight
r128 = df1.iloc[27,2]
r228 = df2.iloc[27,2]
r328 = df3.iloc[27,2]
r428 = df4.iloc[27,2]
r528 = df5.iloc[27,2]
r628 = df6.iloc[27,2]
r728 = df7.iloc[27,2]
r828 = df8.iloc[27,2]
r928 = df9.iloc[27,2]
r1028 = df10.iloc[27,2]
r1128 = df11.iloc[27,2]
r1228 = df12.iloc[27,2]
r1328 = df13.iloc[27,2]
r1428 = df14.iloc[27,2]
r1528 = df15.iloc[27,2]
r1628 = df16.iloc[27,2]
r1728 = df17.iloc[27,2]
r1828 = df18.iloc[27,2]
r1928 = df19.iloc[27,2]
r2028 = df20.iloc[27,2]
r2128 = df21.iloc[27,2]
r2228 = df22.iloc[27,2]
r2328 = df23.iloc[27,2]
r2428 = df24.iloc[27,2]
r2528 = df25.iloc[27,2]
r2628 = df26.iloc[27,2]
r2728 = df27.iloc[27,2]
r2828 = df28.iloc[27,2]
r2928 = df29.iloc[27,2]
r3028 = df30.iloc[27,2]
r3128 = df31.iloc[27,2]
r3228 = df32.iloc[27,2]
r3328 = df33.iloc[27,2]
r3428 = df34.iloc[27,2]
r3528 = df35.iloc[27,2]

# Data Frame baru
new_df = pd.DataFrame()

# Simpan nilai di tempat yang sesuai
# Timestep 1
    # Baris 1
new_df['dateTimeStart'] = [ts1]
new_df['dateTimeEnd'] = [te1]
new_df['waveHeight'] = [r11]
new_df['waveHeight1'] = [r21]
new_df['waveHeight2'] = [r31]
new_df['waveHeight3'] = [r41]
new_df['waveHeight4'] = [r51]
new_df['waveHeight5'] = [r61]
new_df['waveHeight6'] = [r71]
new_df['waveHeightChange'] = [whc]
new_df['waveHeightChange1'] = [whc]
new_df['waveHeightChange2'] = [whc]
new_df['waveHeightChange3'] = [whc]
new_df['waveHeightChange4'] = [whc]
new_df['waveHeightChange5'] = [whc]
new_df['waveHeightChange6'] = [whc]
new_df['probabilityOfHeightsExceeding'] = [poh]
new_df['probabilityOfHeightsExceeding1'] = [poh]
new_df['probabilityOfHeightsExceeding2'] = [poh]
new_df['probabilityOfHeightsExceeding3'] = [poh]
new_df['probabilityOfHeightsExceeding4'] = [poh]
new_df['probabilityOfHeightsExceeding5'] = [poh]
new_df['probabilityOfHeightsExceeding6'] = [poh]
    # Baris 2
new_df.loc[1] = [ts1, te1, r141, r131, r121, r111, r101, r91, r81, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[2] = [ts1, te1, r151, r161, r171, r181, r191, r201, r211, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[3] = [ts1, te1, r281, r271, r261, r251, r241, r231, r221, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[4] = [ts1, te1, r291, r301, r311, r321, r331, r341, r351, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]

# Timestep 2
new_df.loc[5] = [ts2, te2, r12, r22, r32, r42, r52, r62, r72, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[6] = [ts2, te2, r142, r132, r122, r112, r102, r92, r82, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[7] = [ts2, te2, r152, r162, r172, r182, r192, r202, r212, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[8] = [ts2, te2, r282, r272, r262, r252, r242, r232, r222, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[9] = [ts2, te2, r292, r302, r312, r322, r332, r342, r352, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 3
new_df.loc[10] = [ts3, te3, r13, r23, r33, r43, r53, r63, r73, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[11] = [ts3, te3, r143, r133, r123, r113, r103, r93, r83, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[12] = [ts3, te3, r153, r163, r173, r183, r193, r203, r213, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[13] = [ts3, te3, r283, r273, r263, r253, r243, r233, r223, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[14] = [ts3, te3, r293, r303, r313, r323, r333, r343, r353, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 4
new_df.loc[15] = [ts4, te4, r14, r24, r34, r44, r54, r64, r74, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[16] = [ts4, te4, r144, r134, r124, r114, r104, r94, r84, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[17] = [ts4, te4, r154, r164, r174, r184, r194, r204, r214, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[18] = [ts4, te4, r284, r274, r264, r254, r244, r234, r224, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[19] = [ts4, te4, r294, r304, r314, r324, r334, r344, r354, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 5
new_df.loc[20] = [ts5, te5, r15, r25, r35, r45, r55, r65, r75, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[21] = [ts5, te5, r145, r135, r125, r115, r105, r95, r85, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[22] = [ts5, te5, r155, r165, r175, r185, r195, r205, r215, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[23] = [ts5, te5, r285, r275, r265, r255, r245, r235, r225, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[24] = [ts5, te5, r295, r305, r315, r325, r335, r345, r355, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 6
new_df.loc[25] = [ts6, te6, r16, r26, r36, r46, r56, r66, r76, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[26] = [ts6, te6, r146, r136, r126, r116, r106, r96, r86, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[27] = [ts6, te6, r156, r166, r176, r186, r196, r206, r216, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[28] = [ts6, te6, r286, r276, r266, r256, r246, r236, r226, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[29] = [ts6, te6, r296, r306, r316, r326, r336, r346, r356, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 7
new_df.loc[30] = [ts7, te7, r17, r27, r37, r47, r57, r67, r77, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[31] = [ts7, te7, r147, r137, r127, r117, r107, r97, r87, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[32] = [ts7, te7, r157, r167, r177, r187, r197, r207, r217, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[33] = [ts7, te7, r287, r277, r267, r257, r247, r237, r227, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[34] = [ts7, te7, r297, r307, r317, r327, r337, r347, r357, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 8
new_df.loc[35] = [ts8, te8, r18, r28, r38, r48, r58, r68, r78, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[36] = [ts8, te8, r148, r138, r128, r118, r108, r98, r88, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[37] = [ts8, te8, r158, r168, r178, r188, r198, r208, r218, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[38] = [ts8, te8, r288, r278, r268, r258, r248, r238, r228, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[39] = [ts8, te8, r298, r308, r318, r328, r338, r348, r358, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 9
new_df.loc[40] = [ts9, te9, r19, r29, r39, r49, r59, r69, r79, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[41] = [ts9, te9, r149, r139, r129, r119, r109, r99, r89, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[42] = [ts9, te9, r159, r169, r179, r189, r199, r209, r219, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[43] = [ts9, te9, r289, r279, r269, r259, r249, r239, r229, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[44] = [ts9, te9, r299, r309, r319, r329, r339, r349, r359, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 10
new_df.loc[45] = [ts10, te10, r110, r210, r310, r410, r510, r610, r710, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[46] = [ts10, te10, r1410, r1310, r1210, r1110, r1010, r910, r810, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[47] = [ts10, te10, r1510, r1610, r1710, r1810, r1910, r2010, r2110, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[48] = [ts10, te10, r2810, r2710, r2610, r2510, r2410, r2310, r2210, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[49] = [ts10, te10, r2910, r3010, r3110, r3210, r3310, r3410, r3510, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 11
new_df.loc[50] = [ts11, te11, r111, r211, r311, r411, r511, r611, r711, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[51] = [ts11, te11, r1411, r1311, r1211, r1111, r1011, r911, r811, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[52] = [ts11, te11, r1511, r1611, r1711, r1811, r1911, r2011, r2111, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[53] = [ts11, te11, r2811, r2711, r2611, r2511, r2411, r2311, r2211, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[54] = [ts11, te11, r2911, r3011, r3111, r3211, r3311, r3411, r3511, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 12
new_df.loc[55] = [ts12, te12, r112, r212, r312, r412, r512, r612, r712, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[56] = [ts12, te12, r1412, r1312, r1212, r1112, r1012, r912, r812, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[57] = [ts12, te12, r1512, r1612, r1712, r1812, r1912, r2012, r2112, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[58] = [ts12, te12, r2812, r2712, r2612, r2512, r2412, r2312, r2212, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[59] = [ts12, te12, r2912, r3012, r3112, r3212, r3312, r3412, r3512, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 13
new_df.loc[60] = [ts13, te13, r113, r213, r313, r413, r513, r613, r713, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[61] = [ts13, te13, r1413, r1313, r1213, r1113, r1013, r913, r813, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[62] = [ts13, te13, r1513, r1613, r1713, r1813, r1913, r2013, r2113, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[63] = [ts13, te13, r2813, r2713, r2613, r2513, r2413, r2313, r2213, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[64] = [ts13, te13, r2913, r3013, r3113, r3213, r3313, r3413, r3513, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 14
new_df.loc[65] = [ts14, te14, r114, r214, r314, r414, r514, r614, r714, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[66] = [ts14, te14, r1414, r1314, r1214, r1114, r1014, r914, r814, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[67] = [ts14, te14, r1514, r1614, r1714, r1814, r1914, r2014, r2114, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[68] = [ts14, te14, r2814, r2714, r2614, r2514, r2414, r2314, r2214, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[69] = [ts14, te14, r2914, r3014, r3114, r3214, r3314, r3414, r3514, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 15
new_df.loc[70] = [ts15, te15, r115, r215, r315, r415, r515, r615, r715, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[71] = [ts15, te15, r1415, r1315, r1215, r1115, r1015, r915, r815, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[72] = [ts15, te15, r1515, r1615, r1715, r1815, r1915, r2015, r2115, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[73] = [ts15, te15, r2815, r2715, r2615, r2515, r2415, r2315, r2215, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[74] = [ts15, te15, r2915, r3015, r3115, r3215, r3315, r3415, r3515, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 16
new_df.loc[75] = [ts16, te16, r116, r216, r316, r416, r516, r616, r716, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[76] = [ts16, te16, r1416, r1316, r1216, r1116, r1016, r916, r816, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[77] = [ts16, te16, r1516, r1616, r1716, r1816, r1916, r2016, r2116, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[78] = [ts16, te16, r2816, r2716, r2616, r2516, r2416, r2316, r2216, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[79] = [ts16, te16, r2916, r3016, r3116, r3216, r3316, r3416, r3516, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 17
new_df.loc[80] = [ts17, te17, r117, r217, r317, r417, r517, r617, r717, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[81] = [ts17, te17, r1417, r1317, r1217, r1117, r1017, r917, r817, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[82] = [ts17, te17, r1517, r1617, r1717, r1817, r1917, r2017, r2117, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[83] = [ts17, te17, r2817, r2717, r2617, r2517, r2417, r2317, r2217, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[84] = [ts17, te17, r2917, r3017, r3117, r3217, r3317, r3417, r3517, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 18
new_df.loc[85] = [ts18, te18, r118, r218, r318, r418, r518, r618, r718, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[86] = [ts18, te18, r1418, r1318, r1218, r1118, r1018, r918, r818, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[87] = [ts18, te18, r1518, r1618, r1718, r1818, r1918, r2018, r2118, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[88] = [ts18, te18, r2818, r2718, r2618, r2518, r2418, r2318, r2218, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[89] = [ts18, te18, r2918, r3018, r3118, r3218, r3318, r3418, r3518, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 19
new_df.loc[90] = [ts19, te19, r119, r219, r319, r419, r519, r619, r719, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[91] = [ts19, te19, r1419, r1319, r1219, r1119, r1019, r919, r819, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[92] = [ts19, te19, r1519, r1619, r1719, r1819, r1919, r2019, r2119, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[93] = [ts19, te19, r2819, r2719, r2619, r2519, r2419, r2319, r2219, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[94] = [ts19, te19, r2919, r3019, r3119, r3219, r3319, r3419, r3519, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 20
new_df.loc[95] = [ts20, te20, r120, r220, r320, r420, r520, r620, r720, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[96] = [ts20, te20, r1420, r1320, r1220, r1120, r1020, r920, r820, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[97] = [ts20, te20, r1520, r1620, r1720, r1820, r1920, r2020, r2120, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[98] = [ts20, te20, r2820, r2720, r2620, r2520, r2420, r2320, r2220, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[99] = [ts20, te20, r2920, r3020, r3120, r3220, r3320, r3420, r3520, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 21
new_df.loc[100] = [ts21, te21, r121, r221, r321, r421, r521, r621, r721, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[101] = [ts21, te21, r1421, r1321, r1221, r1121, r1021, r921, r821, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[102] = [ts21, te21, r1521, r1621, r1721, r1821, r1921, r2021, r2121, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[103] = [ts21, te21, r2821, r2721, r2621, r2521, r2421, r2321, r2221, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[104] = [ts21, te21, r2921, r3021, r3121, r3221, r3321, r3421, r3521, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 22
new_df.loc[105] = [ts22, te22, r122, r222, r322, r422, r522, r622, r722, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[106] = [ts22, te22, r1422, r1322, r1222, r1122, r1022, r922, r822, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[107] = [ts22, te22, r1522, r1622, r1722, r1822, r1922, r2022, r2122, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[108] = [ts22, te22, r2822, r2722, r2622, r2522, r2422, r2322, r2222, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[109] = [ts22, te22, r2922, r3022, r3122, r3222, r3322, r3422, r3522, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 23
new_df.loc[110] = [ts23, te23, r123, r223, r323, r423, r523, r623, r723, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[111] = [ts23, te23, r1423, r1323, r1223, r1123, r1023, r923, r823, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[112] = [ts23, te23, r1523, r1623, r1723, r1823, r1923, r2023, r2123, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[113] = [ts23, te23, r2823, r2723, r2623, r2523, r2423, r2323, r2223, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[114] = [ts23, te23, r2923, r3023, r3123, r3223, r3323, r3423, r3523, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 24
new_df.loc[115] = [ts24, te24, r124, r224, r324, r424, r524, r624, r724, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[116] = [ts24, te24, r1424, r1324, r1224, r1124, r1024, r924, r824, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[117] = [ts24, te24, r1524, r1624, r1724, r1824, r1924, r2024, r2124, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[118] = [ts24, te24, r2824, r2724, r2624, r2524, r2424, r2324, r2224, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[119] = [ts24, te24, r2924, r3024, r3124, r3224, r3324, r3424, r3524, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 25
new_df.loc[120] = [ts25, te25, r125, r225, r325, r425, r525, r625, r725, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[121] = [ts25, te25, r1425, r1325, r1225, r1125, r1025, r925, r825, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[122] = [ts25, te25, r1525, r1625, r1725, r1825, r1925, r2025, r2125, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[123] = [ts25, te25, r2825, r2725, r2625, r2525, r2425, r2325, r2225, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[124] = [ts25, te25, r2925, r3025, r3125, r3225, r3325, r3425, r3525, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 26
new_df.loc[125] = [ts26, te26, r126, r226, r326, r426, r526, r626, r726, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[126] = [ts26, te26, r1426, r1326, r1226, r1126, r1026, r926, r826, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[127] = [ts26, te26, r1526, r1626, r1726, r1826, r1926, r2026, r2126, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[128] = [ts26, te26, r2826, r2726, r2626, r2526, r2426, r2326, r2226, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[129] = [ts26, te26, r2926, r3026, r3126, r3226, r3326, r3426, r3526, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 27
new_df.loc[130] = [ts27, te27, r127, r227, r327, r427, r527, r627, r727, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[131] = [ts27, te27, r1427, r1327, r1227, r1127, r1027, r927, r827, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[132] = [ts27, te27, r1527, r1627, r1727, r1827, r1927, r2027, r2127, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[133] = [ts27, te27, r2827, r2727, r2627, r2527, r2427, r2327, r2227, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[134] = [ts27, te27, r2927, r3027, r3127, r3227, r3327, r3427, r3527, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
# Timestep 28
new_df.loc[135] = [ts28, te28, r128, r228, r328, r428, r528, r628, r728, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[136] = [ts28, te28, r1428, r1328, r1228, r1128, r1028, r928, r828, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[137] = [ts28, te28, r1528, r1628, r1728, r1828, r1928, r2028, r2128, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[138] = [ts28, te28, r2828, r2728, r2628, r2528, r2428, r2328, r2228, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]
new_df.loc[139] = [ts28, te28, r2928, r3028, r3128, r3228, r3328, r3428, r3528, whc, whc, whc, whc, whc, whc, whc, poh, poh, poh, poh, poh, poh, poh]

# Simpan DataFrame ke dalam satu file CSV
new_df.to_csv("superRaster.csv", index=False)

print("File CSV:", os.path.abspath('superRaster.csv'))

print("CSV Raster Telah Dibuat")

#----------------------------------Converter Script-------------------------------------#
#Membaca data dari file CSV

df = pd.read_csv("D:/WEB Capstone/S100Converter/superRaster.csv", delimiter=',')
# Timestep 1
df11 = df.iloc[0:5,2:9]
df21 = df.iloc[0:5,9:16]
df31 = df.iloc[0:5,16:25]
# Timestep 2
df12 = df.iloc[5:10,2:9]
df22 = df.iloc[5:10,9:16]
df32 = df.iloc[5:10,16:25]
# Timestep 3
df13 = df.iloc[10:15,2:9]
df23 = df.iloc[10:15,9:16]
df33 = df.iloc[10:15,16:25]
# Timestep 4
df14 = df.iloc[15:20,2:9]
df24 = df.iloc[15:20,9:16]
df34 = df.iloc[15:20,16:25]
# Timestep 5
df15 = df.iloc[20:25,2:9]
df25 = df.iloc[20:25,9:16]
df35 = df.iloc[20:25,16:25]
# Timestep 6
df16 = df.iloc[25:30,2:9]
df26 = df.iloc[25:30,9:16]
df36 = df.iloc[25:30,16:25]
# Timestep 7
df17 = df.iloc[30:35,2:9]
df27 = df.iloc[30:35,9:16]
df37 = df.iloc[30:35,16:25]
# Timestep 8
df18 = df.iloc[35:40,2:9]
df28 = df.iloc[35:40,9:16]
df38 = df.iloc[35:40,16:25]
# Timestep 9
df19 = df.iloc[40:45,2:9]
df29 = df.iloc[40:45,9:16]
df39 = df.iloc[40:45,16:25]
# Timestep 10
df110 = df.iloc[45:50,2:9]
df210 = df.iloc[45:50,9:16]
df310 = df.iloc[45:50,16:25]
# Timestep 11
df111 = df.iloc[50:55,2:9]
df211 = df.iloc[50:55,9:16]
df311 = df.iloc[50:55,16:25]
# Timestep 12
df112 = df.iloc[55:60,2:9]
df212 = df.iloc[55:60,9:16]
df312 = df.iloc[55:60,16:25]
# Timestep 13
df113 = df.iloc[60:65,2:9]
df213 = df.iloc[60:65,9:16]
df313 = df.iloc[60:65,16:25]
# Timestep 14
df114 = df.iloc[65:70,2:9]
df214 = df.iloc[65:70,9:16]
df314 = df.iloc[65:70,16:25]
# Timestep 15
df115 = df.iloc[70:75,2:9]
df215 = df.iloc[70:75,9:16]
df315 = df.iloc[70:75,16:25]
# Timestep 16
df116 = df.iloc[75:80,2:9]
df216 = df.iloc[75:80,9:16]
df316 = df.iloc[75:80,16:25]
# Timestep 17
df117 = df.iloc[80:85,2:9]
df217 = df.iloc[80:85,9:16]
df317 = df.iloc[80:85,16:25]
# Timestep 18
df118 = df.iloc[85:90,2:9]
df218 = df.iloc[85:90,9:16]
df318 = df.iloc[85:90,16:25]
# Timestep 19
df119 = df.iloc[90:95,2:9]
df219 = df.iloc[90:95,9:16]
df319 = df.iloc[90:95,16:25]
# Timestep 20
df120 = df.iloc[95:100,2:9]
df220 = df.iloc[95:100,9:16]
df320 = df.iloc[95:100,16:25]
# Timestep 21
df121 = df.iloc[100:105,2:9]
df221 = df.iloc[100:105,9:16]
df321 = df.iloc[100:105,16:25]
# Timestep 22
df122 = df.iloc[105:110,2:9]
df222 = df.iloc[105:110,9:16]
df322 = df.iloc[105:110,16:25]
# Timestep 23
df123 = df.iloc[110:115,2:9]
df223 = df.iloc[110:115,9:16]
df323 = df.iloc[110:115,16:25]
# Timestep 24
df124 = df.iloc[115:120,2:9]
df224 = df.iloc[115:120,9:16]
df324 = df.iloc[115:120,16:25]
# Timestep 25
df125 = df.iloc[120:125,2:9]
df225 = df.iloc[120:125,9:16]
df325 = df.iloc[120:125,16:25]
# Timestep 26
df126 = df.iloc[125:130,2:9]
df226 = df.iloc[125:130,9:16]
df326 = df.iloc[125:130,16:25]
# Timestep 27
df127 = df.iloc[130:135,2:9]
df227 = df.iloc[130:135,9:16]
df327 = df.iloc[130:135,16:25]
# Timestep 28
df128 = df.iloc[135:140,2:9]
df228 = df.iloc[135:140,9:16]
df328 = df.iloc[135:140,16:25]

# Ngambil array
arr1 = df11.values
arr2 = df21.values
arr3 = df31.values
arr4 = df12.values
arr5 = df22.values
arr6 = df32.values
arr7 = df13.values
arr8 = df23.values
arr9 = df33.values
arr10 = df14.values
arr11 = df24.values
arr12 = df34.values
arr13 = df14.values
arr14 = df24.values
arr15 = df34.values
arr16 = df15.values
arr17 = df25.values
arr18 = df35.values
arr19 = df16.values
arr20 = df26.values
arr21 = df36.values
arr22 = df17.values
arr23 = df27.values
arr24 = df37.values
arr25 = df18.values
arr26 = df28.values
arr27 = df38.values
arr28 = df19.values
arr29 = df29.values
arr30 = df39.values
arr31 = df110.values
arr32 = df210.values
arr33 = df310.values
arr34 = df111.values
arr35 = df211.values
arr36 = df311.values
arr37 = df112.values
arr38 = df212.values
arr39 = df312.values
arr40 = df113.values
arr41 = df213.values
arr42 = df313.values
arr43 = df114.values
arr44 = df214.values
arr45 = df314.values
arr46 = df115.values
arr47 = df215.values
arr48 = df315.values
arr49 = df116.values
arr50 = df216.values
arr51 = df316.values
arr52 = df117.values
arr53 = df217.values
arr54 = df317.values
arr55 = df118.values
arr56 = df218.values
arr57 = df318.values
arr58 = df119.values
arr59 = df219.values
arr60 = df319.values
arr61 = df120.values
arr62 = df220.values
arr63 = df320.values
arr64 = df121.values
arr65 = df221.values
arr66 = df321.values
arr67 = df122.values
arr68 = df222.values
arr69 = df322.values
arr70 = df123.values
arr71 = df223.values
arr72 = df323.values
arr73 = df124.values
arr74 = df224.values
arr75 = df324.values
arr76 = df125.values
arr77 = df225.values
arr78 = df325.values
arr79 = df126.values
arr80 = df226.values
arr81 = df326.values
arr82 = df127.values
arr83 = df227.values
arr84 = df327.values

# DATA GROUP F
dt = np.dtype([('code', 'S50'), 
               ('name', 'S50'),
               ('uomName', 'S50'),
               ('fillValue', 'f8'),
               ('dataType', 'S50'),
               ('lower', 'f8'),
               ('upper', 'f8'),
               ('closure', 'S50')])

swave = np.zeros((3,), dtype=dt)
swave[0] = ('waveHeight','Wave Height','meters',-9999.0,'f', 0.0, 360, 'geLtInterval')
swave[1] = ('waveHeightChange','Wave Height Change','enumeration',-9999.0,'f', 0.0, 360, 'geLtInterval')
swave[2] = ('probabilityOfHeightsExceeding','Probability of Heights Exceeding','meters',-9999.0,'f', 0.0, 360, 'geLtInterval')
#-9999 default, 0 terendah, 360 tertinggi, closure belum bisa nentuin
feacod = np.array(['SignificantWave'], dtype=np.string_)

# HEADER DATA
header = np.dtype([('waveHeight','f'), ('waveHeightChange','f'), ('probabilityOfHeightsExceeding','f')])
#positi = np.dtype([('longitude','f'),('latitude','f')])

# Konversi ke format ISO
dateTimeStart = datetime.strptime(df.iloc[0]['dateTimeStart'], '%d%m%Y %H:%M:%S')
dateTimeEnd = datetime.strptime(df.iloc[-1]['dateTimeEnd'], '%d%m%Y %H:%M:%S')

# Create a structured array to hold the data with the specified header
data1 = np.zeros((5, 7), dtype=header)
data2 = np.zeros((5, 7), dtype=header)
data3 = np.zeros((5, 7), dtype=header)
data4 = np.zeros((5, 7), dtype=header)
data5 = np.zeros((5, 7), dtype=header)
data6 = np.zeros((5, 7), dtype=header)
data7 = np.zeros((5, 7), dtype=header)
data8 = np.zeros((5, 7), dtype=header)
data9 = np.zeros((5, 7), dtype=header)
data10 = np.zeros((5, 7), dtype=header)
data11 = np.zeros((5, 7), dtype=header)
data12 = np.zeros((5, 7), dtype=header)
data13 = np.zeros((5, 7), dtype=header)
data14 = np.zeros((5, 7), dtype=header)
data15 = np.zeros((5, 7), dtype=header)
data16 = np.zeros((5, 7), dtype=header)
data17 = np.zeros((5, 7), dtype=header)
data18 = np.zeros((5, 7), dtype=header)
data19 = np.zeros((5, 7), dtype=header)
data20 = np.zeros((5, 7), dtype=header)
data21 = np.zeros((5, 7), dtype=header)
data22 = np.zeros((5, 7), dtype=header)
data23 = np.zeros((5, 7), dtype=header)
data24 = np.zeros((5, 7), dtype=header)
data25 = np.zeros((5, 7), dtype=header)
data26 = np.zeros((5, 7), dtype=header)
data27 = np.zeros((5, 7), dtype=header)
data28 = np.zeros((5, 7), dtype=header)

# Fill the structured array with data from arr1, arr2, and arr3
data1['waveHeight'] = arr1
data1['waveHeightChange'] = arr2
data1['probabilityOfHeightsExceeding'] = arr3
data2['waveHeight'] = arr4
data2['waveHeightChange'] = arr5
data2['probabilityOfHeightsExceeding'] = arr6
data3['waveHeight'] = arr7
data3['waveHeightChange'] = arr8
data3['probabilityOfHeightsExceeding'] = arr9
data4['waveHeight'] = arr10
data4['waveHeightChange'] = arr11
data4['probabilityOfHeightsExceeding'] = arr12
data5['waveHeight'] = arr13
data5['waveHeightChange'] = arr14
data5['probabilityOfHeightsExceeding'] = arr15
data6['waveHeight'] = arr16
data6['waveHeightChange'] = arr17
data6['probabilityOfHeightsExceeding'] = arr18
data7['waveHeight'] = arr19
data7['waveHeightChange'] = arr20
data7['probabilityOfHeightsExceeding'] = arr21
data8['waveHeight'] = arr22
data8['waveHeightChange'] = arr23
data8['probabilityOfHeightsExceeding'] = arr24
data9['waveHeight'] = arr25
data9['waveHeightChange'] = arr26
data9['probabilityOfHeightsExceeding'] = arr27
data10['waveHeight'] = arr28
data10['waveHeightChange'] = arr29
data10['probabilityOfHeightsExceeding'] = arr30
data11['waveHeight'] = arr31
data11['waveHeightChange'] = arr32
data11['probabilityOfHeightsExceeding'] = arr33
data12['waveHeight'] = arr34
data12['waveHeightChange'] = arr35
data12['probabilityOfHeightsExceeding'] = arr36
data13['waveHeight'] = arr37
data13['waveHeightChange'] = arr38
data13['probabilityOfHeightsExceeding'] = arr39
data14['waveHeight'] = arr40
data14['waveHeightChange'] = arr41
data14['probabilityOfHeightsExceeding'] = arr42
data15['waveHeight'] = arr43
data15['waveHeightChange'] = arr44
data15['probabilityOfHeightsExceeding'] = arr45
data16['waveHeight'] = arr46
data16['waveHeightChange'] = arr47
data16['probabilityOfHeightsExceeding'] = arr48
data17['waveHeight'] = arr49
data17['waveHeightChange'] = arr50
data17['probabilityOfHeightsExceeding'] = arr51
data18['waveHeight'] = arr52
data18['waveHeightChange'] = arr53
data18['probabilityOfHeightsExceeding'] = arr54
data19['waveHeight'] = arr55
data19['waveHeightChange'] = arr56
data19['probabilityOfHeightsExceeding'] = arr57
data20['waveHeight'] = arr58
data20['waveHeightChange'] = arr59
data20['probabilityOfHeightsExceeding'] = arr60
data21['waveHeight'] = arr61
data21['waveHeightChange'] = arr62
data21['probabilityOfHeightsExceeding'] = arr63
data22['waveHeight'] = arr64
data22['waveHeightChange'] = arr65
data22['probabilityOfHeightsExceeding'] = arr66
data23['waveHeight'] = arr67
data23['waveHeightChange'] = arr68
data23['probabilityOfHeightsExceeding'] = arr69
data24['waveHeight'] = arr70
data24['waveHeightChange'] = arr71
data24['probabilityOfHeightsExceeding'] = arr72
data25['waveHeight'] = arr73
data25['waveHeightChange'] = arr74
data25['probabilityOfHeightsExceeding'] = arr75
data26['waveHeight'] = arr76
data26['waveHeightChange'] = arr77
data26['probabilityOfHeightsExceeding'] = arr78
data27['waveHeight'] = arr79
data27['waveHeightChange'] = arr80
data27['probabilityOfHeightsExceeding'] = arr81
data28['waveHeight'] = arr82
data28['waveHeightChange'] = arr83
data28['probabilityOfHeightsExceeding'] = arr84

# Membuat file HDF5
with h5py.File('41XNAWHLOM.h5', 'w') as hdf:
    # FILE's MAIN METADATA
    hdf.attrs['productSpecification'] = 'INT.IHOS-100.5.0'
    hdf.attrs['issueTime'] = datetime.now().strftime('%H:%M:%S')
    hdf.attrs['issueDate'] = datetime.now().strftime('%d%m%Y')
    hdf.attrs['horizontalCRS'] = '1' #Geodetic 2d EPSG 4326
    hdf.attrs['horizontalDatumReference'] = '2'
    hdf.attrs['horizontalDatumValue'] = 'EPSG_4326'
    hdf.attrs['epoch'] = 'string'
    hdf.attrs['westBoundLongitude'] = '116.5'
    hdf.attrs['eastBoundLongitude'] = '115'
    hdf.attrs['southBoundLongitude'] = '-9'
    hdf.attrs['northBoundLongitude'] = '-7.9'
    hdf.attrs['geographicIdentifier'] = 'Lombok Strait'
    hdf.attrs['metadata'] = 'Not available' # Name of XML metadata file
    hdf.attrs['verticalCS'] = 'EPSG code; allowed values'
    hdf.attrs['verticalCoordinateBase'] = '1' # The base of the vertical coordinate system is the sea surface
    hdf.attrs['verticalDatumReference'] = 'only if vcb=2'
    hdf.attrs['verticalDatum'] = 'only if vcb=2' # 3 (MSL), 24 (local datum)
    hdf.attrs['metaFeatures'] = 'Not available' # Name of 8211 or GML file containing meta-features
    
    # GROUP F
    Group_F = hdf.create_group('Group_F')
    Group_F.create_dataset('WeatherCondition', dtype=dt, data=swave)
    Group_F.create_dataset('featureCode', data=feacod)
    
    # WeatherCondition group
    WeatherCondition = hdf.create_group('WeatherCondition')
    # Weather Condition Group Metadata
    WeatherCondition.attrs['dataCodingFormat'] = '2' #Regular Grid
    WeatherCondition.attrs['dimension'] = '2' # latitude and longitude
    WeatherCondition.attrs['commonPointRule'] = '3' # (high) Use the greatest of the attribute values
    WeatherCondition.attrs['horizontalPositionUncertainty'] = '-1.0'
    WeatherCondition.attrs['verticalUncertainty'] = '-1.0'
    WeatherCondition.attrs['timeUncertainty'] = '-1.0'
    WeatherCondition.attrs['numInstances'] = '1'
    # Additional because of DCF = 2
    WeatherCondition.attrs['sequencingRule.type'] = '1' #Linear
    WeatherCondition.attrs['sequencingRule.scanDirection'] = 'Longitude, Latitude'
    WeatherCondition.attrs['interpolationType'] = '10' #discrete, no interpolation method applies to the coverage
    WeatherCondition.attrs['validDateTime'] = hdf.attrs['issueTime']
    WeatherCondition.attrs['dateTimeStart'] = dateTimeStart.isoformat()
    WeatherCondition.attrs['dateTimeEnd'] = dateTimeEnd.isoformat()
    # Dataset
    WeatherCondition.create_dataset('axisNames', data= ['longitude','latitude'], dtype='S10')
    
    # SignificantWave group
    SignificantWave = WeatherCondition.create_group('SignificantWave')
    SignificantWave.attrs['westBoundLongitude'] = '116.5'
    SignificantWave.attrs['eastBoundLongitude'] = '115'
    SignificantWave.attrs['southBoundLongitude'] = '-9'
    SignificantWave.attrs['northBoundLongitude'] = '-7.9'
    SignificantWave.attrs['numberOfTimes'] = '28' # The total number of time records
    SignificantWave.attrs['timeRecordInterval'] = '21600' # The interval between time records (s)
    SignificantWave.attrs['dateTimeOfFirstRecord'] = dateTimeStart.isoformat()
    SignificantWave.attrs['dateTimeOfLastRecord'] = dateTimeEnd.isoformat()
    SignificantWave.attrs['numGRP'] = '28' # The number of data values groups contained in this instance group
    # Additional because of DCF 2
    SignificantWave.attrs['gridOriginLongitude'] = 'float'
    SignificantWave.attrs['gridOriginLatitude'] = 'float'
    SignificantWave.attrs['gridSpacingLongitudinal'] = '0.25' # cell size in arc degrees
    SignificantWave.attrs['gridSpacingLatitudinal'] = '0.25'
    SignificantWave.attrs['numPointsLongitudinal'] = '7'
    SignificantWave.attrs['numPointsLatitudinal'] = '5'
    SignificantWave.attrs['startSequence'] = '0,0'
    
    # Data Group_001
    Group_001 = SignificantWave.create_group('Group_001')
    Group_001.create_dataset('values',data=data1)
    # Metadata
    Group_001.attrs['dateTimeStart'] = df.iloc[0,0]
    Group_001.attrs['dateTimeEnd'] = df.iloc[0,1]
    
    # Data Group_002
    Group_002 = SignificantWave.create_group('Group_002')
    Group_002.create_dataset('values',data=data2)
    # Metadata
    Group_002.attrs['dateTimeStart'] = df.iloc[5,0]
    Group_002.attrs['dateTimeEnd'] = df.iloc[5,1]
    
    # Data Group_003
    Group_003 = SignificantWave.create_group('Group_003')
    Group_003.create_dataset('values',data=data3)
    # Metadata
    Group_003.attrs['dateTimeStart'] = df.iloc[10,0]
    Group_003.attrs['dateTimeEnd'] = df.iloc[10,1]
    
    # Data Group_004
    Group_004 = SignificantWave.create_group('Group_004')
    Group_004.create_dataset('values',data=data4)
    # Metadata
    Group_004.attrs['dateTimeStart'] = df.iloc[15,0]
    Group_004.attrs['dateTimeEnd'] = df.iloc[15,1]
    
    # Data Group_005
    Group_005 = SignificantWave.create_group('Group_005')
    Group_005.create_dataset('values',data=data5)
    # Metadata
    Group_005.attrs['dateTimeStart'] = df.iloc[20,0]
    Group_005.attrs['dateTimeEnd'] = df.iloc[20,1]
    
    # Data Group_006
    Group_006 = SignificantWave.create_group('Group_006')
    Group_006.create_dataset('values',data=data6)
    # Metadata
    Group_006.attrs['dateTimeStart'] = df.iloc[25,0]
    Group_006.attrs['dateTimeEnd'] = df.iloc[25,1]
    
    # Data Group_007
    Group_007 = SignificantWave.create_group('Group_007')
    Group_007.create_dataset('values',data=data7)
    # Metadata
    Group_007.attrs['dateTimeStart'] = df.iloc[30,0]
    Group_007.attrs['dateTimeEnd'] = df.iloc[30,1]
    
    # Data Group_008
    Group_008 = SignificantWave.create_group('Group_008')
    Group_008.create_dataset('values',data=data8)
    # Metadata
    Group_008.attrs['dateTimeStart'] = df.iloc[35,0]
    Group_008.attrs['dateTimeEnd'] = df.iloc[35,1]
    
    # Data Group_009
    Group_009 = SignificantWave.create_group('Group_009')
    Group_009.create_dataset('values',data=data9)
    # Metadata
    Group_009.attrs['dateTimeStart'] = df.iloc[40,0]
    Group_009.attrs['dateTimeEnd'] = df.iloc[40,1]
    
    # Data Group_010
    Group_010 = SignificantWave.create_group('Group_010')
    Group_010.create_dataset('values',data=data10)
    # Metadata
    Group_010.attrs['dateTimeStart'] = df.iloc[45,0]
    Group_010.attrs['dateTimeEnd'] = df.iloc[45,1]
    
    # Data Group_011
    Group_011 = SignificantWave.create_group('Group_011')
    Group_011.create_dataset('values',data=data11)
    # Metadata
    Group_011.attrs['dateTimeStart'] = df.iloc[50,0]
    Group_011.attrs['dateTimeEnd'] = df.iloc[50,1]
    
    # Data Group_012
    Group_012 = SignificantWave.create_group('Group_012')
    Group_012.create_dataset('values',data=data12)
    # Metadata
    Group_012.attrs['dateTimeStart'] = df.iloc[55,0]
    Group_012.attrs['dateTimeEnd'] = df.iloc[55,1]
    
    # Data Group_013
    Group_013 = SignificantWave.create_group('Group_013')
    Group_013.create_dataset('values',data=data13)
    # Metadata
    Group_013.attrs['dateTimeStart'] = df.iloc[60,0]
    Group_013.attrs['dateTimeEnd'] = df.iloc[60,1]
    
    # Data Group_014
    Group_014 = SignificantWave.create_group('Group_014')
    Group_014.create_dataset('values',data=data14)
    # Metadata
    Group_014.attrs['dateTimeStart'] = df.iloc[65,0]
    Group_014.attrs['dateTimeEnd'] = df.iloc[65,1]
    
    # Data Group_015
    Group_015 = SignificantWave.create_group('Group_015')
    Group_015.create_dataset('values',data=data15)
    # Metadata
    Group_015.attrs['dateTimeStart'] = df.iloc[70,0]
    Group_015.attrs['dateTimeEnd'] = df.iloc[70,1]
    
    # Data Group_016
    Group_016 = SignificantWave.create_group('Group_016')
    Group_016.create_dataset('values',data=data16)
    # Metadata
    Group_016.attrs['dateTimeStart'] = df.iloc[75,0]
    Group_016.attrs['dateTimeEnd'] = df.iloc[75,1]
    
    # Data Group_017
    Group_017 = SignificantWave.create_group('Group_017')
    Group_017.create_dataset('values',data=data17)
    # Metadata
    Group_017.attrs['dateTimeStart'] = df.iloc[80,0]
    Group_017.attrs['dateTimeEnd'] = df.iloc[80,1]
    
    # Data Group_018
    Group_018 = SignificantWave.create_group('Group_018')
    Group_018.create_dataset('values',data=data18)
    # Metadata
    Group_018.attrs['dateTimeStart'] = df.iloc[85,0]
    Group_018.attrs['dateTimeEnd'] = df.iloc[85,1]
    
    # Data Group_019
    Group_019 = SignificantWave.create_group('Group_019')
    Group_019.create_dataset('values',data=data19)
    # Metadata
    Group_019.attrs['dateTimeStart'] = df.iloc[90,0]
    Group_019.attrs['dateTimeEnd'] = df.iloc[90,1]
    
    # Data Group_020
    Group_020 = SignificantWave.create_group('Group_020')
    Group_020.create_dataset('values',data=data20)
    # Metadata
    Group_020.attrs['dateTimeStart'] = df.iloc[95,0]
    Group_020.attrs['dateTimeEnd'] = df.iloc[95,1]
    
    # Data Group_021
    Group_021 = SignificantWave.create_group('Group_021')
    Group_021.create_dataset('values',data=data21)
    # Metadata
    Group_021.attrs['dateTimeStart'] = df.iloc[100,0]
    Group_021.attrs['dateTimeEnd'] = df.iloc[100,1]
   
    # Data Group_022
    Group_022 = SignificantWave.create_group('Group_022')
    Group_022.create_dataset('values',data=data22)
    # Metadata
    Group_022.attrs['dateTimeStart'] = df.iloc[105,0]
    Group_022.attrs['dateTimeEnd'] = df.iloc[105,1]
    
    # Data Group_023
    Group_023 = SignificantWave.create_group('Group_023')
    Group_023.create_dataset('values',data=data23)
    # Metadata
    Group_023.attrs['dateTimeStart'] = df.iloc[110,0]
    Group_023.attrs['dateTimeEnd'] = df.iloc[110,1]
   
    # Data Group_024
    Group_024 = SignificantWave.create_group('Group_024')
    Group_024.create_dataset('values',data=data24)
    # Metadata
    Group_024.attrs['dateTimeStart'] = df.iloc[115,0]
    Group_024.attrs['dateTimeEnd'] = df.iloc[115,1]
    
    # Data Group_025
    Group_025 = SignificantWave.create_group('Group_025')
    Group_025.create_dataset('values',data=data25)
    # Metadata
    Group_025.attrs['dateTimeStart'] = df.iloc[120,0]
    Group_025.attrs['dateTimeEnd'] = df.iloc[120,1]
    
    # Data Group_026
    Group_026 = SignificantWave.create_group('Group_026')
    Group_026.create_dataset('values',data=data26)
    # Metadata
    Group_026.attrs['dateTimeStart'] = df.iloc[125,0]
    Group_026.attrs['dateTimeEnd'] = df.iloc[125,1]
    
    # Data Group_027
    Group_027 = SignificantWave.create_group('Group_027')
    Group_027.create_dataset('values',data=data27)
    # Metadata
    Group_027.attrs['dateTimeStart'] = df.iloc[130,0]
    Group_027.attrs['dateTimeEnd'] = df.iloc[130,1]
    
    # Data Group_028
    Group_028 = SignificantWave.create_group('Group_028')
    Group_028.create_dataset('values',data=data28)
    # Metadata
    Group_028.attrs['dateTimeStart'] = df.iloc[135,0]
    Group_028.attrs['dateTimeEnd'] = df.iloc[135,1]
    
print("File HDF5 telah dibuat di:", os.path.abspath('41XNAWHLOM.h5'))

storage.child(f'41XNAWHLOM{today_date}.h5').put(f'41XNAWHLOM.h5')

print("Data Telah Diupload")
