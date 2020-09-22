from sys import argv
from sys import exit
from ventilation_system import VentilationSystem

if (len(argv) < 2):
    print("invalid input")
    exit(1)
vsys = VentilationSystem()
if argv[1] == 'rep':
    vsys.periodical_report(argv[2])
elif argv[1] == 'wrn':
    vsys.weather.set_weather(argv[2])
    vsys.warning(argv[3], argv[4])
