#pragma once
#include "files.hpp"
// Return an ASCII spelling of an existing directory, using a private junction if needed.
fs::path asciiDirectory(const fs::path& directory);
