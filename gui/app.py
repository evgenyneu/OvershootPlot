import platform

def start_app(app, title):
    app.update()
    app.minsize(app.winfo_width(), app.winfo_height())
    if platform.system() != 'Linux':
        app.after(50, app.iconbitmap('icon.ico'))
    app.configure(background='white')
    app.title(title)

    def main_loop():
      try:
        app.mainloop()
      except UnicodeDecodeError:
        main_loop()

    main_loop()