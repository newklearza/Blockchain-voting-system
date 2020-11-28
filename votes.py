import time
import pickledb
from hashlib import sha256

db = pickledb.load('votes.db', True)

def init_Parties():
    if not db.exists('parties'):
        num_Parties = int(input("Please enter Total number of Entities/Parties/Persons in the Election: "))
        if num_Parties >= 2:
            db.lcreate('Parties')
            for k in range(0, num_Parties):
                exec(f'party_{k} = input("Enter Entity/Party/Person Name: ")')
                exec(f'db.ladd("Parties", party_{k})')
            print('The following Items have been added to the Election: ')
            print(db.lgetall('Parties'))
            db.set('parties', num_Parties)
            input("Press Enter to commence the Election...")
        else:
            print('You need 2 or more Entities to Vote for, Goodbye.')
            exit()

def init_Votes():
    init_Parties()
    print('Welcome to this Blockchain Vote System'.center(60, "-"))
    time.sleep(1)
    print('Today is:', time.ctime())
    time.sleep(1)
    not_13 = False
    while not not_13:
        id = int(input('*** Please Enter Your Valid ID Number to Vote or Enter 9 to Quit: '))
        if str(id) == '9':
            print('Goodbye!'.center(60, "-"))
            time.sleep(1)
            exit()
        if str(id) == '1':
            showWeb()
        if str(id) == '2':
            stat = db.get('Votes')
            print('Printing all party votes recorded in the database:')
            for x in range(0, db.get('parties')):
                a = db.lget('Parties', x)
                print(db.lget('Parties', x).center(10), db.get(a), 'Votes -', "{:.2%}".format(db.get(a) / stat))
            input("Press Enter to continue...")
        if len(str(id)) == 13:
            not_13 = True
    if not db.exists(str(id)):
        print("Enter the Party you would like to vote for, exactly as it reads without the ' '.")
        time.sleep(1)
        while True:
            print('The Nominees are: ', db.lgetall('Parties'))
            vote = input("Please enter one: ")
            if (vote in db.lgetall('Parties')):
                db.set(vote, db.get(vote) + 1)
                db.set(str(id), time.time())
                # Hashes go here
                hashId = sha256(str(id).encode('utf-8')).hexdigest()
                if not db.exists('oldHash'):
                    db.lcreate('Hashes')
                    db.set('oldHash', hashId)  # old
                    db.set('newHash', hashId)  # new
                    db.ladd('Hashes', hashId)
                else:
                    db.set('oldHash', db.get('newHash'))
                    db.set('newHash', hashId)
                    db.ladd('Hashes', hashId)
                db.set('Votes', db.get('Votes') + 1)
                print('Number of', vote, 'Votes:', db.get(vote), 'Out of', db.get('Votes'), ', All Party Votes.', "{:.2%}".format(db.get(vote) / db.get('Votes')))
                time.sleep(1)
                showWeb()
                time.sleep(1)
                input("Press Enter to continue...")
                time.sleep(1)
                print('Goodbye!'.center(60, "-"))
                time.sleep(5)
                exit()
    else:
        print('You have already Voted! Your last vote was on:', time.ctime(db.get(str(id))))
        input("Press Enter to continue...")
        time.sleep(1)
        print('Goodbye!'.center(60, "-"))
        time.sleep(5)
        exit()


votePage = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
    <head>
    <meta content="text/html; charset=ISO-8859-1"
    http-equiv="content-type">
    <title>BlockChain Vote Results</title>
    <link rel="icon" href="icon.ico" type="image/icon type">
    </head>
    <body>
    <div style="background-color:blue;color:yellow;padding:20px;">
    <h2>Hello {person}, Thank You for your vote!</h2>
    </div>
    <div style="background-color:orange;color:black;padding:20px;">
    <p id="spam"></p>
    </div>
    <script>
    function randomtext() {{
    var randomtxt = [
    '"Dwell on the beauty of life. Watch the stars, and see yourself running with them." - Marcus Aurelius',
    '"A kiss is a lovely trick designed by nature to stop speech when words become superfluous." - Ingrid Bergman',
    '"The secret of life, though, is to fall seven times and to get up eight times." - Paulo Coelho'
    ];
     return randomtxt[Math.floor((Math.random() * 3.99))];
    }}
    document.getElementById("spam").innerHTML = randomtext();
    </script>
   <br>
   <div style="background-color:navy;color:orange;padding:20px;">
   <hr>
    <p>Total Amount of Verified Votes: {votesDisplay}</p>
    <br>
    <p>Vote Results so far:</p>
   <p>These are the Nominees Voted for: {partyNames}</p>
   <p>These are the Amount of Votes: {partyResults}</p>
   <hr>
    </div>
    <br>
    <div style="background-color:black;color:red;padding:20px;">
    <p>These Results are accurate as of: {timeDisplay}</p>
    <p>New Hash: {newHash} Old Hash: {oldHash}</p>
    </div>
    <hr>
    </body>
    </html>
    '''

def showWeb():
    person = input('Enter a Display Name (This is confidential): ')
    timeDisplay = time.ctime()
    votesDisplay = db.get('Votes')
    parties = db.get('parties')
    oldHash = db.get('oldHash')
    newHash = db.get('newHash')
    db.lcreate('partyNames')
    db.lcreate('partyResults')
    for x in range(0, parties):
        db.ladd('partyNames', db.lget('Parties', x))
        db.ladd('partyResults', db.get(db.lget('Parties', x)))
    partyNames = db.lgetall('partyNames')
    partyResults = db.lgetall('partyResults')
    db.lremlist('partyNames')
    db.lremlist('partyResults')
    contents = votePage.format(**locals())
    browseLocal(contents)

def strToFile(text, filename):
    output = open(filename, "w")
    output.write(text)
    output.close()

def browseLocal(webpageText, filename='voteResults.html'):
    import webbrowser, os.path
    strToFile(webpageText, filename)
    webbrowser.open("file:///" + os.path.abspath(filename))


init_Votes()
