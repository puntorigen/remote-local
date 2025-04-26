from setuptools import setup, find_packages

setup(
    name="remote-local",
    version="0.0.2",
    description="Expose your local FastAPI, NiceGUI, or development servers remotely — easily, reliably, and for free.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Pablo Schaffner",
    author_email="pablo@puntorigen.com",
    url="https://github.com/puntorigen/remote-local",
    packages=find_packages(),
    install_requires=[
        "pyngrok>=5.3.0",
        "psutil>=5.9.0",
        "fastapi>=0.100.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
    ],
    project_urls={
        "Source": "https://github.com/puntorigen/remote-local",
        "Documentation": "https://github.com/puntorigen/remote-local",
    },
    include_package_data=True,
)
