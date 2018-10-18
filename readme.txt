Code structure:

1.	Program will accept user input through command line arguemnets.
	It will accept the input in the following format:
		find_route uninf input1.txt London Frankfurt
		find_route inf input1.txt Munich Kassel h_kassel.txt

2.	Flow of the code:
	i.	User input would be accepted in the main.
	ii.	According to the input given searchAS or searchUCS function will be called.

3. Possible output:

	distance: 455 km
	route: 
	Bremen to Dortmund, 234 km 
	Dortmund to Frankfurt, 221 km 

	and

	distance: infinity
	route: 
	none
