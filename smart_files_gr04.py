import os , math
def unwanted_character(ligne: str)-> list:
    """    
    This function cleans a string given by deleting the ponctuation, the stopwords and the words less than 3 letters 
    
    Parameters:
    -----------
    ligne : the line we want to clean (str)


    Returns:
    --------
    ligne : cleaned line (list)

    """
    #Creating the list that contains the 'stopwords' that are high frequency words in english 
    ponctuation = ['?', '.', ',', ';', ':', '\n', '!', '"', "'", '(', ')', '{', '}']
    stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", 
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", 
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", 
    "i", "i'd", "i'll", "i'm", "i've", "if", "in","from", "into", "is", "isn't", "it", "it's", "its", "itself", 
    "let's", "me", "more", "most", "mustn't", "my", "myself","no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", 
    "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", 
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", 
    "under", "until", "up","very","was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", 
    "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]
    
    #Cleaning the line 
    for character in ligne : 
        if character in stop_words or character in ponctuation : 
            ligne = ligne.replace(character, ' ')
    ligne = ligne.split()
    i = 0
    #Cleaning from the words that have less than three letters 
    while i < len(ligne) : 
        if len(ligne[i]) < 3 :
            del(ligne[i])
        else : 
            i = i + 1 
    return ligne 

def apprentissage(path:str) -> dict: 
    """
    This function creates a data structure that contains the number of occurence of each word in all the files of each theme in the sorted directory

    Parameters :
    ------------ 
    path :The path of the file that contains all our files (str)


    Returns :
    ---------
    base : the dictionnary that contains the number of occurence of each words in each file of each theme of the sorted file and the total number of words in the theme


    Notes : 
    -------
    The data structure : 
    base = {'theme_1': {'nb_apparition':{'word1 : int , 'word2' : int }, 'Total de mot': int} , 'theme_2': {'nb_apparition':{'word1 : int , 'word2' : int }}

    we have chosen a dictionnary for our data structure, because we need to identify uniquely each theme of the sorted file by its own name, and each theme needs to have its own information seperately 
    we found that it will be easier to organise the number of occurence in a dictionnary so that if we want to get the number of occurence of a specific word in a theme 
    we will get it just by calling : base['theme']['nb_apparition']['the word'] and ,also because the dictionnary offers the possibility to change easily the values just by affecting a new one 
    for exemple if we want to change the number of occurence of a word we just assign it to a new number base['theme']['nb_apparition']['the word'] = int which is very useful in incrementing the number of occurences
    """
    #Initialising of the data base
    base = {} 
    #Get all theme from the sorted directory
    themes = os.listdir('%s/sorted'%path) 

    for theme in themes : 
        base[theme] = {}

        #Initialization of occurance 
        base[theme]['nb_apparition'] = {}

        #Initialization of the total number of words
        base[theme]['Total de mot'] = 0 

        #Browse all files for each theme
        for sous_rep in os.listdir('%s/sorted/%s'%(path,theme)) :
            fh = open('%s/sorted/%s/%s'%(path,theme,sous_rep),'r')
            for line in fh.readlines() :#Read the file line by line
                line = line.lower()
                line = unwanted_character(line)#Clean the line          
                for mot in line :#browse all the words 
                    if mot in base[theme]['nb_apparition'] :#if the word is already in our database  
                        base[theme]['nb_apparition'][mot] = base[theme]['nb_apparition'][mot]+ 1 #we increment its occurence
                    else : 
                        base[theme]['nb_apparition'][mot] = 1 #if not we affect the number one in its occurence 
                    base[theme]['Total de mot'] = base[theme]['Total de mot'] + 1 
    fh.close()
    return base


