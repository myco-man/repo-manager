
import argparse
import operations as ops
import os
from pathlib import Path

########################################
######          Paths             ######
home = "C:\\Users\\kolendoi\\AppData\\Local\\Programs\\Git\\repos" #This will need to be set by the user
###### Commonly Used Git Commands ######
########################################
checkOutMainCmd = "git checkout main"
checkOutCmd = "git checkout "
fetchCmd = "git fetch"
pullCmd = "git pull"
changeDirCmd = "cd "
upDir ="cd .."
printDir = "os.getcwd()" 
########################################
######       Intro Phrases       #######
deleteIntro = "Delete Branch -delete or --delete-branch"
newBranchIntro = "Create New branch -nb or --new-branch"
renameIntro = "Rename a Branch -rn or --rename"
updateRepoIntro = "Update Repo -u or --update-repo"
updateAllReposIntro = "Update All Repos -ua or --update-all-repos"
introEx = "For examples Re-Run with option -ex enabled"
space ="\n            ---             \n"
########################################
### Utility Class ###
##########################################
class utilFuncts:
    def exe(self, cmd=None, cmds=None, repo=None):
        if cmd != None and repo != None: # single command setting repo
            os.chdir( home + "\\" + repo)
            os.system(cmd)
        elif cmd != None:  # single command setting no repo
            os.system(cmd)
        elif cmds != None and repo != None: #multiple commands setting repo 
            os.chdir( home + "\\" + repo)
            for command in cmds:
                os.system(command)
        elif cmds != None: #multiple commands setting no repo
            for command in cmds:
                os.system(command)


    ### Used for building the Intro + Example Statements
    def lineBuilder(self, line, ns):
        if not ns:
            return "  " + line + space
        else:
            return " " + line
    
    def statementBuilder(self, lines):
        statement = ""
        for line in lines:
            statement = statement + self.lineBuilder(line, 0)
        return statement

util = utilFuncts()

### Operations ###
###############################################################################################
def deleteBranch(args):
    toDelete = args["delete_branch"]
    repository = args["repository"]
    print("You are about to delete the ", toDelete, " branch in the", repository," repository. Do you want to continue?")
    cont = input("y/n:  ")
    if cont == "y":
        remoteDeleteCmd = "git push origin --delete " + str(toDelete)
        localDeleteCmd = "git branch --delete " + str(toDelete)
        cmds = [remoteDeleteCmd, localDeleteCmd]
        util.exe(None, cmds, repository)
    else: 
        print("Operation canceled")

def newBranch(args):
    newBranch = args["new_branch"]
    repository = args["repository"]
    print("You are creating a new branch in repository ", repository, " called ", newBranch,". Do you want to continue?")
    cont = input("y/n:  ")
    if cont == "y":
        newLocalCmd = "git checkout -b " + str(newBranch)
        pushRemoteCmd = "git push -u origin "+str(newBranch)
        cmds = [newLocalCmd, pushRemoteCmd]
        util.exe(None, cmds, repository)
    else: 
        print("Operation canceled")

def renameBranch(args):
    oldBranch = args["branch"]
    newBranch = args["rename"]
    repository = args["repository"]
    print("You are renaming the ", oldBranch, " in the ", repository , " repository to ", newBranch, ". Do you want to continue?")
    cont = input("y/n:  ")
    if cont == "y":
        checkOutCmd = "git checkout "+ str(oldBranch)
        renameCmd = "git branch -m " + str(newBranch) 
        pushRemoteCmd = "git push origin -u " + str(newBranch)
        deleteOldRemoteCmd = "git push origin --delete " +str(oldBranch)
        cmds = [checkOutCmd, renameCmd, pushRemoteCmd, deleteOldRemoteCmd]
        util.exe(None, cmds, repository)
    else: 
        print("Operation canceled.")

def updateRepos():
    os.chdir(home)
    cmds = [upDir ,checkOutMainCmd, fetchCmd, pullCmd]
    repos = os.listdir()
    updatedRepos = []
    for r in repos:
        cmds[0] = ("cd " + r)
        util.exe(None, cmds, r)
        util.exe(upDir, None, None)
        updatedRepos.insert(0, r)
    print(*updatedRepos)

def updateRepo(args):
    os.chdir(home + "//" + args["repository"])
    if not args["branch"]:
        cmds = [checkOutMainCmd, fetchCmd, pullCmd]
        util.exe(None, cmds, None)
    else:
        checkOutBranchCmd= checkOutCmd + args["branch"]
        cmds = [checkOutBranchCmd, fetchCmd, pullCmd]
        util.exe(None, cmds, None)



def intro():
    useCases = [deleteIntro, newBranchIntro, renameIntro, updateRepoIntro, updateAllReposIntro]
    introMessage = util.statementBuilder(useCases)

    print("##########################################################################")
    print("             Welcome to RepoManager\nImplemented Use Cases:")
    print(introMessage)
    print("##########################################################################")



parser = argparse.ArgumentParser(
    prog='Repo Manager',
    description='A collection of commonly used git commands'
)
parser.add_argument('-r','--repository') 
parser.add_argument('-delete', '--delete-branch', help='This flag is used to indicate and store the branch ou wnat deleted. Ex. -r sys-bankware -delete FEATURE_1111')
parser.add_argument('-b', '--branch', help='This flag is used to designate the branch being operated on. Ex. -r sys-bankware -b FEATURE_1111 -rn FEATURE_2222')
parser.add_argument('-nb', '--new-branch', help='This flag is set when a new branch is being created. Ex. -r sys-bankware -nb FEATURE_1111')
parser.add_argument('-rn', '--rename', help='The flag that holds the name a branch is being renamed to. Ex. -r sys-bankware -b FEATURE_1111 -rn FEATURE_2222')
parser.add_argument('-u', '--update-repo', action='store_true', help='Flag used to update a single repo. Ex. -r sys-bankware -u')
parser.add_argument('-ua', '--update-all-repos', action='store_true', help='Flag used to update all repos. Ex. -ua')
parser.add_argument('-c', '--commit', action='store_true', help='')
parser.add_argument('-p', '--push', action='store_true', help='')
parser.add_argument('-cap', '--commit-and-push', action='store_true', help='')
parser.add_argument('-i', '--intro', action='store_true', help='')


def repoManager(args):
    if not args["repository"]:
        if not args["update_all_repos"] and not args["intro"]:
            args["repository"] = input("Repository Name: ")
    if args["delete_branch"]:
        ops.deleteBranch(args)
    elif args["new_branch"]:
        ops.newBranch(args)
    elif args["rename"]:
        ops.renameBranch(args)
    elif args["update_repo"]:
        ops.updateRepo(args)
    elif args["update_all_repos"]:
        ops.updateRepos()
    elif args["intro"]:
        ops.intro()


if __name__ == '__main__':
    args = vars(parser.parse_args())
    repoManager(args)