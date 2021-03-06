import data_collector
import query
# TODO: Validate email. Decide if there are password rules. Decide how user retrieves password if they lose it.
# Decide how this will be done how far I will go
def isValidEmail(email):
    if email == "":
        return False
    return True

# TODO: Make better check auth key function
def isValidAuthKey(authKey):
    return True

# TODO: Make better auth link function
def authenticateLink(link):
    if link == "":
        return False
    return True

def main():
    # Create Query object. 
    queryMaster = query.Query()
    # In API, user entered email address
    email = input("Please enter your email address or any unique username: ")
    while isValidEmail(email) is False:
        email = input("Invalid email, please try again: ")
    # Email Does exist, enter it, enter password 
    if queryMaster.doesAccountExist(email):
        password = input("Account exists, please enter your password: ") 
        i = 0
        while (queryMaster.authenticate(email, password) is False):
            if i == 2:
                print("Three invalid log in attempt. Exiting program. Goodbye.")
                return
            password = input("Invalid attempt. Please enter your password: ")
            i += 1
    else:
        ans = input("Account does not exist. Would you like to create an account? (Y/N): ")
        if ans is "Y" or ans is "y":
            # Allow user to create an account
            password = input("Please enter password: ")
            # TODO: Enter auth key validation here
            queryMaster.createAccount(email, password)
        elif ans is "N" or ans is "n":
            print("Answer was no. Exiting program. Goodbye.")
            return
        else:
            print("Invalid answer. Exiting program. Goodbye.")
    #They are in! Now allow email alone to query information.

    #They can now query data with their email and password
    userData = [email, password]

    while True:
        command = input("Please enter a command: ")
        if (command == 'Help'):
            print("Possible commands: \nHelp, \nCreateAnalysis, \nRetrieveAllAnalysisSummaries, \nRetrieveSpecificAnalysis, \nDeleteSpecificAnalysis, \nDeleteEveryAnalysis, \nDeleteAccount, \nUpdateAnalysis, \nQuit.")
        elif (command == "CreateAnalysis"): 
            # Enter search string
            searchString = input("Please enter a string to search: ")
            # Enter list of reference links (1-3), authenticate them
            howManyRefLinks = input("Please enter how many reference links you would like to enter (1-3 per query): ")
            while str.isdigit(howManyRefLinks) is False or int(howManyRefLinks) > 3 or int(howManyRefLinks) < 1:   
                howManyRefLinks = input("Not a number between 1 and 3. Please try again: ")
                # TODO: Auth links to make sure they are valid websites before we call API 
            print("Please enter reference links")
            listOfRefLinks = []
            for i in range(0, int(howManyRefLinks), 1):
                link = input("Reference link " + str(i + 1) + ": ")
                if authenticateLink(link) is False:
                     link = input("False link. Please try again.\nReference link " + str(i + 1) + ": ")
                listOfRefLinks.append(link)        
            # Enter how many hit links you would like back (1-10)
            howManyHitLinks = input("Please enter how many hit links would you like to get back to be analyzed (1-25 per query): ")
            while str.isdigit(howManyHitLinks) is False or int(howManyHitLinks) > 25 or int(howManyHitLinks) < 1:   
                howManyHitLinks = input("Not a number between 1 and 25. Please try again: ")
            # Call Data_Collector.Collect_Data to return the data retrieval object
            collectData = data_collector.collect(listOfRefLinks, searchString, int(howManyHitLinks))
            if collectData is not None:
                # Pass the Data_Retrieval object to the CreateAnalysis function in the Query clss. 
                queryMaster.createNewQuery(userData[0], collectData)
        elif (command == "RetrieveAllAnalysisSummaries"):
            results = queryMaster.retrieveAllSummaries(userData[0])
            if len(results) == 0:
                print("No analyses stored.")
            else: 
                for row in results:
                    print(row)
        elif (command == "RetrieveSpecificAnalysis"):
            print("Please enter a unique id to specify which analysis to retrieve.")
            print("Tip: To recall which id's are available, enter command 'RetrieveAllAnalysisSummaries'")
            print("and type in the query id, reference link id, and hit link id to retrieve the analysis")
            queryNumber = input("Please enter the query id here: ")
            while str.isdigit(queryNumber) is False:
                queryNumber = input("Invalid entry. Please enter the query id here: ")
            rlNumber = input("Please enter the reference link id here: ")
            while str.isdigit(rlNumber) is False:
                rlNumber = input("Invalid entry. Please enter the reference link id here: ")
            hlNumber = input("Please enter the hit link id here: ")
            while str.isdigit(hlNumber) is False:
                hlNumber = input("Invalid entry. Please enter the hit link id here: ")
            table = queryMaster.retrieveSpecificAnalysis(userData[0], queryNumber, rlNumber, hlNumber) 
            if len(table) > 0:
                print(table)
            else:
                print("Query: ", queryNumber, ",", rlNumber, ",", hlNumber, "does not exist or is associated with a different account.")
        elif (command == "DeleteSpecificAnalysis"):
            print("Please enter a unique id to specify which analysis to delete.")
            print("Tip: To recall which id's are available, enter command 'RetrieveAllAnalysisSummaries'")
            print("and type in the query id, reference link id, and hit link id to delete the analysis")
            queryNumber = input("Please enter the query id here: ")
            while str.isdigit(queryNumber) is False:
                queryNumber = input("Invalid entry. Please enter the query id here: ")
            rlNumber = input("Please enter the reference link id here: ")
            while str.isdigit(rlNumber) is False:
                rlNumber = input("Invalid entry. Please enter the reference link id here: ")
            hlNumber = input("Please enter the hit link id here: ")
            while str.isdigit(hlNumber) is False:
                hlNumber = input("Invalid entry. Please enter the hit link id here: ")
            ans = input("Are you sure you wish to continue? (Y/N)")
            if ans is not "Y" and ans is not "y":
                return 
            queryMaster.deleteSpecificAnalysis(userData[0], queryNumber, rlNumber, hlNumber)
        elif (command == "DeleteEveryAnalysis"):
            queryMaster.deleteEveryAnalysis(userData[0])
        elif (command == "DeleteAccount"):
            wasAccountDeleted = queryMaster.deleteAccount(userData[0])
            if wasAccountDeleted is True:
                print("Goodbye.")
                return
        elif (command == "UpdateAnalysis"):
            print("Please enter a unique id to specify which analysis to delete.")
            print("Tip: To recall which id's are available, enter command 'RetrieveAllAnalysisSummaries'")
            print("and type in the query id, reference link id, and hit link id to delete the analysis")
            queryNumber = input("Please enter the query id here: ")
            while str.isdigit(queryNumber) is False:
                queryNumber = input("Invalid entry. Please enter the query id here: ")
            rlNumber = input("Please enter the reference link id here: ")
            while str.isdigit(rlNumber) is False:
                rlNumber = input("Invalid entry. Please enter the reference link id here: ")
            hlNumber = input("Please enter the hit link id here: ")
            while str.isdigit(hlNumber) is False:
                hlNumber = input("Invalid entry. Please enter the hit link id here: ")
            queryMaster.updateAnalysis(email, queryNumber, rlNumber, hlNumber)
        elif (command == "Quit"):
            print("Exiting program. Goodbye.")
            return
        else:
            print("invalid command. Please press Help to see menu.")

    # HELP
    # User asks for help: they get a list of possible commands

    # CreateAnalysis
    # User asks to create sentiment analysis. Inputs 1...3 reference links, search string, and 1...10 return requests
    # Returns RetrievePossibleAnalysis

    # RetrievePossibleAnalysis
    # Returns the list with a queryID, search strings, reference links, and a summary of each analysis
    
    # RetreieveSpecificAnalsis
    # With that list of querID, referenceLinkID, and hitLinkID, retrieve a detailed sentiment analysis on each 

    # Delete:
    # Can delete an analysis given queryID, referenceLinkID, and hitLinkID

    # Delete Account:
    # Can delete all their queries, account, and id. Exits out of the API. 

    # Update Analysis
    # Given a queryID, update the contents of the sentiment analysis and re-run it with more up to date websites 

if __name__ == "__main__":
    main()
