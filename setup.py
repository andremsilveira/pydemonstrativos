from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='pydemonstrativos',
    version='0.0.1',
    url='https://github.com/andremsilveira/pydemonstrativos',
    license='MIT License',
    author='Andre Silveira',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='andre.a.silveira@icloud.com',
    keywords='Pacote',
    description=u'Demonstrativos Financeiros - Dados CVM',
    packages=['pydemonstrativos'],
    install_requires=['pandas'],)