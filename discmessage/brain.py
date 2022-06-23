import json

options = {
	"waterbothelp": """Welcome to WaterBot 1.0 help menu! Options are:
	log
	register
	remove
	start
	track
	start
	end""",
	"waterbothelplog": """logs contestant water ingestion when given a contest name and amount in mL
	example use: '!log [CONTEST_NAME] mL'
	""",
	"waterbothelpregister": """registers users into water contest
	example use: '!register [USER] or [CONTEST_NAME]'
	""",
	"waterbothelpremove": """removes a user from a water contest
	example use '!remove [USER] or [CONTEST_NAME]'
	""",
	"waterbothelptrack": """displays current water ingestion of a given contest
	example use: '!track [CONTEST_NAME]'
	""",
	"waterbothelpstart": """displays current water contestants and contest
	example use: '!start [CONTEST_NAME]'
	""",
    "waterbothelpend": """removes a contest
    example use: '!end [CONTEST_NAME]"""
}
log = {
    'log': '',
    'register': '',
    'remove': '',
    'track': '',
    'start': '',
    'end': '',
}
with open('waterlog.json') as f:
    contests = json.load(f)

def writelog():
    with open('waterlog.json', 'w') as f:
        json.dump(contests, f)

def parse(message):
    parsed = str(message.content)[1:]
    dp = False
    if ' ' in parsed:
        deepParse = parsed.split(' ')
        cName = deepParse[1]
        dp = True

    if parsed in options.keys():
        return options[parsed]
    elif dp == True and deepParse[0] in log.keys():
        if deepParse[0] == 'start':
            if cName not in contests.keys():
                contests[cName] = log
                writelog()
                return cName + " has begun!"
            else:
                return cName + " has already started!"

        elif deepParse[0] == 'end':
            try:
                header = "{:<15} {:<10}\n".format('user', 'amount')
                cLog = contests[cName]['track']
                for k, v in cLog.items():
                    row = "{:<15} {:<10}mL\n".format(k, v)
                    header += row
                final = "final rankings: \n" + header
                return final

            except:
                return "unable to end - not found"

        elif deepParse[0] == 'track':
            header = "{:<15} {:<10}\n".format('user', 'amount')
            cLog = contests[cName]['track']
            for k, v in cLog.items():
                row = "{:<15} {:<10}mL\n".format(k, v)
                header += row
            return header

        elif deepParse[0] == 'log':
            if message.author.name in contests[cName]['register']:
                if contests[cName]['track'] != '':
                    contests[cName]['track'][message.author.name] += int(deepParse[2])
                    writelog()
                    return f'logged {message.author.name} in {cName}'
                elif message.author.name not in contests[cName]['track'] and isinstance(contests[cName]['track'], dict):
                    contests[cName]['track'][message.author.name] = int(deepParse[2])
                    writelog()
                    return f'logged {message.author.name} in {cName}'
                else:
                    contests[cName]['track'] = {message.author.name: int(deepParse[2])}
                    writelog()
                    return f'logged {message.author.name} in {cName}'
            else:
                return f'user not registered in {cName}'

        elif deepParse[0] == 'register':
            registered = contests[cName]['register']
            if registered == '':
                contests[cName]['register'] = [message.author.name]
                writelog()
                return f'registered {message.author.name} in {cName}'

            else:
                registered.append(message.author.name)
                writelog()
                return f'registered {message.author.name} in {cName}'

        elif deepParse[0] == 'remove':
            loc = contests[cName]['register'].index(deepParse[1])
            del contests[cName]['register'][loc]
            del contests[cName]['track'][deepParse[1]]



    else:
        return "option not found"



