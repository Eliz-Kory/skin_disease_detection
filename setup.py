from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="skin_disease_detection",
    version="0.1.0",
    author="Кожакина Анна, Корочкина Елизавета, Муротхонова Гулсанам",
    description="Web application for skin disease detection using neural networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eliz-Kory/skin_disease_detection",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
)