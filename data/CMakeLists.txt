cmake_minimum_required(VERSION 2.8)
PROJECT(morfessor-demo-data)

install(DIRECTORY ${Models_DIR} DESTINATION share/morfessor-demo-data/models )

###############
set (CPACK_GENERATOR "DEB")
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "Peter Smit")
set(CPACK_DEBIAN_PACKAGE_ARCHITECTURE amd64)
include(CPack)

