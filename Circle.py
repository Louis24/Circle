import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

class CircularCropApp:
  def __init__(self, master):
    self.master = master
    self.master.title("Circular Crop Tool")

    self.canvas = tk.Canvas(self.master)
    self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    self.load_button = tk.Button(self.master, text="Open Image", command=self.load_image)
    self.load_button.pack(side=tk.LEFT)

    self.crop_button = tk.Button(self.master, text="Crop Circular Area", command=self.crop_circular_area)
    self.crop_button.pack(side=tk.RIGHT)

    self.image_path = None
    self.original_image = None
    self.display_image = None
    self.circle_id = None
    self.start_x = 0
    self.start_y = 0

    self.canvas.bind("<B1-Motion>", self.on_drag)
    self.canvas.bind("<ButtonPress-1>", self.on_click)

  def load_image(self):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
      self.image_path = file_path
      self.original_image = Image.open(file_path)
      # Resize the image to fit the screen
      screen_width = self.master.winfo_screenwidth() - 100  # Adjust the width as needed
      screen_height = self.master.winfo_screenheight() - 100  # Adjust the height as needed
      self.original_image = self.original_image.resize((screen_width, screen_height), Image.LANCZOS)
      self.display_image = ImageTk.PhotoImage(self.original_image)
      self.canvas.config(width=screen_width, height=screen_height)
      self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)

  def crop_circular_area(self):
    if self.original_image:
      image_width, image_height = self.original_image.size
      radius = min(abs(self.end_x - self.start_x), abs(self.end_y - self.start_y)) / 2
      center_x = (self.start_x + self.end_x) / 2
      center_y = (self.start_y + self.end_y) / 2

      mask = Image.new("L", (image_width, image_height), 0)
      draw = ImageDraw.Draw(mask)
      draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)

      circular_image = Image.new("RGBA", (image_width, image_height))
      circular_image.paste(self.original_image, mask=mask)

      save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
      if save_path:
        circular_image.save(save_path)

  def on_click(self, event):
    self.start_x = self.canvas.canvasx(event.x)
    self.start_y = self.canvas.canvasy(event.y)
    self.circle_id = self.canvas.create_oval(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

  def on_drag(self, event):
    self.end_x = self.canvas.canvasx(event.x)
    self.end_y = self.canvas.canvasy(event.y)
    # Adjust the ellipse to be a circle
    radius = min(abs(self.end_x - self.start_x), abs(self.end_y - self.start_y)) / 2
    center_x = (self.start_x + self.end_x) / 2
    center_y = (self.start_y + self.end_y) / 2
    self.canvas.coords(self.circle_id, center_x - radius, center_y - radius, center_x + radius, center_y + radius)

if __name__ == "__main__":
  root = tk.Tk()
  app = CircularCropApp(root)
  root.mainloop()
