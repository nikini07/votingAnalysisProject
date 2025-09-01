# Voting Analysis System

A **Python-based Election Information System** that reads real election data from a CSV file, analyzes results by **candidates, parties, and constituencies**, and presents insights through text-based menus and visualizations.

---

##  Features
- **Candidate Analysis**
  - View candidate details (name, gender, constituency, party).
  - Check votes received by a candidate.
- **Constituency Analysis**
  - View total registered voters and votes cast.
  - List MPs representing a constituency.
- **Party Analysis**
  - View total votes received by a party.
  - Calculate a party’s vote percentage of the national total.
  - List MPs belonging to a party.
- **Data Persistence**
  - Saves a summary of results (votes per party & constituency turnout) into a text file.
- **Visualization**
  - Generates a **pie chart** of the top 5 parties’ vote share (with "Other" category).

---

## 🛠 Technologies Used
- **Python 3**
- **CSV** (for data input)
- **Matplotlib** + **NumPy** (for charts and calculations)

---

##  Project Structure
```plaintext
VotingAnalysisSystem/
│── EditedData.csv         # Election dataset (input file)
│── voting_analysis.py     # Main program
│── ElectionStatistics.txt # Auto-generated summary output
│── README.md              # Project documentation
```

## How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/VotingAnalysisSystem.git
   cd votingAnalysisSystem
   ```
2. **Install dependencies:**
   ```bash
   pip install matplotlib numpy
   ```
3. **Prepare your dataset:**
- Ensure you have a CSV file named EditedData.csv in the project folder.
- The CSV should contain columns like:
- Member first name
- Member surname
- Member gender
- Constituency name
- Electorate
- First party (and party vote counts)
  
4. **Run the program:**
   ```bash
   python voting_analysis.py
   ```
---

## Future Improvements
- Add error handling for incomplete/malformed CSV data.
- Support ranked-choice or proportional representation.
- Export results to Excel or PDF.
- Web-based interface for interactive analysis.

⸻
