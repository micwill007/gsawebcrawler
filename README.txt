GSA Advantage web scraper


========== 
Installation ==========

1. Install python 3.5+ from https://www.python.org/downloads/ 

!IMPORTANT! When installing, make sure the PATH variable is added (it should be a checkbox early on in the installation).



2. Place the gsawebscraper folder onto your desktop.


3. Go to your windows search bar and open cmd. (type 'cmd' and hit enter)


4: type these out and hit return (not the a. and b., just cd 'Desktop/gsawebscraper'. It is case sensitive as well.)
	
    a. cd Desktop/gsawebscraper
	
    b. python pipinstaller.py



6: type this out to run the main program
  
    a. python main.py

7. Follow the GUI instructions. Make sure proxy is HTTPS and set Country to United States. See image in directory for a screen shot. Please read the "Checkboxes" Section for more detail.
  a. Example input: 198.0.0.1:9000 (Don't forget to add the port).

8. Once the search checkbox is checked and you hit the Run your browser will pop up and you will see the program pulling information in real time. Do not close this browser.

9. Now that the first script has obtained the correct URLs, you can now uncheck the search checkbox and check the scrape checkbox. 

10. Hit run and the final CSV will be created.




==========
 Checkboxes
 ==========



I have not added the functionality to run these back-to-back - only check one of these boxes - or it may break.

 The 'search' checkbox is the first half of the script, which performs a search on GSA advantage for each product in the tony-export.csv file. It then grabs the search results and throws everything into productnumbers.csv.

 The 'scrape' checkbox is the second half of the script, which requests the links and grabs the pricing/vendor data and places them into final.csv. 

Grabbing a free https proxy is necessary for both scripts. Without using a proxy, they may blacklist your companies IP address! So if you have any questions on getting the proxy to work give us a call.


========== Troubleshooting ==========

'python' is not recognized as an internal or external command, operable program or batch file.
    This likely occured because you didn't check the "Add Python to PATH" option upon installation. You can rerun the python executable that you downloaded to uninstall. Run again to reinstall.
