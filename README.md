# PullRepoScript
A simple Python script providing a GUI interface to pull multiple at once.

## Manual Execution
* Place `PullRepos.py` in the parent directory containing your repositories.
* From the terminal, navigate to the directory and run `python PullRepos.py`
* You should now see a dialog with all of the repositories found in the directory.
![GUI](https://www.upnad.am/images/gui.png)

## As a Cron Job
* From the terminal navigate to your root directory and open crontab: `cd ~/. && crontab -e`
* Add an entry for the new job at an [interval of your choosing](https://opensource.com/article/17/11/how-use-cron-linux) to navigate to, and run the script.
```
// Example: To run the script once at 9:00AM each morning, your entry would be:
00 09 * * * cd /Users/youruserid/yourdirectory && python PullRepos.py
```
* Save and exit the editor. You can confirm your job is scheduled by running crontab - l to print all of your scheduled Cron jobs.
