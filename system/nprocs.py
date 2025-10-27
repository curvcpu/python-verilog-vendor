import os, math

def get_nprocs() -> int:
    """
    Get number of effective CPUs, accounting for the fact that we may be in a container.
    Returns:
        int: Number of effective CPUs
    """
    # 1) Affinity (best: respects taskset/cpuset)
    try:
        return len(os.sched_getaffinity(0))
    except AttributeError:
        pass  # not on macOS/Windows

    # 2) cgroups CPU quota (containers without cpuset)
    try:
        # cgroups v2
        p = "/sys/fs/cgroup/cpu.max"
        if os.path.exists(p):
            q, period = open(p).read().split()
            if q != "max":
                return max(1, math.ceil(int(q) / int(period)))
        # cgroups v1
        q1, p1 = "/sys/fs/cgroup/cpu/cpu.cfs_quota_us", "/sys/fs/cgroup/cpu/cpu.cfs_period_us"
        if os.path.exists(q1) and os.path.exists(p1):
            q, period = int(open(q1).read()), int(open(p1).read())
            if q > 0 and period > 0:
                return max(1, math.ceil(q / period))
    except Exception:
        pass  # ignore if not accessible

    # 3) Total logical CPUs
    return os.cpu_count() or 1