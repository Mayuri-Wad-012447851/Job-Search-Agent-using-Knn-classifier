import urllib
import math

class Job:

    #initializing all job features
    def __init__(self):
        self.id = None
        self.jobTitle = None
        self.companyName = None
        self.address = None
        self.homeURL = None
        self.jobLink = None
        self.skills = []
        self.summary = []
        self.TFvector = []
        self.TF_IDF = []

    #method to print job features
    def printDetails(self):
        print "\nJob Title:\t"+self.jobTitle
        print "Company:\t"+self.companyName
        joburl = urllib.quote(self.jobLink.encode('utf8'), ':/')
        print "Link:\t"+joburl
        print "HomeURL:\t"+self.homeURL



