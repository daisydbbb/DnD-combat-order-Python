import random
import tkinter as tk
from tkinter.filedialog import askopenfilename

class DndCombatSequence:
  def __init__(self):
    # Tkinter GUI setup
    self.root = tk.Tk()
    self.root.geometry('400x250')
    self.root.title("DnD Combat Dice Rolling ⚔️🐉")
    self.setup_widgets()
    self.player_list = []

  def setup_widgets(self):
    '''This is the function that sets up the GUI widges: display, load button and exit button
    '''
    self.result_display = tk.Text(self.root, height=10, width=50)
    self.result_display.pack(pady=20)

    self.load_button = tk.Button(self.root, text="Load File and Play", command=self.load_file)
    self.load_button.pack(side=tk.LEFT, padx=(20, 10))

    self.exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
    self.exit_button.pack(side=tk.RIGHT, padx=(10, 20))

  def show_result(self, result):
    '''This function cleans up the old result and display the new result on the widget
    '''
    self.result_display.delete('1.0', tk.END)
    self.result_display.insert('1.0', result)

  def load_file(self):
    '''This function will open the file and call the major functions of the game app
    '''
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        print('File path not found!')
        return
    self.read_file(filepath)
    self.calc_score()
    self.sort_order()
    self.show_result(self.modify())

  def read_file(self, filePath):
    '''This function reads the file and store player and matching dex in player_list
    '''
    with open(filePath, 'r') as file:
      next(file)  # Skip the first line
      for line in file:
          player, dexterity = (item.strip() for item in line.split(","))
          if not dexterity.isdigit():
              raise ValueError(f'{dexterity} is not an integer!')
          self.player_list.append([player, int(dexterity)])

  def calc_score(self):
    '''This function adds a random number between 1-20 to modified dex score, and append
       the total score to the back of each player's list
    '''
    for player in self.player_list:
      dex = player[1]
      score = random.randint(1, 21) + (dex-10)/2 #simulate dice rolling
      player.append(score)
    return self.player_list

  def modify(self):
    '''This function turns list result into a string and add team emoji at the back of each
       character. It will return the string of combat order
    '''
    result = []
    for player in self.player_list:
      if player[0].startswith('NPC'):
        result.append(f'{player[0]}🧟')
      else:
        result.append(f'{player[0]}🧝')
    order = 'Combat order: '+ ' --> '.join(result)
    return order

  def sort_order(self):
    '''This funtion sort the play_list from highest to lowest based on:
       1) total score and 2) inital dexterity
    '''
    self.player_list.sort(reverse = True, key = lambda item: item[2])

    # if same score, higher dex first
    for i in range(len(self.player_list)-1):
      if self.player_list[i][2] == self.player_list[i+1][2]:
        left = i
        right = i+1
        # find all the items with same score
        while right < len(self.player_list) and self.player_list[left][2] == self.player_list[right][2]:
          right += 1
        # parse the sublist
        sublist = self.player_list[left: right]
        # sort the sublist based on dex score at index1
        sublist.sort(reverse = True, key = lambda item: item[1])

        # replace sublist in the old list
        for j in range(left, right):
          self.player_list[j]= sublist[j-left]
    print(self.player_list)

  def run_app(self):
    '''This funciton will run the app
    '''
    self.root.mainloop()

if __name__ == "__main__":
  game = DndCombatSequence()
  game.run_app()

