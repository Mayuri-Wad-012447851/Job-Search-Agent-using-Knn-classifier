from WebScrapper import *
import math
import operator

class Agent:
    def __init__(self):
        pass

    def dotproduct(self,v1, v2):
        return sum((a * b) for a, b in zip(v1, v2))

    def length(self,v):
        return math.sqrt(self.dotproduct(v, v))

    def angle(self,v1, v2):
        return math.acos(self.dotproduct(v1, v2) / (self.length(v1) * self.length(v2)))

    #this method calculated cosine distance between given percept document and normalized TFdocument
    def calculateCosineSimilarity(self,perceptDoc,jobDoc):
        try:
            cosTheta =  math.acos(self.dotproduct(perceptDoc,jobDoc) / (self.length(perceptDoc) * self.length(jobDoc)))
            return 1 - cosTheta
        except:
            return 1

    # this method calculates float Euclidean distance between a percept from test dataset and a record from training dataset
    def calculateEucledeanDistance(self,TFDoc,meanTFDoc):
        d = 0.0
        for i in range(0,len(meanTFDoc)-1):
            x = float(TFDoc[i])
            y = float(meanTFDoc[i])
            d += ((x-y) ** 2)
        d = math.sqrt(d)
        return d

    #this method returns a predicted class attribute for percept received from Environment
    def findKnn(self,perceptVector,jobsFetched,K):
        cosine_Similarity = []

        for job in jobsFetched:
            d = self.calculateCosineSimilarity(perceptVector, job.TF_IDF)
            cosine_Similarity.append((job, d))

            cosine_Similarity.sort(key=operator.itemgetter(1))

        knnJobs = cosine_Similarity[:int(K)]

        return knnJobs