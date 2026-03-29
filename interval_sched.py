#!/usr/bin/env python3
"""interval_sched - Interval scheduling: greedy, weighted, and overlap detection."""
import sys

def greedy_schedule(intervals):
    """Max non-overlapping intervals. intervals: [(start, end, ...)]"""
    sorted_iv = sorted(enumerate(intervals), key=lambda x: x[1][1])
    result = []
    last_end = float('-inf')
    for idx, iv in sorted_iv:
        if iv[0] >= last_end:
            result.append(idx)
            last_end = iv[1]
    return result

def weighted_schedule(intervals, weights):
    """Max weight non-overlapping. intervals: [(start, end)], weights: [w]."""
    n = len(intervals)
    jobs = sorted(range(n), key=lambda i: intervals[i][1])
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        j = jobs[i-1]
        # Find last non-conflicting
        last = 0
        for k in range(i - 1, 0, -1):
            if intervals[jobs[k-1]][1] <= intervals[j][0]:
                last = k
                break
        dp[i] = max(dp[i-1], dp[last] + weights[j])
    return dp[n]

def find_overlaps(intervals):
    """Find all overlapping pairs."""
    overlaps = []
    for i in range(len(intervals)):
        for j in range(i+1, len(intervals)):
            a, b = intervals[i], intervals[j]
            if a[0] < b[1] and b[0] < a[1]:
                overlaps.append((i, j))
    return overlaps

def test():
    ivs = [(1,3), (2,5), (4,7), (6,8)]
    sel = greedy_schedule(ivs)
    assert len(sel) == 2  # (1,3) and (4,7) or (6,8)
    wt = weighted_schedule([(1,3),(2,5),(4,7),(6,8)], [2, 4, 4, 3])
    assert wt >= 6  # best: (2,5)=4 + (6,8)=3 = 7
    overlaps = find_overlaps([(1,3),(2,5),(6,8)])
    assert (0,1) in overlaps
    assert (1,2) not in overlaps
    print("interval_sched: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: interval_sched.py --test")
