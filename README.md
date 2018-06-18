WhoScored Scraper Instructions

Using this scraper is easy, just follow these instructions and everything will be alright.

1. Don't panic.

2. Create 3 new folders inside of your scraper folder (whatever its name is):
	a) players_data
	b) players_urls
	c) teams_urls
These folders are used to organize the data and make everything cleaner.

3. Open selenium_func.py and read the comments above PATH_TO_DRIVER and PATH_TO_BROWSER.
These are instructions on how to use this script. You have to go to 

	http://selenium-python.readthedocs.io/installation.html

and download the appropriate driver for you. It depends on your operative system and
your browser. Then, search in Google how to find the path to your browser in your
particular operative system.

4. Open get_teams_urls.py

5. Choose a name for the file where the players' urls are going to be stored and write
it in the TEAMS_PATH constant. Remember to always wrap the names' file with quotes.

6. Then, uncomment the last two lines of code and run your script. After the script is done scraping, you will find a file named like TEAMS_PATH in your teams_urls folder.

7. Open get_players_urls.py

8. Write the name of your TEAMS_PATH on the constant with the same name. Choose a name for PLAYERS_PATH and for ERRORS_PATH.

9 Then, uncomment the last two lines of code and run your script. After the script is done scraping, you will find two files named like PLAYERS_PATH and ERRORS_PATH in your players_urls folder.

10. Open get_players_data.py

11. Write the name of your PLAYERS_URLS_PATH on the constant with the same name. Choose a name for DIVIDE_URLS_PATH, PLAYERS_DATA_PATH, ERRORS_PATH, and SEARCHED_TEAMS.

12. If your PLAYERS_URLS_PATH is too big and you want to divide your file to divide the time that the scraper will take to get the data, then go to the end of the script and uncomment the first # two comments (1. and 2.). The run the script. You will then divide your main urls' path into several files.

13. Then, to run the main scraper, first comment number 2. and uncomment the third # comment (3.). Inside of the run() function, there are written the constants that will be used for scraping. If you divided your main urls' file, then go to the constant DIVIDE_URLS_PATH and write the name of the first file that you will use for scraping. It will have a number inside of the name. Copy this number and add it to the name of PLAYERS_DATA_PATH, SEARCHED_TEAMS, and (this last one is optional) ERRORS_PATH.

14. Then, run your script. Each time the script is finished with scraping it will let you know. Then change the constants' names to read the second divided file (basically just change the current number to the next number). Run the script again until you have scraped all of the divided files.

15. By now, you already have your dataset. If you want to join the divided files then comment number 3. and uncomment number 4. and follow the instructions for the parameters' names. You can use this function to join your errors' files (if you chose to divide them in multiple files in step number 13. You can also use it to join the multiple datasets that where generated in step number 14.

16. If you want to mend the errors, just run the main function run() again (remember to comment and uncomment the appropriate lines.) with the errors' filename as DIVIDE_URLS_PATH.

17. Lastly, to finish, just uncomment number 5. (and comment 2., 3., and 4.) and fill in the appropriate names. players_data should be the complete dataset, players_data_extra should be the dataset you obtained after running the run() function with the errors' files; these are the players that were left out of the dataset because of errors. final_dataset should be the name of your final dataset, without extensions (write it in the constant DATASET). If you don't have an extra dataset, just leave players_data_extra with None.

18. After running step 17. you will have two dataset called DATASET.csv and DATASET.txt (DATASET is the name you chose for you final dataset). The first one is a comma separated file, and the second one a tab separated file. They will be stored in the players_data folder.

18. Now you're done! Congratulations! You have successfully scraped www.whoscored.com. Phewwww, what a journey! I hope you enjoyed it. Have a nice day, you devilish scraper person!# scraper-whoscored
