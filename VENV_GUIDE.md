# Virtual Environment Guide: Don't Break Everything Edition

## What the hell is a virtual environment?

A virtual environment is like a sandbox for your Python project. It keeps all your project's dependencies separate so you don't accidentally break other projects or your system Python. Think of it as giving each project its own room instead of throwing everything in one giant pile.

## Step 1: Activate the virtual environment

This is the part everyone screws up. You need to do this **every single time** you work on the project.

### On Mac/Linux:
```bash
source git-dev-env/Scripts/activate
```

### On Windows (Command Prompt):
```bash
git-dev-env\Scripts\activate
```

### On Windows (PowerShell):
```bash
git-dev-env\Scripts\Activate.ps1
```

**How to know it worked:** Your terminal prompt should change to show `(git-dev-env)` at the beginning, like this:
```
(git-dev-env) your-username@computer:~/project$
```

If you don't see `(git-dev-env)`, it didn't work. Try again.

Now get to work.


## Step 2: When you're done working

```bash
deactivate
```

This exits the virtual environment. Your prompt should go back to normal (no more `(venv)`).

## Common Mistakes (Don't Be This Person)

❌ **Installing packages without activating the virtual environment**
- Result: Packages go to your system Python, defeating the whole purpose

❌ **Forgetting to activate the virtual environment**  
- Result: "ModuleNotFoundError" even though you "just installed it yesterday"

❌ **Deleting the venv folder**
- Result: You have to recreate everything

❌ **Committing the venv folder to git**
- Result: Huge repository size and merge conflicts

❌ **Using different Python versions**
- Result: Nothing works and everyone blames you

## Quick Reference Commands

```bash
# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Check what's installed
pip list

# Save current packages to requirements.txt
pip freeze > requirements.txt

# Deactivate
deactivate
```

## Troubleshooting

**"python: command not found"**
- Try `python3` instead of `python`

**"Permission denied" on Windows**
- Run PowerShell as Administrator
- Or use Command Prompt instead

**"Module not found" errors**
- Make sure virtual environment is activated (look for `(venv)` in prompt)
- Make sure you installed requirements: `pip install -r requirements.txt`

**Virtual environment folder is huge**
- This is normal, don't panic
- Make sure `venv/` is in your `.gitignore` file

## Final Notes

- **Always activate before coding**
- **Never commit the venv folder to git**  
- **When in doubt, deactivate and reactivate**
- **If something breaks, ask for help before randomly deleting things**

Now stop breaking the build and get back to work! 🚀