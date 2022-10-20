from application import app, db
from application.models import User, Stats
from flask import render_template, session, url_for, redirect, request, url_for
import bcrypt
from datetime import datetime
import os
import random

deck = ['2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd', 'Ad', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah']

vev = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
       'J': 10, 'Q': 10, 'K': 10, 'A': 11}

def updateChips(user, newAmt):
    ent = Stats.query.filter_by(username = user).first()
    ent.chip_total = int(newAmt)
    db.session.commit()

def updateWager(user, newAmt):
    ent = Stats.query.filter_by(username = user).first()
    ent.current_wager = int(newAmt)
    db.session.commit()

def updateHandCount(user, newAmt):
    ent = Stats.query.filter_by(username = user).first()
    ent.hands_played = int(newAmt)
    db.session.commit()

def updateWins(user, newAmt):
    ent = Stats.query.filter_by(username = user).first()
    ent.hands_won = int(newAmt)
    db.session.commit()

def getChips(user):
    ent = Stats.query.filter_by(username = user).first()
    return ent.chip_total
    
def getWager(user):
    ent = Stats.query.filter_by(username = user).first()
    return ent.current_wager
    
def getHandCount(user):
    ent = Stats.query.filter_by(username = user).first()
    return ent.hands_played 
  
def getWins(user):
    ent = Stats.query.filter_by(username = user).first()
    return ent.hands_won

def makeWager(user, amt):
    hc = getHandCount(user)
    plusone = int(hc)+ 1
    c = getChips(user)
    new = int(c) - int(amt)
    updateChips(user, int(new))
    updateWager(user, int(amt))
    updateHandCount(user, int(plusone))

def regWin(user, wager):
    w = getWins(user)
    plusone = int(w) + 1
    c = int(getChips(user))
    won = int(wager) + int(wager)
    new = int(c) + int(won)
    updateChips(user, int(new))
    updateWins(user, int(plusone))

def BJWin(user, wager):
    w = getWins(user)
    plusone = int(w) + 1
    c = getChips(user)
    won = wager * 2.5
    new = int(c) + int(won)
    updateChips(user, int(new))
    updateWins(user, int(plusone))

def push(user, wager):
    c = getChips(user)
    won = wager 
    new = int(c) + int(won)
    updateChips(user, int(new))

def newDeck():
    deck = ['2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd', 'Ad', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah']
    return deck

class Hand:
    def __init__(self, who, cards, value):
        self.who = who
        self.cards = cards
        self.value = value

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.who!r}, {self.cards!r}, {self.value!r})')

    def __str__(self):
        return f'{self.who}s hand is {self.cards}, value is {self.value}'

    def __call__(self, pluck):
        self.cards.append(pluck[0])
        vim = value(pluck)
        self.value += vim
        return self.cards

    def __iter__(self):
        return iter([('who', self.who),('cards', self.cards),('value',self.value)])

def stampNow():
	t = datetime.isoformat(datetime.now())
	ti = t.replace('T', " ")
	tim = ti[:-7]
	return tim

def value(hand):
    num = len(hand)
    val = []
    for i in range(int(num)):
        val.append(vev[hand[i][0]])
    if sum(val) < 22:
        return sum(val)
    else:
        x = 11 in val
        if x:
            val.remove(11)
            val.append(1)
            if sum(val) < 22:
                return sum(val)
            else:
                y = 11 in val
                if y:
                    val.remove(11)
                    val.append(1)
                    if sum(val) < 22:
                        return sum(val)
                    else:
                        if sum(val) < 22:
                            return sum(val)
                        else:
                            z = 11 in val
                            if z:
                                val.remove(11)
                                val.append(1)
                                print('is the fourth up your sleeve cowboy?')
                                return sum(val)
                            else:
                                print('busted')
                                return sum(val)
                                
                else:
                    print('busted')
                    return sum(val)
                    
        else:
            print('busted')
            return sum(val)

playerBJ = False
dealerBJ = False

def check_player_BJ(hand):
    numb = len(hand)
    valBJ = []
    for i in range(int(numb)):
        valBJ.append(vev[hand[i][0]])
    if numb == 2:
        if hand[0][0].isalpha() and hand[0][1].isalpha():
            if sum(valBJ) == 21:
                playerBJ = True
                return playerBJ 
            else:
                pass
        else:
            pass
    else:
        pass

def check_dealer_BJ(hand):
    numb = len(hand)
    valBJ = []
    for i in range(int(numb)):
        valBJ.append(vev[hand[i][0]])
    if numb == 2:
        if hand[0][0].isalpha() and hand[0][1].isalpha():
            if sum(valBJ) == 21:
                dealerBJ = True
                return dealerBJ 
            else:
                pass
        else:
            pass
    else:
        pass



