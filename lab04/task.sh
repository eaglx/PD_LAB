#!/bin/bash
# TASK_1 ************************************************************** Ranking popul. pisoenek
task1Fun() {
  awk -F'<SEP>' '{
    listen[$2]++;
  }
  END {
    for (key in listen) {
      print key "\v" listen[key] > "/dev/shm/ex_1_1.tmp"
    }
  }' samples_formatted.txt
  sort --numeric-sort -t $'\v' -k 2 -r /dev/shm/ex_1_1.tmp | head -n 10 > /dev/shm/ex_1_2.tmp
  # ^ wylistowanie 10 najpopular
  sort -t $'\v' -k 1 /dev/shm/ex_1_2.tmp > /dev/shm/ex_1_3.tmp # Posortuj według indeksu
  join -1 1 -t $'\v' /dev/shm/ex_1_3.tmp tracks_unique.txt > /dev/shm/ex_1_4.tmp # Dodaj tytuł
  sort --numeric-sort -t $'\v' -k 2 -r /dev/shm/ex_1_4.tmp > /dev/shm/ex_1_5.tmp # Sortowanie po ilości wystąpień
  awk -F $'\v' '{ print $4 " " $3 " " $2 }' /dev/shm/ex_1_5.tmp > /dev/shm/task1_sol.txt
  rm /dev/shm/ex_1_1.tmp /dev/shm/ex_1_2.tmp /dev/shm/ex_1_3.tmp /dev/shm/ex_1_4.tmp /dev/shm/ex_1_5.tmp
}
# TASK_2 ************************************************************** Ranking użytkowników
task2Fun() {
  awk -F'<SEP>' '{
    listen[$1][$2] = 1
  }
  END {
    for (key in listen) {
      print key " " length(listen[key]) > "/dev/shm/ex_2.tmp"
    }
  }' samples_formatted.txt
  sort --numeric-sort -k2 -r /dev/shm/ex_2.tmp | head -n 10  > /dev/shm/task2_sol.txt
  rm /dev/shm/ex_2.tmp
}
# TASK_3 **************************************************************Artysta z naj. odsłuch
task3Fun() {
  # Policz odsłuch piosenek
  awk -F'<SEP>' '{
    listen[$2]++;
  }
  END {
    for (key in listen) {
      print key "\v" listen[key] > "/dev/shm/ex_3_1.tmp"
    }
  }' samples_formatted.txt
  sort -t $'\v' -k 1 /dev/shm/ex_3_1.tmp > /dev/shm/ex_3_2.tmp # sort art
  join -1 1 -t $'\v' /dev/shm/ex_3_2.tmp tracks_unique.txt > /dev/shm/ex_3_3.tmp # Dodanie nazwy artyst i tytuł piosenki
  # Sumowanie odsłuchani pisoenek danego artysty
  awk -F $'\v' '{
    listen[$3] += $2;
  }
  END {
    for (key in listen) {
      print key "\v" listen[key] > "/dev/shm/ex_3_4.tmp"
    }
  }' /dev/shm/ex_3_3.tmp
  sort --numeric-sort -t $'\v' -k 2 -r /dev/shm/ex_3_4.tmp > /dev/shm/ex_3_5.tmp # Sorotwanie wzgędem ilości odsłuchań
  head -n 1 /dev/shm/ex_3_5.tmp | tr '\v' ' ' > /dev/shm/task3_sol.txt
  rm /dev/shm/ex_3_1.tmp /dev/shm/ex_3_2.tmp /dev/shm/ex_3_3.tmp /dev/shm/ex_3_4.tmp /dev/shm/ex_3_5.tmp
}
# TASK_4 **************************************************************Liczba odsłuch w miesiacach
task4Fun() {
  awk -F'<SEP>' '{
    split($4, date, "-");
    months[date[2]]++;
  }
  END {
    n = asorti(months, indexes);

    for (i = 1; i <= n; i++) {
      print i " " months[indexes[i]];
    }
  }' samples_formatted.txt  > /dev/shm/task4_sol.txt
}
# TASK_5 **************************************************************Uzytk, odsłuch queen popular
task5Fun() {
  # Wyszukanie piosenek queen
  awk -F $'\v' '{
    if ($2 == "Queen") {
      print $1 > "/dev/shm/ex_5_1.tmp"
    }
  }' tracks_unique.txt
  # Policzenie piosenek 5.3, a 5.2 pole 1 to id usera
  awk -F '<SEP>' '
  FNR==NR {
    queen[$1] = $1
  }
  FNR!=NR {
    if ($2 in queen) {
      listen[$2]++
      print $1 " " $2 > "/dev/shm/ex_5_2.tmp"
    }
  }
  END {
    for (key in listen) {
      print key " " listen[key] > "/dev/shm/ex_5_3.tmp"
    }
  }' /dev/shm/ex_5_1.tmp samples_formatted.txt
  sort --numeric-sort -k 2 -r /dev/shm/ex_5_3.tmp | head -n 3 > /dev/shm/ex_5_4.tmp # 3 piosenki
  sort /dev/shm/ex_5_2.tmp | uniq > /dev/shm/ex_5_5.tmp
  awk 'FNR==NR {
    queen[$1] = $1
  }
  FNR!=NR {
    if ($2 in queen) {
      listen[$1]++
    }
  }
  END {
    for (key in listen) {
      print key " " listen[key] > "/dev/shm/ex_5_6.tmp"
    }
  }' /dev/shm/ex_5_4.tmp /dev/shm/ex_5_5.tmp
  sort --numeric-sort -k 2 -r /dev/shm/ex_5_6.tmp > /dev/shm/ex_5_7.tmp #Przesłuchali 3 pisoenki
  awk '{
    if ($2 == "3") {
      print $1 > "/dev/shm/ex_5_8.tmp"
    }
  }' /dev/shm/ex_5_7.tmp
  sort /dev/shm/ex_5_8.tmp | head -n 10  > /dev/shm/task5_sol.txt
  rm /dev/shm/ex_5_1.tmp /dev/shm/ex_5_2.tmp /dev/shm/ex_5_3.tmp /dev/shm/ex_5_4.tmp /dev/shm/ex_5_5.tmp /dev/shm/ex_5_6.tmp /dev/shm/ex_5_7.tmp /dev/shm/ex_5_8.tmp
}
# *********************************************************************
TZ=GMT0;
export TZ;
set -m # Enable Job Control
# Zmiana ISO-8859-2 na UTF-8
iconv -t UTF-8 -f ISO-8859-2 unique_tracks.txt > utf_qt.txt
# Usuń track_id
sed -i -e $'s/<SEP>/\v/g' utf_qt.txt # Zmień <SEP> na tab
cut -d $'\v' -f 2- utf_qt.txt > tracks.txt
rm utf_qt.txt
# Usuń duplikaty
sort --output=sorted_tracks.txt tracks.txt
uniq -i sorted_tracks.txt tracks_unique.txt
rm tracks.txt sorted_tracks.txt
# Data
awk -F'<SEP>' '{
  year_month_day = strftime("%Y-%m-%d", $3);
  date[year_month_day] = 1
  print $0 FS year_month_day > "samples_formatted.txt"
}
END {
  n = asorti(date, indexes);
  for (i = 1; i <= n; i++) {
    split(indexes[i], array, "-");
    print indexes[i] "," array[1] "," array[2] "," array[3] > "dates.txt"
  }
}' triplets_sample_20p.txt
task1Fun &
task2Fun &
task3Fun &
task4Fun &
task5Fun &
# Wait for all parallel jobs to finish
while [ 1 ]; do fg 2> /dev/null; [ $? == 1 ] && break; done
reset
cat  /dev/shm/task1_sol.txt
echo
cat  /dev/shm/task2_sol.txt
echo
cat  /dev/shm/task3_sol.txt
echo
cat  /dev/shm/task4_sol.txt
echo
cat  /dev/shm/task5_sol.txt
echo
rm  /dev/shm/task1_sol.txt  /dev/shm/task2_sol.txt /dev/shm/task3_sol.txt /dev/shm/task4_sol.txt /dev/shm/task5_sol.txt
