SHELL=/bin/bash

init:
		@docker-compose -f notebook.yml up --build

notebook:
		@docker-compose -f notebook.yml up --no-build
