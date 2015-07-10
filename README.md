# slitherlink-solver

This file implements a solver for the slitherlink puzzle.

## How the slitherlink solver works

Initially, I set the solver to simply go through edges and create a list of partial solutions by copying a partial solution and then setting a particular edge to either be included or not be included in the solution. By pruning branches that violated the rules, this was able to solve some small boards, but was too slow for larger boards.

I then changed the solver to look for edges that immediately lead to contradictions and to choose those. This solver can now solve very large boards, but could not solve even relatively small boards that were "hard" (as described by puzzle-loop.com, which I use to test the solver).