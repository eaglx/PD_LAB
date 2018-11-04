import sys
import random
import numpy as np

suspecious_pairs = 0
suspecious_pairs_days = 0 
# Ile razy ta sama para spotkala sie w rozne dni
histogram = {}
suspecious_people = 0


if(len(sys.argv) < 6):
  print("Not enough args!!!")
  print("people_number hotels_number days_number probability amount_repetitions")
  exit()

people_number = int(sys.argv[1])
hotels_number = int(sys.argv[2])
days_number = int(sys.argv[3])
probability = float(sys.argv[4])
amount_repetitions = int(sys.argv[5])

print("Wejscie:")
print("people_number: ", people_number)
print("hotels_number: ", hotels_number)
print("days_number: ", days_number)
print("probability: ", probability)
print("amount_repetitions: ", amount_repetitions)
print("*********************************")

for i in range(amount_repetitions):
  r_suspecious_pairs = 0
  r_suspecious_pairs_days = 0
  r_histogram = {}
  count_meeting = np.zeros((people_number, people_number))
  people_in_hotels = []

  for day in range(days_number):
    people_in_hotels.clear()
    for k in range(people_number):
      people_in_hotels.append([])
    probability_person_go_hotel = np.random.rand(people_number)
    # Prawdopodobienstwo pojscia do hotelu
    for person in range(people_number):
      if probability_person_go_hotel[person] < probability:
        people_in_hotels[np.random.randint(hotels_number)].append(person)
    # Pary osob w danym hotelu 
    for hotel in people_in_hotels:
      for person in range(len(hotel)):
        for next_person in range(person + 1, len(hotel)):
          count_meeting[hotel[person]][hotel[next_person]] += 1

  r_suspecious_people = np.zeros(people_number)
  for person in range(people_number):
    for next_person in range(person + 1, people_number):
      analysis_pair = count_meeting[person][next_person]
      if analysis_pair > 1:
        r_suspecious_pairs += 1
        '''
        Osob_i_dni = (Spotkan_pary*(spotkan_pary-1))/2
        Maks podejrzanych osob: liczba_par * 2
        Min podejrzanych osob: (dla 10 jest 4, bo sqrt(2*10))
        '''
        r_suspecious_pairs_days += (analysis_pair * (analysis_pair-1)) // 2
        r_suspecious_people[person] = 1
        r_suspecious_people[next_person] = 1

      # Dane do histogramu
      if analysis_pair > 0:
        if analysis_pair in r_histogram:
          r_histogram[count_meeting[person][next_person]] += 1
        else:
          r_histogram[count_meeting[person][next_person]] = 1

  r_suspecious_amount_people = np.sum(r_suspecious_people)

  print("Iteracja: ", i+1)
  print("Podejrzane pary osob i dni: ", r_suspecious_pairs_days)
  print("Podejrzane pary: ", r_suspecious_pairs)
  print("Histogram: ", r_histogram)
  print("Liczba podejrzanych osob: ", r_suspecious_amount_people)
  print("***************************************")
  suspecious_pairs += r_suspecious_pairs
  suspecious_pairs_days += r_suspecious_pairs_days
  suspecious_people += r_suspecious_amount_people
  for key, value in r_histogram.items():
    if key in histogram:
      histogram[key] += value
    else:
      histogram[key] = value

print("\nWyniki ostateczne:")
print("Podejrzane pary osob i dni: ", suspecious_pairs_days // amount_repetitions)
print("Podejrzane pary: ", suspecious_pairs // amount_repetitions)
for key, value in histogram.items():
  histogram[key] = value // amount_repetitions
print("Histogram: ", histogram)
print("Liczba podejrzanych osob: ", suspecious_people // amount_repetitions)
