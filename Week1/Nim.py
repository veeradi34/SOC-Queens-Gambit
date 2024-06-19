nim_board=[[0 for i in range(7)] for j in range(4)]
k=0

for j in range(4):
     for i in range(j+1):
        nim_board[j][3-i]="|"
        nim_board[j][3]="|"
        nim_board[j][3+i]="|"
for i in range(4):
    for j in range(7):
        print(nim_board[i][j],end=" ")
    print(f" Row {i+1}")
    print("\n")
game_is_on=True
chance=0

while game_is_on:
    places=[]
    if chance%2==0:
        print("Player 1 turn: ")
        b=int(input("Choose Row 1,2,3 or 4: "))
        print(nim_board[b-1])
        for i in range(len(nim_board[b-1])):
            if nim_board[b-1][i]=="|":
                places.append(i)
        numberofStick=int(input("Enter number of sticks to delete: "))
        if numberofStick<=len(places):
            for j in range(numberofStick):
                nim_board[b-1].pop(places[len(places)-1-j])
        else:
            print("Invalid Input, Game Ended!")
            game_is_on=False

    if chance%2!=0:
        print("Player 2 turn: ")
        b = int(input("Choose Row 1,2,3 or 4: "))
        print(nim_board[b -1])
        for i in range(len(nim_board[b-1])):
            if nim_board[b-1][i] == "|":
                places.append(i)
        numberofStick = int(input("Enter number of sticks to delete: "))
        if numberofStick <= len(places):
            for j in range(numberofStick):
                nim_board[b-1].pop(places[len(places)-1-j])
        else:
            print("Invalid Input, Game Ended!")
            game_is_on=False
    sum=0

    for i in range(len(nim_board)):
        for j in range(len(nim_board[i])):

            if nim_board[i][j]=="|":
                sum=sum+1
                print(nim_board[i][j],end=" ")
            else:
                print(" ",end=" ")
        print(f"Row {i+1}")

        print("\n")
    if sum==0:
        if chance%2==0:
            print("Player 2 wins")
        else:
            print("Player 1 wins")
        game_is_on=False

    chance=chance+1
