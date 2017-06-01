# Scheduling a backup task on Windows

At some point you gonna want to schedule your backup routines.

If so, this walktrough will help you with that...

## Setting up your script

1. Create a folder on your preference
2. Create your backup.py and settings.py file into this folder. My is looking like this:
![Settings.py](settings.PNG)
![backup.py](backup.PNG)
3. Create a batch file, which looks like this
![backup.cmd](script.PNG) 

For more info about how to configure settings, [refer to this ling](https://github.com/FRReinert/PyBackup/blob/master/documentation/SETTINGS.md)

## Open your Task Manager and add a new task on the right menu

![New task](new_task.PNG)

## Setup the relevant information

![Gereral Setup](general_task_setup.png)

## Go to the trigger tab and hit new/add

![New Trigger](new_trigger.png)

## Setup as you prefer and hit OK

![Trigger Setup](trigger.png)

## Go to action tab and hit new/add action

![New Action](new_action.png)

## Point it to the .cmd file and set the location to the .cmd file (Important, set it right!)

![Action](action.png)

## Done!


