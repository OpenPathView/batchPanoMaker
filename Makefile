.PHONY: filemanager api stop

filemanager:
	python filemanager/server.py run --storage-location=/tmp --debug &> /tmp/filemanager.log &
api:
	python api/server.py run --debug &> /tmp/api.log &

stop:
	@http -b POST :5000/shutdown
	@http -b POST :5001/shutdown

start: filemanager api
	@sleep 1 # Wait one second that every server correctly started

tests: start
	pytest; STATUS=$?; make stop; exit $(STATUS)

# vim: noexpandtab filetype=make
