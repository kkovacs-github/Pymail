#!/usr/bin/env python

"""
Pymail by Kristof Kovacs and Daniel Zheleznov
REQUIREMENTS:
	1. Google mail account.
	2. Turn on less secure app access in Google mail account.
	3. Python 3.
"""

#Imports
import smtplib
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo


def login():
	'''
	Called when login button is pressed.

	1. Stores is email address and password input into a variable and globalises it.
	2. Deletes all text in entries.
	3. Checks if the last ten characters of the email address input is equal to '@gmail.com' to confirm that the email is a Google Mail.
	4. Checks if password input does not equal to nothing.
	5. If the conditions return true then the window will be destroyed, a pop up window will appear letting the user know their login was successful and the email() function is called.
	6. Else the User will know the login was unsuccessful.
	'''

	global email_address_input
	global password_input

	email_address_input = email_address.get()
	password_input = password.get()

	email_address_entry.delete(0, END)
	password_entry.delete(0, END)

	if (email_address_input[-10:] == '@gmail.com') and (password_input != ''):
		showinfo('Login Successful', 'Successfully logged in as {}'.format(email_address_input))
		window.destroy()
		email()

	else:
		showinfo('Error', 'Login Unsuccessful.')


def email():
	'''
	Called when Login() is successful.

	1. Creates a new window with basic email entries.
	2. Configures the window to be placed at the centre of the screen.
	3. Stores new inputs into variables and are globalised to be used in other functions.
	4. The window and progress_bar is globalised so they can be used when emails are sent.

	Note: The window like the login window is not resizeable because the app is not meant to be resized.
	'''

	global window
	global progress_bar

	global receiver_input
	global subject_input
	global message_box

	window = Tk()
	window.title('Pymail')
	window.resizable(False, False)
	window.config(bg = '#303942')

	window_width = 1000
	window_height = 800

	screen_width = window.winfo_screenwidth()
	screen_height = window.winfo_screenheight()

	x = int((screen_width / 2) - (window_width / 2))
	y = int((screen_height / 2) - (window_height / 2))

	window.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))

	receiver_input = StringVar()
	subject_input = StringVar()

	from_label1 = Label(window, text = 'From:', width = 20, height = 2, fg = 'white', bg = '#303942', font = ('calibri', 25))
	from_label1.grid(row = 0, column = 0)

	from_label2 = Label(window, text = email_address_input, width = 35, height = 1, fg = 'black', bg = 'white', font = ('calibri', 20))
	from_label2.grid(row = 0, column = 1)

	to_label = Label(window, text = 'To:', width = 20, height = 2, fg = 'white', bg = '#303942', font = ('calibri', 25))
	to_label.grid(row = 1, column = 0)

	to_entry = Entry(window, textvariable = receiver_input, width = 35, fg = 'black', bg = 'white', font = ('calibri', 20))
	to_entry.grid(row = 1, column = 1)

	subject_label = Label(window, text = 'Subject:', width = 20, height = 2, fg = 'white', bg = '#303942', font = ('calibri', 25))
	subject_label.grid(row = 2, column = 0)

	subject_entry = Entry(window, textvariable = subject_input, width = 35, fg = 'black', bg = 'white', font = ('calibri', 20))
	subject_entry.grid(row = 2, column = 1)

	message_box = Text(window, width = 70, height = 13, fg = 'black', bg = 'white', font = ('calibri', 20))
	message_box.place(relx = 0.5, rely = 0.9, anchor = 's')

	email_by_kristof = Label(window, text = 'Email app by Kristof Kovacs', width = 30, height = 1, fg = 'white', bg = '#303942', font = ('calibri', 20))
	email_by_kristof.place(relx = 0.25, rely = 0.975, anchor = 's')

	send_button = Button(window, text = 'Send', width = 10, height = 1, fg = 'black', bg = 'white', font = ('arial', 15), command = send)
	send_button.place(relx = 0.5, rely = 0.975, anchor = 's')

	spam_button = Button(window, text = 'Spam X10', width = 10, height = 1, fg = 'black', bg = 'white', font = ('arial', 15), command = spam)
	spam_button.place(relx = 0.7, rely = 0.975, anchor = 's')

	progress_bar = ttk.Progressbar(window, orient = HORIZONTAL, length = 200, mode = 'determinate')
	progress_bar.place(relx = 0.88, rely = 0.965, anchor = 's')


def send():
	'''
	Called when send_button is pressed.

	1. Stores the integer 1 in a variable how many, indicating that the email will be sent once to the recipient.
	2. Calls send_mail() function.
	'''

	global how_many
	how_many = 1
	send_mail()


def spam():
	'''
	Called when spam_button is pressed.

	1. Stores the integer 10 in a variable how many, indicating that the email will be sent ten times to the recipient, just for fun.
	2. Calls send_mail() function.
	'''

	global how_many
	how_many = 10
	print(type(how_many))
	send_mail()


