import utils; from utils import rf
def multiplyAll(inString): 
    # split on whitespace 
    numbers = inString.split()  

    # convert strings to integers
    for i in range(len(numbers)):  
        numbers[i] = int(numbers[i]) 

    # compute the product of the numbers array
    product = 1  
    for num in numbers: 
        product = product * num   
        
    # convert the product to a string, and return it
    productString = str(product) 
    return productString 

