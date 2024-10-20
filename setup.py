from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="rayinfer",
    version="0.1.0",
    author="Zhihui Xie",
    author_email="zhxieml@example.com",
    description="A simple and efficient LLM inference service based on vllm and Ray Serve",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhxieml/rayinfer",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "rayinfer=rayinfer.scripts:main",
        ],
    },
)