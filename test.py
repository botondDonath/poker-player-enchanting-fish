import player


test_data = {
  "tournament_id":"550d1d68cd7bd10003000003",

  "game_id":"550da1cb2d909006e90004b1",



  "round":0,

  "bet_index":0,

  "small_blind": 10,


  "current_buy_in": 320,

  "pot": 400,

  "minimum_raise": 240,


  "dealer": 1,


  "orbits": 7,


  "in_action": 1,

  "players": [
      {

          "id": 0,

          "name": "Albert",

          "status": "active",





          "version": "Default random player",

          "stack": 1010,


          "bet": 320
      },
      {
          "id": 1,
          "name": "Bob",
          "status": "active",
          "version": "Default random player",
          "stack": 1590,
          "bet": 80,
          "hole_cards": [

              {
                  "rank": "5",
                  "suit": "hearts"
              },
              {
                  "rank": "2",
                  "suit": "diamonds"
              }
          ]
      },
      {
          "id": 2,
          "name": "Chuck",
          "status": "out",
          "version": "Default random player",
          "stack": 0,
          "bet": 0
      }
  ],
  "community_cards": [
      {
          "rank": "4",
          "suit": "spades"
      },
      {
          "rank": "A",
          "suit": "hearts"
      },
      {
          "rank": "6",
          "suit": "clubs"
      }
  ]
}


def main():
    p = player.Player()
    current_bet = p.betRequest(test_data)
    test_data["players"][1]["bet"] = current_bet
    print "Type is: " + str(type(current_bet))
    if type(current_bet) is int and current_bet >= 0:
        print 'TEST OK'
    else:
        print 'TEST FAILED'

    print "Current bet: " + str(current_bet)





if __name__ == '__main__':
    main()