@app.route('/')
def index():
    if session.get('user') is None:
        return render_template('auth/loginform.html')
    else:
        username = session['user']
        chips = getChips(username)
        hands = getHandCount(username)
        wins = getWins(username)
        return render_template('first_test.html', uu = username, chips = chips, hands = hands, wins = wins)

@app.route('/createuser', methods=['POST', 'GET'])
def hashes():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirmpass']

        if confirm != password:
            return render_template('auth/createform.html')

        else:
            b = password.encode('utf-8') 
            pw_hash = bcrypt.hashpw(b, bcrypt.gensalt())
            stamp = stampNow()
            profile = User(username = username, email = email, hashy = pw_hash, tstamp = stamp)
            cage = Stats(username=username, chip_total=500, current_wager=0, hands_played=0, hands_won=0)
            db.session.add(profile)
            db.session.commit()
            db.session.add(cage)
            db.session.commit()
            

            return render_template('auth/loginform.html')        

    else:

        return render_template('auth/createform.html')
      

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        passy = request.form['password']
        bb = passy.encode('utf-8')

        q = User.query.filter_by(username = username).first()
        hashy = q.hashy
        
        pw_hash = bcrypt.checkpw(bb, hashy)

        if pw_hash == True:
            session['user'] = username
            uu = username
            chips = getChips(username)
            hands = getHandCount(username)
            wins = getWins(username)
            return render_template('first_test.html', uu = uu, chips = chips, hands = hands, wins = wins)

        else:
            return render_template('auth/loginform.html')        

    else:
        if session.get('user') is None:
            return render_template('auth/loginform.html')
        else:
            uu = session['user']
            uu = username
            chips = getChips(username)
            hands = getHandCount(username)
            wins = getWins(username)
            return render_template('first_test.html', user = uu, chips = chips, hands = hands, wins = wins)

@app.route('/deal', methods=['POST', 'GET'])
def deal():
    if request.method == 'POST':
        bet = request.form['wager']
        if session.get('user') is None:
            return render_template('auth/loginform.html')
        else:
            uu = session['user']
            session['bet'] = bet
            makeWager(uu, bet)
            chips = getChips(uu)
            wager = int(bet)
            deck = newDeck()
            random.shuffle(deck)
            c = []
            c.append(deck.pop())
            c.append(deck.pop())
            v = value(c)
            p = Hand('player', c, v)
            phd = dict(Hand('player', c, v))
    
            cc = []
            cc.append(deck.pop())
            cc.append(deck.pop())
            vv = value(cc)
            d = Hand('dealer', cc, vv)
            dhd = dict(Hand('dealer', cc, vv))
    
            playerBJ = check_player_BJ(phd['cards'])
            dealerBJ = check_dealer_BJ(dhd['cards'])
            sink = dhd['cards']
            bink = phd['cards']
            uu = session['user']    
            pcard1 = phd['cards'][0]
            pcard2 = phd['cards'][1]
            pval = phd['value']
            dcard1 = dhd['cards'][0]
            session['dealer'] = dhd
            session['player'] = phd
            session['deck'] = deck
            if playerBJ == True:
                info = "Player has Blackjack!!"
                info2 = "Player wins! Game Over."
                dcard2 = dhd['cards'][1]
                dval = int(value(dhd['cards']))
                winnings = int(wager) * 2.5
                BJWin(uu, wager)
                chips = getChips(uu)
                return render_template('grid2loss_test.html', winnings = winnings, chips = chips, bink = bink, uu = uu, info = info, info2 = info2, pval = pval, sink = sink, dval = dval)
            elif dealerBJ == True:
                winnings = 0
                info = "Dealer has Blackjack!!"
                info2 = "Dealer wins! Game Over."
                dcard2 = dhd['cards'][1]
                dval = int(value(dhd['cards']))
                return render_template('grid2loss_test.html', winnings = winnings, wager = wager, chips = chips, bink = bink, uu = uu, info = info, info2 = info2, pval = pval, sink = sink, dval = dval)
            elif playerBJ == True and dealerBJ == True:
                info = "Both Player and Dealer have Blackjack!!"
                info2 = "Issa Push! Game Over."
                dcard2 = dhd['cards'][1]
                dval = int(value(dhd['cards']))
                push(uu, wager)
                chips = getChips(uu)
                return render_template('grid2loss_test.html', winnings = wager, wager = wager, chips = chips, bink = bink, uu = uu, info = info, info2 = info2, pval = pval, sink = sink, dval = dval)
            else:
                winnings = 0
                info = 'hit stand or double'
                info2 = ''
                dcard2 = "cardBack"
                dval = int(value(list(dhd['cards'][0][0])))
            return render_template('grid1_test.html', winnings = winnings, wager = wager, chips = chips, bink = bink, uu = uu, pval = pval, info = info, info2 = info2, dcard1 = dcard1, dcard2 = dcard2, dval = dval)

    else:
        return redirect(url_for('login'))
    
