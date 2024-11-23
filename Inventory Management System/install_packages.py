import subprocess
import sys

def install_packages(requirements_file):
    print("Installing required packages...")

    with open(requirements_file, 'r') as file:
        packages = file.readlines()
    
    
    for package in packages:
        package = package.strip()
        if package:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Installation done for {package}")
            
    print("All packages installed.")
    
    


    
    