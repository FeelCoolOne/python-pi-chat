from setuptools import setup, find_packages

setup(
    name="pi-chat",
    version="0.1.0",
    description="Pi client",
    author="Maxime Renou",
    author_email="contact@maximerenou.fr",
    packages=find_packages("heypi"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.26.0",
        "sseclient>=1.7.2",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
