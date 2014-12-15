cmake_minimum_required(VERSION 2.8)
PROJECT(morfessor-demo)

install(FILES bottle/bottle.py DESTINATION lib/pypy/dist-packages)
install(DIRECTORY morfessor-dev/morfessor DESTINATION lib/pypy/dist-packages/)
install(PROGRAMS morfessor-demo DESTINATION bin)
install(DIRECTORY static DESTINATION share/morfessor-demo)

set (CPACK_GENERATOR "DEB")
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "Peter Smit")
set(CPACK_DEBIAN_PACKAGE_ARCHITECTURE amd64)
set(CPACK_PACKAGE_VERSION 0.1.3)
set(CPACK_DEBIAN_PACKAGE_DEPENDS "pypy, morfessor-demo-data")
include(CPack)
