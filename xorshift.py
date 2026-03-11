#!/usr/bin/env python3
"""Xorshift PRNG family — fast pseudo-random number generators.

One file. Zero deps. Does one thing well.

Implements xorshift32, xorshift64, xorshift128, and xorshift128+ (used in V8 JS engine).
Based on George Marsaglia's "Xorshift RNGs" (2003).
"""
import sys, time

class Xorshift32:
    MASK = 0xFFFFFFFF
    def __init__(self, seed=None):
        self.state = (seed or int(time.time())) & self.MASK or 1
    def next(self):
        x = self.state
        x ^= (x << 13) & self.MASK
        x ^= x >> 17
        x ^= (x << 5) & self.MASK
        self.state = x
        return x
    def random(self):
        return self.next() / (self.MASK + 1)

class Xorshift64:
    MASK = 0xFFFFFFFFFFFFFFFF
    def __init__(self, seed=None):
        self.state = (seed or int(time.time())) & self.MASK or 1
    def next(self):
        x = self.state
        x ^= (x << 13) & self.MASK
        x ^= x >> 7
        x ^= (x << 17) & self.MASK
        self.state = x
        return x
    def random(self):
        return self.next() / (self.MASK + 1)

class Xorshift128:
    MASK = 0xFFFFFFFF
    def __init__(self, seed=None):
        s = seed or int(time.time())
        self.x = s & self.MASK or 1
        self.y = (s >> 32 | 362436069) & self.MASK
        self.z = (s >> 16 | 521288629) & self.MASK
        self.w = (s >> 48 | 88675123) & self.MASK
    def next(self):
        t = self.x ^ ((self.x << 11) & self.MASK)
        self.x, self.y, self.z = self.y, self.z, self.w
        self.w = self.w ^ (self.w >> 19) ^ (t ^ (t >> 8))
        self.w &= self.MASK
        return self.w
    def random(self):
        return self.next() / (self.MASK + 1)

class Xorshift128Plus:
    """Used in V8, SpiderMonkey, and WebKit."""
    MASK = 0xFFFFFFFFFFFFFFFF
    def __init__(self, seed=None):
        s = seed or int(time.time())
        self.s0 = s & self.MASK or 1
        self.s1 = ((s >> 32) ^ 0x9E3779B97F4A7C15) & self.MASK or 1
    def next(self):
        s1 = self.s0
        s0 = self.s1
        self.s0 = s0
        s1 ^= (s1 << 23) & self.MASK
        self.s1 = (s1 ^ s0 ^ (s1 >> 17) ^ (s0 >> 26)) & self.MASK
        return (self.s1 + s0) & self.MASK
    def random(self):
        return self.next() / (self.MASK + 1)


def main():
    print("Xorshift PRNG Family Demo\n")
    for name, cls in [("xorshift32", Xorshift32), ("xorshift64", Xorshift64),
                       ("xorshift128", Xorshift128), ("xorshift128+", Xorshift128Plus)]:
        rng = cls(42)
        vals = [rng.next() for _ in range(5)]
        print(f"{name:15s}: {', '.join(str(v) for v in vals)}")
    # Speed test
    rng = Xorshift128Plus(42)
    n = 1_000_000
    t0 = time.perf_counter()
    for _ in range(n):
        rng.next()
    dt = time.perf_counter() - t0
    print(f"\nxorshift128+: {n:,} calls in {dt:.3f}s ({n/dt:,.0f}/s)")

if __name__ == "__main__":
    main()
