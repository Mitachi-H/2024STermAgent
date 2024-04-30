clear-log clean-log delete-log:
	@rm ./log/*.log

run:
ifeq ($(OS),Windows_NT)
	java --class-path ./src/;'./lib/*' net/kanolab/aiwolf/server/automatic/AutoGameStarter
else  # MacOS or Linux
	java --class-path ./src/:'./lib/*' net/kanolab/aiwolf/server/automatic/AutoGameStarter
endif