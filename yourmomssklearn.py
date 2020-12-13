from sklearn import linear_model
import numpy
from pprint import pprint

# Only works for Aberporth rn, too lazy

"""
========== MODEL: TIME => TEMPERATURE ==========
"""

with open('Temperature Data/aberporthdata.txt', 'r') as txt:
    temperature_data = txt.readlines()
    temperature_data = [entry.split() for entry in temperature_data]
    temperature_data = temperature_data[7:]

time_x = []
temperature_y = []

for entry in temperature_data:
    if entry[2] != '---' and entry[3] != '---':
        year = float(entry[0])
        month = float(entry[1])
        time = year + (month - 1) / 12
        mean_temperature = (float(entry[2]) + float(entry[3])) / 2
        time_x.append([time])
        temperature_y.append(mean_temperature)

time_x, temperature_y = numpy.array(time_x), numpy.array(temperature_y)
time_to_temperature_model = linear_model.LinearRegression()
time_to_temperature_model.fit(time_x, temperature_y)
# time_to_temperature_model can now take time and give temperature

# print(time_to_temperature_model.predict([[2020]]))
# print(time_to_temperature_model.predict([[2050]]))

"""
========== MODEL: TEMPERATURE => ECOLI ==========
"""

from misc1 import find_closest_weather_stations
from e_coli_data import total_infections_by_codes

# Using Hyak's api
ecoli_file_name = 'Monthly E.Coli 2012-2020 with Location.csv'
temperature_dir = 'Temperature Data'
weather_stations = find_closest_weather_stations(ecoli_file_name, temperature_dir)
ecoli = total_infections_by_codes(weather_stations['Aberporth']).to_frame()
ecoli_time = ecoli.index.tolist()
ecoli_time = [time[:7] for time in ecoli_time]
ecoli_value = ecoli.values.tolist()

temperature_x = []
ecoli_y = []

for entry in temperature_data:
    year = entry[0]
    month = entry[1]
    time = "{}-{}".format(year, month)
    if time in ecoli_time:
        mean_temperature = (float(entry[2]) + float(entry[3])) / 2
        ecoli_index = ecoli_time.index(time)
        ecoli = ecoli_value[ecoli_index][0]
        temperature_x.append([mean_temperature])
        ecoli_y.append(ecoli)

temperature_x, ecoli_y = numpy.array(temperature_x), numpy.array(ecoli_y)
temperature_to_ecoli_model = linear_model.LinearRegression()
temperature_to_ecoli_model.fit(temperature_x, ecoli_y)
# temperature_to_ecoli_model can now take temperature and give ecoli

# print(temperature_to_ecoli_model.predict([[10]]))
# print(temperature_to_ecoli_model.predict([[20]]))

"""
========== PROFIT ==========
"""

years_to_predict = [2020, 2100, 2500, 10000]

for year in years_to_predict:
    temperature_prediction = time_to_temperature_model.predict([[year]])[0]
    ecoli_prediction = temperature_to_ecoli_model.predict([[temperature_prediction]])
    print("ecoli prediction for {}: {}".format(year, ecoli_prediction))
