# 19.01.2025
import datetime as dt
ostatnie_zajecia = dt.datetime(2024,12,17)
kolokwium = dt.datetime(2025,1,19)
data_dzisiejsza = dt.datetime.now()
dni_do_kolokwium = (kolokwium-data_dzisiejsza).days
dni_od_ostatnich_zajec=(data_dzisiejsza-ostatnie_zajecia).days
print(f"Mineło {dni_od_ostatnich_zajec} dni od ostatnich zajęć w grudniu, zostało {dni_do_kolokwium} dni do kolokwium")