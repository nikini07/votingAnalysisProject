import csv
import matplotlib.pyplot as plt
import numpy as np

class MP:
    def __init__(self, firstName, lastName, gender, constituency, votesCast, party): #defining the MP class
        #attributes
        self.firstName = firstName
        self.lastName = lastName
        self.gender = gender
        self.constituency = constituency
        self.votesCast = votesCast
        self.party = party

class Party:
    def __init__(self, name): #defining the party class
        #attributes
        self.name = name
        self.mps = [] #list to store MP objects
        self.totalVotes = 0 #track the total votes received by the party

    def AddMP(self, mp): #method to add an MP and update total votes
        self.mps.append(mp)
        self.totalVotes += mp.votesCast

class Constituency:
    def __init__(self, name, totalVoters=0): #defining the constituency class
        #attributes
        self.name = name
        self.totalVoters = totalVoters
        self.totalVotesCast = 0 #track the total votes cast in the constituency
        self.mps = [] #list to store MPs representing the constituency

    def AddMP(self, mp):
        #method to add an MP and update total votes cast
        self.mps.append(mp)
        self.totalVotesCast += mp.votesCast
        
    def getConstituencyData(self):
        #method to return constituency data in a dictionary format
        return { #return data
            "name": self.name,
            "totalVoters": self.totalVoters,
            "totalVotesCast": self.totalVotesCast,
        }
        
    
        
#function to read the election data from a CSV file
def readFile(csvfile):
    mp_list = []
    party_dict = {}
    constituency_dict = {}

    try:
        with open('EditedData.csv', newline='', encoding='ISO-8859-1') as csvfile: #using dictReader to read csv as dictionaries
            reader = csv.DictReader(csvfile)
            for row in reader:

                try: 
                    #extracting MP data form the row
                    firstName = row.get('Member first name', '')
                    lastName = row.get('Member surname', '')
                    # gender = row.get('Gender', 'Unknown')
                    gender = row.get('Member gender', 'Unknown').strip().capitalize()
                        
                    constituency_name = row.get('Constituency name', '')
                    party_name = row.get('First party', 'Independent')
                    totalVotes = int(row.get(party_name, 0)) if party_name else 0
                    
                    #creating MP object and adding it to the list
                    mp = MP(firstName, lastName, gender, constituency_name, totalVotes, party_name) #mp objects
                    mp_list.append(mp)
                    
                    #adding the MP to the corresponding party and constituency
                    if party_name not in party_dict: #adding Mp to party object
                        party_dict[party_name] = Party(party_name) #create a party if doesnt exist
                    party_dict[party_name].AddMP(mp)
                    
                    if constituency_name not in constituency_dict: #adding MP to constituency object
                        totalVoters = int(row.get('Electorate', 0))
                        constituency_dict[constituency_name] = Constituency(constituency_name, totalVoters) #create constituency if doesnt exist
                    constituency_dict[constituency_name].AddMP(mp)

                except KeyError as e: #to handle missing columns in the CSV data
                    print(f"Error: Missing column - {e}")

    except FileNotFoundError: #to handle the file not found error
        print(f"Error: The file {fileName} was not found.")

    return mp_list, party_dict, constituency_dict




def welcomeMessage():
    print("Welcome to the Election Information System!")
    print("Please choose an option from the following menu:")
    
def displayMainMenu():  # menu options of the main menu
    print("\nMain Menu")
    print("1. View Candidate Information")
    print("2. View Constituency Information")
    print("3. View Party Information")
    print("4. Save and exit program")

def displayCandidateMenu():  # menu options of the candidate menu
    print("\nCandidate Menu - Please choose an option:")
    print("1. View Candidate Data")
    print("2. View Candidate Votes")
    print("3. Back to Main Menu")

def displayConstituencyMenu():  # menu options of the constituency menu
    print("\nConstituency Menu - Please choose an option:")
    print("1. View Constituency Data")
    print("2. View MPs in a Constituency")
    print("3. Back to Main Menu")

def displayPartyMenu():
    print("\nParty Menu - Please choose an option:")  # menu options of the party menu
    print("1. View Total Votes for a Party")
    print("2. View Party Percentage of Total Votes")
    print("3. View MPs in a Party")
    print("4. Back to Main Menu")





