# Line 1 to 20 are here to render the help output pretty, not to be read and even less understood!! :)
GREEN  := $(shell tput -Txterm setaf 2)
WHITE  := $(shell tput -Txterm setaf 7)
YELLOW := $(shell tput -Txterm setaf 3)
RESET  := $(shell tput -Txterm sgr0)
# From https://gist.github.com/prwhite/8168133#gistcomment-1727513
# Add the following 'help' target to your Makefile
# And add help text after each target name starting with ##
# A category can be added with @category
HELP_DESCRIPTION = \
    %help; \
    while(<>) { push @{$$help{$$2 // 'options'}}, [$$1, $$3] if /^([a-zA-Z\-]+)\s*:.*\#\#(?:@([a-zA-Z\-]+))?\s(.*)$$/ }; \
    print "usage: make [target]\n\n"; \
    for (sort keys %help) { \
    print "${WHITE}$$_:${RESET}\n"; \
    for (@{$$help{$$_}}) { \
    $$sep = " " x (32 - length $$_->[0]); \
    print "  ${YELLOW}$$_->[0]${RESET}$$sep${GREEN}$$_->[1]${RESET}\n"; \
    }; \
    print "\n"; }


help:		## Show this help.
	@perl -e '$(HELP_DESCRIPTION)' $(MAKEFILE_LIST)

setup:		##@setup Install the pre-commit
	pip install pre-commit
	pre-commit install

launch-jupyter:            ##@docker Launch a jupyter notebook from a fresh container
	docker exec ecodev_app jupyter notebook --no-browser --ip 0.0.0.0 --allow-root --port 5000

prod-launch:            ##@docker Launch production containers
	docker compose -f docker-compose.yml up -d

prod-build:            ##@docker build production image
	docker build --tag ecodev_app .

dev-build:            ##@docker build development image
	docker build --tag ecodev_app . -f Dockerfile-dev

all-tests:		##@tests Run all the tests
	docker exec ecodev_app python3 -m unittest discover tests
