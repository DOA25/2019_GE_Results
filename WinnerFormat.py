parties ={
	"CON":"Conservertive",
	"LAB": "Labour",
	"SPE": "Labour",
	"SF": "Sinn Fein",
	"DUP": "Democratic Unionist Party",
	"LD": "Liberal Democrats",
	"SNP": "Scottish National Party",
	"GRN": "Green Party",
	"PC": "Plaid Cymru",
	"SDL": "Social Democratic & Labour Party",
	"APN":"Alliance Party" 

}

def formatParty(info):
	return parties[info[0:3].strip()]