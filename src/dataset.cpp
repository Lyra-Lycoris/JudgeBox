#include "dataset.hpp"
#include <algorithm>

Dataset loadDataset(const std::string& directory) {
    if(directory.empty()) throw std::runtime_error("请选择数据目录");
    Dataset result;
    result.directory=fs::weakly_canonical(fs::path(wide(directory)));
    if(!fs::is_directory(result.directory)) throw std::runtime_error("数据目录不存在或不是目录");
    for(const auto& entry:fs::recursive_directory_iterator(result.directory,fs::directory_options::skip_permission_denied)) {
        if(!entry.is_regular_file() || entry.path().extension()!=L".in") continue;
        DatasetCase item;
        item.name=utf8(fs::relative(entry.path(),result.directory).generic_wstring());
        item.input=entry.path();
        item.inputBytes=entry.file_size();
        auto answer=entry.path(); answer.replace_extension(L".ans");
        auto output=entry.path(); output.replace_extension(L".out");
        if(fs::is_regular_file(answer)) item.expected=answer;
        else if(fs::is_regular_file(output)) item.expected=output;
        if(!item.expected.empty()) item.expectedBytes=fs::file_size(item.expected);
        result.totalBytes+=item.inputBytes+item.expectedBytes;
        result.maxExpectedBytes=std::max(result.maxExpectedBytes,item.expectedBytes);
        result.cases.push_back(std::move(item));
        if(result.cases.size()>10000) throw std::runtime_error("单个数据目录最多导入 10000 个测试点");
    }
    if(result.cases.empty()) throw std::runtime_error("目录及其子目录中没有找到 .in 输入文件");
    std::sort(result.cases.begin(),result.cases.end(),[](const auto& a,const auto& b){return a.name<b.name;});
    return result;
}
Json datasetSummary(const Dataset& dataset) {
    Json cases=Json::array();
    for(const auto& item:dataset.cases) cases.push_back({{"name",item.name},{"inputBytes",item.inputBytes},{"expectedBytes",item.expected.empty()?Json(nullptr):Json(item.expectedBytes)}});
    return {{"directory",utf8(dataset.directory.wstring())},{"cases",cases},{"totalBytes",dataset.totalBytes}};
}
