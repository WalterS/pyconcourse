import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyconcourse',
    version='0.1.0',
    author='Walter S.'
    author_email='720628+WalterS@users.noreply.github.com'
    description='Talk to Concourse API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/WalterS/pyconcourse',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=(
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ),
)
