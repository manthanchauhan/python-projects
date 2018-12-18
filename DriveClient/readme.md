# Readme for DriveClient

**Login**: `Python -u "main.py"` *(No Command for Login)*

## Commands:  
#### 1. logout: 
Logs out from the current GDrive session.  
use: `Python -u "main.py" logout`  
#### 2. p_dir:  
Toggles p_dir which determines whether to show additional human friendly error clarifications.  
use: `Python -u "main.py" p_dir`  
#### 3. cd:  
changes current working directory of GDrive.  
use:   
`Python -u "main.py" cd` *(move to the parent directory of current directory)*  
`Python -u "main.py" cd <childname>` *(move to the child directory)*  
`Python -u "main.py" cd root` *(move to the root of GDrive)*  
`Python -u "main.py" cd this` *(prints the name of the current directory of GDrive)*  
#### 4. list:  
lists the contents of the current GDrive directory.  
use:  
`Python -u "main.py" list 2-3` *(list files 100 to 300)*  
`Python -u "main.py" list 1-1 -det` *(list files 0 to 100 with all details)*  
`Python -u "main.py" list 2-2 -dir` *(list only folders among files 100 to 200)*
#### 5. download:
download a selected file from GDrive.  
use:  
`Python -u "main.py" download <filename> <destination address>`  
`Python -u "main.py" download <filename> default` *(download at a predefined address)*  
#### 6. export:  
download any google document in any supported format.  
use:  
`Python -u "main.py" export <filename> <required format> <destination address>` *(gives error if format is unsupported)*  
`Python -u "main.py" export <filename> <required format> default`  
#### 7. upload:
upload any file to current GDrive directory.  
use:  
`Python -u "main.py" upload <filename>`  
#### 8. find:  
finds a file and moves to the directory containing the file  
use:  
`Python -u "main.py" find <filename>`   
`Python -u "main.py" find <filename> -det` *(print file details also)*

  
