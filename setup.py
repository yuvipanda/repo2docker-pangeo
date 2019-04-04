from setuptools import setup, find_packages

setup(
    name='repo2docker-pangeo',
    version='0.0.1',
    python_requires='>=3.4',
    packages=find_packages(),
    install_requires=[
        'jupyter-repo2docker'
    ]
)
