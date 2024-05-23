profile = ""
print("Welcome to Dental Clinic. Select your profile:")
print("\t[1] Patient")
print("\t[2] Doctor")
while profile != "1" and profile != "2":
    profile = input("Selection: ")
    
if profile == "1":
    # It is a patient
    print("\nYou chose 'patient'. Select an operation, o press [X] to exit")
    print("\t[1] Log into system")
    print("\t[2] Create profile")
    print("\t[3] Update profile")
    print("\t[4] Get profile\n")
    print("\t[4] Change password\n")
    
    operation = "0"
    while operation != "X":
        while operation not in ["1","2","3","4","5","X"]: 
            operation = input("Selection: ")

                
        print(f"YOUR SELECTION IS {operation}")
        
        match operation:
            case "1":
                # Login
            case "2":
                # Create
            case "3":
                # Update
            case "4":
                # Read     
            case "5":
                # change       
            case _:
                "Invalid option"
        
else:
    # It is a doctor
    print("It is a doctor")



