import pyscript
from pyscript import document

from js import console




def test(array):

    word = array[0]
    
    print(word)

    element = document.createElement('h1')
    element.innerText = "Hello"
    document.getElementById("output").append(element)
    
    
    #https://stackoverflow.com/questions/72197815/html-output-in-pyscript
    
    
    
