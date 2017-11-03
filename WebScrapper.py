from Agent import *
from bs4 import BeautifulSoup as Soup
from Job import *

import urllib
import re


class WebScrapper:
    Corpus = {}
    jobsFetched = []
    ReversedCorpus = {}
    idf_terms = {}

    #this method scraps jobs from Indeed
    def scrapIndeed(self,urlKeyword,k_value):
        Jobcounter = 0
        webURL = "http://www.indeed.com/jobs?q=" + urlKeyword + "&start="

        for page in range(1, 101):
            page = (page - 1) * 10
            url = "%s%d" % (webURL, page)
            target = Soup(urllib.urlopen(url), "lxml")

            targetElements = target.findAll('div', attrs={'class': ' row result'})
            if targetElements == []:
                break
            for element in targetElements:
                #creating a job instance to store details like job title, company, address, JobLink
                job = Job()

                company = element.find('span', attrs={'itemprop': 'name'})
                if company != None:
                    job.companyName = company.getText().strip()
                title = element.find('a', attrs={'class': 'turnstileLink'}).attrs['title']
                if title != None:
                    job.jobTitle = title.strip()
                addr = element.find('span', attrs={'itemprop': 'addressLocality'})
                if addr != None:
                    job.address = addr.getText().strip()
                job.homeURL = "http://www.indeed.com"
                job.jobLink = "%s%s" % (job.homeURL, element.find('a').get('href'))

                skillsElement = element.find('span', attrs={'class': 'experienceList'})
                job.skills = self.cleanAndProcess(skillsElement)

                summaryElement = element.find('span', attrs={'class': 'summary'})
                job.summary = self.cleanAndProcess(summaryElement)

                if (job.jobTitle != None and job.jobLink != None):
                    self.jobsFetched.append(job)
                    Jobcounter += 1

                if (Jobcounter >= max(k_value, 15)):
                    break
            if (Jobcounter >= max(k_value, 15)):
                break

    # webscrapping for jobs.acm.com
    def scrapACM(self,urlKeyword,N):
        Jobcounter = 0
        webURL = "http://jobs.acm.org/jobs/results/keyword/" + urlKeyword + "?&locationType=text&radius=50&page="

        for page in range(1, 101):
            page = (page - 1) * 10
            url = "%s%d" % (webURL, page)

            target = Soup(urllib.urlopen(url), "lxml")
            targetElements = target.findAll('div', attrs={'class': 'aiResultsMainDiv'})
            if targetElements == []:
                break
            for element in targetElements:
                # creating a job instance to store details like job title, company, address, JobLink
                job = Job()

                company = element.find('li', attrs={'class': 'aiResultsCompanyName'})
                if company != None:
                    job.companyName = company.getText().strip()
                title = element.find('div', attrs={'class': 'aiResultTitle aiDevIconSection '})
                if title != None:
                    job.jobTitle = title.getText().strip()
                addr = element.find('span', attrs={'class': 'aiResultsLocationSpan'})
                if addr != None:
                    job.address = addr.getText().strip()
                job.homeURL = "http://jobs.acm.org"
                job.jobLink = "%s%s" % (job.homeURL, element.find('a').get('href'))
                if ((job.jobLink != "") and (job.jobLink != None)):
                    joburl = urllib.quote(job.jobLink.encode('utf8'), ':/')
                    joblinkTarget = Soup(urllib.urlopen(joburl), "lxml")
                    summaryElement = joblinkTarget.find('div', attrs={'class': 'aiListingTabContainer'})
                    job.summary = self.cleanAndProcess(summaryElement)

                if (job.jobTitle != None and job.jobLink != None and job.summary != []):
                    self.jobsFetched.append(job)
                    Jobcounter += 1

                if (Jobcounter >= N):
                    break
            if (Jobcounter >= N):
                break

    # webscrapping for http://jobs.ieee.org
    def scrapIEEE(self,urlKeyword,N):
        Jobcounter = 0
        webURL = "http://jobs.ieee.org/jobs/results/keyword/" + urlKeyword + "?&locationType=text&radius=50&page="

        for page in range(1, 101):
            page = (page - 1) * 10
            url = "%s%d" % (webURL, page)

            target = Soup(urllib.urlopen(url), "lxml")
            targetElements = target.findAll('div', attrs={'class': 'aiResultsMainDiv'})

            if targetElements == []:
                break
            for element in targetElements:
                if (Jobcounter < (N)):
                    # creating a job instance to store details like job title, company, address, JobLink
                    job = Job()

                    company = element.find('li', attrs={'class': 'aiResultsCompanyName'})
                    if company != None:
                        job.companyName = company.getText().strip()
                    title = element.find('div', attrs={'class': 'aiResultTitle aiDevIconSection '})
                    if title != None:
                        job.jobTitle = title.getText().strip()
                    addr = element.find('span', attrs={'class': 'aiResultsLocationSpan'})
                    if addr != None:
                        job.address = addr.getText().strip()
                    job.homeURL = "http://jobs.ieee.org"
                    job.jobLink = "%s%s" % (job.homeURL, element.find('a').get('href'))
                    if ((job.jobLink != "") and (job.jobLink != None)):
                        joburl = urllib.quote(job.jobLink.encode('utf8'), ':/')
                        joblinkTarget = Soup(urllib.urlopen(joburl), "lxml")

                        summaryElement = joblinkTarget.find('span', attrs={'itemprop': 'description'})
                        job.summary = self.cleanAndProcess(summaryElement)

                    if (job.jobTitle != None and job.jobLink != None and job.summary != []):
                        self.jobsFetched.append(job)
                        Jobcounter += 1

                    if (Jobcounter >= N):
                        break
                if (Jobcounter >= N):
                    break

    def cleanAndProcess(self,soupObject):
        stopwords = ['a', "a's", 'able', 'about', 'above', 'according', 'accordingly', 'across', 'actually', 'after',
                     'afterwards', 'again', 'against', "ain't", 'all', 'allow', 'allows', 'almost', 'alone', 'along',
                     'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'another', 'any',
                     'anybody', 'anyhow', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'appear',
                     'appreciate', 'appropriate', 'are', "aren't", 'around', 'as', 'aside', 'ask', 'asking',
                     'associated', 'at', 'available', 'away', 'awfully', 'b', 'be', 'became', 'because', 'become',
                     'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'believe', 'below',
                     'beside', 'besides', 'best', 'better', 'between', 'beyond', 'both', 'brief', 'but', 'by', 'c',
                     "c'mon", "c's", 'came', 'can', "can't", 'cannot', 'cant', 'cause', 'causes', 'certain',
                     'certainly', 'changes', 'clearly', 'co', 'com', 'come', 'comes', 'concerning', 'consequently',
                     'consider', 'considering', 'contain', 'containing', 'contains', 'corresponding', 'could',
                     "couldn't", 'course', 'currently', 'd', 'definitely', 'described', 'despite', 'did', "didn't",
                     'different', 'do', 'does', "doesn't", 'doing', "don't", 'done', 'down', 'downwards', 'during', 'e',
                     'each', 'edu', 'eg', 'eight', 'either', 'else', 'elsewhere', 'enough', 'entirely', 'especially',
                     'et', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex',
                     'exactly', 'example', 'except', 'f', 'far', 'few', 'fifth', 'first', 'five', 'followed',
                     'following', 'follows', 'for', 'former', 'formerly', 'forth', 'four', 'from', 'further',
                     'furthermore', 'g', 'get', 'gets', 'getting', 'given', 'gives', 'go', 'goes', 'going', 'gone',
                     'got', 'gotten', 'greetings', 'h', 'had', "hadn't", 'happens', 'hardly', 'has', "hasn't", 'have',
                     "haven't", 'having', 'he', "he's", 'hello', 'help', 'hence', 'her', 'here', "here's", 'hereafter',
                     'hereby', 'herein', 'hereupon', 'hers', 'herself', 'hi', 'him', 'himself', 'his', 'hither',
                     'hopefully', 'how', 'howbeit', 'however', 'i', "i'd", "i'll", "i'm", "i've", 'ie', 'if', 'ignored',
                     'immediate', 'in', 'inasmuch', 'inc', 'indeed', 'indicate', 'indicated', 'indicates', 'inner',
                     'insofar', 'instead', 'into', 'inward', 'is', "isn't", 'it', "it'd", "it'll", "it's", 'its',
                     'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kept', 'know', 'knows', 'known', 'l', 'last',
                     'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', "let's", 'like', 'liked',
                     'likely', 'little', 'look', 'looking', 'looks', 'ltd', 'm', 'mainly', 'many', 'may', 'maybe', 'me',
                     'mean', 'meanwhile', 'merely', 'might', 'more', 'moreover', 'most', 'mostly', 'much', 'must', 'my',
                     'myself', 'n', 'name', 'namely', 'nd', 'near', 'nearly', 'necessary', 'need', 'needs', 'neither',
                     'never', 'nevertheless', 'new', 'next', 'nine', 'no', 'nobody', 'non', 'none', 'noone', 'nor',
                     'normally', 'not', 'nothing', 'novel', 'now', 'nowhere', 'o', 'obviously', 'of', 'off', 'often',
                     'oh', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others',
                     'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'own', 'p',
                     'particular', 'particularly', 'per', 'perhaps', 'placed', 'please', 'plus', 'possible',
                     'presumably', 'probably', 'provides', 'q', 'que', 'quite', 'qv', 'r', 'rather', 'rd', 're',
                     'really', 'reasonably', 'regarding', 'regardless', 'regards', 'relatively', 'respectively',
                     'right', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'second', 'secondly', 'see',
                     'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sensible', 'sent',
                     'serious', 'seriously', 'seven', 'several', 'shall', 'she', 'should', "shouldn't", 'since', 'six',
                     'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat',
                     'somewhere', 'soon', 'sorry', 'specified', 'specify', 'specifying', 'still', 'sub', 'such', 'sup',
                     'sure', 't', "t's", 'take', 'taken', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx',
                     'that', "that's", 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence',
                     'there', "there's", 'thereafter', 'thereby', 'therefore', 'therein', 'theres', 'thereupon',
                     'these', 'they', "they'd", "they'll", "they're", "they've", 'think', 'third', 'this', 'thorough',
                     'thoroughly', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to',
                     'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying',
                     'twice', 'two', 'u', 'un', 'under', 'unfortunately', 'unless', 'unlikely', 'until', 'unto', 'up',
                     'upon', 'us', 'use', 'used', 'useful', 'uses', 'using', 'usually', 'uucp', 'v', 'value', 'various',
                     'very', 'via', 'viz', 'vs', 'w', 'want', 'wants', 'was', "wasn't", 'way', 'we', "we'd", "we'll",
                     "we're", "we've", 'welcome', 'well', 'went', 'were', "weren't", 'what', "what's", 'whatever',
                     'when', 'whence', 'whenever', 'where', "where's", 'whereafter', 'whereas', 'whereby', 'wherein',
                     'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', "who's", 'whoever',
                     'whole', 'whom', 'whose', 'why', 'will', 'willing', 'wish', 'with', 'within', 'without', "won't",
                     'wonder', 'would', 'would', "wouldn't", 'x', 'y', 'yes', 'yet', 'you', "you'd", "you'll", "you're",
                     "you've", 'your', 'yours', 'yourself', 'yourselves', 'z', 'zero', '', 'attr', 'job','var','strong']
        finalSummary = []

        if soupObject != None:
            #converting job summary tokens to lower case
            text = soupObject.getText().lower().strip()
            #using regular expressions to clean words containing unwanted characters
            text = re.sub('[^a-z\ \']+'," ", text)
            text = text.split(" ")
            for word in text:
                #removing stopwords from job summary
                if word not in stopwords:
                    word = word.encode('ascii', 'ignore')
                    finalSummary.append(word)

        return finalSummary

    #This method builds a job document term matrix
    def buildCorpus(self):
        self.Corpus = {}
        self.ReversedCorpus = {}

        for job in self.jobsFetched:
            for word in job.summary:
                if word not in self.Corpus.keys():
                    frequencies = []
                    for i in range(0, len(self.jobsFetched)):
                        frequencies.append(0)
                    self.Corpus[word] = frequencies
                self.Corpus[word][job.id] += 1

        terms = self.Corpus.keys()

        # reversing the corpus
        for i in range(0, len(self.jobsFetched)):
            array_termFrequency = []
            for k in range(0, len(terms)):
                array_termFrequency.append(0)
            self.ReversedCorpus[i] = array_termFrequency

        jobIDs = self.ReversedCorpus.keys()

        for jobIdkey in jobIDs:
            for j in range(0, len(terms)):
                word = terms[j]
                self.ReversedCorpus[jobIdkey][j] = self.Corpus[word][jobIdkey]

        for job in self.jobsFetched:
            termFreq = self.ReversedCorpus[job.id]
            # finding TF for each job document
            for k in range(0, len(termFreq)):
                var1 = termFreq[k]
                var2 = sum(self.ReversedCorpus[job.id])
                job.TFvector.append(float(var1 / var2))

        #calculating IDFs of all terms
        self.idf_terms = {}
        for term in terms:
            termVector = self.Corpus[term]
            occurance = 0
            for k in range(0,len(termVector)):
                if termVector[k] != 0:
                    occurance += 1
            self.idf_terms[term] = math.log(float(len(jobIDs) / occurance))

        #computing TF*IDF for every job document
        for job in self.jobsFetched:
            for i in range(0,len(terms)):
                val = float(self.idf_terms[terms[i]])
                val2 = float(job.TFvector[i])
                job.TF_IDF.append(float(val * val2))

    #This method normalizes term frequency job document
    def normalizePercept(self,vector):
        factor = 0
        NormalizedVector = []

        for val in vector:
            factor += val
        for val in vector:
            NormalizedVector.append(float(val/factor))

        terms = self.Corpus.keys()
        perceptIDF = []
        for i in range(0,len(vector)):
            perceptIDF.append(float(NormalizedVector[i]*self.idf_terms[str(terms[i])]))

        return perceptIDF

    #This method builds a precept for entered keywords, which can be used to find Knn jobs.
    #Percept is built using average of term frquency over all job documents and normalizing the same
    def buildPerceptVector(self):
        percept = []

        terms = self.Corpus.keys()

        #logic to build percept
        summation = 0
        for i in range(0,len(terms)):
            for jobKey in self.ReversedCorpus.keys():
                summation += self.ReversedCorpus[jobKey][i]
            average = float(summation/len(self.jobsFetched))
            percept.append(average)

        normalizedPercept = self.normalizePercept(percept)

        return normalizedPercept

    #this method sends agent a percept and fetched jobs
    def scrapAndGetKnn(self,agent,keyword,N,k_value):

        keywords = keyword.split()
        urlKeyword = ""

        #seperating all keywords in a list
        for i in range(0,(len(keywords)-1)):
            urlKeyword = urlKeyword+keywords[i]+"+"
        urlKeyword = urlKeyword+keywords[-1]

        self.jobsFetched = []

        #scrapping all the three websites
        self.scrapIndeed(urlKeyword,k_value)
        self.scrapACM(urlKeyword,N)
        self.scrapIEEE(urlKeyword,N)

        #assigning jobId to all fetched and stored jobs
        idCounter = 0
        for job in self.jobsFetched:
            job.id = idCounter
            idCounter += 1

        #creating dictionary to store frquency of terms in all fetched job

        #building corpus
        self.buildCorpus()

        #generating a percept for given keyword
        perceptVector = self.buildPerceptVector()

        #sending agent a percept, fetched jobs and K
        return agent.findKnn(perceptVector,self.jobsFetched,k_value)


