"""Update Docs"""

from os import listdir, system


def main():
    url = "https://github.com/dotflow-io/examples/blob/master/{}"
    files = listdir(path="examples")
    files.sort()

    system("echo '| Example | Command |' >> file.txt")
    system("echo '| ------- | ------- |' >> file.txt")

    for index, file in enumerate(files):
        if file.endswith(".py"):
            file_name = file.replace(".py", "")
            system(f"echo '| [{file_name}]({url.format(file)}) | `python examples/{file}` |' >> file.txt")


if __name__ == "__main__":
    main()
