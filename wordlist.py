import os
import sys



class Reading_wordlist:
    
    def __init__(self, path):
        self.path_to_file = path
        
    @staticmethod
    def rerun():
       
       pass
        
    # @staticmethod
    def Reading_file(self):
        words=set()
        
        try:
            
            if os.path.splitext(self.path_to_file)[1]==".txt":
                # filename = 'example.txt'
                # file_extension = os.path.splitext(filename)[1]  # Returns the extension including the period

                # print(file_extension)  # Output: ".txt"

                if os.path.isfile(self.path_to_file):
                    with open(self.path_to_file,"r") as file:
                        words = {line.strip() for line in file if line.strip()}
                        #line.strip() strips the line in file if the line.striip() is true. 
                    #if the it's like line.strip()=for line in file if line.strip is true.
                    #if you want furter about this then remove .strip from line.strip() check output you will understand

                        return words
                else:
                    print("\n******************************************************************************************")
                    print (f""" "{self.path_to_file}" file path not found""")
                    
                   
                    
                    
                    
            else:
                print("\n******************************************************************************************")
                print("File extension is not supportable, Make sure to use '.txt' file ")
                # path2=input('enter the path2: ')
                # re.rerun()
               
                    
        except FileNotFoundError:
            pass
            

def main():
    print("************************************************************************************************")
    
    path=input("enter the path: ")
    re=Reading_wordlist(path).Reading_file()
    while re is None:
        path=input("enter the path: ")
        re=Reading_wordlist(path).Reading_file()
        if re is not None:
            print(re)
            return re
        else:
            continue
        
if __name__ == "__main__":
    main()
        
   
    
    
    
    
  
    
    
    
   
             
            
