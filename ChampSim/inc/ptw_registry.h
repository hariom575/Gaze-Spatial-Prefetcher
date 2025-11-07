#ifndef PTW_REGISTRY_H
#define PTW_REGISTRY_H

#include <vector>
#include <mutex>

class PageTableWalker;

namespace champsim {
namespace ptw_registry {

// Register a PTW instance (call after construction).
void register_ptw(PageTableWalker* ptw);

// Return a snapshot copy of the registered PTW pointers.
std::vector<PageTableWalker*> get_ptw_list();

} // namespace ptw_registry
} // namespace champsim

#endif // PTW_REGISTRY_H