import datetime as date
import pickle

fName = "citations.txt"


class Website:

    def __init__(self):

        self.authorFirst, self.authorLast = None, None
        self.setAuthorName()

        self.articleTitle = None
        self.setSourceTitle()

        self.websiteTitle = None
        self.setWebsiteTitle()

        self.DOPYear, self.DOPMonth, self.DOPDay = None, None, None
        self.setDOP()
        self.DOP = self.DOPDay + " " + self.DOPMonth + " " + self.DOPYear

        self.yearOfAccess, self.monthOfAccess, self.dayOfAccess = None, None, None
        self.setDOA()
        self.DOA = self.dayOfAccess + " " + self.monthOfAccess + " " + self.yearOfAccess

        self.URL = None
        self.setURL()

        self.citation = None

    def setAuthorName(self):

        first = input("\nAuthor's First Name")
        last = input("Author's Last Name")

        self.authorFirst = first
        self.authorLast = last

    def setSourceTitle(self):
        title = input("Article Title")
        self.articleTitle = title

    def setWebsiteTitle(self):
        title = input("Website Title")
        self.websiteTitle = title

    def setDOP(self):

        year = input("Year of Publication")
        month = input("Month of Publication")
        day = input("Day of Publication")

        self.DOPYear, self.DOPMonth, self.DOPDay = year, month, day

    def setDOA(self):

        year = input("Year of Access")
        month = input("Month of Access")
        day = input("Day of Access")

        self.yearOfAccess, self.monthOfAccess, self.dayOfAccess = year, month, day

    def setURL(self):

        url = input("URL")

        if (url[0:7] == "http://"):
            url = url[7:]

        if (url[0:8] == "https://"):
            url = url[8:]

        self.URL = url

    def compile(self):
        tempCitation = ""

        if ((self.authorLast + ", " + self.authorFirst + ". ") != ", . "):
            tempCitation += self.authorLast + ", " + self.authorFirst + ". "

        tempCitation += "\"" + self.articleTitle + ".\" " + self.websiteTitle + ", "

        if (self.DOP != "  "):
            tempCitation += self.DOP + ", "

        tempCitation += self.URL + "."

        if (self.DOP == "  "):
            tempCitation += " Accessed " + self.DOA + "."

        self.citation = tempCitation

    def get(self):
        self.compile()
        return self.citation

    def getForSort(self):
        c = self.get()

        if (c[0] == '"'): return c[1:]

        return c


class WorksCitedPage:

    def __init__(self, pageName, start):
        self.name = pageName
        self.lastEdited, self.friendlyLastEdited = None, None
        self.Update()
        self.works = []

    def ls(self):
        print("\n" + self.get())
        if len(self.works) == 0:
            print("\tPAGE HAS NO WORKS")
            print()
            return True

        else:
            self.printWorks()
            print()
            return False

    def printWorks(self, forList=True):

        for source in self.works:
            if forList:
                print("\t{}. {}".format(self.works.index(source) + 1, source.get()))
            else:
                print("\n{}".format(source.get()))

    def Update(self):
        self.lastEdited, self.friendlyLastEdited = date.datetime.now(), date.datetime.now().strftime("%m/%d/%Y %I:%M%p")

    def getForSort(self):
        return self.lastEdited

    def addWork(self):
        self.works.append(Website())
        self.Update()
        self.sortWorks()

    def removeWork(self, index):
        del self.works[index]
        self.Update()

    def sortWorks(self):

        n1 = len(self.works) - 1
        while (n1 >= 0):

            posMax = 0

            n2 = 0
            while (n2 <= n1):
                if (self.works[n2].getForSort() > (self.works[posMax].getForSort())):
                    posMax = n2
                n2 += 1

            temp = self.works[n1]
            self.works[n1] = self.works[posMax]
            self.works[posMax] = temp

            n1 -= 1

    def get(self):
        return "{} (Last Edited: {})".format(self.name, self.friendlyLastEdited)


class ListOfPages:

    def __init__(self, fileName):
        self.file = fileName
        self.pages = []
        self.loadPages()

    def get(self, index):
        return self.pages[index]

    def loadPages(self):

        try:
            with open(self.file, 'rb') as f:
                
                try:
                    self.pages = pickle.load(f)
                except:
                    print("\nFILE EMPTY")
        except:
            f = open(self.file, 'x')

        f.close()

    def savePages(self):
        with open(self.file, 'wb') as f:
            pickle.dump(self.pages, f)
        f.close()

    def addPage(self, pageName):
        self.pages.append(WorksCitedPage(pageName, len(self.pages)))
        self.savePages()

    def removePage(self, index):
        del self.pages[index]
        self.savePages()

    def ls(self):  # List pages
        print("\nWorks Cited Pages")
        self.SortPages()
        for n in range(len(self.pages)):
            print("{}. {}".format(n + 1, self.pages[n].get()))

    def SortPages(self):

        n1 = len(self.pages) - 1
        while (n1 >= 0):

            posMax = 0

            n2 = 0
            while (n2 <= n1):
                if (self.pages[n2].getForSort() > (self.pages[posMax].getForSort())):
                    posMax = n2
                n2 += 1

            temp = self.pages[n1]
            self.pages[n1] = self.pages[posMax]
            self.pages[posMax] = temp

            n1 -= 1


if __name__ == "__main__":

    file = ListOfPages(fName)

    while True:
        # if no pages exist, make new page
        if len(file.pages) == 0:
            print("\nThe file destination has no Works Cited Pages. Adding Page...")
            name = input("Please name the new page\n")
            file.addPage(name)

        file.ls()
        choice = input("\nA. Edit a Page\n"
                       "B. Delete a Page\n"
                       "C. Add a Page\n"
                       "Q. Quit")

        if choice == "q" or choice == "Q":
            break

        elif choice == "A" or choice == "a" or choice == "B" or choice == "b":

            page = int(input("\nPlease Select The Page Number"))

            if choice == "B" or choice == "b":
                file.removePage(page - 1)
                print("\nPAGE DELETED")

            else:
                c2 = None
                while True:

                    if c2 != "C" and c2 != "c":
                        empty = file.get(page - 1).ls()

                    if empty:
                        c2 = input("A. Add Work\n"
                                   "Q. Back")
                    else:
                        c2 = input("A. Add Work\n"
                                   "B. Delete Work\n"
                                   "C. Print Page For Copy/Paste\n"
                                   "Q. Back")

                    if c2 == "Q" or c2 == "q":
                        break

                    elif c2 == "A" or c2 == "a":
                        file.get(page - 1).addWork()
                        file.savePages()

                    elif c2 == "B" or c2 == "b":
                        work = int(input("\nPlease Select The Work Number"))
                        file.get(page - 1).removeWork(work - 1)
                        file.savePages()

                    elif c2 == "C" or c2 == "c":
                        print("\n")
                        file.get(page - 1).printWorks(False)
                        print("\n")

        elif choice == "C" or choice == "c":
            name = input("\nPlease Name The New Page")
            file.addPage(name)
