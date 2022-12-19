from heapq import heappush, heappop
import re

DATA = open('day19.txt').read()


def push(S, t, ore, clay, obsidian, geode, ore_robots,
         clay_robots, obsidian_robots, geode_robots, limits):
    heuristic = t * geode_robots + t * (t - 1) // 2
    heappush(
        S,
        (-(geode + heuristic),
         t,
         min(limits[0], ore),
         min(limits[1], clay),
         min(limits[2], obsidian),
         geode,
         ore_robots,
         clay_robots,
         obsidian_robots,
         geode_robots))


def max_geodes(time, ore_ore, clay_ore, obsidian_ore,
               obsidian_clay, geode_ore, geode_obsidian):
    max_ore = max(ore_ore, clay_ore, obsidian_ore, geode_ore)
    limits = (2 * max_ore, 2 * obsidian_clay, 2 * geode_obsidian)
    S = []
    push(S, time, 0, 0, 0, 0, 1, 0, 0, 0, limits)
    visited = set()
    while S:
        state = heappop(S)
        if state in visited:
            continue
        visited.add(state)
        _, t, ore, clay, obsidian, geode, ore_robots, clay_robots, obsidian_robots, geode_robots = state
        if t == 0:
            return geode
        if ore >= geode_ore and obsidian >= geode_obsidian:
            push(S,
                 t - 1,
                 ore + ore_robots - geode_ore,
                 clay + clay_robots,
                 obsidian + obsidian_robots - geode_obsidian,
                 geode + geode_robots,
                 ore_robots,
                 clay_robots,
                 obsidian_robots,
                 geode_robots + 1,
                 limits)
            continue
        if ore >= ore_ore and ore_robots < max_ore:
            push(S,
                 t - 1,
                 ore + ore_robots - ore_ore,
                 clay + clay_robots,
                 obsidian + obsidian_robots,
                 geode + geode_robots,
                 ore_robots + 1,
                 clay_robots,
                 obsidian_robots,
                 geode_robots,
                 limits)
        if ore >= clay_ore and clay_robots < obsidian_clay:
            push(S,
                 t - 1,
                 ore + ore_robots - clay_ore,
                 clay + clay_robots,
                 obsidian + obsidian_robots,
                 geode + geode_robots,
                 ore_robots,
                 clay_robots + 1,
                 obsidian_robots,
                 geode_robots,
                 limits)
        if ore >= obsidian_ore and clay >= obsidian_clay and obsidian_robots < geode_obsidian:
            push(S,
                 t - 1,
                 ore + ore_robots - obsidian_ore,
                 clay + clay_robots - obsidian_clay,
                 obsidian + obsidian_robots,
                 geode + geode_robots,
                 ore_robots,
                 clay_robots,
                 obsidian_robots + 1,
                 geode_robots,
                 limits)
        push(S,
             t - 1,
             ore + ore_robots,
             clay + clay_robots,
             obsidian + obsidian_robots,
             geode + geode_robots,
             ore_robots,
             clay_robots,
             obsidian_robots,
             geode_robots,
             limits)


result = 0
for blueprint in (tuple(map(int, re.findall(r'\d+', line)))
                  for line in DATA.splitlines()):
    geodes = max_geodes(24, *blueprint[1:])
    result += blueprint[0] * geodes

print(result)
assert result == 1266


result = 1
for blueprint in (tuple(map(int, re.findall(r'\d+', line)))
                  for line in DATA.splitlines()[:3]):
    geodes = max_geodes(32, *blueprint[1:])
    result *= geodes

print(result)
assert result == 5800
