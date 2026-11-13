#pragma once
#include "data.hpp"
#include "files.hpp"

// Submission records live under <cacheRoot>/.cache/submissions/<problemId>/.
fs::path submissionsRoot(const fs::path& cacheRoot);
std::string newSubmissionId();
Json submissionSummary(const Json& submission);
void saveSubmission(const fs::path& cacheRoot,const Json& submission);
Json listSubmissions(const fs::path& cacheRoot,const std::string& problemId);
Json readSubmission(const fs::path& cacheRoot,const std::string& submissionId);
Json bestFor(const fs::path& cacheRoot,const std::string& problemId);
Json problemStats(const fs::path& cacheRoot,const std::string& problemId);
long long clearSubmissions(const fs::path& cacheRoot,const std::string& problemId);
long long removeProblemSubmissions(const fs::path& cacheRoot,const std::string& problemId);
