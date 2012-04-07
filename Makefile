default:

rebase:
	git pull upstream master
	git push
	source bin/activate && pip install -r requirements.txt
