#pragma once
#include "files.hpp"
void extractZip(const fs::path& zip,const fs::path& destination);
void createZip(const fs::path& zip,const fs::path& sourceDirectory);
// 读取 zip 内单个文本条目（用于从题库 zip 里取 problem.json，避免整包解压）。
std::string readZipEntry(const fs::path& zip,const std::string& entry);
