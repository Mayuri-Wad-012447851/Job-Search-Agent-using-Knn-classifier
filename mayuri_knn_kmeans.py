from Environment import *
from Agent import *
import datetime

def isvalidKeyword(keyword):
    for word in keyword.split():
        if not word.isalpha():
            return False
    return True

def invalidKvalue(Kstr):

    if Kstr.isdigit():
        return False
    else:
        return True

def invalidNoOfClusters(num):
    if num.isdigit():
        return False
    else:
        return True

def main():

    #creating objects for Environment, Agent and WebScrapper class
    env = Environment()
    agent = Agent()
    webscrapper = WebScrapper()

    #loop for agent to run persistently until quit signal is received
    while(True):

        #storing timestamps for lookup table prebuild
        #If current date does not match with Lookup table build date, lookuptable will get rebuild
        #In this case lookup table will be built once everyday
        date = datetime.date.today()
        if date != env.lookupTableBuildDate:
            print "\nBuilding Lookup Table...This may take a few minutes to complete"
            env.lookupTable.clear()
            #env.prebuildLookupTable(agent,webscrapper)
            env.lookupTableBuildDate = date

        print "\nPlease enter 1 to search and 2 to cluster:\t"
        print "\n1. Search for jobs:\t"
        print "\n2. Cluster jobs\t"
        print "\n3. Quit"

        choice = raw_input("\nType your option : \t").strip()
        if choice == "3":
            exit(0)

        if choice == "1":
            keyword = raw_input("\n\nEnter keywords for the Job:\t").lower().strip()

            if (isvalidKeyword(keyword) == False):
                print "\nInvalid keyword entered. Please enter english words to search."
                continue

            Kstr = raw_input("\nEnter value of K for Knn:\t").strip()
            if (invalidKvalue(Kstr)):
                print "\nInvalid value for K. Please enter positive integer value."
                continue

            K = int(Kstr)

            print "\n\nYou entered: \"" + str(keyword) + "\" and K = " + str(K)

            print 'Fetching jobs..'
            if K <= 15 and (keyword in env.lookupTable.keys()):
                print "\nKeywords exists in lookup table. Fetching from lookup table..."
                outputJobs = env.getJobsFromLookup(keyword)
                for job in outputJobs[0:K]:
                    job[0].printDetails()
            else:
                print "\nKeyword not found in lookup table. Fetching from web..."
                outputJobs = env.scrapeWeb(agent,webscrapper, keyword, max(K, 15))
                env.lookupTable[keyword] = outputJobs[0:15]
                for job in outputJobs[0:K]:
                    job[0].printDetails()

        elif choice == "2":
            keyword = raw_input("\n\nEnter keywords for the Job:\t").lower().strip()
            if (isvalidKeyword(keyword) == False):
                print "\nInvalid keyword entered. Please enter english words to search."
                continue

            noOfCluster = raw_input('\nEnter number of clusters:\t').strip()
            if(invalidNoOfClusters(noOfCluster)):
                print "\nInvalid number entered. Please enter positive integer value."
                continue
            noOfClusters = int(noOfCluster)

            if noOfClusters > 15 or noOfClusters <= 0:
                print "\nCapping number of clusters to 15."
                noOfClusters = 15

            print '\nClustering jobs'
            # If keyword already exists in lookup table, relevant knn jobs are fetched from lookup table
            if (keyword in env.lookupTable.keys()) and (noOfClusters <= 15):
                print "\nKeywords exists in lookup table. Fetching from lookup table..."
                outputJobs = env.getJobsFromLookup(keyword)
                env.cluster(agent,outputJobs, noOfClusters)
            else:
                print "\nKeyword not found in lookup table. Fetching from web..."
                # If keyword not present in lookup table, jobs will be fetched from three websites
                outputJobs = env.scrapeWeb(agent,webscrapper, keyword, 15)
                env.cluster(agent,outputJobs, noOfClusters)
        else:
            print '\nYou entered values other than 1, 2 or 3. Please try again.'
            continue


    print "\nYou chose to Quit. Hopefully, you enjoyed my service"

if __name__ == '__main__':
    main()