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

def encrypt(string, shift=5):
	res = ""
	for i in range(len(string)):
		value = ord(string[i])
		value += shift + i
		res += chr(value)
	return res

def decrypt(string, shift=5):
	res = ""
	for i in range(len(string)):
		value = ord(string[i])
		value -= (shift + i)
		res += chr(value)
	return res

def full_encrypt(site, user, password):
	"""uses encrypted site as string"""
	total = sum([ord(site[i]) for i in range(len(site))])
	shift = total % 13
	res_user = encrypt(user, shift)
	res_pass = encrypt(password, shift)
	return res_user, res_pass

def partial_decrypt(site, user, password):
	"""uses encrypted site as string"""
	total = sum([ord(site[i]) for i in range(len(site))])
	shift = total % 13
	res_user = decrypt(user, shift)
	res_pass = decrypt(password, shift)
	return res_user, res_pass

def recrypt(old_site, new_site, user_encrypted, password_encrypted):
	duser, dpass = partial_decrypt(old_site, user_encrypted, password_encrypted)
	new_user_encrypted, new_password_encrypted = full_encrypt(new_site, duser, dpass)
	return new_user_encrypted, new_password_encrypted

def add(login_db):
	print("_____Adding_____")
	site = input("Site: ")
	user = input("User/Email: ")
	password = input("Password: ")
	#encrypt
	site_encrypted = encrypt(site)
	user_encrypted, password_encrypted = full_encrypt(site_encrypted, user, password)

	#add
	login_db[site_encrypted] = [user_encrypted, password_encrypted]
	print("Finished adding entry '{}'.".format(site))
	print()
	cont()

def retrieve(login_db):
	print("_____Retrieving_____")
	if not login_db:
		print("Empty Bank.")
	else:
		site = input("Site: ")
		try:
			site_encrypted = encrypt(site)
			values = login_db[site_encrypted]
		except KeyError:
			print(site, "not found in database.")
			print()
		else:
			print("Retrieving entry '{}'.".format(site))
			duser, dpass = partial_decrypt(site_encrypted, values[0], values[1])
			print("User/Email: ", duser)
			print("Password: ", dpass)
			print()
	cont()

def view(login_db):
	print("_____Viewing_____")
	if not login_db:
		print("Empty Bank.")
	else:
		for site in sorted(login_db.keys()):
			dsite = decrypt(site)
			print(dsite)
	print()
	cont()

def edit(login_db):
	print("_____Editing_____")
	if not login_db:
		print("Empty Bank.")
	else:
		site = input("Site to edit: ")
		try:
			site_encrypted = encrypt(site)
			values = login_db[site_encrypted]
		except KeyError:
			print(site, "not found in database.")
			print()
		else:
			print("Retrieving entry {}".format(site))
			duser, dpass = partial_decrypt(site_encrypted, values[0], values[1])
			print("User/Email: ", duser)
			print("Password: ", dpass)
			print()
			while True:
				inp = input("Press 1 to edit site, 2 to edit user/email, 3 to edit password, c to cancel: ")
				if inp == "1":
					print("Current Site: ", site)
					user_site = input("New Site: ")
					#check if already exists
					user_site_encrypted = encrypt(user_site)
					if login_db.get(user_site_encrypted):
						print("Entry {} already exists. You will overwrite it.".format(user_site))
						decision = ays()
						if decision == "y":
							new_user, new_pass = recrypt(site_encrypted, user_site_encrypted, values[0], values[1])
							login_db[user_site_encrypted] = [new_user, new_pass]
							del login_db[site_encrypted]
							break
						elif decision == "n":
							continue 
					else:
						new_user, new_pass = recrypt(site_encrypted, user_site_encrypted, values[0], values[1])
						login_db[user_site_encrypted] = [new_user, new_pass]
						del login_db[site_encrypted]
						break
				elif inp == "2":
					print("Current User/Email: ", duser)
					user_email = input("New User/Email: ")
					decision = ays()
					if decision == "y":
						new_user, _ = full_encrypt(site_encrypted, user_email, dpass)
						values[0] = new_user
						break
					elif decision == "n":
						continue 
				elif inp == "3":
					print("Current Password: ", dpass)
					user_password = input("New Password: ")
					decision = ays()
					if decision == "y":
						_, new_pass = full_encrypt(site_encrypted, duser, user_password)
						values[1] = new_pass
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
			site_encrypted = encrypt(site)
			values = login_db[site_encrypted]
		except KeyError:
			print(site, "not found in database.")
			print()
		else:
			duser, dpass = partial_decrypt(site_encrypted, values[0], values[1])
			print("User/Email: ", duser)
			print("Password: ", dpass)
			print("You are going to delete entry {} including user/email and password.".format(site))
			decision = ays()
			if decision == "y":
				del login_db[site_encrypted]
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
		pickle.dump({}, open("save.p", "wb"))
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
