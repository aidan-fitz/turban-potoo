# Cleans out the bytecode files
squeaky-clean: clean
	rm -f *.pyc *.png *.gif

# Cleans out the folder but keeps the .pyc bytecode files
# This makes it faster the next time you run
# -f means don't cough up error when files aren't deleted
clean:
	rm -f *~ *.ppm