def send_mail():
	'''
	Called by either the send() function or the spam() function.

	1. All inputs are stored in new variables.
	2. Constructs the message using most inputs.
	3. Creates a server object 'smtp.gmail.com' at port 587.
	4. Communication will be encrypted using Transport Layer Security, obscuring message, email and password over the internet.
	This prevents someone from eavesdropping. For example, using a packet sniffer with Wireshark.
	5. If the how_many variable is equal to 1 or 10, the program will try to login with the email and password that was entered in the login window.
	6. Next, the program will send the email from the sender to the receiver with the message.
	7. The server object will then quit.
	8. While the emails are being sent, the progress bar will be updated to the emails that were successfully sent.
	9. There are exceptions for when the login is unsuccessful and when the email did not reach the recipient.

	NOTE: If the email is being sent once, the progress bar will not look like it is working because it is being automatically reset when the email is sent.
	'''

	sender = email_address_input
	password = password_input
	receiver = receiver_input.get()
	subject = subject_input.get()
	body = message_box.get(0.0, END)

	message = f'''From:{sender}
	To:{receiver}
	Subject:{subject}\n
	{body}
	'''

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()

	try:
		if how_many == 1:
			server.login(sender, password)
			progress_bar['value'] += 100
			server.sendmail((sender), (receiver), (message))
			server.quit()
			progress_bar.stop()
			showinfo('Email Sent', f'Email successfully sent to {receiver}.')

	except smtplib.SMTPAuthenticationError:
		server.quit()
		progress_bar.stop()
		showinfo('Error', f'Email was not sent to {receiver}')

	except smtplib.SMTPRecipientsRefused:
		server.quit()
		progress_bar.stop()
		showinfo('Error', f'Email was not sent to {receiver}')

	try:
		if how_many == 10:
			progress_bar.stop()
			server.login(sender, password)
			for i in range(10):
				server.sendmail((sender), (receiver), (message))
				progress_bar['value'] += 10
				window.update_idletasks()
			server.quit()
			progress_bar.stop()
			showinfo('Emails Sent', f'Emails successfully sent to {receiver}.')

	except smtplib.SMTPAuthenticationError:
		server.quit()
		progress_bar.stop()
		showinfo('Error', f'Emails were not sent to {receiver}')

	except smtplib.SMTPRecipientsRefused:
		server.quit()
		progress_bar.stop()
		showinfo('Error', f'Email was not sent to {receiver}')


def manual():
	'''
	Called when Manual menu is pressed.

	Tells the user how to use the program.
	'''

	showinfo('Manual', 'Requirements:\n1. Google Mail.\n2. Less secure app access:ON, https://myaccount.google.com/lesssecureapps.\n\nHow to use:\n1. Enter a valid gmail address and its password.\n2. Click login.\n3. Enter the receiver address, the subject and the text into the corresponding entries.\n4. Click send.\n5. Finished.')


def about():
	'''
	Called when About menu is pressed.

	Tells the user who wrote this program.
	'''

	showinfo('About this program', 'This is an email application written by Kristof Kovacs!\nIn collaboration with Daniel Zheleznov.')


def saving():
	'''
	Called when save_checkbox is checked.

	1. Checks if the checkbox is checked.
	2. Changes colour of the checkbox to show the user they have checked the checkbox.
	'''

	if save.get() == 1:
		save_checkbox['fg'] = 'green'

	else:
		save_checkbox['fg'] = 'white'


'''
Start of program.
Creates login window.
Configures window size and its position on the x and y axis on the screen.
Displays labels, entries, menus...
Obfuscates password when entered into the entry.
Keeps the program in a loop.
'''

window = Tk()
window.title('Login')
window.resizable(False, False)
window.config(bg = '#303942')

window_width = 375
window_height = 450

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))

email_address = StringVar()
password = StringVar()
save = IntVar(window)

menu = Menu(window)
window.config(menu = menu)

help_menu = Menu(menu, tearoff = 0)
menu.add_cascade(label = 'Help', menu = help_menu)
help_menu.add_command(label = 'Manual', command = manual)
help_menu.add_separator()
help_menu.add_command(label = 'About', command = about)

Label(window, text = '', bg = '#303942').pack()
Label(window, text = 'Login:', width = 5, height = 1, fg = 'black', bg = 'green', font = ('arial', 30)).pack()
Label(window, text = '', bg = '#303942').pack()

Label(window, text = 'Email Address:', width = 20, height = 2, fg = 'white', bg = '#303942', font = ('calibri', 15)).pack()
email_address_entry = Entry(window, textvariable = email_address, fg = 'black', bg = 'white', font = ('consolas', 10))
email_address_entry.pack()

Label(window, text = '', bg = '#303942').pack()
Label(window, text = 'Password:', width = 20, height = 2, fg = 'white', bg = '#303942', font = ('calibri', 15)).pack()
password_entry = Entry(window, textvariable = password, fg = 'black', bg = 'white', font = ('consolas', 10), show = '*')
password_entry.pack()

save_checkbox = Checkbutton(window, text = "Remember Me", variable = save, bg = '#303942', fg = 'white', activebackground = '#303942', command = saving)
save_checkbox.pack()

Label(window, text = '', bg = '#303942').pack()
Button(window, text = 'Login', width = 10, height = 1, fg = 'black', bg = 'white', font = ('arial', 10), command = login).pack()

Label(window, text = '', bg = '#303942').pack()
Label(window, text = 'Pymail by Kristof Kovacs\nand Daniel Zheleznov', width = 20, height = 2, fg = 'white', bg = '#303942', font = ('calibri', 15)).pack()

window.mainloop()
