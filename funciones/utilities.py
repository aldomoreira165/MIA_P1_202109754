def printConsole(text): print("\033[36m<<System>> {}\033[00m" .format(text))

def printError(error): print("\033[91m<<Error>> {}\033[00m" .format(error))

def printSuccess(success): print("\033[1;32m<<Success>> {}\033[00m" .format(success))

def printWarning(question): 
      confirm = "no"
      confirm = input("\033[1;33m<<Confirm>> {}\033[00m\n" .format(question))
      return confirm == "s" or confirm == "S"

def coding_str(string,size):
    return string.encode('utf-8')[:size].ljust(size, b'\0')