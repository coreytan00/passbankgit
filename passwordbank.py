import pickle
import hashlib
import getpass

def take_input():
	usr_input = input().strip()
	result = check_input_one(usr_input)
	print()
	return result

def check_input_one(usr_input):
	if usr_input in ["1", "add", "ADD", "Add"]:
		return 1
	elif usr_input in ["2", "retrieve", "RETRIEVE", "Retrieve"]:
		return 2
	elif usr_input in ["3", "view", "View", "VIEW", "view bank", "VIEW BANK", "View Bank"]:
		return 3
	elif usr_input in ["4", "edit", "Edit", "EDIT"]:
		return 4
	elif usr_input in ["5", "delete", "Delete", "\rDELETE"]:
		return 5
	elif usr_input in ["q", "quit", "QUIT", "Quit"]:
		return "q"
	else:
		return
def cont():
	input("Press any key to continue...")
	print()

def ays():
	"""are you sure"""
	while True:
		yn = input("Are you sure? (y/n): ")
		if yn in ["y", "Y", "yes", "YES"]:
			return "y"
		elif yn in ["n", "N", "no", "NO"]:
			return "n"
		else:
			print("Invalid input. y/n")

def add(login_db):
	print("_____Adding_____")
	site = input("Site: ")
	user = input("User/Email: ")
	password = input("Password: ")
	login_db[site] = [user, password]
	print("Finished adding entry {}".format(site))
	print()
	cont()

def retrieve(login_db):
	print("_____Retrieving_____")
	if not login_db:
		print("Empty Bank.")
	else:
		site = input("Site to retrieve from: ")
		try:
			values = login_db[site]
		except KeyError:
			print(site, "not found in database.")
			print()
		else:
			print("Retrieving entry {}".format(site))
			print("User/Email: ", values[0])
			print("Password: ", values[1])
			print()
	cont()

def view(login_db):
	print("_____Viewing_____")
	if not login_db:
		print("Empty Bank.")
	else:
		for site, values in sorted(login_db.items()):
			print(site)
			#print("User/Email: ", values[0])
			#print("Pass: ", values[1])
	print()
	cont()

def edit(login_db):
	print("_____Editing_____")
	if not login_db:
		print("Empty Bank.")
	else:
		site = input("Site to edit: ")
		try:
			values = login_db[site]
		except KeyError:
			print(site, "not found in database.")
			print()
		else:
			print("Retrieving entry {}".format(site))
			print("User/Email: ", values[0])
			print("Password: ", values[1])
			print()
			while True:
				inp = input("Press 1 to edit site, 2 to edit user/email, 3 to edit password, c to cancel: ")
				if inp == "1":
					print("Current Site: ", site)
					user_site = input("New Site: ")
					#check if already exists
					if login_db.get(user_site):
						print("Entry {} already exists. You will overwrite it.".format(user_site))
						decision = ays()
						if decision == "y":
							login_db[user_site] = values
							del login_db[site]
							break
						elif decision == "n":
							continue 
					else:
						login_db[user_site] = values
						del login_db[site]
						break
				elif inp == "2":
					print("Current User/Email: ", values[0])
					user_email = input("New User/Email: ")
					decision = ays()
					if decision == "y":
						values[0] = user_email
						break
					elif decision == "n":
						continue 
				elif inp == "3":
					print("Current Password: ", values[1])
					password = input("New Password: ")
					decision = ays()
					if decision == "y":
						values[1] = password
						break
					elif decision == "n":
						continue
				elif inp == "c":
					print("Cancelling.")
					break
				else:
					print("Invalid input. 1/2/c")
			print()
	cont()

def delete(login_db):
	print("_____Deleting_____")
	if not login_db:
		print("Empty Bank.")
	else:
		site = input("Site and respective information to delete: ")
		try:
			values = login_db[site]
		except KeyError:
			print(site, "not found in database.")
			print()
		else:
			print("Retrieving entry {}".format(site))
			print("User/Email: ", values[0])
			print("Password: ", values[1])
			print("You are going to delete entry {} including user/email and password.".format(site))
			decision = ays()
			if decision == "y":
				del login_db[site]
			print()
	cont()

def menu():
	print("_____Menu_____")
	print("Add (1)")
	print("Retrieve (2)")
	print("View Bank (3)")
	print("Edit Entry (4)")
	print("Delete Entry (5)")
	print("Save and Quit (q)")

def main(login_db):
	print("_____Welcome to Corey's Simple Password Bank_____")
	print("-------------------------------------------------")
	while True:
		menu()
		result = take_input()
		if not result:
			print("Invalid input. Choose from menu.")
			print()
			continue 
		elif result == "q":
			print("Saving...")
			pickle.dump(login_db, open("save.p", "wb"))
			print("Shutting Down")
			exit()
		elif result == 1:
			add(login_db)
		elif result == 2:
			retrieve(login_db)
		elif result == 3:
			view(login_db)
		elif result == 4:
			edit(login_db)
		elif result == 5:
			delete(login_db)
		else:
			print("howd you get here?")

def checkPassword():
	master_pass = None
	try:
		master_pass = pickle.load(open("pass.p", "rb"))
	except FileNotFoundError:
		while True:
			str_to_hash = input("Please create a master password for this program: ")
			decision = ays()
			if decision == "y":
				master_pass = hashlib.md5(str_to_hash.encode())
				master_pass = master_pass.hexdigest()
				pickle.dump(master_pass, open("pass.p", "wb"))
				break
			elif decision == "n":
				continue
	finally:
		for i in range(3):
			password = getpass.getpass(prompt="Master Password: ")
			mdpass = hashlib.md5(password.encode())
			if mdpass.hexdigest() == master_pass:
				return True
			else:
				print("Wrong Password. Try again.")
		print("Noob")
		return False

def prework():
	if checkPassword():
		try:
			login_db = pickle.load(open("save.p", "rb"))
		except FileNotFoundError:
			login_db = {}
		return login_db
	else:
		exit()

if __name__ == "__main__":
	login_db = prework()
	main(login_db)
