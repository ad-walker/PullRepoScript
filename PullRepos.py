from tkinter import * 
# messagebox is a module and requires seperate import
from tkinter import messagebox
import os
import subprocess
from subprocess import call, STDOUT
import collections

# Tkinter window
root = Tk(className=' Repo Updater')
root.minsize(int(root.winfo_screenwidth() * 0.25), int(root.winfo_screenheight() * 0.25)) 

# Navigate to the paths provided in the repoList and calls git pull
def getRepos(repoList):
    for repo in repoList:
        if repo.pull.get() == True:
            # Navigate to the directory.
            try: 
                os.chdir(repo.path)
                subprocess.call(["git", "pull"])   
            except:
                messagebox.showerror("Error!", message="Super helpful error message\n\n{}.".format(sys.exc_info()))
    messagebox.showinfo('Complete', 'All requests have been processed.')

def main():
    Label(root, text="Select repos to PULL", font=("TkDefaultFont", 18)).pack(pady=5)
    # Store the directories with repos as a list of tuples.
    repoList = []
    try: 
        # Script assumes all repositories are in a central folder, e.g. /projects.
        directories = list((filter(os.path.isdir, [os.path.join(os.getcwd(),f) for f in os.listdir(os.getcwd())])))
        for dir in directories:
            # Parse a string from the list of paths, then navigate to that directory.
            path = "".join(dir)
            os.chdir(path)
            # Make sure the directory has a git repo, otherwise skip it.
            if call(["git", "branch"], stderr=STDOUT, stdout=open(os.devnull, 'w')) != 0:
                continue
            # Each repo will have a checkbox for the user to choose whether or not to pull it, this var will store that state.
            boolVar = BooleanVar(root, True, name ='{}'.format(path))
            # Create a tuple of the path and the boolean and append it to the list.
            Repo = collections.namedtuple("Repo", ["path", "pull"])
            r = Repo(path = path, pull = boolVar)
            repoList.append(r)
            # Draw the checkbox.
            Checkbutton(root, text = '{repo}'.format(repo=path), font=("TkDefaultFont", 18), variable = boolVar, onvalue = True, offvalue = False).pack(padx=10, pady=2, anchor=W)
    except:
        messagebox.showerror("Error!", message="Super helpful error message:\n\n{}".format(sys.exc_info()))

    Button(root, text ="Pull Repos", command = lambda : getRepos(repoList)).pack(pady = 10)
    root.mainloop()

if __name__ == "__main__":
    main()