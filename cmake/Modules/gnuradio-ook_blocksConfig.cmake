find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_OOK_BLOCKS gnuradio-ook_blocks)

FIND_PATH(
    GR_OOK_BLOCKS_INCLUDE_DIRS
    NAMES gnuradio/ook_blocks/api.h
    HINTS $ENV{OOK_BLOCKS_DIR}/include
        ${PC_OOK_BLOCKS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_OOK_BLOCKS_LIBRARIES
    NAMES gnuradio-ook_blocks
    HINTS $ENV{OOK_BLOCKS_DIR}/lib
        ${PC_OOK_BLOCKS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-ook_blocksTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_OOK_BLOCKS DEFAULT_MSG GR_OOK_BLOCKS_LIBRARIES GR_OOK_BLOCKS_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_OOK_BLOCKS_LIBRARIES GR_OOK_BLOCKS_INCLUDE_DIRS)
