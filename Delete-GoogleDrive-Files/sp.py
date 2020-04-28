from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

file_list = drive.ListFile(
    {'q': "'root' in parents and trashed=false"}).GetList()


def main():
    godMode = False
    ask = input(
        f"{bcolors.RED}{bcolors.BOLD}\n\n Do you want to delete all files?:{bcolors.ENDC} ")

    if ask.lower() == 'y' or ask.lower() == 'yes':
        godMode = True

    for file1 in file_list:
        if not godMode:
            ask = input(
                f"{bcolors.BOLD}{bcolors.HEADER}\nDo you want to delete {bcolors.WARNING}{file1['title']}{bcolors.ENDC}?:{bcolors.ENDC} ")
            if ask.lower() == 'y':
                print(
                    f"{bcolors.OKBLUE}deleting {file1['title']}....{bcolors.ENDC}")
                try:
                    file1.Trash()
                    print(
                        f"{bcolors.OKGREEN}Sucessfully Deleted {bcolors.BOLD}{bcolors.WARNING}{file1['title']}{bcolors.ENDC}")
                except:
                    print(
                        f"{bcolors.WARNING}\npermisson denied {bcolors.UNDERLINE}seems like a shared file, moving on{bcolors.ENDC}")

        else:
            try:
                print(f"{bcolors.OKBLUE}Deleting, {file1['title']}...", end="")
                file1.Trash()
                print(
                    f"{bcolors.OKGREEN}\nSucessfully Deleted {bcolors.BOLD}{file1['title']}{bcolors.ENDC}")
            except:
                print(
                    f"{bcolors.WARNING}\npermisson denied {bcolors.UNDERLINE}seems like a shared file, moving on{bcolors.ENDC}")


if __name__ == "__main__":
    main()
