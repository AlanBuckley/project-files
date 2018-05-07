# project-files

This is the repository for my final year project
Identifying Cyberbullying and Analyzing Emotions in Twitter. 

To run this repository follow the steps below:

1: Clone/download the repo

2: Im port all necessary packages and files. see requirements.txt

3: To download files from twitter API, edit the credentials in the file and enter the username/twitter-handle of the account you wish to get tweets from.

4: To run the emotion analysis file, enter the command 'python emotion-analysis.py' in the command prompt. The results will be saved to the db and displayed on the dashboard.

5: To run the Cyberbullying dection algorithm, enter 'python CyberBullying_classifier.py' in the command prompt.
in order to run this classifier you need a tweets file containing the tweets you want classified, a Test_Answers file containing the expected outcome of each tweet, a good-corpus.txt file and bad-corpus.txt file.

6: Finally to run the application locally enter the command 'python manage.py runserver'
(make sure all packegs and frameworks are installed such as python and django.)
