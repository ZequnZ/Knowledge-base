SHELL=/bin/bash

init:
		@docker-compose -p kb -f notebook.yml up --build

notebook:
		@docker-compose -p kb -f notebook.yml up --no-build

bash:
		@docker exec -it kb_nbk_1 "bash"
