SHELL=/bin/bash

init:
		docker-compose -p kb -f notebook.yml up --build

notebook:
		docker-compose -p kb -f notebook.yml up --no-build

# https://stackoverflow.com/questions/32343607/how-can-i-set-the-current-working-directory-for-docker-exec-with-an-internal-bas
bash:
		docker exec -w /app/leetcode -it kb_nbk_1 "bash"
