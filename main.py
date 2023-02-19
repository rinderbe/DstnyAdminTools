import dstnyauth
import mysoluno
from tabulate import tabulate
import csv
import getpass
import logging


logging.basicConfig(filename='logging.log', encoding='utf-8', level=logging.DEBUG)


def login():
    inp_user = input("Enter your username: ")
    inp_passwd = getpass.getpass("Enter your password: ")
    auth = dstnyauth.DstnyAuth(inp_user, inp_passwd)
    if auth.status:
        print("Login successfull!")
    else:
        logging.debug(f"Login failed for user {inp_user}")
    return auth


def get_table(data):
    headers = data[0].keys()
    rows = [list(item.values()) for item in data]
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def bulk_login(auth, organization, acd_id):
    data = mysoluno.get_agent_login_state(auth, organization, acd_id)
    success = 0
    failed = 0
    for user in data:
        data = mysoluno.enable_agent_login_state(auth, organization, acd_id, user['userId'])
        if data:
            success += 1
        else:
            failed += 1
            logging.debug(f"Failed to login user {user['userId']} for domain {organization}")
    print(f"Successfully logged in {success} users. Failed {failed} users.")


def bulk_logout(auth, organization, acd_id):
    data = mysoluno.get_agent_login_state(auth, organization, acd_id)
    success = 0
    failed = 0
    for user in data:
        data = mysoluno.disable_agent_login_state(auth, organization, acd_id, user['userId'])
        if data:
            success += 1
        else:
            failed += 1
            logging.debug(f"Failed to logout user {user['userId']} for domain {organization}")
    print(f"Successfully logged out {success} users. Failed {failed} users.")


def csv_import_rbn(auth, organization, path="rulebased_number_import.csv"):
    with open(path, encoding='utf-8-sig') as csvf:
        success = 0
        failed = 0
        csv_reader = csv.DictReader(csvf)
        for row in csv_reader:
            request = mysoluno.post_call_api("FunctionNumber/SaveRuleBasedNumber", auth, organization, row)
            if request:
                success += 1
            else:
                failed += 1
                logging.debug(f"Failed to import rulebased number for {row['fnr']}")
        return success, failed


def main_menu(auth, inp_domain):
    while True:
        if auth.status:
            print("--== DS7NY 4DM1N 700LZ ==--")
            print("\n")
            print("""
            1 : Print ACDs
            2 : Print External Systems
            3 : Print Rule Based Numbers
            4 : Print logged in agents
            5 : Log in agent to ACD
            6 : Logout agent to ACD
            7 : BULK login ALL agents to ACD
            8 : BULK logout ALL agents to ACD
            9 : Import Rulebased Numbers
            0 : Back to authentication
            q : Exit application"""
                  )
            choice = input("\nEnter your choice : ")

            if choice == '1':
                data = mysoluno.get_all_function_numbers_acd(auth, inp_domain)
                get_table(data)
            elif choice == '2':
                data = mysoluno.get_all_function_numbers_external(auth, inp_domain)
                get_table(data)
            elif choice == '3':
                data = mysoluno.get_all_function_numbers_rbn(auth, inp_domain)
                get_table(data)
            elif choice == '4':
                acd_id = input("Enter the ID of the ACD: ")
                data = mysoluno.get_agent_login_state(auth, inp_domain, acd_id)
                get_table(data)
            elif choice == '5':
                acd_id = input("Enter the ID of the ACD: ")
                user_id = input("Enter the ID of the User: ")
                data = mysoluno.enable_agent_login_state(auth, inp_domain, acd_id, user_id)
                if data:
                    print("Log in successfull!")
                else:
                    print("Login failed!")
            elif choice == '6':
                acd_id = input("Enter the ID of the ACD: ")
                user_id = input("Enter the ID of the User: ")
                data = mysoluno.disable_agent_login_state(auth, inp_domain, acd_id, user_id)
                if data:
                    print("Logout successfull!")
                else:
                    print("Logout failed!")
            elif choice == '7':
                acd_id = input("Enter the ID of the ACD: ")
                bulk_login(auth, inp_domain, acd_id)
            elif choice == '8':
                acd_id = input("Enter the ID of the ACD: ")
                bulk_logout(auth, inp_domain, acd_id)
            elif choice == '9':
                print(
                    "The format of the CSV-file should be: name,metadata,defaultForwardNumber,fnr,billingId,locale,"
                    "overrideMetadata,preferDiversionAsANumber")
                path = input("Enter the path to the CSV-file containin the rulebased numbers: ")
                req_import = csv_import_rbn(auth, inp_domain, path)
                print(f"Successfully imported {req_import[0]}. Failed import of {req_import[1]}")
            elif choice == '0':
                main()
                return
            elif choice == 'q':
                exit()
        else:
            auth = login()


def main():
    auth = login()
    while True:
        print("--== DS7NY 4DM1N 700LZ ==--")
        if auth.status:
            data = mysoluno.get_manageable_orgs(auth)
            get_table(data)
            domain = input("Enter domain to administrate: ")
            if domain != "":
                main_menu(auth, domain)
                return
        else:
            print("Authentication failed.")
            main()
            return


if __name__ == "__main__":
    main()
