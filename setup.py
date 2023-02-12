from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='pydemonstrativo',
    version='0.0.1',
    url='https://github.com/andremsilveira/pydemonstrativos',
    license='MIT License',
    author='Andre Silveira',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='martinslucianofigueira@gmail.com',
    keywords='Pacote',
    description=u'Demonstrativos Financeiros - Dados CVM',
    packages=['pydemonstrativo'],
    install_requires=['pandas'],)