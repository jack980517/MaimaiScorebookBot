#MaimaiScorebookBot
##General Info
My own personal project. A scorebook for maimai ORANGE PLUS in regions where maimai is operated offline.<br>
Works as a bot for Telegram. Currently WIP. You can use it at [@maimaiscorebookbot](http://telegram.me/maimaiscorebookbot).<br>

Update 2016/08/30: The `!update` command is now fully working as intended. The `!query` command is not completed yet, and would return the raw values without explanation. Other filtering and sorting options are planned but not implemented yet.

Compared to spreadsheets, it has the following advantages:<br>
* Accessible in every platform on which Telegram is available, i.e. you don't need to worry about syncing the file between different devices
* Use little to none system resources, while spreadsheets this large would slow down the phone
* No need to navigate the grids: just type the data when updating your score.

##Usage
First: `pip install telepot`<br>
Then put your token in `token.txt` for the program to read and start `main.py`.

Works with Python 2.7.