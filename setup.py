from setuptools import setup, find_packages

setup(
    name="curso-matic",
    version="0.1.0",
    description="CLI tool to manage and translate online courses",
    author="Jose Arturo Mora Soto",
    packages=find_packages(),  # Automatically find curso_matic package
    include_package_data=True,
    install_requires=[
        "typer[all]",
        "openai==0.28",
        "python-dotenv",
        "pathlib"
    ],
    entry_points={
        "console_scripts": [
            "curso-matic=curso_matic.main:app",  # Command = module:function
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