def saveStatistics(party_dict, constituency_dict, output_file="ElectionStatistics.txt"):
    
    #function to save the statistics to a structured text file.
    try:
        with open(output_file, 'w') as file: #open the output file in write mode
            file.write("Election Results Summary\n")
            file.write("=" * 40 + "\n") #adding a line separator
            
            #writing party statistics to a file
            file.write("Party Statistics:\n")
            for party_name, party in party_dict.items():
                file.write(f"{party_name}: {party.totalVotes} votes\n") #write each party's total vote count
            file.write("\n") #newline after party statistics
            
            #writing constituency statistics to a file
            file.write("Constituency Statistics:\n")
            for constituency_name, constituency in constituency_dict.items():
                #get constituency data like total voters and votes cast
                data = constituency.getConstituencyData()
                #writing the statistics for each constituency
                file.write(
                    f"{data['name']}: {data['totalVoters']} registered voters, "
                    f"{data['totalVotesCast']} votes cast\n" #newline after constituency statistics
                )
            file.write("\n")
            
        print(f"Statistics have been successfully saved to {output_file}.")
        
    except IOError as e:
        print(f"Error writing to file: {e}")
        
        
        
        
        
def create_pie_chart(party_dict): #defining function
    total_votes = sum(party.totalVotes for party in party_dict.values()) #to calculates the sum to represent the total number of votes across all parties.
    
    #sort parties by total votes in descending order
    sorted_parties = sorted(party_dict.items(), key=lambda item: item[1].totalVotes, reverse=True)
    top_parties = sorted_parties[:5]  #top 5 parties
    other_parties = sorted_parties[5:]  #remaining parties

    #preparing data for the pie chart
    party_labels = [party_name for party_name, _ in top_parties] #sorting parties by votes
    party_votes = [party.totalVotes for _, party in top_parties] #extracts the names of the top 5 parties
    others_votes = sum(party.totalVotes for _, party in other_parties) #extracts the names of the other parties

    if others_votes > 0:
        party_labels.append("Other")  #adds other as a category
        party_votes.append(others_votes)

    # Explode only the top 5 parties slightly
    explode = [0.1 if i < 5 else 0.0 for i in range(len(party_votes))]
    colors = plt.cm.tab20.colors[:len(party_votes)]  #use of a color palette

    #function for formatting the labels
    def func(pct, allvalues):
        absolute = int(pct / 100. * np.sum(allvalues))
        #shows details of top 5 parties only
        if pct < 100 * others_votes / total_votes:
            return ""  #to hide details
        return f"{pct:.1f}%\n({absolute} votes)"
    
    #create the pie chart
    fig, ax = plt.subplots(figsize=(10, 7))
    wedges, texts, autotexts = ax.pie(
        party_votes, #sizes of the slices
        labels=party_labels, #labels for each slices
        autopct=lambda pct: func(pct, party_votes), #uses func to format the percentages
        explode=explode, #adds the broken effect
        shadow=True, #adds shadows
        startangle=90, #this allows the chrt to rotate 90degrees to start
        colors=colors, #colours of slices
        wedgeprops={'linewidth': 1, 'edgecolor': "green"},
        textprops=dict(color="black")
    )

    #customize slices
    if "Other" in party_labels:
        other_index = party_labels.index("Other")
        autotexts[other_index].set_text("")  #hide percentage and vote count for "Other"
    
    #adding legend allows list all party names and their corresponding slices and position it to the side of the chart
    ax.legend(wedges, party_labels, title="Parties", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_title("Election Results: Vote Distribution by Party (Top 5 and Other)") #title of the chart

    plt.setp(autotexts, size=8, weight="bold") #customize text appearance
    plt.show() #display chart



    

def main():
    welcomeMessage()
    
    #to read the data from the csv file
    mp_list, party_dict, constituency_dict = readFile("EditedData.csv") 
    #to calculate the total votes across all parties for percentage calculations in choice 3 subchoice 2
    totalVotesAcrossParties = sum(p.totalVotes for p in party_dict.values()) 


    while True:
        displayMainMenu()
        choice = input("Enter your choice: ")
        
        #Beginning of choice 01
        if choice == "1":
            while True:
                displayCandidateMenu() #Display candidate submenu.
                sub_choice = input("Enter your choice: ")
                if sub_choice == "1":
                    candidate_name = input("Enter candidates name (first/last): ")
                    found = False
                    for mp in mp_list:
                        if candidate_name.lower() in (mp.firstName.lower(), mp.lastName.lower()): #method to case sensitivity for name input
                            print(f"The candidate {mp.firstName} {mp.lastName} ({mp.gender}) is from the {mp.party} party, representing the {mp.constituency} constituency.")
                            found = True
                    if not found:
                        print("Candidate not found.")
                        
                elif sub_choice == "2":
                    candidate_name = input("Enter candidate name (first/last): ")
                    found = False
                    for mp in mp_list:
                        if candidate_name.lower() in (mp.firstName.lower(), mp.lastName.lower()): #method to case sensitivity for name input
                            print(f"Candidate: {mp.firstName} {mp.lastName} ({mp.gender}), received {mp.votesCast} votes.")
                            found = True
                    if not found:
                        print("Candidate not found.")
                        
                elif sub_choice == "3":
                    break #Exit candidate submenu loop
                else:
                    print("Invalid choice. Please try again.")
                    #End of choice 01
                    
                    
        #Beginning of choice 02
        elif choice == "2":
            while True:
                displayConstituencyMenu() #Display constituency submenu.
                sub_choice = input("Enter your choice: ")
                if sub_choice == "1":
                    constituency_name = input("Enter constituency name: ")
                    if constituency_name in constituency_dict:
                        data = constituency_dict[constituency_name].getConstituencyData()
                        print(f"Constituency of {data['name']}, total of {data['totalVoters']} registered voters, of which {data['totalVotesCast']} votes have been cast.")
                    else:
                        print("Constituency not found.")
                elif sub_choice == "2":
                    constituency_name = input("Enter constituency name: ")
                    if constituency_name in constituency_dict:
                        print(f"MPs in {constituency_name}: ")
                        for mp in constituency_dict[constituency_name].mps:
                            print(f"{mp.firstName} {mp.lastName} ({mp.gender}) with {mp.votesCast} votes.")
                    else:
                        print("Constituency not found.")
                elif sub_choice == "3":
                    break #Exit constituency submenu loop.
                else:
                    print("Invalid choice. Please try again.")
                    #End of choice 02
        
        
        #Beginning of choice 03            
        elif choice == "3":
            while True:
                displayPartyMenu() #Display party submenu.
                sub_choice = input("Enter your choice: ")
                if sub_choice == "1":
                    party_name = input("Enter party name: ")
                    if party_name in party_dict:
                        print(f"The {party_name} party has received a total of {party_dict[party_name].totalVotes} votes.")
                    else:
                        print("Party not found.")
                elif sub_choice == "2":
                    party_name = input("Enter party name: ")
                    if party_name in party_dict:
                        percentage = (party_dict[party_name].totalVotes / totalVotesAcrossParties) * 100
                        print(f"The {party_name} party secured {percentage:.2f}% of the total votes.")
                    else:
                        print("Party not found.")
                elif sub_choice == "3":
                    party_name = input("Enter party name: ")
                    if party_name in party_dict:
                        print(f"MPs in {party_name} party:")
                        for mp in party_dict[party_name].mps:
                            print(f"{mp.firstName} {mp.lastName} ({mp.gender}) with {mp.votesCast} votes.")
                    else:
                        print("Party not found.")
                elif sub_choice == "4":
                    break
                else:
                    print("Invalid choice. Please try again.")
                    #End of choice 03
                    
        #exit program
        elif choice == "4":
            print("Exiting the program.")
            saveStatistics(party_dict, constituency_dict)
            #show the pie chart
            create_pie_chart(party_dict)
            print("Thank You for using Election Results System!")
            print("Have a great day!")
            break
        else:
            print("Invalid choice. Please try again.")
            
                    
                    
if __name__ == "__main__":
    main() 