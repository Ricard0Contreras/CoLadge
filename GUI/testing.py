import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Square Grid Example")
        self.canvas = tk.Canvas(self, width=500, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")

        # Define grid parameters
        self.rows = 20
        self.columns = 20
        self.cellwidth = 25
        self.cellheight = 25
        self.rect = {}

        # Create rectangles for each cell
        for column in range(self.columns):
            for row in range(self.rows):
                x1 = column * self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags="rect")

        # Add a scale for rows and columns
        self.row_scale = tk.Scale(self, from_=1, to=self.rows, orient="horizontal", label="Rows", command=self.update_grid)
        self.row_scale.pack()
        self.column_scale = tk.Scale(self, from_=1, to=self.columns, orient="horizontal", label="Columns", command=self.update_grid)
        self.column_scale.pack()

    def update_grid(self, event=None):
        # Update grid based on scale values
        self.rows = self.row_scale.get()
        self.columns = self.column_scale.get()

        for column in range(self.columns):
            for row in range(self.rows):
                x1 = column * self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", tags="rect")
        
        for column in range(self.columns):
            for row in range(self.rows):
                x1 = column * self.cellwidth
                y1 = row * self.cellheight
                x2 = y1 - self.cellwidth
                y2 = y1 - self.cellheight
                self.rect[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", tags="rect")

if __name__ == "__main__":
    app = App()
    app.mainloop()