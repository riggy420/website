# site

Esstinally, this is source code for flask website 

Here is the tutorial for using this website: 

Esstinally, you will need to input the region and ID (For example: for SS-600600, it is region:"SS" stockID:"600600")

For america notes, it will be just inputting the stockID => "AAPL" 

So far, there is only three function that is activated : only "rise to 40 is not working"

Once inputted: 
* it will show a list of information
* * function that you have inputted
* * region : (Where yo you are)
* * ID : (Which stock are you checking))
* * last_updated : (Date that it has last updated))
* * result : (Calucation result)


Change log:

* 22-7
* successful attached the stylesheet and make everything align at cetner

* 23-7
* Have rewritten the code for page.py and have fixed the bugs in Rise_to_40 and have written some readMe.md and have modify the risk_assessment library to help display date_return

* 24-7
* Have kind of fixed the problem for finding one's agpd => Wasn't that successful as the formatting and \n character is kind of problem but at least it is kind of working as you can see the bunch of words that appears accordingly. But one problem remains that the ag value remains zero => May need to give another though to it. Besides, I have set up back the css document for result.html so that I can start formatting later on

* 29-7
* Implemented two buttons (Update in China and America) and can be able to check if there is any other function running actively in the terminal if you continue to access it. Next step: Implementing cookie/dynamic domanin's name????

* 8-4
* Finished Making a table and a search bar(Just copy :^)  NExt step: Dynamic domain name, (user login?) 

* 12-8
* Finished fixing the problem regarding the connection loss problem (It is somehow related to the runtime problem that I have, may need to figure out a better way to do so) and have drop down list about the different industry that i have  
* Porblem: The current database is not competent with the new format, we may need to fix it accordingly. Afterward, we may also need to figure it out with the data problem

* 14-8
* now, the database can accpet for pandas dataframe and normal txt file (pandas dataframe is only for industry P.S. may see for later) Besides. spectific country can also work with industry itself in the list. (May need to fix the datapath tho~~~)
* Problem remains: runtime error (Seems like my program is getting complicated over time) (may need to use the subprocess to deal with the thing) (flash is aqlso gone btw)

* 15-8 
* Now the program can mulitprocess, with mutliple shit running at the same time. However, there is a porblem, regarding the limit problem. If you go click on the button for a few times, it will go on forever.
* Problem: We may need to add lock and keys model => It can't autop generate the documents as well too for some reason (Can't keep it running )

* 2-9
* Two more buttons being added, which is going to be "Overview" (a button that allowed you to view all the status of the industry/concept) and a "Update ALl" function, which allows you to update all concept at once .. 
* Problems remains: Didn't really resolve the problem that is there previously sadge - may need to work hard to resolve it
* Further improvement: may also need to corporate with react to provide a more of a front end experience :^) 