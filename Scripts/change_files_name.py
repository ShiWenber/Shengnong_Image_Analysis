from io import FileIO
import os
print(os.getcwd())

changed_files = []

def get_files(base, all_files=[]):

  os.chdir(base)
  print(base)

  for file in os.listdir():
    if "\uf03a" in file:
      os.rename(file, file.replace("\uf03a", "_"))
      changed_files.append(base + "\\" + file)
  
  for file in os.listdir():
    if not os.path.isdir(base + "\\" + file):
      all_files.append(base)
    else:
      get_files((base + "\\" + file), all_files)
  return all_files

files = []
print("input base path, or using the default base path (F:\dataFileForAll\OneDrive\images):")
input_base = input()
if input_base == "":
  input_base = r"F:\dataFileForAll\OneDrive\images"
get_files(input_base, files)

# for file in files:
#     print(file)


print("----------------")
print("changed files:")
print("----------------")
for file in changed_files:
    print(file)

