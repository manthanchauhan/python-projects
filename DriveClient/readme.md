#Readme for DriveClient

Common usage: Python -u "main.py" **command** **input** **arguments**  
**Login**: Python -u "main.py" *(No Command for Login)*

##Commands:
####1. logout: 
Logs out from the current GDrive session.  
use: Python -u "main.py" logout  
####2. p_dir:  
Toggles p_dir which determines whether to show additional human friendly error clarifications.  
use: Python -u "main.py" p_dir  
####3. cd:  
changes current working directory of GDrive.  
use:   
Python -u "main.py" cd *(move to the parent directory of current directory)*  
Python -u "main.py" cd <childname> *(move to the child directory)*  
Python -u "main.py" cd root *(move to the root of GDrive)*  
Python -u "main.py" cd this *(prints the name of the current directory of GDrive)*
####4. list:  
lists the contents of the current GDrive directory.  
use:  
Python -u "main.py" list 2-3 *(list files 100 to 300)*  
Python -u "main.py" list 1-1 -det *(list files 0 to 100 with all details)*  
Python -u "main.py" list 2-2 -dir *(list only folders among files 100 to 200)*


  
