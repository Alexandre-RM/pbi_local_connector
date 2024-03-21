import os
import logging
import subprocess

def getVersion(incrementVersion = False) -> str:
    with open("currentVersion.txt") as f:
        version = f.readline()
    
    if incrementVersion:
        with open("currentVersion.txt", mode="w") as f:
            s = version.split(".")
            version = f"{s[0]}.{int(s[1]) + 1}"
            f.write(version)

    return version



logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
    logging.info("Attempting to build the project...")

    # stream = os.popen("py -m build")
    stream = os.popen("py setup.py sdist bdist_wheel")
    output = stream.read()

    if f"creating 'dist\\pbi_local_connector-{getVersion()}-py3-none-any.whl' and adding 'build\\bdist.win-amd64\\wheel' to it" in output:
        logging.info("\n-----\nBuild success!\n-----" + "\n\n")
    else:
        logging.error("\n-----\nBUILD FAILURE!\n-----\n Full log: \n " + output + "\n\n")


    logging.info("Attempting to publish the project...")


    stream = os.popen(f"twine upload --skip-existing --config-file={os.path.abspath(".pypirc")} dist/*")
    output = stream.read()

    if "View at:" in output:
        logging.info(f"\n-----\nPublished to PyPI successfully! Build version: {getVersion()}\n-----\n")
    else:
        logging.error("\n-----\nPUBLISH FAILURE!\n-----\n Full log: \n " + output)
