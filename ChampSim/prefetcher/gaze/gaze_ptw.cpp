#include "gaze.h"

#include <algorithm>
#include <iostream>

namespace gaze {

// Register the page size reported by PTW.
void Gaze::notify_page_size(uint64_t page_base_vaddr, uint32_t page_size_bytes)
{
    page_size_map_[page_base_vaddr] = page_size_bytes;
    // Optional: debug print for first few entries (comment/uncomment as needed)
    static int cnt = 0;
    if (cnt++ < 20) std::cout << "[GAZE] PTW notify: base=0x" << std::hex << page_base_vaddr << std::dec << " size=" << page_size_bytes << "\n";
}

// Attach to PTW: register callback
void Gaze::attach_ptw(PageTableWalker* ptw)
{
    if (!ptw) return;
    ptw->register_page_size_callback([this](uint64_t base, uint32_t psize) {
        this->notify_page_size(base, psize);
    });
}

// Return page size hint (bytes) for virtual address, or 0 if unknown.
// It tries to match supported_page_sizes_ (if set) or falls back to exact page-base if present.
uint32_t Gaze::get_page_size_hint(uint64_t vaddr)
{

    if (supported_page_sizes_.empty()) {
        // Try direct exact-match lookup for the standard page base (4KB)
        uint64_t base4 = (vaddr / static_cast<uint64_t>(PAGE_SIZE)) * static_cast<uint64_t>(PAGE_SIZE);
        auto it = page_size_map_.find(base4);
        if (it != page_size_map_.end()) return it->second;
        return 0;
    }

    // Try supported sizes in order (prefer larger first if provided)
    for (uint32_t ps : supported_page_sizes_) {
        uint64_t base = (vaddr / static_cast<uint64_t>(ps)) * static_cast<uint64_t>(ps);
        auto it = page_size_map_.find(base);
        if (it != page_size_map_.end()) return it->second;
    }
    return 0;
}

// Initialize supported region/page sizes
void Gaze::init_multi_phts(const std::vector<uint32_t>& region_sizes)
{
    supported_page_sizes_.clear();
    supported_page_sizes_ = region_sizes;
    // sort descending (larger page sizes first)
    std::sort(supported_page_sizes_.begin(), supported_page_sizes_.end(), std::greater<uint32_t>());
    // Remove duplicates
    supported_page_sizes_.erase(std::unique(supported_page_sizes_.begin(), supported_page_sizes_.end()), supported_page_sizes_.end());
}

} // namespace gaze
