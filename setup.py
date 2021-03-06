# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from shutil import rmtree
from setuptools import setup, find_packages, Command
import codecs

__version__ = None
exec(open("servicing/version.py").read())

here = os.path.abspath(os.path.dirname(__file__))

long_description = ""
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as readme:
    long_description = readme.read()

tests_require = ["pytest", "coverage", "flake8", "black", "psutil"]


class BaseCommand(Command):
    """Base Command"""

    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def _run(self, s, command):
        try:
            self.status(s + "\n" + " ".join(command))
            subprocess.check_call(command)
        except subprocess.CalledProcessError as error:
            sys.exit(error.returncode)


class UploadCommand(BaseCommand):
    """Support setup.py upload. Thanks @kennethreitz!"""

    description = "Build and publish the package."

    def run(self):
        self._run(
            "Installing upload dependencies…",
            [sys.executable, "-m", "pip", "install", "wheel"],
        )
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self._run(
            "Building Source and Wheel (universal) distribution…",
            [sys.executable, "setup.py", "sdist", "bdist_wheel", "--universal"],
        )

        self._run("Creating git tags…", ["git", "tag", f"v{__version__}"])
        self._run("Pushing git tags…", ["git", "push", "--tags"])


class ValidateCommand(BaseCommand):
    """Support setup.py validate."""

    description = "Run Python static code analyzer (flake8), formatter (black) and unit tests (pytest)."

    user_options = [
        ('unit-test-target=', 'i', 'tests/{unit-test-target}'),
        ('utt=', 'i', 'tests/{utt}'),
        ('test-target=', 'i', 'tests/{test-target}')
    ]

    def initialize_options(self):
        self.unit_test_target = ""
        self.utt = ""
        self.test_target = ""

    def run(self):
        self._run(
            "Installing test dependencies…",
            [sys.executable, "-m", "pip", "install"] + tests_require,
            )
        self._run("Running black…", [sys.executable, "-m", "black", f"{here}/servicing"])
        self._run("Running flake8…", [sys.executable, "-m", "flake8", f"{here}/servicing"])

        target = (self.utt or self.unit_test_target or self.test_target).replace("tests/", "")

        self._run(
            "Running pytest…",
            [
                sys.executable,
                "-m",
                "coverage",
                "run",
                "--branch",
                f"--source={here}/servicing",
                "-m",
                "pytest",
                f"tests/{target}",
            ],
        )
        self._run("Generating coverage...", [sys.executable, "-m", "coverage", "xml", "-i"])



class RunAllTestsCommand(ValidateCommand):
    """Support setup.py integration_test."""

    description = ValidateCommand.description + "\nRun integration tests (pytest)."

    user_options = [
        ('unit-test-target=', 'i', 'tests/{unit-test-target}'),
        ('utt=', 'i', 'tests/{utt}'),
        ('integration-test-target=', 'i', 'integration_tests/{integration-test-target}'),
        ('itt=', 'i', 'integration_tests/{itt}'),
        ('test-target=', 'i', 'integration_tests/{test-target}')
    ]

    def initialize_options(self):
        self.unit_test_target = ""
        self.utt = ""
        self.integration_test_target = ""
        self.itt = ""
        self.test_target = ""

    def run(self):
        ValidateCommand.run(self)
        target = (self.itt or self.integration_test_target or self.test_target).replace("integration_tests/", "")
        self._run(
            "Running pytest…",
            [
                sys.executable,
                "-m",
                "coverage",
                "run",
                "--branch",
                f"--source={here}/servicing",
                "-m",
                "pytest",
                f"integration_tests/{target}",
            ]
        )
        self._run(
            "Generating integration coverage...",
            [
                sys.executable,
                "-m",
                "coverage",
                "xml",
                "-i",
                "-o",
                "coverage-integration.xml"
            ]
        )


setup(
    name="servicingclient",
    version=__version__,
    description="LoanStreet Servicing API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loanstreet-usa/python-servicingclient",
    author="LoanStreet, Inc.",
    author_email="support@loan-street.com",
    python_requires=">=3.6.0",
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Chat",
        "Topic :: System :: Networking",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="loanstreet servicing",
    packages=find_packages(
        exclude=["integration_tests", "tests", "tests.*"]
    ),
    setup_requires=["pytest-runner"],
    test_suite="tests",
    tests_require=tests_require,
    cmdclass={
        "upload": UploadCommand,
        "validate": ValidateCommand,
        "run_all_tests": RunAllTestsCommand
    },
)