@app.route('/hit1')
def hit1():
    wager = session['bet']
    uu = session['user']
    chips = getChips(uu)
    winnings = 0
    phd = session['player']
    dhd = session['dealer']
    deck = session['deck']
    phd['cards'].append(deck.pop())
    nol = value(phd['cards'])
    phd['value'] = nol
    pval = phd['value']
    bink = phd['cards']
    sink = dhd['cards']
    dval = dhd['value']
    session['dealer'] = dhd
    session['player'] = phd
    session['deck'] = deck
    if phd['value'] > 21:
        info = 'Player busts'
        info2 = 'Game Over'
        
        return render_template('grid2loss_test.html', winnings = winnings, wager = wager, chips = chips, bink = bink, uu = uu, info = info, info2 = info2, pval = pval, sink = sink, dval = dval)
    else:
        info = 'hit or '
        info2 = 'stand?'
        dcard1 = dhd['cards'][0]
        dcard2 = "cardBack"
        dval = int(value(list(dcard1[0][0])))
    return render_template('grid1_test.html', winnings = winnings, wager = wager, chips = chips, bink = bink, uu = uu, info = info, info2 = info2, pval = pval, dcard1 = dcard1, dcard2 = dcard2, dval = dval)

@app.route('/double')
def double():
    wager = session['bet']
    double = int(wager) + int(wager)
    
    uu = session['user']
    chips = getChips(uu)
    dub = int(chips) - int(wager)
    updateChips(uu, dub)
    chips = getChips(uu)
    wager = double
    session['bet'] = double
    winnings = 0
    phd = session['player']
    dhd = session['dealer']
    deck = session['deck']
    phd['cards'].append(deck.pop())
    nol = value(phd['cards'])
    phd['value'] = nol
    pval = phd['value']
    bink = phd['cards']
    sink = dhd['cards']
    dval = dhd['value']
    session['dealer'] = dhd
    session['player'] = phd
    session['deck'] = deck
    if phd['value'] > 21:
        info = 'Player busts'
        info2 = 'Game Over'
        
        return render_template('grid2loss_test.html', winnings = winnings, wager = wager, chips = chips, bink = bink, uu = uu, info = info, info2 = info2, pval = pval, sink = sink, dval = dval)
    else:
        return redirect(url_for('stand2'))
    
@app.route('/stand2')
def stand2():
    wager = session['bet']
    uu = session['user']
    chips = getChips(uu)
    phd = session['player']
    dhd = session['dealer']
    deck = session['deck']
    if dhd['value'] >= 17 and dhd['value'] <= 21:
        if phd['value'] < dhd['value']:
            winnings = 0
            info = 'Dealer has highest hand without going over'
            info2 = 'Player loses, Game Over'
        elif phd['value'] > dhd['value']:
            regWin(uu, wager)
            winnings = int(wager) * 2
            chips = getChips(uu)
            info = 'Player has highest hand without going over'
            info2 = 'Player wins, Game Over'
        elif phd['value'] == dhd['value']:
            push(uu, wager)
            winnings = int(wager)
            chips = getChips(uu) 
            info = 'Player and dealer tie'
            info2 = 'issa push'
    elif dhd['value'] < 17:
        dhd['cards'].append(deck.pop())
        noop = value(dhd['cards'])
        dhd['value'] = noop
        session['dealer'] = dhd
        session['player'] = phd
        session['deck'] = deck    
        return redirect(url_for('standing2'))
    elif dhd['value'] > 21:
        regWin(uu, wager)
        winnings = int(wager) * 2
        chips = getChips(uu)
        info = 'Dealer busts'
        info2 = 'Player Wins, Game Over!'
    session['dealer'] = dhd
    session['player'] = phd
    session['deck'] = deck    
    sink = dhd['cards']        
    bink = phd['cards']
    pval = phd['value']
    dval = dhd['value']
    return render_template('grid2loss_test.html', winnings = winnings, wager = wager, chips = chips, bink = bink, sink = sink, uu = uu, info = info, info2 = info2, pval = pval, dval = dval)

@app.route('/logout')
def logout():
    session.pop('user', None)
        
    return render_template('auth/loginform.html')
