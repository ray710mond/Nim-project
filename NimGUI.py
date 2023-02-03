from tkinter import *
from PIL import ImageTk,Image
from NimAI import AI

root = Tk()
root.title("Nim Game by Raymond Provost")
root.iconbitmap("NimGameIcon.ico")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

print(screen_width)
print(screen_height)

entry2 = "3, 5, 4, 7, 2, 6"
player1 = "Player 1"
player2 = "AI"
play_style = "normal"
circles_per_pile = entry2.split(", ")
num_piles = len(circles_per_pile)
end_game = []
for i in range(len(circles_per_pile)):
    circles_per_pile[i] = int(circles_per_pile[i])
    end_game.append(0)

pixel_img = Image.open("pixel.png")
pixel = ImageTk.PhotoImage(pixel_img)

current_player = Label(root, text=player1, image = pixel, width = 75, height = 30, fg = "black", compound = "c")
current_player.grid(row=0, column=num_piles)
button_quit = Button(root, text="Quit Game", image = pixel, width = 75, height = 30, compound = "c", bg = "red", fg = "black", command=root.quit).grid(row = 1, column = num_piles)

circle_size = min([(screen_height - 175) // max(circles_per_pile), (screen_width - 75 - (num_piles)) // num_piles])

nim_png = Image.open("NimCircle.png")
nim_circle_img = nim_png.resize((circle_size, circle_size), Image.ANTIALIAS)
nim_circle = ImageTk.PhotoImage(nim_circle_img)

def click(pile_num, button_num):
    for i in range(button_num, circles_per_pile[pile_num]):
        button = buttons[pile_num][i]
        button.grid_forget()
        button.destroy()
        empty_space = Label(root, image = pixel, width = circle_size, height = circle_size)
        empty_space.grid(row = (max(circles_per_pile)-i + 1), column = pile_num, sticky = "SW")
        buttons[pile_num][i] = empty_space
    circles_per_pile[pile_num] = button_num

    if current_player["text"] == player1:
        current_player["text"] = player2
    elif current_player["text"] == player2:
        current_player["text"] = player1
    if circles_per_pile == end_game:
        if play_style == "misere":
            win_message = Label(root, text=current_player["text"]+" WINS!", image = pixel, width = screen_width/1.5, height = (screen_height-140), fg = "black", compound = "c")
        elif play_style == "normal":
            if current_player["text"] == player1:
                winner = player2
            elif current_player["text"] == player2:
                winner = player1
            win_message = Label(root, text=winner+" WINS!", image = pixel, width = screen_width/1.5, height = (screen_height-140), fg = "black", compound = "c")
        win_message.grid(row = 2, column = 0)
        current_player.grid_forget()

    if current_player["text"] == "AI":
        target_state = AI(circles_per_pile, play_style)
        print(target_state)
        for i in range(len(circles_per_pile)):
            if circles_per_pile[i] != target_state[i]:
                click(i, target_state[i])
        print("AI moved")

buttons = []
for i in range(num_piles):
    buttons.append([])
    for j in range(circles_per_pile[i]):
        button = Button(root, image = nim_circle, width = circle_size, height = circle_size, command=lambda i=i, j=j: click(i, j))
        button.grid(row = (max(circles_per_pile)-j + 1), column = i, sticky = "SW")
        buttons[i].append(button)

def get_state():
    return circles_per_pile

def get_player():
    return current_player

def get_style():
    return play_style

root.mainloop()