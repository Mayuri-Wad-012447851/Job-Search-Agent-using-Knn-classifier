from Agent import *
import operator
import numpy as np

class Environment:

    #It stores 15 nearest jobs for each keyword searched by user previously
    lookupTable = {}
    #Date timestamp to rebuild the lookup table
    lookupTableBuildDate = None

    #this method prebuilds the lookup table for some popular keywords
    def prebuildLookupTable(self,agent,scrapper):
        popularKeywords = ["data scientist","artificial intelligence",
                           "assistant professor","technical writer",
                           "accountant", "nurse"]

        for keyword in popularKeywords:
            knn = self.scrapeWeb(agent,scrapper,keyword, 15)
            self.insertInLookup(keyword,knn)

    #inserts the new keyword and fetched 15 nearest jobs for corresponding keyword in a lookup table for future reference
    def insertInLookup(self,keyword,jobs):
        self.lookupTable[keyword] = jobs

    #fetches jobs stored in lookup table for given keyword
    def getJobsFromLookup(self,keyword):
        jobList = self.lookupTable[keyword]
        return jobList

    #For never seen before keyword, environment scraps the web.
    def scrapeWeb(self, agent, scrapper, keyword, k_value):

        #Dividing total number of jobs to be fetched from each website in order to make sure that enough jobs are available to present to user
        #This will restrict scrapper from fetching too many jobs
        if (k_value * 3) <= 15:
            N = 15
        else:
            N = k_value * 3

        #scrapper internally calls agent to get K nearest jobs
        knnJobs = scrapper.scrapAndGetKnn(agent,keyword,N,k_value)

        return knnJobs

    #starting point for clustering algorithm
    def cluster(self,agent,data,noOfClusters):
        jobs = []

        for job in data:
            jobs.append(job[0])

        #assigning centroids
        centroids = jobs[0:noOfClusters]

        #iterator for termination and to calculate iterations
        iteration = 1
        maxIteration = 3

        #calling kmeans algorithm for given number of clusters and centroids
        clusters = self.kmeans(noOfClusters, centroids, jobs, iteration, maxIteration,agent)

        #printing final clusters
        for i in range(0,len(clusters)):
            print "Cluster "+str(i)+":\n"
            cluster = clusters[i]
            print "[",
            for job in cluster:
                print str(job.jobLink)+",\n"
            print "]"

    def kmeans(self,k, centroids, jobs,iteration, maxIteration,agent):
        clusters = [[] for i in range(k)]

        #finding closest centroid for each job document in cluster
        for i in range(len(jobs)):
            datapoint = jobs[i]
            clusterIdentifier = self.findClosestCentroid(datapoint,centroids,agent)
            clusters[clusterIdentifier].append(datapoint)

        newCentroids = self.findNewCentroid(clusters,agent)

        if not self.equals(centroids,newCentroids):
            print "Iteration "+str(iteration)
            iteration += 1
            if iteration <= maxIteration:
                clusters = self.kmeans(k,newCentroids,jobs,iteration,maxIteration,agent)

        return clusters

    def findClosestCentroid(self, datapoint, centroids,agent):
        minDistance = float('inf')
        clusterIdentifier = None

        for i in range(0,len(centroids)):
            centroid = centroids[i]
            print "Centroid"+str(centroid)
            distance = agent.calculateCosineSimilarity(datapoint.TF_IDF,centroid.TF_IDF)
            if(distance < minDistance):
                minDistance = distance
                clusterIdentifier = i
        return clusterIdentifier

    def findNewCentroid(self,clusters,agent):
        newCentroids = []
        listVector = []
        meanTFDoc = []

        for cluster in clusters:

            if cluster != []:
                for job in cluster:
                    listVector.append(job.TF_IDF)


            #newCentroids.append(np.mean(listVector))

                for i in range(0,len(listVector[0])):
                    sum = 0
                    for j in range(0,len(listVector)):
                        sum += listVector[j][i]
                    avg = float(sum/len(cluster))
                    meanTFDoc.append(avg)
                print "MeanTFDOC"+str(meanTFDoc)

                eu_dist = []
                for job in cluster:
                    currentTFDoc = job.TFvector
                    dist = agent.calculateEucledeanDistance(currentTFDoc,meanTFDoc)
                    eu_dist.append((dist,job))

                eu_dist.sort(key=operator.itemgetter(0))
                if eu_dist != []:
                    newCentroids.append(eu_dist[0][1])

        return newCentroids

    def equals(self,centroids,newCentroids):

        if len(centroids) != len(newCentroids):
            return False

        for i in range(0,len(centroids)):
            job1 = centroids[i]
            job2 = newCentroids[i]
            if job1.id != job2.id:
                return False

        return True



