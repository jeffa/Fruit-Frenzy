import random
try:
    import tkinter as tk
except ImportError:
    tk = None

class Fruit:
    def __init__(self, canvas, x, size, color='red'):
        self.canvas = canvas
        self.size = size
        self.id = canvas.create_oval(x, 0, x+size, size, fill=color)

    def move(self, dy):
        self.canvas.move(self.id, 0, dy)

    def coords(self):
        return self.canvas.coords(self.id)

    def delete(self):
        self.canvas.delete(self.id)

class Basket:
    def __init__(self, canvas, width, height, color='blue'):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.canvas_width = int(canvas['width'])
        self.canvas_height = int(canvas['height'])
        x1 = (self.canvas_width - width) / 2
        y1 = self.canvas_height - height - 10
        x2 = x1 + width
        y2 = y1 + height
        self.id = canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def move(self, dx):
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        if x1 + dx >= 0 and x2 + dx <= self.canvas_width:
            self.canvas.move(self.id, dx, 0)

    def coords(self):
        return self.canvas.coords(self.id)

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fruit Frenzy")
        self.width = 400
        self.height = 600
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='white')
        self.canvas.pack()
        self.basket = Basket(self.canvas, width=80, height=20, color='blue')
        self.fruits = []
        self.score = 0
        self.lives = 3
        self.speed = 5
        self.spawn_interval = 1500
        self.game_over = False
        self.score_text = self.canvas.create_text(10, 10, anchor='nw',
                                                  text=f"Score: {self.score}", font=('Arial', 14))
        self.lives_text = self.canvas.create_text(10, 30, anchor='nw',
                                                  text=f"Lives: {self.lives}", font=('Arial', 14))
        self.root.bind('<Left>', self.on_left)
        self.root.bind('<Right>', self.on_right)
        self.root.bind('r', self.on_restart)
        self.start_game()

    def start_game(self):
        self.schedule_spawn()
        self.update()

    def schedule_spawn(self):
        if not self.game_over:
            x = random.randint(0, self.width - 30)
            color = random.choice(['red', 'green', 'orange', 'yellow', 'purple'])
            fruit = Fruit(self.canvas, x, size=30, color=color)
            self.fruits.append(fruit)
            self.root.after(self.spawn_interval, self.schedule_spawn)

    def update(self):
        if self.game_over:
            return
        for fruit in self.fruits[:]:
            fruit.move(self.speed)
            x1, y1, x2, y2 = fruit.coords()
            bx1, by1, bx2, by2 = self.basket.coords()
            if x2 >= bx1 and x1 <= bx2 and y2 >= by1:
                fruit.delete()
                self.fruits.remove(fruit)
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
            elif y1 > self.height:
                fruit.delete()
                self.fruits.remove(fruit)
                self.lives -= 1
                self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
                if self.lives <= 0:
                    self.end_game()
                    return
        self.root.after(50, self.update)

    def end_game(self):
        self.game_over = True
        self.canvas.create_text(self.width/2, self.height/2,
                                text="Game Over", font=('Arial', 24), fill='red')
        self.canvas.create_text(self.width/2, self.height/2 + 30,
                                text="Press 'r' to restart", font=('Arial', 14), fill='black')

    def on_left(self, event):
        if not self.game_over:
            self.basket.move(-20)

    def on_right(self, event):
        if not self.game_over:
            self.basket.move(20)

    def on_restart(self, event):
        if self.game_over:
            self.canvas.delete("all")
            self.fruits.clear()
            self.score = 0
            self.lives = 3
            self.game_over = False
            self.score_text = self.canvas.create_text(10, 10, anchor='nw',
                                                      text=f"Score: {self.score}", font=('Arial', 14))
            self.lives_text = self.canvas.create_text(10, 30, anchor='nw',
                                                      text=f"Lives: {self.lives}", font=('Arial', 14))
            self.basket = Basket(self.canvas, width=80, height=20, color='blue')
            self.start_game()

def main():
    if not tk:
        print("Tkinter is required to run this game.")
        return
    Game()
    tk.mainloop()

if __name__ == '__main__':
    main()