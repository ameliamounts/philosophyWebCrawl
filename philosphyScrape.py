import sys
import requests
from bs4 import BeautifulSoup



def firstLink(currentURL):
    """
    Ingests a link to a wikipedia page and returns the first non-italicized link in the body text
    """
    page = requests.get(currentURL)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup.i.decompose() # removes all italics tags in soup

    
    paras = soup.find_all('p') 
    # find all paragraph tags and iterate through each
    for para in paras:
        links = (BeautifulSoup(str(para), features='html.parser')).find_all('a', href=True) 
        # find all links with an href tag and iterate through them
        for link in links:
            # check that it goes to a wikipedia page
            if 'wiki/' in (link['href']): 
                # check that it's not a file, not religious philosophy and not a help page (those lead to loops)
                if 'file' not in (link['href']).lower():
                    if link['href']!="/wiki/Religious_philosophy" and 'help' not in (link['href'].lower()):
                        # return the first link found that fits all of this criteria
                        return 'https://en.wikipedia.org' + link['href']

    # if no link found, return None, this is handled in the main code
    return None





def main(args):
    """
    This will have a global variable count and will check if the link returned by the firstLink is equal to the philosophy link
    """
    # link counter and url history dictionary are initialized
    counter = 0
    urlDict = {}
    currentURL = args[0]

    # make sure the inputted url is a wikipedia page 
    page = requests.get(currentURL)
    if (("https://en.wikipedia.org/wiki/" in currentURL) == False) or page.status_code!=200:
        print("Invalid URL")
        return
    
    while currentURL.lower() != "https://en.wikipedia.org/wiki/philosophy":
        
        print(currentURL) 
        if counter>100: 
            print("Philosophy could not be found in under 100 clicks...")
            return
        
        currentURL = firstLink(currentURL)
        # add url to history dictionary unless None
        if currentURL == None:
            print("No links found, search reached a dead end.")
            return

        elif currentURL in urlDict:
            print("In a loop, search terminated after %d clicks." %counter)
            return

        else:
            urlDict[currentURL] = 1 

        # increment the clicks counter
        counter+=1
        

    print("Philosophy was found in %d clicks!" %counter)
    return
    

main(sys.argv[1:])