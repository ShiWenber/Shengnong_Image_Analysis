import os
print(os.getcwd())
for direct in os.listdir():
    print(direct)

for i in os.listdir():
    if i.endswith(".tar"):
        print(i)
        print(os.popen(f"tar -xf {i}").readlines())
        os.rename("269f4f01-0813-4ee2-aea1-a9bb7c16ae2e", i.removesuffix(".tar"))
        print(os.popen(f"rm {i}").readlines())
print("---------------------------")
print("done, results:")
print("---------------------------")

for direct in os.listdir():
    print(direct)