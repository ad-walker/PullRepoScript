from tkinter import * 
# messagebox is a module and requires seperate import
from tkinter import messagebox
import ttk
import os
from os import path
import subprocess
from subprocess import call, STDOUT
import collections

# Tkinter window
root = Tk(className=' Repo Updater')
root.resizable(FALSE, FALSE)
# Use the grid layout, add a header row.
Label(root, text="PULL", font=("TkDefaultFont", 16)).grid(row=1, column=1, padx=5, pady=2)
Label(root, text="MAKE", font=("TkDefaultFont", 16)).grid(row=1, column=3, padx=5)
Label(root, text="REPOSITORY", font=("TkDefaultFont", 16)).grid(row=1, column=5, padx=5, pady=2)
ttk.Separator(root).grid(column=1, row=2, sticky="ew", columnspan=5)

# Navigate to the paths provided in the repoList and calls git pull
def getRepos(repoList):
    for repo in repoList:
        if repo.pull.get() == True:
            try: 
                os.chdir(repo.path)
                subprocess.call(["git", "pull"]) 
            except:
                messagebox.showerror("Git Pull Error", message="Repo: {}\n\n{}.".format(repo.path, sys.exc_info()))

# Navigate to the paths provided in the repoList and calls git pull
def makeRepos(repoList):
    for repo in repoList:
        if repo.make.get() == True:
            try: 
                os.chdir(repo.path)
                subprocess.call(["make"])
            except:
                messagebox.showerror("Make Error", message="Super helpful error message\n\n{}.".format(sys.exc_info()))

def main():
    # Define a "Repo" as a tuple containing key/value pairs for the repo path (string) and the user preferences (bools).
    Repo = collections.namedtuple("Repo", ["path", "pull", "make"])
    # Store our tuples in a list.
    repoList = []
    try: 
        # Get the path of all subdirectories of the current working directory (depth: 1) to loop over.
        directories = list((filter(os.path.isdir, [os.path.join(os.getcwd(),f) for f in os.listdir(os.getcwd())])))
        for idx, dir in enumerate(directories):
            # Parse a string from the list of filtered paths, then navigate to that directory.
            path = "".join(dir)
            os.chdir(path)
            # Make sure the directory has a git repo, otherwise skip it.
            if call(["git", "branch"], stderr=STDOUT, stdout=open(os.devnull, 'w')) != 0:
                continue

            #Populate the UI with a row of elements for each repo (checkboxes for pull and make, label for path)
            doPull = BooleanVar(root, True, name ='pull_{}'.format(path))
            Checkbutton(root, variable = doPull, onvalue = True, offvalue = False).grid(column=1, row=idx + 3)
            # Default make to false.
            doMake = BooleanVar(root, False, name ='make_{}'.format(path))
            # Add a checkbox only if we find a valid Makefile.
            if os.path.isfile('Makefile'):
                Checkbutton(root, variable = doMake, onvalue = True, offvalue = False).grid(column=3, row=idx + 3)
            # Full path as repo text.
            Label(root, text="{}".format(path), font=("TkDefaultFont", 18)).grid(row=idx + 3, column=5, sticky=W, padx=5)

            # Instantiate a Repo tuple for each row referenceing the checkbox variables, add it to the list.
            r = Repo(path = path, pull = doPull, make=doMake)
            repoList.append(r)
    except:
        messagebox.showerror("Error!", message="Super helpful error message:\n\n{}".format(sys.exc_info()))
    
    # Add column seperators once we know how many rows to span.
    ttk.Separator(root, orient=VERTICAL).grid(row=2, column=2, columnspan=1, rowspan=len(repoList) + 1, sticky="ns") 
    ttk.Separator(root, orient=VERTICAL).grid(row=2, column=4, columnspan=1, rowspan=len(repoList) + 1, sticky="ns")
    ttk.Separator(root).grid(column=1, row=len(repoList) + 3, sticky="ew", columnspan=5)

    # Finally add a button to run an ugly function chain.
    Button(root, text ="Update Repos", command = lambda : [getRepos(repoList), makeRepos(repoList),
        messagebox.showinfo('Complete', 'All requests have been processed.')]).grid(column=1, columnspan=5, row=len(repoList) + 4, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()