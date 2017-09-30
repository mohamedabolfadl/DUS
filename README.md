# DUS
Apartment pricing in Düsseldorf

To run:

main_scraper.py:
  1. Check how many results are there for running the link:
  link = "https://www.immobilienscout24.de/Suche/S-T/P-"+str(pg)+"/Wohnung-Miete/Nordrhein-Westfalen/Duesseldorf/-/"+str(min_room)+",00-/"+str(min_area)+",00-/EURO--"+str(max_rent)+",00"

  2. Change tot_pages to the number of pages you want to scrape, and change the directory of phantomjs.exe

  3. Change the csv save file to the current date at the end of main_scraper.py and twice in analyzer.py

analyzer.py
  4. Run analyzer.py to get out.csv. If running Python 2.7: in clean_price uncomment 'x = inp.encode("utf-8")' and comment 'x = inp'. In clean_qm, uncomment 'x = x.encode("utf-8")'
  
  5. Do som power BI analytics on the output with power_BI postfix
  
time_to_x_combiner.py

  6. Run time_to_x_combiner to get train.csv
  
optimal.py

  7. Run optimal.py to get the top apartment expose IDs in result_df
  
Regressors.py

  8. Run Regressors.py to get the regressor models


