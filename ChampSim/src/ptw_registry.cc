#include <algorithm>   
#include <mutex>
#include <vector>
#include "ptw_registry.h"

namespace champsim {
namespace ptw_registry {

static std::vector<PageTableWalker*> g_ptws;
static std::mutex g_ptw_mtx;

void register_ptw(PageTableWalker* ptw) {
    if (!ptw) return;
    std::lock_guard<std::mutex> lk(g_ptw_mtx);
    if (std::find(g_ptws.begin(), g_ptws.end(), ptw) == g_ptws.end())
        g_ptws.push_back(ptw);
}

std::vector<PageTableWalker*> get_ptw_list() {
    std::lock_guard<std::mutex> lk(g_ptw_mtx);
    return g_ptws;
}

} // namespace ptw_registry
} // namespace champsim