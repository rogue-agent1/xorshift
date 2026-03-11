#!/usr/bin/env python3
"""Xorshift PRNGs — fast non-cryptographic random number generators."""
import sys

class Xorshift32:
    def __init__(self, seed=2463534242):
        self.state = seed & 0xFFFFFFFF
    def next(self):
        x = self.state
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        self.state = x
        return x
    def random(self): return self.next() / 0xFFFFFFFF

class Xorshift128:
    def __init__(self, seed=None):
        s = seed or 42
        self.s = [(s * (i+1) * 2654435761) & 0xFFFFFFFF for i in range(4)]
    def next(self):
        t = self.s[3]
        t ^= (t << 11) & 0xFFFFFFFF; t ^= t >> 8
        self.s[3] = self.s[2]; self.s[2] = self.s[1]; self.s[1] = self.s[0]
        s0 = self.s[0]; t ^= s0; t ^= (s0 >> 19) & 0xFFFFFFFF
        self.s[0] = t & 0xFFFFFFFF
        return self.s[0]

class SplitMix64:
    def __init__(self, seed=0): self.state = seed & ((1<<64)-1)
    def next(self):
        self.state = (self.state + 0x9E3779B97F4A7C15) & ((1<<64)-1)
        z = self.state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & ((1<<64)-1)
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & ((1<<64)-1)
        return z ^ (z >> 31)

if __name__ == "__main__":
    rng = Xorshift32(12345)
    vals = [rng.random() for _ in range(10000)]
    print(f"Xorshift32 — mean: {sum(vals)/len(vals):.4f} (expect ~0.5)")
    rng128 = Xorshift128(42)
    print(f"Xorshift128 sample: {[rng128.next() for _ in range(5)]}")
    sm = SplitMix64(0)
    print(f"SplitMix64 sample: {[sm.next() for _ in range(3)]}")
