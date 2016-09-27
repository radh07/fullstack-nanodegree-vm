#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
import random

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM Matches;")
    conn.commit()
    print "delete matches = ", cur.rowcount 
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    print "inside deleteplayers"
    conn = connect()
    print conn
    cur = conn.cursor()
    cur.execute("DELETE FROM Players;")
    print "delete players = ", cur.rowcount
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(Id) FROM Players;")
    count = cur.fetchone()
    conn.close()
    return count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO Players (Name) VALUES (%s);", (bleach.clean(name),))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT Name, Players.ID, \
        coalesce(SCORECARD.WON,0) as WON, coalesce(SCORECARD.LOST,0) as LOST FROM \
        (SELECT coalesce(WON_GB.ID, LOST_GB.ID) AS ID, \
        coalesce(WON, 0) AS WON, coalesce(LOST, 0) AS LOST \
        FROM \
        (SELECT WINNER AS Id, COUNT(Id) AS WON FROM Matches \
        GROUP BY WINNER) AS WON_GB \
        FULL OUTER JOIN \
        (SELECT LOSER  AS Id, COUNT(Id) AS LOST FROM Matches \
        GROUP BY LOSER) AS LOST_GB \
        ON WON_GB.ID = LOST_GB.ID) AS SCORECARD \
        RIGHT OUTER JOIN \
        Players \
        on SCORECARD.ID = Players.Id \
        ORDER BY WON DESC;")
    rows = cur.fetchall()
    conn.close()
    # Process the fetched rows here
    standings = [(row[1], row[0], row[2], row[2]+row[3]) for row in rows]
    # print "standings ", standings
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    query = "INSERT INTO Matches (Winner, Loser) VALUES (%s, %s);"
    data = ( int(bleach.clean(winner)), int(bleach.clean(loser)) )
    cur.execute( query , data )
    
    conn.commit()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    if not standings:
        return
    newwon = won = standings[0][2]
    listnum = 0
    # create a list (outer) of lists (inner) of tuples
    # tuples contain the ID/name combo of players
    # inner list contains tuples of players that won the same number of games so far in the tournament
    # outer list contains all the players grouped per their wins
    plist = [[] for x in range(newwon+1)]
    for s in standings:
        newwon = s[2]
        if newwon != won:
            listnum += 1
            won = newwon
        plist[listnum].append( (s[0], s[1]) )
    
    # Now, for each inner list (that is, for every rank, shuffle the players and pair them off)
    retlist = []
    for e in plist:
        random.shuffle(e)
        for i in range(0, len(e) , 2):
            retlist.append( (e[i] + e[i+1]) )
    return retlist






