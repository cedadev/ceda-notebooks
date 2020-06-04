# Workflow for staff contributing to this repository

Here are some basic instructions for creating your own fork of the 
main "ceda-notebooks" repository. It provides useful pointers on 
committing changes, pushing them to your own repository (on GitHub)
and tracking the master ("upstream") repository, based at:

https://github.com/cedadev/ceda-notebooks

## Creating a fork 

Forks are listed here:

https://github.com/cedadev/ceda-notebooks/network/members

To create a fork, go to the GitHub site and click "Fork".
This will result in a fork existing under:

https://github.com/USERNAME/ceda-notebooks/network/members

Where `USERNAME` is your GitHub user ID.

## Cloning a copy of the fork to your local machine

To get a copy of your fork on a local (or JASMIN) machine, do:

```
git clone https://USERNAME@github.com/USERNAME/ceda-notebooks
```

## Link the clone of your forked repo to the "upstream" cedadev repo

Set the "upstream" repository on your local git repo (to use the 
"cedadev" repo) - so that you can keep your local version updated 
with the centralised master copy:

```
git remote add upstream https://github.com/cedadev/ceda-notebooks
```

## Pull changes from the "upstream" cedadev repo

Pull any remote changes from the "cedadev" version to your local git repo:

```
git fetch upstream
git merge upstream/master
```

## Making changes

Try making a change. The workflow for git and github is:

 - make change(s)
 - add file(s) to git
 - commit the change(s)
 - push to github

E.g.:

```
echo "hello" > "hello.txt"
```

Add and commit to local repo:

```
git add hello.txt
git commit -m 'Added: hello.txt'
```

Push to GitHub fork:

```
git push
```

## Create a Pull Request to ask for your change to be merged to the "upstream" repo

Create a Pull Request (PR) on your own GitHub repo, and assign another 
person to review before they accept the changes to the "cedadev" repo.

That person will get an e-mail, read the PR, and accept it if they like it.


