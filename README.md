# pyqremis

v0.0.3

[![Build Status](https://travis-ci.org/uchicago-library/pyqremis.svg?branch=master)](https://travis-ci.org/uchicago-library/pyqremis) [![Coverage Status](https://coveralls.io/repos/github/uchicago-library/pyqremis/badge.svg?branch=master)](https://coveralls.io/github/uchicago-library/pyqremis?branch=master)

A python library for implementing the qremis metadata standard.


Information about the qremis specification is available [here](https://github.com/uchicago-library/qremis)

Provides a python class for every qremis element which includes the following methods

- .get\_$x() for every attribute
- .set\_$x() for every attribute
- .del\_$x() for every attribute
- .add\_$x() for every applicable attribute (those that are repeatable)
- .to_dict()
- .to_xml_element()
- .from_dict()

Classes can be inited by passing fields as either args (if they are QremisNode instances themselves) or kwargs for QremisNode instances or strs.

See the [qremiser](https://github.com/uchicago-library/qremiser) for a quick example of using this library to build records.


# Author
Brian Balsamo <brian@brianbalsamo.com>
