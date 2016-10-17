
# 0.2 (released October 15, 2016)

- Better color schemes. Right now DEBUG is just white and it makes it odd to read. 
The color schemes should reflect what the level implies.
- Errors and Stdout should be better formatted with logging. If an exception happens, 
we see a traceback, which is useless. The stderr and stdout should be more nicely 
formatted and presented to the user when an error occurs.
- We can use `raw_input` to get input via `stdin`, but it would be nice if the 
Sultan API also supported it.
- Context Management:
  - `sudo=<True/False>`: Set a command should be run as sudo with Context Management.
  - `user=<username>`: Set a user to run command as
  - `host=<hostname>`: Should be able to run a command on a remote host, by setting a 
