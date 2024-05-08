This is a web-based Exposure Time Calculator (ETC) intended for deployment to the [Lockhart Planetarium](http://www.physics.umanitoba.ca/astro/?page_id=8) website. The current version only supports calculations for point sources, support for extended sources is to be added in the future. This application was made in collaboration with GitHub user RJWeir. 


##### Installation Requirements
	Python 3.8 or higher
	PyScript
	NumPy
	SciPy
	matplotlib


### Local Usage
To run the ETC without deployment, open a terminal window in the same directory as the following files
```
ETC.py
index.html
config.json
```
Run the following command to initialize a local server

```
python3 -m http.server
```

In a browser, enter the following URL
```
http://localhost:8000/server
```
This opens a local session of the ETC which will run as long as the previous command is active in the terminal.


### Website
This feature will be supported in a future release. 