def calculate_score(path : str ,base : dict ) -> dict: 
    """
    This function calculates the score of the themes of each file in the unsorted directory and classify them in a dictionnary 

    Parameters : 
    ------------
    path :The path of the file that contains all our files (str)
    base : The data structure that contains all the words, their number of occurence, and the total number of words, in each theme (dict)

    Returns : 
    ---------
    par_theme : the dictionnary that contains the score of the themes of each file of the unsorted directory (dict)

    Notes :
    -------
    the Data structure : 
    par_theme = {'file_1' : {'theme_1': score(int) ,'theme_2' : score(int) }, 'file_2' : {'theme_1': score(int) ,'theme_2' : score(int) }}

    we have chosen a dictionnary for our data structure , because we need to stock the information of each file in the unsorted directory seperately, so the files
    should be uniquely identifed by their name (5478 for exemple) 
    since each file should contain two seperate information we will create a dictionnary that organise the score of the first theme and the score of the second, in this way 
    it will be easier to access the score of a theme just by calling: par_theme['file_1']['theme_1'] and we will get the score of the file_1 for the theme_1 which is very useful
    for the comparaison in the classifying part 
    """
    #Initialization our data base 
    par_theme ={}

    #Browse all files of unsorted 
    for file in os.listdir('%s/unsorted'%path) : 
        par_theme[file] = {} 
        for theme in base : #categorize the scores by theme to compare and decide at the end
            score = 0
            fd = open('%s/unsorted/%s'%(path,file),'r') 
            for line in fd.readlines() : #Clean the line 
                line = line.lower()
                line = unwanted_character(line)
                for mot in line : #Read every words to check if it existe in our data base, if yes we calculate the probability, if no we assume that it as already occurde 
                    if mot in base[theme]['nb_apparition'] : 
                        proba = (base[theme]['nb_apparition'][mot]) / base[theme]['Total de mot'] #Calculate the probability  
                    else : 
                        proba  = 1 / base[theme]['Total de mot']
                    score = score + math.log(proba) #Calculate the score 
            par_theme[file][theme] = score #associate the score to the theme
    fd.close()
    return par_theme

def smart_sort_files(path: str ) -> None : 
    """
    This function creates the sorted_2 directory containing the themes and the files of the unsorted directory well classified 

    Parameters : 
    ------------
    path : The path of the file that contains all our files (str)



    """
    #Retrieval of the model and scores
    base = apprentissage(path)
    dico = calculate_score(path, base)

    #Creation of directory sorted_2 
    if not os.path.exists('%s/sorted_2'%path): 
        os.mkdir('%s/sorted_2'%path)
    
    #Retrieving themes to create subdirectories of sorted_2
    themes = [theme for theme in base]
    for i in range(len(themes)): 
        if not os.path.exists('%s/sorted_2/%s'%(path,themes[i])): 
            os.mkdir('%s/sorted_2/%s'%(path,themes[i])) 
     
    #Retrieving the maximum score for each file
    for file in dico : 
        maximum = dico[file][themes[0]]
        theme_voulu = themes[0]
        for theme in themes :
            if dico[file][theme] > maximum : 
                theme_voulu = theme #Only keep the theme with higher score

        fh = open('%s/unsorted/%s'%(path,file),'r') # Open the original file in sorted
        fd = open('%s/sorted_2/%s/%s'%(path,theme_voulu,file),'w') # Open the file in directory sorted_2 in writting mode to create it at the same time
        lines = fh.read() # Copy all data of the filer 
        fd.write(lines) #Rewrite the data in our new file
    fd.close()
    fh.close()

def check_accuracy(path:str) : 
    """
    This function calculate the accuracy of our model and prints it 

    Parameters:
    -----------
    path : The path of the file that contains all our files (str)
    """
    # Retrieving the number of all files for use in precision calculations
    sigma = len(os.listdir('%s/unsorted'%path))

    #Read the labels file
    fh = open('%s/labels.txt'%path,'r')

    #create our dictionnary as a correction to compare 
    corrige = {}

    
    for line in fh.readlines() : 
        line = line[:-1].split()
        corrige[line[0]] = line[1]

    correct_classification = 0 #Initialise the correct classification

    #Browse through all the files in the sorted_2 directory and compare each theme with the answer key 
    for theme in os.listdir('%s/sorted_2'%path) : 
        for file in os.listdir('%s/sorted_2/%s'%(path,theme)) : 
            for corrected_file in corrige : 
                if corrected_file == file :#Finding the correct file
                    if corrige[corrected_file] == theme :
                        correct_classification += 1
    
    accuracy = (correct_classification/(sigma))*100
                    
                    
    
    
    fh.close()
    print(accuracy)


smart_sort_files('./archive_3')
check_accuracy('./archive_3')
