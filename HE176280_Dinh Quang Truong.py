import random

player_money = 1000
player_chips = 0

def buy_chips(amount):
    global player_money, player_chips
    chips_price = 11
    max_chips = amount // chips_price
    player_chips += max_chips
    player_money -= max_chips * chips_price
    leftover_cash = amount - (max_chips * chips_price)
    return leftover_cash

def sell_chips(amount):
    global player_money, player_chips
    chips_price = 10
    sold_chips = min(amount // chips_price, player_chips)
    player_chips -= sold_chips
    player_money += sold_chips * chips_price
    return sold_chips * chips_price

def play_craps():
    global player_money, player_chips
    dice = [random.randint(1, 6), random.randint(1, 6)]
    roll_sum = sum(dice)
    
    if roll_sum == 7 or roll_sum == 11:
        player_money += player_chips * 10
        player_chips = 0
        print("You win!")
    elif roll_sum == 2 or roll_sum == 3 or roll_sum == 12:
        player_chips = 0
        print("You lose!")
    else:
        point = roll_sum
        print("Your point is", point)
        while True:
            dice = [random.randint(1, 6), random.randint(1, 6)]
            roll_sum = sum(dice)
            print("You rolled", roll_sum)
            if roll_sum == point:
                player_money += player_chips * 10
                player_chips = 0
                print("You win!")
                break
            elif roll_sum == 7:
                player_chips = 0
                print("You lose!")
                break

def play_arups_game_of_dice():
    global player_money, player_chips
    dice = [random.randint(1, 6), random.randint(1, 6)]
    roll_sum = sum(dice)
    
    if roll_sum == 11 or roll_sum == 12:
        player_money += player_chips * 10
        player_chips = 0
        print("You win!")
    elif roll_sum == 2:
        player_chips = 0
        print("You lose!")
    else:
        point = roll_sum
        print("Your point is", point)
        dice = [random.randint(1, 6), random.randint(1, 6)]
        roll_sum = sum(dice)
        print("You rolled", roll_sum)
        if roll_sum > point:
            player_money += player_chips * 10
            player_chips = 0
            print("You win!")
        else:
            player_chips = 0
            print("You lose!")

def status_report():
    global player_money, player_chips
    print("Money: $", player_money)
    print("Chips:", player_chips)

def main():
    global player_money, player_chips
    
    while True:
        print("1) Buy chips")
        print("2) Sell chips")
        print("3) Play Craps")
        print("4) Play Arup's Game of Dice")
        print("5) Status Report")
        print("6) Quit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            amount = int(input("Enter the amount of money to buy chips: $"))
            leftover_cash = buy_chips(amount)
            print("You bought", player_chips, "chips.")
            print("Leftover cash: $", leftover_cash)
        elif choice == '2':
            amount = int(input("Enter the amount of chips to sell: "))
            sold_cash = sell_chips(amount)
            print("You sold", amount, "chips.")
            print("Received cash: $", sold_cash)
        elif choice == '3':
            play_craps()
        elif choice == '4':
            play_arups_game_of_dice()
        elif choice == '5':
            status_report()
        elif choice == '6':
            print("Quitting...")
            break
        else:
            print("Invalid choice. Please try again.")

    print("Money left after gambling: $", player_money)

if __name__ == "__main__":
    main()